## Cryptocurrency Transfer and Exchange API Documentation

This API documentation outlines endpoints for initiating cryptocurrency transfers and performing currency exchanges using Flask.

### Base URL

The base URL for this API is `https://web3-wallet-e40e6d4f61b9.herokuapp.com`.

### Endpoints

#### Get Accounts

- **Endpoint**: `/get_accounts/<int:user_number>`
- **Method**: `GET`
- **Description**: Retrieve cryptocurrency account details associated with a specific user number.
- **Parameters**:
  - `user_number` (integer): User identifier to retrieve account details.
- **Response**:
  ```json
  {
    "btc_address": "string",
    "eth_address": "string",
    "sol_address": "string",
    "trx_address": "string"
  }
  ```




## Cryptocurrency Balance API

This API provides endpoints to retrieve balances for different cryptocurrencies based on their respective blockchain networks.

### Base URL

The base URL for this API is `http://yourdomain.com`.

### Endpoints

#### Get Bitcoin (BTC) Address Balance

- **URL**: `/balance/btc`
- **Method**: `GET`
- **Description**: Get Bitcoin (BTC) balance for a specific address.
- **Query Parameters**:
  - `address` (string, required): Bitcoin address for which balance is required.
- **Success Response**:
  - **Code**: `200 OK`
  - **Content**:
    ```json
    {
      "btc_balance": "balance"
    }
    ```
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Content**: 
    ```json
    {
      "error": "Address parameter is required"
    }
    ```

#### Get Ethereum (ETH) Address Balance

- **URL**: `/balance/eth`
- **Method**: `GET`
- **Description**: Get Ethereum (ETH) balance for a specific address.
- **Query Parameters**:
  - `address` (string, required): Ethereum address for which balance is required.
- **Success Response**:
  - **Code**: `200 OK`
  - **Content**:
    ```json
    {
      "eth_balance": "balance"
    }
    ```
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Content**: 
    ```json
    {
      "error": "Address parameter is required"
    }
    ```

#### Get Solana (SOL) Address Balance

- **URL**: `/balance/sol`
- **Method**: `GET`
- **Description**: Get Solana (SOL) balance for a specific address.
- **Query Parameters**:
  - `address` (string, required): Solana address for which balance is required.
- **Success Response**:
  - **Code**: `200 OK`
  - **Content**:
    ```json
    {
      "sol_balance": "balance"
    }
    ```
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Content**: 
    ```json
    {
      "error": "Address parameter is required"
    }
    ```

#### Get Tron (TRX) Address Balance

- **URL**: `/balance/trx`
- **Method**: `GET`
- **Description**: Get Tron (TRX) balance for a specific address.
- **Query Parameters**:
  - `address` (string, required): Tron address for which balance is required.
- **Success Response**:
  - **Code**: `200 OK`
  - **Content**:
    ```json
    {
      "trx_balance": "balance"
    }
    ```
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Content**: 
    ```json
    {
      "error": "Address parameter is required"
    }
    ```

#### Get USDT (Tether) Address Balance

- **URL**: `/balance/usdt`
- **Method**: `GET`
- **Description**: Get USDT (Tether) balance for a specific address.
- **Query Parameters**:
  - `address` (string, required): USDT address for which balance is required.
- **Success Response**:
  - **Code**: `200 OK`
  - **Content**:
    ```json
    {
      "usdt_balance": "balance"
    }
    ```
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Content**: 
    ```json
    {
      "error": "Address parameter is required"
    }
    ```

---
#### Bitcoin (BTC) Transfer

- **Endpoint**: `/btc-transfer`
- **Method**: `POST`
- **Description**: Initiate a Bitcoin (BTC) transfer.
- **Request Body**:
  ```json
  {
    "user_number": "string",
    "amount": "number",
    "recipient": "string"
  }
  ```
- **Response**:
  ```json
  {
    "signed_tx": "string"
  }
  ```

#### Ethereum (ETH) Transfer

- **Endpoint**: `/eth-transfer`
- **Method**: `POST`
- **Description**: Initiate an Ethereum (ETH) transfer.
- **Request Body**:
  ```json
  {
    "user_number": "string",
    "amount": "number",
    "recipient": "string"
  }
  ```
- **Response**:
  ```json
  {
    "txn_hash": "string"
  }
  ```

#### Tron (TRX) Transfer

- **Endpoint**: `/tron-transfer`
- **Method**: `POST`
- **Description**: Initiate a Tron (TRX) transfer.
- **Request Body**:
  ```json
  {
    "user_number": "string",
    "amount": "number",
    "recipient": "string"
  }
  ```
- **Response**:
  ```json
  {
    "tx_id": "string",
    "status": "string",
    "result": "object"
  }
  ```

#### Solana (SOL) Transfer

- **Endpoint**: `/sol-transfer`
- **Method**: `POST`
- **Description**: Initiate a Solana (SOL) transfer.
- **Request Body**:
  ```json
  {
    "user_number": "string",
    "amount": "number",
    "recipient": "string"
  }
  ```
- **Response**:
  ```json
  {
    "tx_result": "object"
  }
  ```

#### USDT (Tether) Transfer

- **Endpoint**: `/usdt-transfer`
- **Method**: `POST`
- **Description**: Initiate a USDT (Tether) transfer.
- **Request Body**:
  ```json
  {
    "user_number": "string",
    "amount": "number",
    "recipient": "string"
  }
  ```
- **Response**:
  ```json
  {
    "tx_id": "string",
    "status": "string",
    "result": "object"
  }
  ```

#### Exchange Operations

##### TRX to USDT

- **Endpoint**: `/trx-to-usdt`
- **Method**: `POST`
- **Description**: Perform TRX (Tron) to USDT (Tether) conversion.
- **Request Body**:
  ```json
  {
    "user_number": "string",
    "amount_trx": "number"
  }
  ```
- **Response**:
  ```json
  {
    "tx_id": "string",
    "result_status": "string",
    "result": "object"
  }
  ```

##### SOL to USDT

- **Endpoint**: `/sol-to-usdt`
- **Method**: `POST`
- **Description**: Perform SOL (Solana) to USDT (Tether) conversion.
- **Request Body**:
  ```json
  {
    "user_number": "string",
    "amount": "number"
  }
  ```
- **Response**:
  ```json
  {
    "track": "string",
    "response_text": "string"
  }
  ```

##### BTC to USDT

- **Endpoint**: `/btc-to-usdt`
- **Method**: `POST`
- **Description**: Perform BTC (Bitcoin) to USDT (Tether) conversion.
- **Request Body**:
  ```json
  {
    "user_number": "string",
    "amount": "number"
  }
  ```
- **Response**:
  ```json
  {
    "track": "string",
    "response_text": "string"
  }
  ```

##### ETH to USDT

- **Endpoint**: `/eth-to-usdt`
- **Method**: `POST`
- **Description**: Perform ETH (Ethereum) to USDT (Tether) conversion.
- **Request Body**:


  ```json
  {
    "user_number": "string",
    "amount": "number"
  }
  ```
- **Response**:
  ```json
  {
    "track": "string",
    "response_text": "string"
  }
  ```

##### USDT to NGN (Nigerian Naira)

- **Endpoint**: `/usdt-to-ngn`
- **Method**: `POST`
- **Description**: Perform USDT (Tether) to NGN (Nigerian Naira) exchange.
- **Request Body**:
  ```json
  {
    "user_number": "string",
    "amount_udst": "number",
    "account_number": "string",
    "account_bank_code": "string",
    "rate": "number"
  }
  ```
- **Response**:
  ```json
  {
    "message": "string",
    "result": "object"
  }
  ```

#### Exchange Estimate and Swap Status

##### Get Exchange Estimate

- **Endpoint**: `/get-exchange-estimate`
- **Method**: `POST`
- **Description**: Get estimated amount for a cryptocurrency exchange.
- **Request Body**:
  ```json
  {
    "from_coin": "string",
    "to_coin": "string",
    "to_coin_network": "string",
    "amount": "number"
  }
  ```
- **Response**:
  ```json
  {
    "estimated_amount": "number"
  }
  ```

##### Get Swap Status

- **Endpoint**: `/get-swap-status`
- **Method**: `POST`
- **Description**: Get status of a swap operation by track ID.
- **Request Body**:
  ```json
  {
    "track_id": "string"
  }
  ```
- **Response**:
  ```json
  {
    "status": "string",
    "response_text": "string"
  }
  ```

#### Miscellaneous Endpoints

- **Endpoint**: `/price_usd`
- **Method**: `GET`
- **Description**: Get current cryptocurrency prices in USD.
- **Response**: Current USD prices for cryptocurrencies.

- **Endpoint**: `/price-naira`
- **Method**: `GET`
- **Description**: Get current cryptocurrency prices in Nigerian Naira (NGN).
- **Response**: Current NGN prices for cryptocurrencies.

### Running the Application

To run this Flask application locally, execute the following command in your terminal:

```bash
python app.py
```

This will start the Flask development server. By default, the application will run on `http://127.0.0.1:5000/`.

You can access the API endpoints using tools like Postman or by making HTTP requests from your frontend or backend applications.


--- 

This Markdown documentation provides comprehensive details about the endpoints, request formats, response structures, and usage instructions for the cryptocurrency transfer and exchange API implemented with Flask.