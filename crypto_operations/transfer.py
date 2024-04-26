from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.transactions import Transaction
from web3 import Web3
from eth_account import Account
from loguru import logger
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
from tronpy import Tron
from decimal import Decimal
from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price # type: ignore
from solders.keypair import Keypair # type: ignore
from solders.pubkey import Pubkey # type: ignore
from solders.system_program import TransferParams, transfer
from base58 import b58decode, b58encode
from utils.gen_private_key import get_private_key

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

def Tron_Transfer(user_number, recipient: str, amount: float):
    provider = HTTPProvider(api_key='d4e77476-2ae9-426e-b3aa-0488b3667048')
    client = Tron(provider=provider)
    private_key = get_private_key(user_number)
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
    private_key = get_private_key(user_number)
    private_key_bytes = bytes.fromhex(private_key)
# Ensure the private key bytes are 32 bytes long
    if len(private_key_bytes) != 32:
        raise ValueError("Private key must be 32 bytes long")
# Create a Keypair from the 32-byte private key
    sender_keypair = Keypair.from_seed(private_key_bytes)

    src: Keypair = sender_keypair
    # recipient = "AirDCHp6eyPyPxSazfVxhCREPDf2E9FrGn9d4wSbePwE"

    sol_lamports = Decimal("1e+9")

    tx = Transaction(fee_payer=src.pubkey())
# SOL transfer
    tx.add(
    transfer(
    TransferParams(
    from_pubkey=src.pubkey(),
    to_pubkey=Pubkey.from_string(recipient),
    lamports=int(amount * sol_lamports),
    )
    )
    )
# Extra fee
    tx.add(set_compute_unit_limit(300_000))
    tx.add(set_compute_unit_price(1000))

    client = Client("https://api.mainnet-beta.solana.com")
    # Simulate the transaction
    # simulation_result = client.simulate_transaction(tx)
    # return simulation_result
    tx_sig = client.send_transaction(tx, src).value
    return client.confirm_transaction(tx_sig)
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


