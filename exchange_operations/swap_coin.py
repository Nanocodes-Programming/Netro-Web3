import datetime
import requests
from utils.gen_private_key import get_private_key
from tronpy import Tron
from loguru import logger
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
from crypto_operations.accounts import get_accounts
from crypto_operations import transfer
import json

def trx_to_usdt(user_number, amount_trx: float, fee_limit=250):

    provider = HTTPProvider(api_key='d4e77476-2ae9-426e-b3aa-0488b3667048')
    coinwatch_api_key = 'a697c55a-fc6e-4d1f-8ca3-9c6639aabf39'
    client = Tron(provider=provider)
    private_key = get_private_key(user_number)
    private_key = PrivateKey(bytes.fromhex(private_key))
    public_key = private_key.public_key.to_base58check_address()
    block_explorer_tx = 'https://tronscan.org/#/transaction/'
    processing = False
    logger.info('Tron chain loaded! Wallet address: {}'.format(public_key))

    def enum(**enums):
        return type('Enum', (), enums)

    def coin_to_sun( amount: float):
        return int(amount * 1_000_000)

    Contract = enum(
        USDT='TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t',
        TRX='TNUC9Qb1rRpS5CbWLmNMxXBjyFoydXjWFR',
        SUN_SWAP_V2='TKzxdSv2FZKQrEqkKVgp5DcwEXBEKMg2Ax'
    )
    def get_trx_price(coinwatch_api_key, amount: float = 1):
        def livecoinwatch():
            url = "https://api.livecoinwatch.com/coins/single"

            payload = {
                "currency": "USD",
                "code": "TRX",
                "meta": True
            }
            headers = {
                'content-type': 'application/json',
                'x-api-key': coinwatch_api_key
            }

            return requests.post(url, headers=headers, json=payload).json()['rate']

        def coingecko():
            result = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=tron&vs_currencies=usd')
            return result.json()['tron']['usd']

        try:
            one_trx = coingecko()
            logger.info('1 TRX = {} USD | CoinGecko'.format(one_trx))
        except Exception as ex:
            logger.info('CoinGecko error: {} | Trying coinwatch...'.format(ex))
            one_trx = livecoinwatch()
            logger.info('1 TRX = {} USD | LiveCoinWatch'.format(one_trx))

        return amount * one_trx

    contract = client.get_contract(Contract.SUN_SWAP_V2)

    time_window = datetime.datetime.now() + datetime.timedelta(seconds=60)
    min_out = get_trx_price(amount_trx) * 0.99

    logger.info('Trying to swap {:.2f} TRX to min of {:.2f} USDT'.format(amount_trx, min_out))

    txn = (
        contract.functions.swapExactETHForTokens.with_transfer(coin_to_sun(amount_trx))(
            coin_to_sun(min_out),
            [Contract.TRX, Contract.USDT],
            public_key,
            int(time_window.timestamp())
            )
        .with_owner(public_key)
        .fee_limit(coin_to_sun(fee_limit))
        .build()
        .sign(private_key)
        )


    tx_id = txn.txid
    logger.info('Transaction built!')

    result = txn.broadcast().wait()
    logger.info('Transaction sent with status {}! URL: {}{}'.format(
        result['receipt']['result'], block_explorer_tx, tx_id)
    )

    return tx_id, result['receipt']['result'], result

def SOL_USDT(user_number, amount : float) :

    addresses = get_accounts(user_number)
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
    receiving_amount = dat['toAmount']
    track =  dat['id']
    print(" You will be receiving : {} Usdt".format(receiving_amount))
    transfer.Sol_Transfer(user_number, amount, recipient)
    return track, response.text




def BTC_USDT(user_number, amount : float) :

    addresses = get_accounts(user_number)
    Tron_Address = addresses['tron_address']
    url = "https://api.changenow.io/v2/exchange"

    data = {
        "fromCurrency": "BTC",
        "toCurrency": "usdt",
        "fromNetwork": "btc",
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
    receiving_amount = dat['toAmount']
    track =  dat['id']
    print(" You will be receiving : {} Usdt".format(receiving_amount))
    transfer.BTC_Transfer(user_number, amount, recipient)
    return track, response.text


def ETH_USDT(user_number, amount : float) :

    addresses = get_accounts(user_number)
    Tron_Address = addresses['tron_address']
    url = "https://api.changenow.io/v2/exchange"

    data = {
        "fromCurrency": "eth",
        "toCurrency": "usdt",
        "fromNetwork": "eth",
        "toNetwork": "trx",
        "fromAmount": amount, #"Amount is less then minimal: 0.003 ETH"
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
    receiving_amount = dat['toAmount']
    track =  dat['id']
    print(" You will be receiving : {} Usdt".format(receiving_amount))
    transfer.ETH_Transfer(user_number, amount, recipient)
    return track, response.text

