Recover Bitcoin Gold/BGOLD/BTG from GreenAddress wallets

#  Bitcoin Gold/BGOLD/BTG

This is same garecovery tool but for  Bitcoin Gold !!!!

Now only 2of2scan working.

# 2 of 2 Scan

## 1
Make everything the same BCASH 2of2scan. Only different is:

1) --destination-address XXXX have to give BGOLD address
2) have to give --fork 79 when run garecovery-cli to sign BGOLD

## 2

For check transaction is OK, using https://blockchain.info/decode-tx or https://live.blockcypher.com/btc/decodetx/

You take address from "outputs"/"addresses", give to https://sopaxorztaker.github.io/gold-address/

you see that transaction is pay you not me (-:


## 3

For send transaction take transaction hex from garecovery.csv, we call XXXX. Go to
http://www.btgblocks.com/api/sendrawtransaction?hexstring=XXXX in torbrowser, it send
transaction to BGOLD and give transaction hash.


If you happy, thanks for donate at:

Bitcoin: 1ApavmRLr4Trv5UeJni4fp4RRKG6affdN3 ![Bitcoin](https://raw.githubusercontent.com/dumpyourbcash/garecovery/master/img/bitcoin.png "Bitcoin")


Bitcoin Cash: 1GPgWu1cxwMRV2aqAZHSt4dQPbxFNXq7bg ![Bitcoin Cash](https://raw.githubusercontent.com/dumpyourbcash/garecovery/master/img/bcash.png "Bitcoin Cash")


Bitcoin Gold: GLNHjAXLJSqeM9CCjbDrBjRsohpsqZFnRi ![Bitcoin Gold](https://raw.githubusercontent.com/dumpyourbcash/garecovery/master/img/bgold.png "Bitcoin Gold")
