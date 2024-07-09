import requests
from xchainpy_client.models.tx_types import TxHistoryParams
from xchainpy_client.models.types import Network
from xchainpy_litecoin.client import Client
from xchainpy_litecoin.models.client_types import LitecoinClientParams

def get_litecoin_transactions(address):
    url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/full"
    response = requests.get(url)
    transactions = response.json().get('txs', [])
    result = []
    for tx in transactions:
        for output in tx['outputs']:
            if output['addresses'] is not None and address in output['addresses']:
                result.append({
                    "type": "Incoming",
                    "amount": int(output['value']) / 100000000,
                    # "address": output['addresses'][0]
                })
            elif output['addresses'] is not None:
                result.append({
                    "type": "Outgoing",
                    "amount": int(output['value']) / 100000000,
                    "address": output['addresses'][0]
                })
    return result
    # type of transactions is xchainpy_client.models.tx_types.TxPage

#     t = transactions.txs[0]
#     print(t.asset)
#     print(t.tx_from[0].amount)
#     print(t.tx_from[0].address)
#     print(t.tx_to[0].amount)
#     print(t.tx_to[0].address)
#     print(t.tx_date)
#     print(t.tx_type)
#     print(t.tx_hash)

#     transaction = await client.get_transaction_data(t.tx_hash)
#     # transaction object is equal by t object

# # Run the async function using an event loop
# asyncio.run(main())
print(get_litecoin_transactions('ltc1q7hqgud6yrs3e52962j46pay8cyq3x2hjy6adxp'))