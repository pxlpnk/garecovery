Recover Bitcoin Cash/BCASH/BCC/BCH from GreenAddress wallets

#  Bitcoin Cash/BCASH/BCC/BCH

This is same garecovery tool but for  Bitcoin Cash ONLY!!!!


# 2 of 2 Scan

## 1
Scan your main wallet and send all BCASH.

No need nlocktimes.zip, no need BCASH bitcoind!

Maybe you send BCASH to greenaddress wallet after fork. Can get back, only if not segwit address.

## 2

Read old README under here about 2 of 2 for install.

## 3
You run
```
$ garecovery-cli 2of2scan -o garecovery.csv --destination-address XXXX
```

Recovery connect to greenaddress API to get address and sign.

Fee rate is 5 satoshi/byte. You can give --default-feerate XXXX to change.

If twofactor you need code for each tx. twofactor is email or sms if no email.

Read #4, #5 for 2 of 2 for check transaction is ok.


# 2 of 2

## 1
You need nlocktimes.zip from before BCASH fork. If not have, add email twofactor and take nlocktimes.zip from email.

If nlocktimes.zip made after fork maybe not get all BCASH yet (if you send bitcoin after fork). I add scan missing BCASH from wallet soon.

If you have new coins in wallet after fork then some transactions from nlocktimes.zip cannot send, is normal.

## 2

Read old README under here about 2 of 2 for install.

## 3
You run
```
$ garecovery-cli 2of2 --nlocktime-file /path/to/downloaded/nlocktimes.zip -o garecovery.csv --destination-address XXXX
```

Recovery connect to greenaddress API to sign.

Fee rate is 5 satoshi/byte. You can give --default-feerate XXXX to change.

If twofactor you need code for each tx. twofactor is email or sms if no email.

## 4
Check email is for BCASH transaction, dont put code if not!!

You see transaction hex before code. You run
```
get_sha256d transaction-hex
```
and check is same your email.

Also can run

```
bitcoin-cli decoderawtransaction XXXX
```

check vout address to you only like 2 of 3.

After check, give code to garecovery to sign.
Maybe wait 1 minute for each code or greenaddress error "#ratelimited".

## 5

Read 5,6,7 for 2 of 3 for most private and safe way.


# 2 of 3

Everything same garecovery except you use bitcoin cash node not bitcoin.
You can download bitcoin cash node at https://download.bitcoinabc.org/

## 1

Run bitcoind from bitcoin cash. You need
```
 -disablesafemode
```
to bitcoind. bitcoind have to sync to fork to find your bitcoins.

## 2

Read old README under here about 2 of 3 for install.

## 3

You run
```
$ garecovery-cli 2of3 --destination-address=XXXX -o garecovery.csv --ga-xpub=YYYY
```

If no ga-xpub give --search-subaccounts.

Recovery connect to greenaddress API to get path (make scan fast). Maybe can make more fast soon.

Fee rate is 5 satoshi/byte. You can give --default-feerate XXXX to change.

## 4

After you have garecovery.csv file run

```
bitcoin-cli decoderawtransaction XXXX
```

on transaction hex from garecovery.csv before send. You see 1 vout,
check value is ok and no decoderawtransaction error and transaction send to right address:

```
  "vout": [
    {
      "value": XXXX
        "addresses": [
          "--destination-address for you"
        ]
    }, 
```

## 5 For Most private way

Make new --destination-address and run, send only first transaction in 
garecovery.csv. Make new address and run, only send second transaction...
Your address not joined together this way.


## 6 For Most safe way

After make garecovery.csv move money in greenaddress before send BCASH transaction hex.


## 7 Send transaction 

Can send from bitcoin cash bitcoind:

```
bitcoin-cli sendrawtransaction XXXX
```

If bitcoind is not tor then bad for private. Better send transaction hex at
https://cashexplorer.bitcoin.com/tx/send or https://pool.viabtc.com/tools/BCC/broadcast/
from torbrowser.


If you happy, thanks for donate at:

Bitcoin: 1ApavmRLr4Trv5UeJni4fp4RRKG6affdN3 ![Bitcoin](https://raw.githubusercontent.com/dumpyourbcash/garecovery/master/img/bitcoin.png "Bitcoin")


Bitcoin Cash: 1GPgWu1cxwMRV2aqAZHSt4dQPbxFNXq7bg ![Bitcoin Cash](https://raw.githubusercontent.com/dumpyourbcash/garecovery/master/img/bcash.png "Bitcoin Cash")


Here is old README:

For more information on the GreenAddress service, subaccount types and
recovery, please read the [GreenAddress FAQ](https://greenaddress.it/en/faq)

# Dependencies for Ubuntu & Debian
Remove all '{,3}' if you want to use just python2
```
$ sudo apt-get update -qq
$ sudo apt-get install python{,3}-pip python{,3}-dev build-essential python{,3}-virtualenv -yqq
```

# Install
```
$ virtualenv venv
$ source venv/bin/activate
$ pip install --require-hashes -r tools/requirements.txt
$ pip install .
```

# Summary
The GreenAddress Recovery Tool allows you to recover coins from your
GreenAddress account(s) if you cannot use the normal mechanisms for making
payments. This could be due to one of the following scenarios:

* You lose access to your two factor authentication (2FA) mechanism
* The GreenAddress service becomes unavailable

There are two recovery scenarios depending on whether the coins are in a
GreenAddress 2of2 or a 2of3 subaccount. If you have an nlocktimes.zip
recovery file that was emailed to you by the service, then the 2of2 proceedure
should be followed.

The recovery tool supports recovering from both types of subaccounts.

## 2of2 Recovery
Coins held in a 2of2 account need to be signed by both you and GreenAddress.
Provided you have nLocktime emails enabled in your settings, the service
automatically generates special "nLockTime" transactions, pre-signed by
GreenAddress but not spendable until some time in the future (the nLockTime).

To recover coins from a 2of2 account you simply wait until each nLockTime
transaction becomes spendable (90 days by default), then countersign using
the recovery tool and broadcast. The coins are sent to a key derived
from your login mnemonics which you can then sweep into any wallet.

You will need:

1) The latest nlocktimes.zip file sent to your email address from GreenAddress  
2) Your GreenAddress mnemonic  
3) The recovery tool

To run the recovery tool in 2of2 mode:
```
$ garecovery-cli 2of2 --nlocktime-file /path/to/downloaded/nlocktimes.zip -o garecovery.csv
```

Enter your mnemonic when prompted. The recovery tool will print a summary of the
recovery transactions and also write them to a file `garecovery.csv`.

_WARNING_
`garecovery.csv` contains the private keys to which the coins will
be sent. Be sure to perform the recovery on a device you trust and take care
to delete the recovery csv file securely when you are finished with it.

A sample of the printed summary output is:
```
mnemonic: <your mnemonic here...>
    tx id lock time      total out                destination address     coin value
--------- --------- -------------- ---------------------------------- --------------
7a00ab...   1139186 830673.85 bits 19G11T26M6xYwbq5UpJPtGrXbsdQyzpCsx 830673.85 bits

total value = 830673.85 bits in 1 utxo
```

Here you can see the file contains a transaction worth 830673.85 bits, with
locktime = 1139186. The locktime indicates the block number that the bitcoin
blockchain must reach before the coins are available for recovery. You can
find the current block number (also known as the block height) using your local
full node or many available online tools, for example https://blockexplorer.com

Once the transactions are spendable they can be broadcast onto the network. The
raw transactions are in the csv file, along with the private key for the
address they send their coins to. You can broadcast these raw transactions
using your full node via RPC or online tools such as:

https://blockexplorer.com/tx/send  
https://www.smartbit.com.au/txs/pushtx

## 2of3 Recovery
In the case of 2of3 subaccounts you hold the mnemonics for 2 keys: the
default key used for day to day spending and a backup key used for recovery.
Coins held in a 2of3 account can be spent either by signing with your
default key and the GreenAddress key under normal circumstances, or by
signing with both your default and backup keys for recovery.

Unlike 2of2 where GreenAddress sends nLocktime transactions to you for
recovery, unspent coins in 2of3 subaccounts are only discoverable by
scanning the blockchain to look for them. The recovery tool connects
to your bitcoin core full node in order to perform this scanning for
you when recovering.

You will need:

1) A bitcoin core full node configured for local RPC access  
2) The recovery tool  
3) Your GreenAddress mnemonic  
4) The GreenAddress mnemonic for your 2of3 account  
5) The GreenAddress extended public key (xpub) for your 2of3 account  
6) A destination bitcoin address to send the recovered coins to

Setting up and running a bitcoin node is beyond the scope of this document
but instructions are readily available online. Ensure your node is
running, fully synced and you are able to connect to the RPC interface. You can
verify this using a command like:
```
/path/to/bitcoin-core/bin/bitcoin-cli getblockchaininfo
```

Also note that wallet functionality must not be disabled on your node.

Run the recovery tool in 2of3 mode:
```
$ garecovery-cli 2of3 --destination-address=XXXX -o garecovery.csv --ga-xpub=YYYY
```

The tool will prompt you for your mnemonic, recovery mnemonic and xpub. You
should have noted these details down when you created the 2of3 subaccount.

The tool will then connect to your node to scan for the 2of3 transactions.
This may take quite a long time. You can check the scan progress either by
looking in the bitcoind log file or in the bitcoin GUI.

If any recoverable coins were found the tool will display a summary of
them on the console and write the details to the output csv file ready for
broadcasting using the same steps as detailed above for 2of2 subaccounts.

# Troubleshooting

If you find any bugs, or have suggestions or patches, please raise them on
the [garecovery github project](https://github.com/greenaddress/garecovery).
