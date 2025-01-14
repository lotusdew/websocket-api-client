import asyncio
import aiohttp
import websockets
import json
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get environment variables
WEBSOCKET_SERVER_URL = os.getenv("WEBSOCKET_SERVER_URL")
API_KEY = os.getenv("API_KEY")
TOKEN_SERVER_URL = os.getenv("TOKEN_SERVER_URL")
TOKEN_URL = f"{TOKEN_SERVER_URL}/api/token/?api_key={API_KEY}"  # Token endpoint

async def fetch_access_token():
    """Fetch the access token using the provided API key."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(TOKEN_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("status") == "ok":
                        return data.get("access_token")
                    else:
                        raise Exception("Failed to retrieve access token: Invalid response status")
                else:
                    raise Exception(f"Failed to retrieve access token: HTTP {response.status}")
        except Exception as e:
            print(f"Error fetching access token: {e}")
            raise

async def websocket_client():
    """Connect to a WebSocket server, send messages, and receive responses."""
    try:
        # Fetch the access token
        access_token = await fetch_access_token()
        print(f"Access token fetched: {access_token}")

        # Connect to the WebSocket server
        async with websockets.connect(WEBSOCKET_SERVER_URL) as websocket:
            print(f"Connected to {WEBSOCKET_SERVER_URL}")

            # Define the first payload to send
            payload1 = {
                "topic": f"api:{API_KEY}",
                "event": "phx_join",
                "payload": {
                    "access_token": access_token
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
                "topic": f"api:{API_KEY}",
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
