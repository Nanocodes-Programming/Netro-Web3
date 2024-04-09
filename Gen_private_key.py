from web3 import Web3
w3 = Web3()
# This is an example seed phrase
seed_phrase = "letter advice cage absurd amount doctor acoustic avoid letter advice cage above"


w3.eth.account.enable_unaudited_hdwallet_features()
# Generate private keys for 1000 users
for i in range(10):
    # Derive a child key from the seed using the path m/0'/0'/i'
    # The path m/0'/0'/i' means the i-th child key of the first child key of the first c
    acc = w3.eth.account.from_mnemonic(seed_phrase, account_path=f"m/44'/60'/0'/0/{i}")
    key = Web3.to_hex(acc.key)
    private_key = key[2:]
    # master_key = Web3.to_hex(master.privkey.hex())
    # Print the private key and the path
    print(f"\naddress{i + 1} = '{acc.address}'")
    print(f"private{i + 1} = '{private_key}'")

