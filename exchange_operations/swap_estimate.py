import requests
import json

def get_estimate(from_coin : str, to_coin : str, to_coin_network : str, amount : float) :
    url = "https://api.changenow.io/v2/exchange/estimated-amount"

    payload = {
        "fromCurrency": from_coin,
        "toCurrency" : to_coin,
        "toNetwork" : to_coin_network,
        "fromNetwork": from_coin,
        'fromAmount' : amount,
        'flow': "standard"

    }
    headers = {
        'Content-Type': 'application/json',
        'x-changenow-api-key': "d9872c64579f8880ee9da4e78a48af7ef368c4dc5f9c1e5bd2b8a606b64c0d86",
    }
    response = requests.request('GET', url, headers=headers, data=payload)
    print (response.text)
    dat = json.loads(response.text)
    estimatedAmount = dat['toAmount']
    print(estimatedAmount)
    print (response.text)

# code is good but there is an internal server error
