from eth_account import Account
from bitcoin import *
from tron_address_converter import TronConverter
from base58 import b58decode, b58encode


# Example private key
private_key = '77136ff573b032b47590efe38521c04baaa93f6ffcffaacf1d8637d6bfcf74ba'

# Ethereum (ETH)
eth_account = Account.from_key(private_key)
eth_address = eth_account.address
print(f"Ethereum Address: {eth_address}")

# Bitcoin (BTC)
btc_private_key = bytes.fromhex(private_key)
btc_address = privkey_to_address(btc_private_key)
print(f"Bitcoin Address: {btc_address}")

# Bsc (Bsc)
Bsc_account = Account.from_key(private_key)
Bsc_address = Bsc_account.address
print(f"Bsc Address: {Bsc_address}")

# Tron (Trc)
converter = TronConverter()
tron_address = converter.from_hex(eth_address)
print(f'Tron Address : {tron_address}')

# Solana
b58_private_key = b58encode(private_key)
keypair = b58decode(b58_private_key)
sol_priv_key = keypair[:32]
sol_pub_key = keypair[32:]

sol_address = b58encode(sol_pub_key).decode()
print(f'Sol Address : {sol_address}')