import requests
import json

def get_usd_prices():
    # Define the URL for the CoinMarketCap API endpoint
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    # Define the headers for the API request, including the API key
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'e8e906cf-65bc-477f-bb59-71e23e7ee9d0',
    }

    # Create a session to manage the API requests
    session = requests.Session()
    session.headers.update(headers)

    try:
        # Fetch the latest listing for Bitcoin (BTC)
        response = session.get(url, params={'start': '1', 'limit': '1', 'convert': 'USD'})
        data = json.loads(response.text)
        for entry in data['data']:
            Name_BTC = entry['name']
            symbol_BTC = entry["symbol"]
            price_BTC = entry['quote']['USD']["price"]
            percentage_BTC = entry['quote']['USD']["percent_change_24h"]

        # Fetch the latest listing for Ethereum (ETH)
        response = session.get(url, params={'start': '2', 'limit': '1', 'convert': 'USD'})
        data = json.loads(response.text)
        for entry in data['data']:
            Name_ETH = entry['name']
            symbol_ETH = entry["symbol"]
            price_ETH = entry['quote']['USD']["price"]
            percentage_ETH = entry['quote']['USD']["percent_change_24h"]

        # Fetch the latest listing for Tether (USDT)
        response = session.get(url, params={'start': '3', 'limit': '1', 'convert': 'USD'})
        data = json.loads(response.text)
        for entry in data['data']:
            Name_USDT = entry['name']
            symbol_USDT = entry["symbol"]
            price_USDT = entry['quote']['USD']["price"]
            percentage_USDT = entry['quote']['USD']["percent_change_24h"]


        # Fetch the latest listing for Litecoin (LTC)
        response = session.get(url, params={'start': '18', 'limit': '1', 'convert': 'USD'})
        data = json.loads(response.text)
        for entry in data['data']:
            Name_LTC = entry['name']
            symbol_LTC = entry["symbol"]
            price_LTC = entry['quote']['USD']["price"]
            percentage_LTC = entry['quote']['USD']["percent_change_24h"]

        # Return the cryptocurrency prices and changes as a JSON response
        return {
            'BTC': {'name': Name_BTC, 'symbol': symbol_BTC, 'price': price_BTC, 'change': percentage_BTC},
            'ETH': {'name': Name_ETH, 'symbol': symbol_ETH, 'price': price_ETH, 'change': percentage_ETH},
            'USDT': {'name': Name_USDT, 'symbol': symbol_USDT, 'price': price_USDT, 'change': percentage_USDT},
            'LTC': {'name': Name_LTC, 'symbol': symbol_LTC, 'price': price_LTC, 'change': percentage_LTC},
        }
    except Exception as e:
        # Handle exceptions and return an error message
        raise Exception(e)


def get_naira_prices():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'e8e906cf-65bc-477f-bb59-71e23e7ee9d0',
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params={'start': '1', 'limit': '1', 'convert': 'NGN'})
        data = json.loads(response.text)
        for entry in data['data']:
            Name_BTC = entry['name']
            symbol_BTC = entry["symbol"]
            price_BTC = entry['quote']['NGN']["price"]
            percentage_BTC = entry['quote']['NGN']["percent_change_24h"]

        response = session.get(url, params={'start': '2', 'limit': '1', 'convert': 'NGN'})
        data = json.loads(response.text)
        for entry in data['data']:
            Name_ETH = entry['name']
            symbol_ETH = entry["symbol"]
            price_ETH = entry['quote']['NGN']["price"]
            percentage_ETH = entry['quote']['NGN']["percent_change_24h"]

        response = session.get(url, params={'start': '3', 'limit': '1', 'convert': 'NGN'})
        data = json.loads(response.text)
        for entry in data['data']:
            Name_USDT = entry['name']
            symbol_USDT = entry["symbol"]
            price_USDT = entry['quote']['NGN']["price"]
            percentage_USDT = entry['quote']['NGN']["percent_change_24h"]

        response = session.get(url, params={'start': '18', 'limit': '1', 'convert': 'NGN'})
        data = json.loads(response.text)
        for entry in data['data']:
            Name_LTC = entry['name']
            symbol_LTC = entry["symbol"]
            price_LTC = entry['quote']['NGN']["price"]
            percentage_LTC = entry['quote']['NGN']["percent_change_24h"]

        return {
            'BTC': {'name': Name_BTC, 'symbol': symbol_BTC, 'price': price_BTC, 'change': percentage_BTC},
            'ETH': {'name': Name_ETH, 'symbol': symbol_ETH, 'price': price_ETH, 'change': percentage_ETH},
            'USDT': {'name': Name_USDT, 'symbol': symbol_USDT, 'price': price_USDT, 'change': percentage_USDT},
            'LTC': {'name': Name_LTC, 'symbol': symbol_LTC, 'price': price_LTC, 'change': percentage_LTC},
        }
    except Exception as e:
        raise Exception(e)
