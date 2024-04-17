import Gen_private_key
import transfer
from tronpy import Tron
from loguru import logger
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider


def sendUSDT(user_number, recipient: str, amount: float, fee_limit=35):

    def coin_to_sun( amount: float):
        return int(amount * 1_000_000)

    provider = HTTPProvider(api_key='d4e77476-2ae9-426e-b3aa-0488b3667048')
    coinwatch_api_key = 'a697c55a-fc6e-4d1f-8ca3-9c6639aabf39'
    client = Tron(provider=provider)
    private_key = Gen_private_key.get_private_key(user_number)
    private_key = PrivateKey(bytes.fromhex(private_key))
    public_key = private_key.public_key.to_base58check_address()
    block_explorer_tx = 'https://tronscan.org/#/transaction/'
    processing = False
    logger.info('Tron chain loaded! Wallet address: {}'.format(public_key))
    logger.info('Sending {} USDT to {}'.format(amount, recipient))

    contract = client.get_contract('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')
    txn = (
        contract.functions.transfer(recipient, coin_to_sun(amount))
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
