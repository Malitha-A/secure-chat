#!/bin/bash

echo "--- Launching Secure Chat System ---"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 1. Start the Server in the background
echo "[1] Starting Server in the background..."
python3 server.py & # runs the server in the background 
SERVER_PID=$! #saves the PID of the last command that ran in the backgorund

sleep 1 # Give the server a moment to start

echo ""
echo "--- Server is Online ---"
echo "Server PID: $SERVER_PID"
echo "Run 'kill $SERVER_PID' or 'pkill -f server.py' to stop the server."
echo "" # Added space
echo "--- ACTION REQUIRED ---"
echo "Please open TWO new terminal tabs and run the following in each:"
echo "source venv/bin/activate"
echo "python3 client.py"
echo ""
