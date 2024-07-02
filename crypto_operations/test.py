import requests

def get_ltc_balance(addy):
    # Fetch balance data from BlockCypher API
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{addy}/balance')
    if response.status_code != 200:
        if response.status_code == 400:
            print("Invalid LTC address.")
        else:
            print(f"Failed to retrieve balance. Error {response.status_code}. Please try again later.")
        return

    data = response.json()
    balance = data['balance'] / 10 ** 8
    return balance


print(get_ltc_balance("3CDJNfdWX8m2NwuGUV3nhXHXEeLygMXoAj"))

