from flask import Flask, jsonify
from eth_account import Account
from bitcoin import *
from tron_address_converter import TronConverter
from base58 import b58decode, b58encode

import Gen_private_key

app = Flask(__name__)

def get_accounts(user_number):
    # Example private key
    private_key = Gen_private_key.get_private_key(user_number)

    # Ethereum (ETH)
    eth_account = Account.from_key(private_key)
    eth_address = eth_account.address

    # Bitcoin (BTC)
    btc_private_key = bytes.fromhex(private_key)
    btc_address = privkey_to_address(btc_private_key)

    # Bsc (Bsc)
    Bsc_account = Account.from_key(private_key)
    Bsc_address = Bsc_account.address

    # Tron (Trc)
    converter = TronConverter()
    tron_address = converter.from_hex(eth_address)

    # Solana
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

@app.route('/get_accounts/<int:user_number>', methods=['GET'])
def get_accounts_endpoint(user_number):
    accounts = get_accounts(user_number)
    return jsonify(accounts)

if __name__ == '__main__':
    app.run(debug=True)
