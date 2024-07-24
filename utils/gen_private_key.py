from web3 import Web3
from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv()
from bip_utils import  Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
seed_phrase = os.getenv("SEED")
def get_private_key(user_number):
    w3 = Web3()
    # This is an example seed phrase

    w3.eth.account.enable_unaudited_hdwallet_features()
    # Derive a child key from the seed using the path m/0'/0'/i'
    # The path m/0'/0'/i' means the i-th child key of the first child key of the first c
    acc = w3.eth.account.from_mnemonic(seed_phrase, account_path=f"m/44'/60'/0'/0/{user_number}")
    key = Web3.to_hex(acc.key)
    private_key = key[2:]
    return  private_key

def get_ltc_details(user_number, return_type):
    seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
    bip_obj_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.LITECOIN)
    bip_obj_acc = bip_obj_mst.Purpose().Coin().Account(user_number)
    
    # For each account, derive the external chain keys: m/44'/2'/user_number'/0
    bip_obj_chain = bip_obj_acc.Change(Bip44Changes.CHAIN_EXT)
    
    # Generate the first address of each account: m/44'/2'/user_number'/0/0
    bip_obj_addr = bip_obj_chain.AddressIndex(0)

    if return_type == 'address':
        result = bip_obj_addr.PublicKey().ToAddress()
    elif return_type == 'private_key':
        result = bip_obj_addr.PrivateKey().ToWif()
    elif return_type == 'both':
        result = {
            'address': bip_obj_addr.PublicKey().ToAddress(),
            'private_key': bip_obj_addr.PrivateKey().ToWif()
        }
    else:
        raise ValueError("Invalid return_type parameter. Must be 'address', 'private_key', or 'both'.")
    
    return result



print(f"  Address: {get_ltc_details(1, 'address')}")
