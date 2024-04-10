from flask import Flask, request, jsonify
from http import client
from multiprocessing.connection import Client
from moralis import evm_api, sol_api
import requests
import blockcypher
from moneywagon import AddressBalance
from tronpy import Tron
from tronpy.providers import HTTPProvider

app = Flask(__name__)

moralis_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImZlYjI1ZTAxLWIwZTktNGQ0Ny1hN2FjLWIwMTJlMjYxYmE5MCIsIm9yZ0lkIjoiMjE5MjcxIiwidXNlcklkIjoiMjE4OTczIiwidHlwZUlkIjoiZTUyZjM5NWQtNDZlZC00YzI5LTgwNTQtYmVlNGJlNzQ1Yjc0IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MTE4MzkzNzMsImV4cCI6NDg2NzU5OTM3M30.4bP6Vsi81YPRGmvVz4yWgh_7EiBTX4-pr8FRbTL82tw'

def balance_BTC(addr):
    try:
        total = blockcypher.get_total_balance(addr)
        return total
    except:
        total = AddressBalance().action('btc', addr)
        return total

def balance_ETH(addr):
    params = {
        'chain' :'eth',
        'address' : addr }
    result1 = evm_api.balance.get_native_balance(api_key= moralis_api_key, params= params, )
    return result1

def balance_SOL(addr):
    params = {
        'network' :'mainnet',
        'address' : addr }
    res = sol_api.account.get_portfolio(api_key= moralis_api_key, params= params, )
    res1 = res['nativeBalance']['solana']
    return res1

def get_trx_balance(address : str):
    provider = HTTPProvider(api_key='d4e77476-2ae9-426e-b3aa-0488b3667048')
    client = Tron(provider=provider)
    return float(client.get_account_balance(address))

@app.route('/balance', methods=['GET'])
def get_balance():
    btc_address = request.args.get('btc_address')
    eth_address = request.args.get('eth_address')
    sol_address = request.args.get('sol_address')
    trx_address = request.args.get('trx_address')

    response = {}

    if btc_address:
        response['BTC'] = balance_BTC(btc_address)
    if eth_address:
        response['ETH'] = balance_ETH(eth_address)
    if sol_address:
        response['SOL'] = balance_SOL(sol_address)
    if trx_address:
        response['TRX'] = get_trx_balance(trx_address)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)