from flask import Flask, jsonify, request
from crypto_operations.accounts import get_accounts
from crypto_operations.balances import balance_BTC, balance_ETH, balance_SOL, get_trx_balance, USDT_balance
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

# Endpoint to get Bitcoin (BTC) address balance
@app.route('/balance/btc', methods=['GET'])
def get_btc_balance():
    addr = request.args.get('address')
    if not addr:
        return jsonify({"error": "Address parameter is required"}), 400
    btc_balance = balance_BTC(addr)
    return jsonify({"btc_balance": btc_balance}), 200

# Endpoint to get Ethereum (ETH) address balance
@app.route('/balance/eth', methods=['GET'])
def get_eth_balance():
    addr = request.args.get('address')
    if not addr:
        return jsonify({"error": "Address parameter is required"}), 400
    eth_balance = balance_ETH(addr)
    return jsonify({"eth_balance": eth_balance}), 200

# Endpoint to get Solana (SOL) address balance
@app.route('/balance/sol', methods=['GET'])
def get_sol_balance():
    addr = request.args.get('address')
    if not addr:
        return jsonify({"error": "Address parameter is required"}), 400
    sol_balance = balance_SOL(addr)
    return jsonify({"sol_balance": sol_balance}), 200

# Endpoint to get Tron (TRX) address balance
@app.route('/balance/trx', methods=['GET'])
def get_trx_address_balance():
    addr = request.args.get('address')
    if not addr:
        return jsonify({"error": "Address parameter is required"}), 400
    trx_balance = get_trx_balance(addr)
    return jsonify({"trx_balance": trx_balance}), 200

# Endpoint to get USDT (Tether) balance for an address
@app.route('/balance/usdt', methods=['GET'])
def get_usdt_balance():
    addr = request.args.get('address')
    if not addr:
        return jsonify({"error": "Address parameter is required"}), 400
    usdt_balance = USDT_balance(addr)
    return jsonify({"usdt_balance": usdt_balance}), 200


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
