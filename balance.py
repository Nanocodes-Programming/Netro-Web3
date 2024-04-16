# Import necessary libraries
from flask import Flask, request, jsonify
from http import client
from multiprocessing.connection import Client
from moralis import evm_api, sol_api
import requests
import blockcypher
from moneywagon import AddressBalance
from tronpy import Tron
from tronpy.providers import HTTPProvider

# Initialize the Flask application
app = Flask(__name__)

# Define the Moralis API key for interacting with Ethereum and Solana
moralis_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImZlYjI1ZTAxLWIwZTktNGQ0Ny1hN2FjLWIwMTJlMjYxYmE5MCIsIm9yZ0lkIjoiMjE5MjcxIiwidXNlcklkIjoiMjE4OTczIiwidHlwZUlkIjoiZTUyZjM5NWQtNDZlZC00YzI5LTgwNTQtYmVlNGJlNzQ1Yjc0IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MTE4MzkzNzMsImV4cCI6NDg2NzU5OTM3M30.4bP6Vsi81YPRGmvVz4yWgh_7EiBTX4-pr8FRbTL82tw'

# Function to get the balance of a Bitcoin address
def balance_BTC(addr : str):
    try:
        # Use the blockcypher library to get the total balance of the BTC address
        total = blockcypher.get_total_balance(addr)
        return total
    except:
        # If blockcypher fails, use the moneywagon library as a fallback
        total = AddressBalance().action('btc', addr)
        return total

# Function to get the balance of an Ethereum address
def balance_ETH(addr : str):
    # Define the parameters for the Moralis API request
    params = {
        'chain' :'eth',
        'address' : addr }
    # Use the Moralis API to get the native balance of the ETH address
    result1 = evm_api.balance.get_native_balance(api_key= moralis_api_key, params= params, )
    return result1

# Function to get the balance of a Solana address
def balance_SOL(addr : str):
    # Define the parameters for the Moralis API request
    params = {
        'network' :'mainnet',
        'address' : addr }
    # Use the Moralis API to get the portfolio of the SOL address
    res = sol_api.account.get_portfolio(api_key= moralis_api_key, params= params, )
    # Extract the native balance of SOL from the response
    res1 = res['nativeBalance']['solana']
    return res1

# Function to get the balance of a Tron address
def get_trx_balance(address : str):
    # Define the provider for the Tron network
    provider = HTTPProvider(api_key='d4e77476-2ae9-426e-b3aa-0488b3667048')
    # Initialize the Tron client with the provider
    client = Tron(provider=provider)
    # Get the account balance of the Tron address
    return float(client.get_account_balance(address))

# Flask route to get the balance of cryptocurrency addresses
@app.route('/balance', methods=['GET'])
def get_balance():
    # Get the addresses from the query parameters
    btc_address = request.args.get('btc_address')
    eth_address = request.args.get('eth_address')
    sol_address = request.args.get('sol_address')
    trx_address = request.args.get('trx_address')

    # Initialize an empty response dictionary
    response = {}

    # Check if each address is provided and fetch its balance
    if btc_address:
        response['BTC'] = balance_BTC(btc_address)
    if eth_address:
        response['ETH'] = balance_ETH(eth_address)
    if sol_address:
        response['SOL'] = balance_SOL(sol_address)
    if trx_address:
        response['TRX'] = get_trx_balance(trx_address)

    # Return the balances as a JSON response
    return jsonify(response)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
