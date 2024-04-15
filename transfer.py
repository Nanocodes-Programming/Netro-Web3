# Import necessary libraries for each blockchain
from bitcoinlib.wallets import HDWallet
from bitcoinlib.transactions import Transaction
from web3 import Web3
from loguru import logger
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
from tronpy import Tron
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction
from base58 import b58decode, b58encode

# Import a custom module for generating private keys
import Gen_private_key

# Function to transfer Bitcoin (BTC)
def BTC_Transfer(user_number, amount : float, recipient : str ):
    # Generate a private key based on the user number
    private_key = Gen_private_key.get_private_key(user_number)
    # Create a Bitcoin wallet using the private key
    wallet = HDWallet.create('MyWallet', keys=private_key)
    # Convert the amount to satoshis (1 BTC = 100,000,000 satoshis)
    amount = amount / 0.00000001
    # Send the transaction
    tx = wallet.send_to(recipient, amount, fee=1000)
    # Get the signed transaction in hexadecimal format
    signed_tx = tx.info()['hex']
    return signed_tx

# Function to transfer Ethereum (ETH)
def ETH_Transfer(user_number, amount : float, recipient : str):
    # Initialize a Web3 instance with a node URL
    w3 = Web3(Web3.HTTPProvider('your_node_url'))
    # Check if connected to the node
    if not w3.isConnected():
        raise Exception("Node not connected")
    # Generate a private key based on the user number
    private_key = Gen_private_key.get_private_key(user_number)
    # Convert the amount to wei (1 ETH = 1e18 wei)
    amount = w3.toWei(amount, 'ether')
    # Get the nonce for the sender's address
    nonce = w3.eth.getTransactionCount(w3.eth.account.privateKeyToAccount(private_key).address)
    # Get the current gas price
    gas_price = w3.eth.gasPrice
    # Set the gas limit for the transaction
    gas_limit = 21000
    # Define the transaction parameters
    transaction = {
        'to': recipient,
        'value': amount,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'chainId': 1 # Mainnet
    }
    # Sign the transaction
    signed_txn = w3.eth.account.signTransaction(transaction, private_key)
    # Send the signed transaction and get the transaction hash
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
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
    # Create a Solana keypair from the decoded keypair
    sender = Keypair.from_bytes(keypair)
    # Define the transfer parameters
    transfer_ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=recipient, lamports= amount * 1_000_000))
    # Create a Solana transaction with the transfer instruction
    txn = Transaction().add(transfer_ix)
    # Initialize a Solana client
    solana_client = Client("https://api.mainnet-beta.solana.com")
    # Send the transaction and return the result
    return solana_client.send_transaction(txn, sender)
