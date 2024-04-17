from curses.ascii import US
from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider


def USDT_balance( address: str):
  provider = HTTPProvider(api_key='d4e77476-2ae9-426e-b3aa-0488b3667048')
  client = Tron(provider=provider)
  contract = client.get_contract('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')
  precision = contract.functions.decimals()
  return contract.functions.balanceOf(address) / 10 ** precision