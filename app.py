from flask import Flask, jsonify, request
from crypto_operations.accounts import get_accounts
from crypto_operations.balances import balance_BTC, balance_ETH, balance_LTC, USDT_balance
from crypto_operations.transfer import BTC_Transfer, ETH_Transfer,  LTC_Transfer, sendUSDT
from exchange_operations.swap_coin import trx_to_usdt, LTC_USDT, BTC_USDT, ETH_USDT
from exchange_operations.exchange import USDTNGN
from exchange_operations.swap_estimate import get_estimate
from exchange_operations.swap_status import get_status
from api_operations.coin_prices import get_usd_prices, get_naira_prices
from crypto_operations.get_transactions import (get_bitcoin_transactions,get_usdt_transactions,get_litecoin_transactions, get_ethereum_transactions)

app = Flask(__name__)

@app.route('/get_accounts/<int:user_number>', methods=['GET'])
def accounts_endpoint(user_number):
    accounts = get_accounts(user_number)
    return jsonify(accounts)

@app.route('/balance/<string:currency>', methods=['GET'])
def get_currency_balance(currency):
    addr = request.args.get('address')
    if not addr:
        return jsonify({"error": "Address parameter is required"}), 400
    
    balance_functions = {
        'btc': balance_BTC,
        'eth': balance_ETH,
        'ltc': balance_LTC,
        'usdt': USDT_balance
    }
    
    if currency in balance_functions:
        balance = balance_functions[currency](addr)
        return jsonify({f"{currency}_balance": balance}), 200
    else:
        return jsonify({"error": "Unsupported currency type"}), 404

@app.route('/<string:currency>-transfer', methods=['POST'])
def currency_transfer(currency):
    data = request.json
    user_number = data.get('user_number')
    amount = data.get('amount', 0.0)
    recipient = data.get('recipient')
    
    transfer_functions = {
        'btc': BTC_Transfer,
        'eth': ETH_Transfer,
        'ltc': LTC_Transfer,
        'usdt': sendUSDT
    }
    
    if currency in transfer_functions:
        result = transfer_functions[currency](user_number, float(amount), recipient)
        return jsonify(result), 200
    else:
        return jsonify({"error": "Unsupported currency type"}), 404

@app.route('/<string:from_coin>-to-<string:to_coin>', methods=['POST'])
def coin_to_coin(from_coin, to_coin):
    data = request.json
    user_number = data.get('user_number')
    amount = float(data.get('amount', 0.0))
    
    swap_functions = {
        'trx-to-usdt': trx_to_usdt,
        'ltc-to-usdt': LTC_USDT,
        'btc-to-usdt': BTC_USDT,
        'eth-to-usdt': ETH_USDT
    }
    
    key = f"{from_coin}-to-{to_coin}"
    if key in swap_functions:
        track, response_text = swap_functions[key](user_number, amount)
        return jsonify({"track": track, "response_text": response_text}), 200
    else:
        return jsonify({"error": "Unsupported conversion type"}), 404

@app.route('/exchange-rate', methods=['POST'])
def exchange_rate():
    data = request.json
    from_coin = data.get('from_coin')
    to_coin = data.get('to_coin')
    to_coin_network = data.get('to_coin_network', 'mainnet')
    amount = float(data.get('amount', 0.0))
    estimated_amount = get_estimate(from_coin, to_coin, to_coin_network, amount)
    return jsonify({"estimated_amount": estimated_amount})

@app.route('/price/<string:currency>', methods=['GET'])
def price(currency):
    price_functions = {
        'usd': get_usd_prices,
        'naira': get_naira_prices
    }
    
    if currency in price_functions:
        try:
            data = price_functions[currency]()
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"message": "Failed to get prices.", "error": str(e)}), 500
    else:
        return jsonify({"error": "Unsupported currency type"}), 404

@app.route('/balance/all', methods=['POST'])
def get_all_balances():
    data = request.json  # Expecting a JSON with keys as currency names and values as addresses
    balances = {}
    
    balance_functions = {
        'btc': balance_BTC,
        'eth': balance_ETH,
        'ltc': balance_LTC,
        'usdt': USDT_balance
    }
    errors = {}
    for currency, address in data.items():
        if currency in balance_functions:
            try:
                balance = balance_functions[currency](address)
                balances[currency] = balance
            except Exception as e:
                if str(e) == 'account not found on-chain':
                    balances[currency] = 0
                else:
                    errors[currency] = str(e)
        else:
            errors[currency] = "Unsupported currency or missing balance function"
    return jsonify({
        "balances": balances,
        "errors": errors
    }), 200 if not errors else 400


@app.route('/get-swap-status', methods=['POST'])
def get_swap_status():
    data = request.json
    track_id = data['track_id']

    status, response_text = get_status(track_id)
    return jsonify({
        "status": status,
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


@app.route('/transactions/<string:currency>', methods=['GET'])
def get_currency_transactions(currency):
    address = request.args.get('address')
    if not address:
        return jsonify({"error": "Address parameter is required"}), 400
    
    transaction_functions = {
        'btc': get_bitcoin_transactions,
        'eth': get_ethereum_transactions,
        'usdt': get_usdt_transactions,
        'litecoin': get_litecoin_transactions
    }
    
    if currency in transaction_functions:
        transactions = transaction_functions[currency](address)
        return jsonify({f"{currency}_transactions": transactions}), 200
    else:
        return jsonify({"error": "Unsupported currency type"}), 404

@app.route('/transactions', methods=['POST'])
def get_transactions(currency):
    data = request.json  # Expecting a JSON with keys as currency names and values as addresses
    transactions = {}
    errors = {}

    transaction_functions = {
        'btc': get_bitcoin_transactions,
        'eth': get_ethereum_transactions,
        'usdt': get_usdt_transactions,
        'litecoin': get_litecoin_transactions
    }

    for currency, address in data.items():
        if currency in transaction_functions:
            try:
                transaction = transaction_functions[currency](address)
                transactions[currency] = transaction
            except Exception as e:
                errors[currency] = str(e)
        else:
            errors[currency] = "Unsupported currency or missing transaction function"
        
    return jsonify({
        "transactions": transactions,
        "errors": errors
    }), 200 if not errors else 400

@app.route('/', methods=['GET'])
def index():
    return jsonify("Welcome to the Netro Web3 Service")

if __name__ == '__main__':
    app.run(debug=True)
