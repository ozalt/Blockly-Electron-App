import csv
import tkinter as tk
import mysql.connector
import websockets
import asyncio
import json
import os

# Tkinter setup
root = tk.Tk()
root.title("Execution Results")
text_area = tk.Text(root)
text_area.pack()

def log(message):
    text_area.insert(tk.END, message + "\n")

def fetch_from_db(column_name):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",      # Update with your credentials
            password="admin",      # Update with your password
            database="test_database"  # Match your DB name
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT {column_name} FROM test_table")
        return cursor.fetchall()
    except Exception as e:
        log(f"Database error: {str(e)}")
        return None

# WebSocket client
async def send_status(status_data):
    async with websockets.connect('ws://localhost:8765') as websocket:
        await websocket.send(json.dumps(status_data))

# CSV processing
async def process_csv():
    statuses = []
    csv_path = os.path.join(os.path.dirname(__file__), 'csv_output', 'blocks.csv')
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                if row['type'] == 'database_fetch':
                    table = json.loads(row['params'])['TAG']
                    data = fetch_from_db(table)
                    log(f"Fetched {len(data)} rows from {table}")
                    statuses.append({'id': row['id'], 'status': 'success'})
                    
                elif row['type'] == 'controls_if':
                    # Implement if-else logic
                    statuses.append({'id': row['id'], 'status': 'success'})
                
                # Add other block types here
                
            except Exception as e:
                log(f"Error in block {row['id']}: {str(e)}")
                statuses.append({'id': row['id'], 'status': 'error'})
    
    # Send statuses via WebSocket
    await send_status(statuses)

# WebSocket server
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

# Main execution
async def main():
    # Start the WebSocket server in the background
    websocket_server_task = asyncio.create_task(start_server())
    
    # Run async CSV processing
    await process_csv()
    
    # Keep the Tkinter window running
    root.after(100, root.quit)  # Close Tkinter window after processing
    root.mainloop()

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
