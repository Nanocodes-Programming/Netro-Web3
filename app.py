from flask import Flask, jsonify, request
from crypto_operations.accounts import get_accounts
from crypto_operations import balances
from exchange_operations.exchange import BTC_USDT, SOL_USDT
from api_operations.coin_prices import get_usd_prices, get_naira_prices

app = Flask(__name__)

@app.route('/get_accounts/<int:user_number>', methods=['GET'])
def accounts_endpoint(user_number):
    accounts = get_accounts(user_number)
    return jsonify(accounts)

@app.route('/balance', methods=['GET'])
def balance_endpoint():
    btc_address = request.args.get('btc_address')
    eth_address = request.args.get('eth_address')
    sol_address = request.args.get('sol_address')
    trx_address = request.args.get('trx_address')
    response = {}
        # Check if each address is provided and fetch its balance
    if btc_address:
        response['BTC'] = balances.balance_BTC(btc_address)
    if eth_address:
        response['ETH'] = balances.balance_ETH(eth_address)
    if sol_address:
        response['SOL'] = balances.balance_SOL(sol_address)
    if trx_address:
        response['TRX'] = balances.get_trx_balance(trx_address)

    return response

@app.route('/exchange_btc_usdt', methods=['POST'])
def exchange_btc_usdt():
    user_number = request.json['user_number']
    amount = request.json['amount']
    BTC_USDT(user_number, amount)
    return jsonify({'status': 'success'})

@app.route('/price_usd', methods=['GET'])
def price_usd():
    return jsonify(get_usd_prices())


@app.route('/price-naira', methods=['GET'])
def price_naira():
    return jsonify(get_naira_prices())

if __name__ == '__main__':
    app.run(debug=True)
