from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.transactions import Transaction
from web3 import Web3
from eth_account import Account
from loguru import logger
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
from tronpy import Tron
import requests
from base58 import b58decode, b58encode
from utils.gen_private_key import get_private_key, get_ltc_details

def BTC_Transfer(user_number, amount : float, recipient : str ):
    private_key = get_private_key(user_number)
    wallet = wallet_create_or_open('MyWallet', keys=private_key)
    wallet.utxos_update(networks="testnet") # Update UTXOs
    wallet.scan() # Scan the blockchain for transactions
    print("Wallet balance before transaction is : ", wallet.balance())
    amount = amount / 0.00000001
    tx = wallet.send_to(recipient, amount, fee='normal')
    signed_tx = tx.info()['hex']
    return signed_tx

def ETH_Transfer(user_number, amount : float, recipient : str):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/4f32e758e9ae4046ba13e6a4b00a2e88'))
    if not w3.is_connected():
        raise Exception("Node not connected")
    private_key = get_private_key(user_number)
    account = Account.from_key(private_key)
    amount = w3.to_wei(amount, 'ether')
    nonce = w3.eth.get_transaction_count(account.address)
    gas = w3.eth.gas_price
    gas_limit = 21000
    transaction = {
        'to': recipient,
        'value': amount,
        'gas': gas_limit,
        'gasPrice': gas,
        'nonce': nonce,
        'chainId': 1 # Mainnet
    }
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return txn_hash.hex()


def LTC_Transfer(user_number, amount : float, recipient : str ):
    # Create the payload for the transaction
    payload = {
        "sender": get_ltc_details(user_number, 'address'),
        "private_key": get_ltc_details(user_number, 'private_key'), 
        "amount": round(amount, 8),
        "receiver": recipient
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    # Send the transaction using the API (replace with your actual API endpoint)
    transaction = requests.post("https://litecoinapi-send.vercel.app/api/litecoin/send", json=payload, headers=headers)

    # Check the response
    if transaction.status_code == 200:
        # print(f"Sending {amount_ltc} LTC to {recipient_address}")
       return transaction.text
    else:
       return transaction.text

def sendUSDT(user_number, recipient: str, amount: float, fee_limit=2.5):

    def coin_to_sun( amount: float):
        return int(amount * 1_000_000)

    provider = HTTPProvider(api_key='d4e77476-2ae9-426e-b3aa-0488b3667048')
    coinwatch_api_key = 'a697c55a-fc6e-4d1f-8ca3-9c6639aabf39'
    client = Tron(provider=provider)
    private_key = get_private_key(user_number)
    private_key = PrivateKey(bytes.fromhex(private_key))
    public_key = private_key.public_key.to_base58check_address()
    block_explorer_tx = 'https://tronscan.org/#/transaction/'
    processing = False
    logger.info('Tron chain loaded! Wallet address: {}'.format(public_key))
    logger.info('Sending {} USDT to {}'.format(amount, recipient))

    contract = client.get_contract('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')
    txn = (
        contract.functions.transfer(recipient, coin_to_sun(amount))
        .with_owner(public_key)
        .fee_limit(coin_to_sun(fee_limit))
        .build()
        .sign(private_key)
    )
    tx_id = txn.txid
    logger.info('Transaction built!')

    result = txn.broadcast().wait()
    logger.info('Transaction sent with status {}! URL: {}{}'.format(
        result['receipt']['result'], block_explorer_tx, tx_id)
    )

    return tx_id, result['receipt']['result'], result


