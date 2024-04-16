<<<<<<< HEAD
from bitcoinlib.wallets import Wallet, wallet_create_or_open
=======
# Import necessary libraries for each blockchain
from bitcoinlib.wallets import HDWallet
>>>>>>> 3dfed24071e0b25c7cadd51bd32397c80bf8f866
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

# Import a custom module for generating private keys
import Gen_private_key

# Function to transfer Bitcoin (BTC)
def BTC_Transfer(user_number, amount : float, recipient : str ):
    # Generate a private key based on the user number
    private_key = Gen_private_key.get_private_key(user_number)
<<<<<<< HEAD
    wallet = wallet_create_or_open('MyWallet', keys=private_key)
    wallet.utxos_update(networks="testnet") # Update UTXOs
    wallet.scan() # Scan the blockchain for transactions
    print("Wallet balance before transaction is : ", wallet.balance())
=======
    # Create a Bitcoin wallet using the private key
    wallet = HDWallet.create('MyWallet', keys=private_key)
    # Convert the amount to satoshis (1 BTC = 100,000,000 satoshis)
>>>>>>> 3dfed24071e0b25c7cadd51bd32397c80bf8f866
    amount = amount / 0.00000001
    # Send the transaction
    tx = wallet.send_to(recipient, amount, fee=1000)
    # Get the signed transaction in hexadecimal format
    signed_tx = tx.info()['hex']
    return signed_tx

# Function to transfer Ethereum (ETH)
def ETH_Transfer(user_number, amount : float, recipient : str):
<<<<<<< HEAD
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/4f32e758e9ae4046ba13e6a4b00a2e88'))
    if not w3.is_connected():
=======
    # Initialize a Web3 instance with a node URL
    w3 = Web3(Web3.HTTPProvider('your_node_url'))
    # Check if connected to the node
    if not w3.isConnected():
>>>>>>> 3dfed24071e0b25c7cadd51bd32397c80bf8f866
        raise Exception("Node not connected")
    # Generate a private key based on the user number
    private_key = Gen_private_key.get_private_key(user_number)
<<<<<<< HEAD
    account = Account.from_key(private_key)
    amount = w3.to_wei(amount, 'ether')
    nonce = w3.eth.get_transaction_count(account.address)
    gas = w3.eth.gas_price
=======
    # Convert the amount to wei (1 ETH = 1e18 wei)
    amount = w3.toWei(amount, 'ether')
    # Get the nonce for the sender's address
    nonce = w3.eth.getTransactionCount(w3.eth.account.privateKeyToAccount(private_key).address)
    # Get the current gas price
    gas_price = w3.eth.gasPrice
    # Set the gas limit for the transaction
>>>>>>> 3dfed24071e0b25c7cadd51bd32397c80bf8f866
    gas_limit = 21000
    # Define the transaction parameters
    transaction = {
        'to': recipient,
        'value': amount,
        'gas': gas_limit,
        'gasPrice': gas,
        'nonce': nonce,
        'chainId': 1 # Mainnet
    }
<<<<<<< HEAD
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
=======
    # Sign the transaction
    signed_txn = w3.eth.account.signTransaction(transaction, private_key)
    # Send the signed transaction and get the transaction hash
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
>>>>>>> 3dfed24071e0b25c7cadd51bd32397c80bf8f866
    return txn_hash.hex()

# Function to transfer Tron (TRX)
def Tron_Transfer(user_number, recipient: str, amount: float, fee_limit=35):
    # Initialize a Tron client with a provider
    provider = HTTPProvider(api_key='d4e77476-2ae9-426e-b3aa-0488b3667048')
    client = Tron(provider=provider)
    # Generate a private key based on the user number
    private_key = Gen_private_key.get_private_key(user_number)
    # Convert the private key to a Tron private key object
    private_key = PrivateKey(bytes.fromhex(private_key))
    # Get the public key and address
    public_key = private_key.public_key.to_base58check_address()
    # Log the wallet address
    logger.info('Tron chain loaded! Wallet address: {}'.format(public_key))
    # Log the transfer details
    logger.info('Sending {} TRC to {}'.format(amount, recipient))
    # Build and sign the transaction
    txn = (
        client.trx.transfer(public_key, recipient, amount * 1000000)
        .build()
        .sign(private_key)
    )
    # Get the transaction ID
    tx_id = txn.txid
    # Log the transaction details
    logger.info('Transaction built!')
    result = txn.broadcast().wait()
    logger.info('Transaction {} sent! URL: {}{}'.format(
        tx_id, 'https://tronscan.org/#/transaction/', tx_id)
    )
    return tx_id, 'SUCCESS', result

# Function to transfer Solana (SOL)
def Sol_Transfer(user_number, recipient: str, amount: float):
    # Generate a private key based on the user number
    private_key = Gen_private_key.get_private_key(user_number)
    # Encode the private key in base58 format
    b58_private_key = b58encode(private_key)
    # Decode the base58 private key to get the keypair
    keypair = b58decode(b58_private_key)
<<<<<<< HEAD
    sol_pub_key = keypair[32:]
    transfer_ix = transfer(TransferParams(from_pubkey=sol_pub_key, to_pubkey=recipient, lamports= amount * 1_000_000))
=======
    # Create a Solana keypair from the decoded keypair
    sender = Keypair.from_bytes(keypair)
    # Define the transfer parameters
    transfer_ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=recipient, lamports= amount * 1_000_000))
    # Create a Solana transaction with the transfer instruction
>>>>>>> 3dfed24071e0b25c7cadd51bd32397c80bf8f866
    txn = Transaction().add(transfer_ix)
    # Initialize a Solana client
    solana_client = Client("https://api.mainnet-beta.solana.com")
<<<<<<< HEAD
    return solana_client.send_transaction(txn, sol_pub_key)
=======
    # Send the transaction and return the result
    return solana_client.send_transaction(txn, sender)
>>>>>>> 3dfed24071e0b25c7cadd51bd32397c80bf8f866
