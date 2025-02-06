import asyncio
import websockets
import json

async def websocket_handler(websocket, path):
    print("WebSocket connected!")
    try:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")
            response = {"status": "ok", "message": "Message received"}
            await websocket.send(json.dumps(response))
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket disconnected")

# Start WebSocket Server
async def start_server():
    server = await websockets.serve(websocket_handler, "localhost", 8765)
    print("WebSocket Server running on ws://localhost:8765")
    await server.wait_closed()

# Run Server
if __name__ == "__main__":
    asyncio.run(start_server())
