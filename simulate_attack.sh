#!/bin/bash

# --- Configuration ---
HOST="127.0.0.1"   # Target IP address for the server
PORT=9999          # Target port number for the server

echo "--- Simulating Attack ---"
echo "Sending 5 malformed packets to $HOST:$PORT..."

# 1. Check for netcat utility
if ! command -v nc > /dev/null; then
    echo "Error: The 'nc' (netcat) utility is required but not installed."
 
    exit 1
fi

# 2. Loop to send the junk data packets
# The sequence {1..5} generates numbers 1, 2, 3, 4, 5.
for i in {1..5}
do
    # Generate 50 bytes of random binary data from /dev/urandom.
    # This data is not a valid encrypted Fernet token and will cause a decryption error.
    head -c 50 /dev/urandom | nc -w 1 $HOST $PORT
    
    # Check the exit status of the previous command (nc)
    if [ $? -eq 0 ]; then
        echo "Packet $i sent successfully."
    else
        echo "Warning: Packet $i failed to send. Server may not be running or port is closed."
    fi
    
    # Pause for a brief period between packets to simulate real-world traffic delay.
    sleep 0.5
done

echo "--- Attack Simulation Complete ---"
echo "Check the 'monitor_logs.sh' terminal for 'WARNING' messages."
