# WebSocket API Documentation

## Overview

This WebSocket API allows clients to connect and interact with the server by exchanging messages. It supports subscribing to updates and receiving real-time data.

---

## Access Token Endpoint

- **URL**: `https://api.airalgo.com/api/token`

## WebSocket Endpoint

- **URL**: `wss://api.airalgo.com/socket/websocket`

---

## Authentication

- **Access Token**: Required in the `phx_join` payload to authenticate the client.
- **API Key**: Included in the topic, must be valid.

---

## Message Format

All messages exchanged between the client and server follow a JSON structure.

### General Structure

```json
{
  "topic": "string",
  "event": "string",
  "payload": "object",
  "ref": "string"
}
```

- **topic**: Identifies the specific API or token (e.g., `api:<api_key>`).
- **event**: Defines the action (e.g., `phx_join`, `subscribe`).
- **payload**: Contains the necessary data for the action.
- **ref**: Used to correlate requests and responses.

---

## Supported Events

### 1. Join Event

- **Description**: Authenticate the client and join a topic.
- **Request**:
  ```json
  {
    "topic": "api:<api_key>",
    "event": "phx_join",
    "payload": {
      "access_token": "<access_token>"
    },
    "ref": ""
  }
  ```
- **Response**:
  ```json
  {
    "event": "phx_reply",
    "payload": {
      "response": {},
      "status": "ok"
    },
    "ref": "",
    "topic": "api:<api_key>"
  }
  ```

---

### 2. Subscribe Event

- **Description**: Subscribe to updates for specific tokens.
- **Request**:
  ```json
  {
    "topic": "api:<api_key>",
    "event": "subscribe",
    "payload": {
      "list": ["<token_number_1>", "<token_number_2>", "<token_number_n>"]
    },
    "ref": ""
  }
  ```
- **Response**:
  ```json
  {
    "event": "ltp",
    "payload": {
      "<token_number_1>": {
        "ltp": "<latest_price>",
        "ltq": "<latest_quantity>",
        "ltt": "<last_traded_time>"
      },
      "<token_number_2>": {
        "ltp": "<latest_price>",
        "ltq": "<latest_quantity>",
        "ltt": "<last_traded_time>"
      },
      "<token_number_2>": {
        "ltp": "<latest_price>",
        "ltq": "<latest_quantity>",
        "ltt": "<last_traded_time>"
      }
    },
    "ref": null,
    "topic": "api:<api_key>"
  }
  ```

---

### 3. Unsubscribe Event

- **Description**: Unsubscribe to updates for specific tokens.
- **Request**:
  ```json
  {
    "topic": "api:<api_key>",
    "event": "unsubscribe",
    "payload": {
      "list": ["<token_number_1>", "<token_number_2>", "<token_number_n>"]
    },
    "ref": ""
  }
  ```
- **Response**:
  ```json
  {
    "event": "unsubscribe",
    "payload": { "tokens": ["22", "2442"] },
    "ref": null,
    "topic": "api:<api_key>"
  }
  ```

---

## Real-Time Updates

Once subscribed, the server sends periodic updates for the subscribed tokens.

### Update Example

```json
{
  "event": "ltp",
  "payload": {
    "22": {
      "ltp": 220800,
      "ltq": 1,
      "ltt": "2025-01-09T12:53:00Z"
    },
    "2442": {
      "ltp": 24295,
      "ltq": 499,
      "ltt": "2025-01-09T12:54:39Z"
    }
  },
  "ref": null,
  "topic": "api:<api_key>"
}
```

---

### 4. Order placement Event

- **Description**: Order palcement payload for placing orders.
- **Request**

  ```json
  {
    "topic": "api:<api_key>",
    "event": "order",
    "payload": {
      "token_number": "2885",
      "market_limit_sl": "market",
      "price": 0,
      "order_type": "B",
      "trigger_price": 0,
      "validity": "Day",
      "quantity": 20,
      "ltp": 0
    },
    "ref": ""
  }
  ```

- **Description of Request Parameters**

  | Parameter | Data Type | Description | Example |
  |--------|--------|--------|--------|
  | token_number | String | Token Number from csv file | "2885" |
  | market_limit_sl | String | Market -> "market", Limit -> "limit", Stop Loss -> "sl", Stop Loss Market ->"slm" | "limit" |
  | price | Integer | For limit and Stop Loss order price should be non-zero, and in Paisa | 234535 |
  | order_type | String | Order type "B" for Buy and "S" for Sell | "B" |
  | trigger_price | Integer | For Stop Loss order trigger_price should be non-zero and in Paisa | 234530 |
  | validity | String | For now only validity is "Day" | "Day" |
  | quantity | Integer | Quantity of the Security that you want to trade | 20 |
  | ltp | Integer | For limit and stop loss order ltp should be non-zero and in Paisa | 234600 |

- **Response 1: Order Entry Confirmation**

  ```json
  {
    "event": "order_response",
    "payload": {
      "book_type": "1",
      "buy_sell": "1",
      "client_id": "1234567890",
      "disclosed_volume": 20,
      "entry_modify_cancel": "0",
      "error": null,
      "executed_price": 0,
      "expiry_date": "0",
      "good_till_date": "0000000000",
      "instrument": "EQUITY",
      "last_modified": 1421348186,
      "market_limit_sl": "market",
      "message": "Order Entry Confirm",
      "net_charges": 0.025,
      "option_type": "EQ",
      "order_flag": null,
      "order_number": 1300000000111170.0,
      "pnl": 0,
      "price": 0.0,
      "required_margin": 0,
      "status": "Pending",
      "strike_price": "0",
      "symbol": "RELIANCE",
      "timestamp": "18:56:26,14-1-2025",
      "token_number": "2885",
      "transaction_id": 11,
      "trigger_price": 0.0,
      "user_id": "47241",
      "volume": 20
    },
    "ref": null,
    "topic": "api:<api_key>"
  }
  ```

- **Response 2 : Order Execution Success**

  ```json
  {
    "event": "order_response",
    "payload": {
      "book_type": "1",
      "buy_sell": "1",
      "client_id": "1234567890",
      "disclosed_volume": 20,
      "entry_modify_cancel": "0",
      "error": null,
      "executed_price": 120275.0,
      "expiry_date": "0",
      "good_till_date": "0000000000",
      "instrument": "EQUITY",
      "last_modified": 1421348186,
      "market_limit_sl": "market",
      "message": "Your Order has been executed successfully",
      "net_charges": 0.025,
      "option_type": "EQ",
      "order_flag": null,
      "order_number": 1300000000111170.0,
      "pnl": 0,
      "price": 0.0,
      "required_margin": 0,
      "status": "Executed",
      "strike_price": "0",
      "symbol": "RELIANCE",
      "timestamp": "18:56:26,14-1-2025",
      "token_number": "2885",
      "transaction_id": 11,
      "trigger_price": 0.0,
      "user_id": "47241",
      "volume": 20
    },
    "ref": null,
    "topic": "api:<api_key>"
  }
  ```

---

### 5. Few more Order placement event examples

- **Description**: Order palcement payload for placing orders.
- **Request**

  ```json
  {
    "topic": "api:<api_key>",
    "event": "order",
    "payload": {
      "token_number": "35013",
      "market_limit_sl": "market",
      "price": 0,
      "order_type": "B",
      "trigger_price": 0,
      "validity": "Day",
      "quantity": 25,
      "ltp": 0
    },
    "ref": ""
  }
  ```

- **Response : Order Rejected**

  ```json
  {
    "event": "order_response",
    "payload": {
      "book_type": "1",
      "buy_sell": "1",
      "client_id": "1234567890",
      "disclosed_volume": 25,
      "entry_modify_cancel": "0",
      "error": null,
      "executed_price": 0,
      "expiry_date": "1425133800",
      "good_till_date": "0000000000",
      "instrument": "FUTIDX",
      "last_modified": "0000000000",
      "market_limit_sl": "market",
      "message": "Order has been Rejected",
      "net_charges": 6602427.364333333,
      "option_type": "XX",
      "order_flag": null,
      "order_number": 1000000000085530.0,
      "pnl": 0,
      "price": 0.0,
      "required_margin": 6602427.333333333,
      "status": "Rejected",
      "strike_price": "0",
      "symbol": "NIFTY",
      "timestamp": "18:58:5,14-1-2025",
      "token_number": "35013",
      "transaction_id": 13,
      "trigger_price": 0.0,
      "user_id": "46950",
      "volume": 25
    },
    "ref": null,
    "topic": "api:<api_key>"
  }
  ```

## Error Handling

The server may return error responses for invalid API usage or authentication issues. Below are the known errors:

### 1. Invalid API Key

- **Condition**: Sent when the `api:<api_key>` is invalid.
- **Error Response**:
  ```json
  {
    "event": "phx_reply",
    "payload": {
      "response": {
        "reason": "Invalid API Key"
      },
      "status": "error"
    },
    "ref": "",
    "topic": "api:<api_key>"
  }
  ```

### 2. Invalid or Expired Access Token

- **Condition**: Sent when the `access_token` is invalid or expired.
- **Error Response**:
  ```json
  {
    "event": "phx_reply",
    "payload": {
      "response": {
        "reason": "Invalid Access Token. Try generating fresh Access Token"
      },
      "status": "error"
    },
    "ref": "",
    "topic": "api:<api_key>"
  }
  ```

### 3. Unmatched Topic

- **Condition**: Sent when any event other than `phx_join` is sent before authenticating via `phx_join`.
- **Error Response**:
  ```json
  {
    "event": "phx_reply",
    "payload": {
      "response": {
        "reason": "unmatched topic"
      },
      "status": "error"
    },
    "ref": "",
    "topic": "api:<api_key>"
  }
  ```

---

## Best Practices

- **Authenticate First**: Always send the `phx_join` event with a valid `access_token` before other events.
- **Handle Errors Gracefully**: Parse error responses and take corrective actions (e.g., refresh the access token if expired).
- **Reconnect on Failures**: Reconnect to the WebSocket server if the connection drops.

---

## Setting Up a Virtual Environment and Installing Requirements Using pip

- Follow these steps to create a virtual environment, install required dependencies, and write the commands in a single file.

### Step 1: Create a virtual environment

```bash
python3 -m venv venv
```

### Step 2: Activate the virtual environment

- On macOS/Linux

```bash
source venv/bin/activate
```

- On Windows

```bash
.\venv\Scripts\activate
```

### Step 3: Install the requirements using pip

```bash
pip install -r requirements.txt
```

### Step 4: Deactivate the virtual environment when done

```bash
deactivate
```

## Create an .env file similar to the given example with your API Key

```bash
WEBSOCKET_SERVER_URL=wss://api.airalgo.com/socket/websocket
TOKEN_SERVER_URL=https://api.airalgo.com
API_KEY=<Paste your API Key here>
```
