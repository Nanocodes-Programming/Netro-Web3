### **API Documentation for Cryptocurrency Operations**
#### Base URL

The base URL for this API is `https://web3-wallet-e40e6d4f61b9.herokuapp.com`.

#### **1. Get User Accounts**
- **Endpoint**: `/get_accounts/<int:user_number>`
- **Method**: `GET`
- **Description**: Retrieves user-specific cryptocurrency accounts.
- **Parameters**:
  - `user_number`: A unique identifier for the user.
- **Response**:
  - **Success**: Returns JSON containing cryptocurrency addresses for the user.
  - **Error**: Returns an error message if the user is not found or on server error.
- **Example Request**:
  ```http
  GET /get_accounts/12345
  ```
- **Example Response**:
  ```json
  {
    "eth_address": "0x....",
    "btc_address": "1P....",
    "bsc_address": "0x....",
    "tron_address": "TQ....",
    "ltc_address": "5P...."
  }

#### **2. Get Currency Balance**
- **Endpoint**: `/balance/<string:currency>`
- **Method**: `GET`
- **Description**: Fetches the balance of the specified cryptocurrency.
- **Parameters**:
  - `currency`: Supported values are `btc`, `eth`, `ltc`, `trx`, `usdt`.
  - `address`: Address of the cryptocurrency wallet.
- **Response**:
  - **Success**: Returns JSON with the balance of the specified currency.
  - **Error**: Returns an error message if the currency is unsupported or address is missing.
- **Example Request**:
  ```http
  GET /balance/eth?address=0x...
  ```
- **Example Response**:
  ```json
  {
    "eth_balance": 2.5
  }
  
#### **3. Currency Transfer**
- **Endpoint**: `/<string:currency>-transfer`
- **Method**: `POST`
- **Description**: Transfers a specified amount of cryptocurrency to a recipient.
- **Request Body**:
  - `user_number`: User's unique identifier.
  - `amount`: Amount of currency to transfer.
  - `recipient`: Recipient's wallet address.
- **Response**:
  - **Success**: Returns transaction details upon successful transfer.
  - **Error**: Returns an error message if the currency is unsupported or transaction fails.
- **Example Request**:
  ```http
  POST /btc-transfer
  {
    "user_number": 12345,
    "amount": 0.1,
    "recipient": "1P..."
  }
  ```
- **Example Response**:
  ```json
  {
    "transaction_id": "abc123...",
    "status": "Success",
    "message": "Transaction successful"
  }

#### **4. Coin to Coin Swap**
- **Endpoint**: `/<string:from_coin>-to-<string:to_coin>`
- **Method**: `POST`
- **Description**: Swaps one type of cryptocurrency for another.
- **Request Body**:
  - `user_number`: User's unique identifier.
  - `amount`: Amount of the `from_coin` to swap.
- **Response**:
  - **Success**: Returns tracking information and swap details.
  - **Error**: Returns an error message if the swap type is unsupported.
- **Example Request**:
  ```http
  POST /btc-to-usdt
  {
    "user_number": 12345,
    "amount": 0.2
  }
  ```
- **Example Response**:
  ```json
  {
    "track": "xyz789...",
    "response_text": "Swap initiated"
  }

#### **5. Get Price**
- **Endpoint**: `/price/<string:currency>`
- **Method**: `GET`
- **Description**: Retrieves the latest price of the specified currency.
- **Parameters**:
  - `currency`: Supported values are `usd` (U.S. Dollar) and `naira` (Nigerian Naira).
- **Response**:
  - **Success**: Returns JSON with price details of cryptocurrencies.
  - **Error**: Returns an error message if the currency type is unsupported.
- **Example Request**:
  ```http
  GET /price/usd
  ```
- **Example Response**:
  ```json
  {
    "BTC": {
      "name": "Bitcoin",
      "symbol": "BTC",
      "price": 47832.32,
      "change": -0.45
    },
    "ETH": {
      "name": "Ethereum",
      "symbol": "ETH",
      "price": 3200.87,
      "change": 0.75
    }
  }

---
Certainly! Here's the detailed API documentation for the endpoint to retrieve multiple cryptocurrency balances in a single request.

---

#### **6. Get All Balances**
- **Endpoint**: `/balance/all`
- **Method**: `POST`
- **Description**: Retrieves balances for multiple cryptocurrencies in a single request.
- **Request Body**: JSON object with currency names as keys and wallet addresses as values.
- **Supported Currencies**: `btc`, `eth`, `ltc`, `trx`, `usdt`
- **Request Format**:
  - Keys: Names of the cryptocurrencies.
  - Values: Corresponding wallet addresses for each cryptocurrency.
- **Response**:
  - **Success**: Returns a JSON object containing balances for the specified currencies and any errors that occurred during the retrieval.
  - **Error**: Returns an error message if a currency is unsupported or if a wallet address is missing.
- **Example Request**:
  ```http
  POST /balance/all
  Content-Type: application/json

  {
    "btc": "1P...",
    "eth": "0x...",
    "trx": "TQ...",
    "ltc": "5P..."
  }
  ```
- **Example Response**:
  ```json
  {
    "balances": {
      "btc": 0.5,
      "eth": 2.5,
      "ltc": 100.0,
      "trx": 1500
    },
    "errors": {
      "usdt": "Unsupported currency or missing balance function"
    }
  }
  ```

#### **7. Get Swap Status**
- **Endpoint**: `/get-swap-status`
- **Method**: `POST`
- **Description**: Fetches the status of a previously initiated swap transaction.
- **Request Body**: JSON object containing the tracking ID of the swap transaction.
- **Request Format**:
  - `track_id`: The tracking ID of the swap transaction.
- **Response**:
  - **Success**: Returns the status and response text of the swap transaction.
  - **Error**: Returns an error message if the swap status could not be retrieved.
- **Example Request**:
  ```http
  POST /get-swap-status
  Content-Type: application/json

  {
    "track_id": "xyz789..."
  }
  ```
- **Example Response**:
  ```json
  {
    "status": "Completed",
    "response_text": "Swap successful and funds transferred"
  }
  ```

#### **8. Convert USDT to NGN**
- **Endpoint**: `/usdt-to-ngn`
- **Method**: `POST`
- **Description**: Converts a specified amount of USDT to Nigerian Naira (NGN) and transfers it to a provided bank account.
- **Request Body**:
  - `user_number`: User's unique identifier.
  - `amount_udst`: Amount of USDT to be converted.
  - `account_number`: The bank account number where NGN will be transferred.
  - `account_bank_code`: The bank code for the destination bank account.
  - `rate`: The conversion rate from USDT to NGN.
- **Response**:
  - **Success**: Returns a message indicating the transfer initiation and details of the result.
  - **Error**: Returns an error message if the conversion or transfer fails.
- **Example Request**:
  ```http
  POST /usdt-to-ngn
  Content-Type: application/json

  {
    "user_number": 12345,
    "amount_udst": 500.0,
    "account_number": "0123456789",
    "account_bank_code": "050",
    "rate": 380.5
  }
  ```
- **Example Response**:
  ```json
  {
    "message": "Transfer initiated successfully.",
    "result": {
      "transaction_id": "abc123...",
      "status": "Pending",
      "amount_ngn": 190250
    }
  }
  ```
#### **9. Cryptocurrency Transactions**
- **Endpoint**: `/transactions/<string:currency>`
- **Method**: `GET`
- **Description**: Retrieves transaction details for a specific cryptocurrency.
- **URL Parameters**:
  - `currency` (string): Cryptocurrency symbol (e.g., `btc`, `eth`, `tron`, `usdt`, `litecoin`).
- **Query Parameters**:
  - `address` (string, required): Cryptocurrency address for which transactions are to be retrieved.
- **Response**:
  ```json
  {
    "btc_transactions": [
      {
        "type": "Incoming/Outgoing",
        "amount": "number",
        "address": "string"
      },
      ...
    ],
    "eth_transactions": [
      {
        "type": "incoming/outgoing",
        "hash": "string",
        "amount": "number",
        "from/to": "string"
      },
      ...
    ],
    "tron_transactions": [
      {
        "type": "incoming/outgoing",
        "amount": "number",
        "from/to": "string"
      },
      ...
    ],
    "usdt_transactions": [
      {
        "type": "incoming/outgoing",
        "amount": "number",
        "from/to": "string"
      },
      ...
    ],
    "litecoin_transactions": [
      {
        "direction": "incoming/outgoing",
        "amount": "number",
        "address_to": "string",
        "address_from": "string"
      },
      ...
    ]
  }


#### **Endpoint**: `/transactions`
- **Method**: `POST`
- **Description**: Retrieves transaction histories for specified cryptocurrencies.
- **Request Body**: JSON object with cryptocurrency names as keys and their corresponding wallet addresses as values.
- **Supported Currencies**: `btc` (Bitcoin), `eth` (Ethereum), `tron` (TRON), `usdt` (Tether), and `litecoin` (litecoin).

#### **Request Format**:
- Keys: Cryptocurrency identifiers (e.g., 'btc', 'eth').
- Values: Corresponding wallet addresses for each cryptocurrency.

#### **Response**:
- **Success**: Returns a JSON object containing transaction histories for each requested cryptocurrency and any errors encountered.
- **Error**: Returns an error message if any currency is unsupported or if there's an issue with fetching transactions.

#### **Example Request**:
```http
POST /transactions
Content-Type: application/json

{
  "btc": "1P...",
  "eth": "0x...",
  "tron": "TQ...",
  "litecoin": "5P...",
  "usdt": "TR..."
}
```

#### **Example Response**:
```
{
  "transactions": {
    "btc": [
      {
        "type": "Incoming",
        "amount": 0.1
      },
      {
        "type": "Outgoing",
        "amount": 0.05,
        "address": "1P..."
      }
    ],
    "eth": [
      {
        "type": "incoming",
        "hash": "0x...",
        "amount": 2.5,
        "from": "0x..."
      }
    ],
    "tron": [
      {
        "type": "outgoing",
        "amount": 150,
        "to": "TQ..."
      }
    ],
    "litecoin": [
      {
        "direction": "incoming",
        "amount": 50,
        "address_to": "5P...",
        "address_from": "3N..."
      },
      {
        "direction": "outgoing",
        "amount": 20,
        "address_to": "4N...",
        "address_from": "5P..."
      }
    ],
    "usdt": [
      {
        "type": "incoming",
        "amount": 1000,
        "from": "TY..."
      },
      {
        "type": "outgoing",
        "amount": 500,
        "to": "TR..."
      }
    ]
  },
  "errors": {}
}

{
  "transactions": {
    "btc": [
      {
        "type": "Incoming",
        "amount": 0.1
      },
      {
        "type": "Outgoing",
        "amount": 0.05,
        "address": "1P..."
      }
    ],
    "eth": [
      {
        "type": "incoming",
        "hash": "0x...",
        "amount": 2.5,
        "from": "0x..."
      }
    ],
    "tron": [
      {
        "type": "outgoing",
        "amount": 150,
        "to": "TQ..."
      }
    ]
  },
  "errors": {
    "usdt": "Unsupported currency or missing transaction function"
  }
}
```