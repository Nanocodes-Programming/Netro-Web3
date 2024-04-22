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

@app.route('/balance/<string:currency>', methods=['GET'])
def get_currency_balance(currency):
    addr = request.args.get('address')
    if not addr:
        return jsonify({"error": "Address parameter is required"}), 400
    
    balance_functions = {
        'btc': balance_BTC,
        'eth': balance_ETH,
        'sol': balance_SOL,
        'trx': get_trx_balance,
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
        'tron': Tron_Transfer,
        'sol': Sol_Transfer,
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
        'sol-to-usdt': SOL_USDT,
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
        'sol': balance_SOL,
        'trx': get_trx_balance,
        'usdt': USDT_balance
    }
    
    errors = {}
    
    for currency, address in data.items():
        if currency in balance_functions:
            try:
                balance = balance_functions[currency](address)
                balances[currency] = balance
            except Exception as e:
                errors[currency] = str(e)
        else:
            errors[currency] = "Unsupported currency or missing balance function"

    return jsonify({
        "balances": balances,
        "errors": errors
    }), 200 if not errors else 400

@app.route('/', methods=['GET'])
def index():
    return jsonify("Welcome to the 9app Web3 Service")

if __name__ == '__main__':
    app.run(debug=True)
