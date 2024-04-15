# Import necessary libraries
from flask import Flask, jsonify
from eth_account import Account
from bitcoin import *
from tron_address_converter import TronConverter
from base58 import b58decode, b58encode

# Import a custom module for generating private keys
import Gen_private_key

# Initialize the Flask application
app = Flask(__name__)

# Function to generate cryptocurrency addresses for different blockchains
def get_accounts(user_number):
    # Generate a private key based on the user number
    private_key = Gen_private_key.get_private_key(user_number)

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

    # Tron (TRC)
    # Use the TronConverter to convert an Ethereum address to a Tron address
    converter = TronConverter()
    tron_address = converter.from_hex(eth_address)

    # Solana
    # Encode the private key in base58 format, then decode it to get the public key
    # Solana addresses are derived from the public key
    b58_private_key = b58encode(private_key)
    keypair = b58decode(b58_private_key)
    sol_priv_key = keypair[:32]
    sol_pub_key = keypair[32:]
    sol_address = b58encode(sol_pub_key).decode()

    # Return the addresses as a dictionary
    return {
        "eth_address": eth_address,
        "btc_address": btc_address,
        "bsc_address": Bsc_address,
        "tron_address": tron_address,
        "sol_address": sol_address
    }

# Flask route to get cryptocurrency addresses for a given user number
@app.route('/get_accounts/<int:user_number>', methods=['GET'])
def get_accounts_endpoint(user_number):
    # Call the get_accounts function with the user number
    accounts = get_accounts(user_number)
    # Return the addresses as a JSON response
    return jsonify(accounts)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

