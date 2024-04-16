from bitcoinlib.wallets import Wallet, wallet_create_or_open
from bitcoinlib.transactions import Transaction
from web3 import Web3
from eth_account import Account
from loguru import logger
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
from tronpy import Tron
from solana.rpc.api import Client
from solders.message import Message # type: ignore
from solders.transaction import Transaction # type: ignore
from solders.system_program import transfer, TransferParams
from solders.pubkey import Pubkey as PublicKey # type: ignore
from solders.keypair import Keypair # type: ignore
from solders.hash import Hash # type: ignore
from solders.commitment_config import CommitmentLevel # type: ignore
from solders.rpc.config import RpcSendTransactionConfig # type: ignore
from solders.rpc.requests import SendLegacyTransaction # type: ignore
from base58 import b58decode, b58encode


import Gen_private_key
def BTC_Transfer(user_number, amount : float, recipient : str ):
    private_key = Gen_private_key.get_private_key(user_number)
    wallet = wallet_create_or_open('MyWallet', keys=private_key)
    wallet.utxos_update(networks="testnet") # Update UTXOs
    wallet.scan() # Scan the blockchain for transactions
    print("Wallet balance before transaction is : ", wallet.balance())
    amount = amount / 0.00000001
    tx = wallet.send_to(recipient, amount, fee=1000)
    signed_tx = tx.info()['hex']
    return signed_tx

def ETH_Transfer(user_number, amount : float, recipient : str):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/4f32e758e9ae4046ba13e6a4b00a2e88'))
    if not w3.is_connected():
        raise Exception("Node not connected")
    private_key = Gen_private_key.get_private_key(user_number)
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

def Tron_Transfer(user_number, recipient: str, amount: float, fee_limit=35):
    provider = HTTPProvider(api_key='d4e77476-2ae9-426e-b3aa-0488b3667048')
    client = Tron(provider=provider)
    private_key = Gen_private_key.get_private_key(user_number)
    private_key = PrivateKey(bytes.fromhex(private_key))
    public_key = private_key.public_key.to_base58check_address()
    block_explorer_tx = 'https://tronscan.org/#/transaction/'
    processing = False
    logger.info('Tron chain loaded! Wallet address: {}'.format(public_key))
    logger.info('Sending {} TRC to {}'.format(amount, recipient))
    txn = (
        client.trx.transfer(public_key, recipient, amount * 1000000)
        .build()
        .sign(private_key)
    )
    tx_id = txn.txid
    logger.info('Transaction built!')
    result = txn.broadcast().wait()
    logger.info('Transaction {} sent! URL: {}{}'.format(
        tx_id, block_explorer_tx, tx_id)
    )
    return tx_id, 'SUCCESS', result

def Sol_Transfer(user_number, recipient: str, amount: float):
    private_key = Gen_private_key.get_private_key(user_number)
    b58_private_key = b58encode(private_key)
    keypair = b58decode(b58_private_key)
    sol_pub_key = keypair[32:]
    transfer_ix = transfer(TransferParams(from_pubkey=sol_pub_key, to_pubkey=recipient, lamports= amount * 1_000_000))
    txn = Transaction().add(transfer_ix)
    solana_client = Client("https://api.mainnet-beta.solana.com")
    return solana_client.send_transaction(txn, sol_pub_key)