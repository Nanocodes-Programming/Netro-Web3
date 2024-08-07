import requests
import json
from crypto_operations.transfer import sendUSDT

def USDTNGN(user_number, amount_udst: float, account_number : str, account_bank_code :str, rate : float):
    sendUSDT(user_number, 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t', amount_udst)
    secret_key = 'FLWSECK_TEST-4f0e0a374609f24bf18d23a0364d6660-X'

# Flutterwave API endpoint for transfers
    url = 'https://api.flutterwave.com/v3/transfers'

    amount = amount_udst * rate
# Transfer details
    transfer_details = {
        "account_bank": account_bank_code, # Bank code for the recipient's bank
        "account_number": account_number, # Recipient's account number
        "amount": amount, # Amount to transfer
        "narration": "9app Convert to naira", # Description of the transfer
        "currency": "NGN", # Currency of the transfer
        "reference": "FLW-TRANSFER-123456789", # Unique reference for the transfer
    }

# Headers for the API request
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {secret_key}',
    }

# Make the POST request to initiate the transfer
    response = requests.post(url, headers=headers, data=json.dumps(transfer_details))

# Check the response
    if response.status_code == 200:
        print("Transfer initiated successfully.")
        print(response.json())
    else:
        print("Failed to initiate transfer.")
        print(response.text)

