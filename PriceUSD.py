from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json



url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
headers = {
'Accepts': 'application/json',
'X-CMC_PRO_API_KEY': 'e8e906cf-65bc-477f-bb59-71e23e7ee9d0',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params={'start' : '1', 'limit' : '1', 'convert':'USD'})
    data = json.loads(response.text)
    # print(data)
    for entry in data['data']:
        Name_BTC = entry['name']
        symbol_BTC = entry["symbol"]
        price_BTC = entry['quote']['USD']["price"]
        percentage_BTC = entry['quote']['USD']["percent_change_24h"]


    print("{} {}: price USD is {:.2f} \nChange: {} ".format(Name_BTC, symbol_BTC, price_BTC, percentage_BTC))
    response = session.get(url, params={'start' : '2', 'limit' : '1','convert':'USD'})
    data = json.loads(response.text)
    # print(data)
    for entry in data['data']:
        Name_ETH = entry['name']
        symbol_ETH = entry["symbol"]
        price_ETH = entry['quote']['USD']["price"]
        percentage_ETH = entry['quote']['USD']["percent_change_24h"]

    print("{} {}: price USD is {:.2f} \nChange: {} ".format(Name_ETH, symbol_ETH, price_ETH, percentage_ETH))
    response = session.get(url, params={'start' : '3', 'limit' : '1','convert':'USD'})
    data = json.loads(response.text)
    # print(data)
    for entry in data['data']:
        Name_USDT = entry['name']
        symbol_USDT = entry["symbol"]
        price_USDT = entry['quote']['USD']["price"]
        percentage_USDT = entry['quote']['USD']["percent_change_24h"]

    print("{} {}: price USD is {:.2f} \nChange: {} ".format(Name_USDT, symbol_USDT, price_USDT, percentage_USDT))
    response = session.get(url, params={'start' : '16', 'limit' : '1','convert':'USD'})
    data = json.loads(response.text)
    # print(data)
    for entry in data['data']:
        Name_TRX = entry['name']
        symbol_TRX = entry["symbol"]
        price_TRX = entry['quote']['USD']["price"]
        percentage_TRX = entry['quote']['USD']["percent_change_24h"]

    print("{} {}: price USD is {:.2f} \nChange: {} ".format(Name_TRX, symbol_TRX, price_TRX, percentage_TRX))
    response = session.get(url, params={'start' : '4', 'limit' : '1','convert':'USD'})
    data = json.loads(response.text)
    # print(data)
    for entry in data['data']:
        Name_SOL = entry['name']
        symbol_SOL = entry["symbol"]
        price_SOL = entry['quote']['USD']["price"]
        percentage_SOL = entry['quote']['USD']["percent_change_24h"]

    print("{} {}: price USD is {:.2f} \nChange: {} ".format(Name_SOL, symbol_SOL, price_SOL, percentage_SOL))
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

