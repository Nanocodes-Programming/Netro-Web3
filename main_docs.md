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
    "sol_address": "5P...."
  }

#### **2. Get Currency Balance**
- **Endpoint**: `/balance/<string:currency>`
- **Method**: `GET`
- **Description**: Fetches the balance of the specified cryptocurrency.
- **Parameters**:
  - `currency`: Supported values are `btc`, `eth`, `sol`, `trx`, `usdt`.
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
- **Supported Currencies**: `btc`, `eth`, `sol`, `trx`, `usdt`
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
    "sol": "5P..."
  }
  ```
- **Example Response**:
  ```json
  {
    "balances": {
      "btc": 0.5,
      "eth": 2.5,
      "sol": 100.0,
      "trx": 1500
    },
    "errors": {
      "usdt": "Unsupported currency or missing balance function"
    }
  }
  ```