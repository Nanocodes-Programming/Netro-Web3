from solana.rpc.api import Client
from solders.message import Message, MessageHeader # type: ignore
from solders.transaction import Transaction # type: ignore
from solders.system_program import transfer, TransferParams
from solders.pubkey import Pubkey as PublicKey # type: ignore
from solders.keypair import Keypair # type: ignore
from solders.hash import Hash # type: ignore
from solana.rpc.types import Commitment 
from solders.commitment_config import CommitmentLevel # type: ignore
from solders.rpc.config import RpcSendTransactionConfig # type: ignore
from solders.rpc.requests import SendLegacyTransaction # type: ignore
from base58 import b58decode, b58encode
from web3 import Web3

def get_private_key(user_number):
    w3 = Web3()
    # This is an example seed phrase
    seed_phrase = "space cook alcohol item save mixture basket public nothing oppose infant winner"

    w3.eth.account.enable_unaudited_hdwallet_features()
    # Derive a child key from the seed using the path m/0'/0'/i'
    # The path m/0'/0'/i' means the i-th child key of the first child key of the first c
    acc = w3.eth.account.from_mnemonic(seed_phrase, account_path=f"m/44'/60'/0'/0/{user_number}")
    key = Web3.to_hex(acc.key)
    private_key = key[2:]
    return  private_key


def Sol_Transfer(user_number, recipient: str, amount: float):
    private_key = get_private_key(user_number)
    private_key_bytes = bytes.fromhex(private_key)
    # Ensure the private key bytes are 32 bytes long
    if len(private_key_bytes) != 32:
        raise ValueError("Private key must be 32 bytes long")
    # Create a Keypair from the 32-byte private key
    sender_keypair = Keypair.from_seed(private_key_bytes)
    # Correctly derive the public key from the Keypair
    sender_pubkey = sender_keypair.pubkey()
    # Create a Message instance
    message = Message(
        instructions=[transfer(TransferParams(from_pubkey=sender_pubkey, to_pubkey=PublicKey.from_string(recipient), lamports=int(amount * 1_000_000)))],
    )
    # Get a recent blockhash
    solana_client = Client("https://dry-twilight-seed.solana-mainnet.quiknode.pro/93de0fea52f81beb0790d7eca7cdd99116cb5d31/")
    # Get the latest blockhash
    latest_blockhash_resp = solana_client.get_latest_blockhash()
    print(latest_blockhash_resp)
    recent_blockhash = latest_blockhash_resp.value.blockhash
    # Create a Transaction instance
    txn = Transaction()
    txn.add_instruction(
    [sender_keypair], 
    message
    )
    txn.recent_blockhash = recent_blockhash
    # Sign the transaction with the recent_blockhash
    txn.sign(sender_keypair)
    # Send the transaction
    return solana_client.send_transaction(txn)




Sol_Transfer(1,'6cm4vNugtBYGeDJrXYnNC2uGPgVeYBtKQLzPW8HwvFVA', 4)