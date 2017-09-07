from zipfile import ZipFile
from io import BytesIO

import base64

from pycoin.encoding import to_bytes_32
from pycoin.tx.Tx import Tx, SIGHASH_ALL
import pycoin.ui

from gaservices.utils.btc_ import tx_segwit_hash
from gaservices.utils import inscript
from wallycore import *
import logging

# BCASH
# Python 2/3 compatibility
try:
    user_input = raw_input
except NameError:
    user_input = input

def _fernet_decrypt(key, data):
    assert hmac_sha256(key[:16], data[:-32]) == data[-32:]
    res = bytearray(len(data[25:-32]))
    written = aes_cbc(key[16:], data[9:25], data[25:-32], AES_FLAG_DECRYPT, res)
    assert written <= len(res) and len(res) - written <= AES_BLOCK_LEN
    return res[:written]


def _unzip(data, key):
    """Unzip a GreenAddress nlocktimes.zip attachment file.

    The file format is double zip encoded with the user's chaincode
    """
    all_data = []
    if not data.startswith(b'PK'):
        all_data.append(data)
    else:
        # Compressed zip file: unzip it
        zf = ZipFile(BytesIO(data))
        for f in zf.namelist():
            data = b''.join(zf.open(f).readlines())
            prefix = b'GAencrypted'
            if data.startswith(prefix):
                # Encrypted inner zip file: Strip prefix, decrypt and unzip again
                encrypted = data[len(prefix):]
                all_data.extend(_unzip(_fernet_decrypt(key, encrypted), key))
            else:
                all_data.append(data)

    return all_data


def private_key_to_wif(key, testnet):
    ver = b'\xef' if testnet else b'\x80'
    compressed = b'\x01'
    return base58check_from_bytes(ver + bip32_key_get_priv_key(key) + compressed,)


P2SH_P2WSH_FORTIFIED_OUT = SEGWIT = 14


class PassiveSignatory:
    """Represent a signatory for which the keys are not known, only the signature

    For use where a transaction has been partially signed. Instances of this class represent the
    known signatures
    """

    def __init__(self, signature):
        self.signature = signature

    def get_signature(self, sighash):
        return self.signature


class ActiveSignatory:
    """Active signatory for which the keys are known, capable of signing arbitrary data"""

    def __init__(self, key):
        self.key = key

    def get_signature(self, sighash):
        sig = ec_sig_from_bytes(self.key, sighash, EC_FLAG_ECDSA)
        signature = ec_sig_to_der(sig) + bytearray([0x41, ]) # BCASH
        return signature


def sign(txdata, signatories, args): # BCASH
    tx = Tx.from_hex(txdata['tx'])

    # BCASH
    inp = []
    you_signings = []

    if args.recovery_mode == "2of2":

        tx.lock_time = 0 # no nloktime
        satoshi = 0

        for prevout_index, txin in enumerate(tx.txs_in):
            script_type = txdata['prevout_script_types'][prevout_index]
            if script_type == SEGWIT:
                return None

            txin.sequence = 0xffffffff # no nloktime, rbf

            inp.append({ "value": int(txdata['prevout_values'][prevout_index]),
                         "script": txdata['prevout_scripts'][prevout_index],
                         "subaccount": txdata['prevout_subaccounts'][prevout_index],
                         "pointer": txdata['prevout_pointers'][prevout_index] })
            satoshi += inp[-1]["value"]

        assert len(tx.txs_out) == 1
        tx.txs_out[0].script = pycoin.ui.script_obj_from_address(args.destination_address).script()

        fee = len(tx.as_bin()) * args.default_feerate
        tx.txs_out[0].coin_value = satoshi - fee

    for prevout_index, txin in enumerate(tx.txs_in):

        script = hex_to_bytes(txdata['prevout_scripts'][prevout_index])
        script_type = txdata['prevout_script_types'][prevout_index]
        if script_type == SEGWIT:
            return None

        value = int(txdata['prevout_values'][prevout_index])
        sighash = tx_segwit_hash(tx, prevout_index, script, value)

        if args.recovery_mode == "2of2":
            # only for you - after is greenaddress
            you_sign = signatories[1].get_signature(sighash)
            you_signings.append(you_sign)
            txin.script = inscript.multisig_2_of_2(script, you_sign)
        else:
            signatures = [signatory.get_signature(sighash) for signatory in signatories]
            txin.script = inscript.multisig(script, signatures)

    if args.recovery_mode == "2of2":
        # BCASH
        h = hex_from_bytes(sha256d(tx.as_bin()))
        logging.warning("sign tx: check same your email!")
        logging.warning("tx:" + tx.as_hex())
        logging.warning("sha256d: " + h)

        # ask code
        twofactor = { }
        if args.twofactor["email"]:
            args.conn.call("twofactor.request_email", "sign_alt_tx", 
                           { "txtype": "bcash", "sha256d": h })
            twofactor = { "method": "email" }
        elif args.twofactor["sms"]:
            args.conn.call("twofactor.request_sms", "sign_alt_tx", 
                           { "txtype": "bcash", "sha256d": h })
            twofactor = { "method": "sms" }
        elif args.twofactor["any"]:
            logging.warning("need email/sms twofactor")
            assert False, "need email/sms twofactor"

        if args.twofactor["any"]:
            twofactor["code"] = user_input(twofactor["method"] + " code:")

        # sign greenaddress
        signing = args.conn.call("vault.sign_alt_tx", tx.as_hex(), "bcash",
                                 inp, twofactor)

        for prevout_index, txin in enumerate(tx.txs_in):
            script = hex_to_bytes(txdata['prevout_scripts'][prevout_index])
            signatures = [ hex_to_bytes(signing['signatures'][prevout_index]),
                           you_signings[prevout_index] ]
            txin.script = inscript.multisig(script, signatures)

    return tx


def countersign(txdata, private_key, args): # BCASH
    #GreenAddress = PassiveSignatory(hex_to_bytes(txdata['prevout_signatures'][0]))
    user = ActiveSignatory(bip32_key_get_priv_key(private_key))
    return sign(txdata, [None, user], args)


def derive_hd_key(root, path, flags=0):
    return bip32_key_from_parent_path(root, path, flags | BIP32_FLAG_SKIP_HASH)


def get_subaccount_path(subaccount):
    if subaccount == 0:
        return []
    else:
        HARDENED = 0x80000000
        return [HARDENED | 3, HARDENED | subaccount]


def derive_user_private_key(txdata, wallet, branch):
    subaccount = txdata['prevout_subaccounts'][0] or 0
    pointer = txdata['prevout_pointers'][0] or 0
    path = get_subaccount_path(subaccount)
    return derive_hd_key(wallet, path + [branch, pointer])
