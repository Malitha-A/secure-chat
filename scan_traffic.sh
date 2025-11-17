#!/bin/bash

# --- Configuration ---
HOST="127.0.0.1" # The IP to scan
PORT=9999        # The port our server is running on
INTERFACE="lo"   # localhost
PCAP_FILE="logs/traffic_capture.pcap" # The file to save the captured traffic

echo "--- Scanning and Capturing Traffic ---"
echo ""

# --- 1. Port Scan ---
echo "[1] Running nmap port scan on $HOST..."
# Run nmap on our host and port to confirm it is open
nmap -p $PORT $HOST
echo "----------------------------------------"

# --- 2. Packet Capture ---
echo "[2] Starting packet capture on $INTERFACE..."
echo "Capturing 20 packets to $PCAP_FILE"
echo "NOTE: This will require sudo (administrator) privileges."
echo ""

# Use tshark to sniff the network
# sudo is required to access network interfaces
# -i $INTERFACE: Listen on the 'lo' interface
# -f "port $PORT": Filter to only capture traffic on our chat port
# -c 20: Stop after capturing 20 packets
# -w $PCAP_FILE: Write the captured packets to this file and overwrite if exists
sudo tshark -i $INTERFACE -f "port $PORT" -c 20 -w $PCAP_FILE

# --- 3. Check Results ---
# Check the exit code of the last command ($?)
# '0' means success
if [ $? -eq 0 ]; then
    echo "--- Capture Complete ---"
    echo "File saved to $PCAP_FILE"
    echo "You can analyze this file in Wireshark to see the encrypted data:"
    echo "wireshark $PCAP_FILE"
else
    # Any non-zero code means an error occurred
    echo "--- Capture Failed ---"
    echo "Please ensure tshark is installed."
fi
