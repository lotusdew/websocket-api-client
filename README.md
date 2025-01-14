# WebSocket API Documentation

## Overview
This WebSocket API allows clients to connect and interact with the server by exchanging messages. It supports subscribing to updates and receiving real-time data.

---

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
      "list": ["<token_number_1>", "<token_number_2>", ...]
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
        "ltp": <latest_price>,
        "ltq": <latest_quantity>,
        "ltt": <last_traded_time>,
      },
      ...
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
      "list": ["<token_number_1>", "<token_number_2>", ...]
    },
    "ref": ""
  }
  ```
- **Response**:
  ```json
  {
    "event": "unsubscribe",
    "payload":{"tokens" : ["25","22","2442","3812","35006","42685","41289"]},
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
    },
    ...
  },
  "ref": null,
  "topic": "api:<api_key>"
}
```

---

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
