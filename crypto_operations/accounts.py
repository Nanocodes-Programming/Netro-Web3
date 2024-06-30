from eth_account import Account
from bitcoin import *
from base58 import b58decode, b58encode
from utils.gen_private_key import get_private_key, get_ltc_details

# Function to generate cryptocurrency addresses for different blockchains
def get_accounts(user_number):
    # Generate a private key based on the user number
    private_key = get_private_key(user_number)

    # Ethereum (ETH)
    # Use the eth_account library to generate an Ethereum address from the private key
    eth_account = Account.from_key(private_key)
    eth_address = eth_account.address

    # Bitcoin (BTC)
    # Convert the private key to bytes and use the bitcoin library to generate a Bitcoin address
    btc_private_key = bytes.fromhex(private_key)
    btc_address = privkey_to_address(btc_private_key)

    # BSC (Binance Smart Chain)
    # Use the eth_account library again, as BSC is compatible with Ethereum addresses
    Bsc_account = Account.from_key(private_key)
    Bsc_address = Bsc_account.address


    # Litecoin
    
    ltc_address = get_ltc_details(user_number, 'address')

    # Return the addresses as a dictionary
    return {
        "eth_address": eth_address,
        "btc_address": btc_address,
        "bsc_address": Bsc_address,
        "ltc_address": ltc_address
    }

