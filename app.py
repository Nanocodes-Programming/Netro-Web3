from flask import Flask, jsonify, request
from crypto_operations.accounts import get_accounts
from crypto_operations import balances
from crypto_operations.transfer import BTC_Transfer, ETH_Transfer, Tron_Transfer, Sol_Transfer, sendUSDT
from exchange_operations.swap_coin import trx_to_usdt, SOL_USDT, BTC_USDT, ETH_USDT
from exchange_operations.exchange import USDTNGN
from exchange_operations.swap_estimate import get_estimate
from exchange_operations.swap_status import get_status
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


# Endpoint for Bitcoin (BTC) Transfer
@app.route('/btc-transfer', methods=['POST'])
def btc_transfer():
    data = request.json
    user_number = data['user_number']
    amount = float(data['amount'])
    recipient = data['recipient']
    signed_tx = BTC_Transfer(user_number, amount, recipient)
    return jsonify({
        "signed_tx": signed_tx
    })

# Endpoint for Ethereum (ETH) Transfer
@app.route('/eth-transfer', methods=['POST'])
def eth_transfer():
    data = request.json
    user_number = data['user_number']
    amount = float(data['amount'])
    recipient = data['recipient']
    txn_hash = ETH_Transfer(user_number, amount, recipient)
    return jsonify({
        "txn_hash": txn_hash
    })

# Endpoint for Tron (TRX) Transfer
@app.route('/tron-transfer', methods=['POST'])
def tron_transfer():
    data = request.json
    user_number = data['user_number']
    recipient = data['recipient']
    amount = float(data['amount'])
    tx_id, status, result = Tron_Transfer(user_number, recipient, amount)
    return jsonify({
        "tx_id": tx_id,
        "status": status,
        "result": result
    })

# Endpoint for Solana (SOL) Transfer
@app.route('/sol-transfer', methods=['POST'])
def sol_transfer():
    data = request.json
    user_number = data['user_number']
    recipient = data['recipient']
    amount = float(data['amount'])
    tx_result = Sol_Transfer(user_number, recipient, amount)
    return jsonify({
        "tx_result": tx_result
    })

# Endpoint for USDT Transfer
@app.route('/usdt-transfer', methods=['POST'])
def usdt_transfer():
    data = request.json
    user_number = data['user_number']
    recipient = data['recipient']
    amount = float(data['amount'])
    tx_id, status, result = sendUSDT(user_number, recipient, amount)
    return jsonify({
        "tx_id": tx_id,
        "status": status,
        "result": result
    })


@app.route('/trx-to-usdt', methods=['POST'])
def trx_to_usdt_endpoint():
    data = request.json
    user_number = data['user_number']
    amount_trx = float(data['amount_trx'])
    tx_id, result_status, result = trx_to_usdt(user_number, amount_trx)
    return jsonify({
        "tx_id": tx_id,
        "result_status": result_status,
        "result": result
    })

# Endpoint for SOL to USDT conversion
@app.route('/sol-to-usdt', methods=['POST'])
def sol_to_usdt_endpoint():
    data = request.json
    user_number = data['user_number']
    amount = float(data['amount'])
    track, response_text = SOL_USDT(user_number, amount)
    return jsonify({
        "track": track,
        "response_text": response_text
    })

# Endpoint for BTC to USDT conversion
@app.route('/btc-to-usdt', methods=['POST'])
def btc_to_usdt_endpoint():
    data = request.json
    user_number = data['user_number']
    amount = float(data['amount'])
    track, response_text = BTC_USDT(user_number, amount)
    return jsonify({
        "track": track,
        "response_text": response_text
    })

# Endpoint for ETH to USDT conversion
@app.route('/eth-to-usdt', methods=['POST'])
def eth_to_usdt_endpoint():
    data = request.json
    user_number = data['user_number']
    amount = float(data['amount'])
    track, response_text = ETH_USDT(user_number, amount)
    return jsonify({
        "track": track,
        "response_text": response_text
    })

@app.route('/usdt-to-ngn', methods=['POST'])
def usdt_to_ngn():
    data = request.json
    user_number = data['user_number']
    amount_udst = float(data['amount_udst'])
    account_number = data['account_number']
    account_bank_code = data['account_bank_code']
    rate = float(data['rate'])

    try:
        # Call the USDT to NGN transfer function from exchange.py
        result = USDTNGN(user_number, amount_udst, account_number, account_bank_code, rate)
        return jsonify({"message": "Transfer initiated successfully.", "result": result}), 200
    except Exception as e:
        return jsonify({"message": "Failed to initiate transfer.", "error": str(e)}), 500


# Endpoint for getting exchange estimate
@app.route('/get-exchange-estimate', methods=['POST'])
def get_exchange_estimate():
    data = request.json
    from_coin = data['from_coin']
    to_coin = data['to_coin']
    to_coin_network = data['to_coin_network']
    amount = float(data['amount'])
    estimated_amount = get_estimate(from_coin, to_coin, to_coin_network, amount)
    return jsonify({
        "estimated_amount": estimated_amount
    })

# Endpoint for getting swap status
@app.route('/get-swap-status', methods=['POST'])
def get_swap_status():
    data = request.json
    track_id = data['track_id']

    status, response_text = get_status(track_id)

    return jsonify({
        "status": status,
        "response_text": response_text
    })


@app.route('/price_usd', methods=['GET'])
def price_usd():
    return jsonify(get_usd_prices())


@app.route('/price-naira', methods=['GET'])
def price_naira():
    return jsonify(get_naira_prices())


if __name__ == '__main__':
    app.run(debug=True)
