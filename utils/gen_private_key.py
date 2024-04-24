from web3 import Web3

def get_private_key(user_number):
    w3 = Web3()
    # This is an example seed phrase
    seed_phrase = "space cook alcohol item save mixture basket public nothing oppose infant winner"

    w3.eth.account.enable_unaudited_hdwallet_features()
    # Derive a child key from the seed using the path m/0'/0'/i'
    # The path m/0'/0'/i' means the i-th child key of the first child key of the first c
    acc = w3.eth.account.from_mnemonic(seed_phrase, account_path=f"m/44'/60'/0'/0/{user_number}")
    key = Web3.to_hex(acc.key)
    private_key = key[2:]
    return  private_key