import requests
import json
import Gen_private_key
import transfer
import Accounts

def SOL_USDT(user_number, amount : float) :

    addresses = Accounts.get_accounts(user_number)
    Tron_Address = addresses['tron_address']
    url = "https://api.changenow.io/v2/exchange"

    data = {
        "fromCurrency": "sol",
        "toCurrency": "usdt",
        "fromNetwork": "sol",
        "toNetwork": "trx",
        "fromAmount": amount, #"Amount is less then minimal: 0.0006343 BTC"
        "toAmount": "",
        "address": Tron_Address,
        "extraId": "",
        "refundAddress": "",
        "refundExtraId": "",
        "userId": "",
        "payload": "",
        "contactEmail": "",
        "source": "",
        "flow": "standard",
        "type": "direct",
        "rateId": ""
    }

    headers = {
        'Content-Type': 'application/json',
        'x-changenow-api-key': "d9872c64579f8880ee9da4e78a48af7ef368c4dc5f9c1e5bd2b8a606b64c0d86",
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    dat = json.loads(response.text)
    recipient = dat['payinAddress']
    transfer.Sol_Transfer(user_number, amount, recipient)

SOL_USDT(1, 0.1)


