import requests
import json

def get_solana_transactions(sol_address):
    # Solana JSON RPC API endpoint
    url = "https://api.mainnet-beta.solana.com"
    
    # Prepare the request payload
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getConfirmedSignaturesForAddress2",
        "params": [
            sol_address,
            {
                "limit": 100 # Adjust the limit as needed
            }
        ]
    }
    
    # Send the request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        print (result)
        transactions = result['result']['transactions']
        # Filter transactions for incoming and outgoing
        incoming_transfers = []
        outgoing_transfers = []
        for tx in transactions:
            if tx['transaction']['message']['accountKeys'][0] == sol_address:
                outgoing_transfers.append(tx)
            else:
                incoming_transfers.append(tx)
        return incoming_transfers, outgoing_transfers
    else:
        print(f"Error: {response.status_code}")
        return None, None

# Example usage
sol_address = "6cm4vNugtBYGeDJrXYnNC2uGPgVeYBtKQLzPW8HwvFVA"
# get_solana_transactions(sol_address)
incoming, outgoing = get_solana_transactions(sol_address)

print("Incoming Transfers:")
for tx in incoming:
    print(tx)

print("\nOutgoing Transfers:")
for tx in outgoing:
    print(tx)

