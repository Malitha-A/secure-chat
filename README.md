# Secure Chat System

This project is a secure, multi-client chat system built with Python, encrypted with the `cryptography` library, and automated with Bash scripts.

## File Functionality

### Python Scripts
* **`server.py`**: The main chat server. It listens for connections, manages all clients in separate threads, logs activity, and broadcasts messages.
* **`client.py`**: The chat client application. It connects to the server and uses two threads: one for sending user input and one for receiving messages.
* **`crypto.py`**: A helper module (not runnable). It loads the `secret.key` and provides the `encrypt_message()` and `decrypt_message()` functions.

### Shell Scripts
* **`setup.sh`**: The one-time installer. It creates the `venv`, installs `cryptography`, and generates the `secret.key`.
* **`launch.sh`**: An *automated* starter script that runs the server in the background and prints its PID. (This guide will use the manual method instead).
* **`monitor_logs.sh`**: The live log monitor (IDS). It watches `logs/chat.log` for `WARNING` messages in real-time.
* **`simulate_attack.sh`**: The attack simulator. It sends junk data to the server port to test security.
* **`scan_traffic.sh`**: The network analyst. It runs `nmap` and `tshark` to scan the port and capture traffic.

---

## How to Run (Manual Demo Guide)

This guide walks through the full demonstration step-by-step, using multiple terminals.

### Step 1: Initial Setup (Run Once)

1.  **Install System Tools:**
    ```bash
    sudo dnf install -y python3-pip python3-venv nmap wireshark-cli nmap-ncat
    ```
2.  **Set File Permissions:**
    ```bash
    chmod +x *.sh
    ```
3.  **Run the Setup Script:**
    ```bash
    ./setup.sh
    ```
    *This creates your `venv` and `secret.key`.*

---

### Step 2: Open Terminals & Run the Demo

You will need **5 separate terminals** open in your `secure-chat` project directory.

#### **Terminal 1: Start the Server**
* **Activate the environment:**
    ```bash
    source venv/bin/activate
    ```
* **Run the server:**
    ```bash
    python3 server.py
    ```
    *Leave this running. It will show `[*] Server listening...`*

#### **Terminal 2: Start the Log Monitor (IDS)**
* **Open another terminal.**
* **Run the monitor script:**
    ```bash
    ./monitor_logs.sh
    ```
    *Leave this running. It will show `Watching logs/chat.log...`*

#### **Terminal 3: Start Client 1 (Alice)**
* **Open another terminal.**
* **Activate the environment:**
    ```bash
    source venv/bin/activate
    ```
* **Run the client:**
    ```bash
    python3 client.py
    ```
    *It will connect and show a `>` prompt.*

#### **Terminal 4: Start Client 2 (Bob)**
* **Open another terminal.**
* **Activate the environment:**
    ```bash
    source venv/bin/activate
    ```
* **Run the client:**
    ```bash
    python3 client.py
    ```
    *It will connect and show a `>` prompt. You can now chat between Terminal 3 and 4.*

#### **Terminal 5: Run Simulations**
* **Open a final terminal.**
* **Run the Attack Simulation:**
    ```bash
    ./simulate_attack.sh
    ```
    *Watch Terminal 2. Red `WARNING` messages will appear.*

* **Run the Network Scan:**
    ```bash
    sudo ./scan_traffic.sh
    ```
    *This will run `nmap` and `tshark`, saving the results to `logs/traffic_capture.pcap`.*

---

### Step 3: Shutdown
1.  Type `exit` in **Terminal 3** and **Terminal 4**.
2.  Press `Ctrl+C` in **Terminal 1** (Server) and **Terminal 2** (Monitor).
