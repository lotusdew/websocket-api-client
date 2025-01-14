import asyncio
import websockets
import json

# Define the WebSocket server URL
WEBSOCKET_SERVER_URL = "ws://10.13.100.101:32000/socket/websocket"

async def websocket_client():
    """Connect to a WebSocket server, send messages, and receive responses."""
    try:
        # Connect to the WebSocket server
        async with websockets.connect(WEBSOCKET_SERVER_URL) as websocket:
            print(f"Connected to {WEBSOCKET_SERVER_URL}")

            # Define the first payload to send
            payload1 = {
                "topic": "api:<api_key>",
                "event": "phx_join",
                "payload": {
                    "access_token": "<access_token>"
                },
                "ref": ""
            }

            # Convert the first payload to a JSON string
            message1 = json.dumps(payload1)

            print(f"Sending message: {message1}")
            await websocket.send(message1)

            # Wait for a response from the server
            response1 = await websocket.recv()
            print(f"Received response for payload 1: {response1}")

            # Define the second payload to send
            payload2 = {
                "topic": "api:<api_key>",
                "event": "subscribe",
                "payload": {
                    "list": ["25", "22", "2442", "3812", "35006", "42685", "41289"]
                },
                "ref": ""
            }

            # Convert the second payload to a JSON string
            message2 = json.dumps(payload2)

            print(f"Sending message: {message2}")
            await websocket.send(message2)

            # Enter a loop to continuously receive responses for payload 2
            print("Listening for updates...")
            while True:
                response = await websocket.recv()
                print(f"Received update: {response}")

    except websockets.ConnectionClosed as e:
        print(f"Connection closed: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Run the WebSocket client
    asyncio.run(websocket_client())
