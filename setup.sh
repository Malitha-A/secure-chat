#!/bin/bash

echo "--- Starting Project Setup ---"

# 1. Check for CentOS and system dependencies
if [ -f /etc/centos-release ]; then
    echo "CentOS detected. Checking for required system tools..."
    
    # List of required command-line utilities.
    TOOLS="python3 python3-pip python3-venv nmap tshark nc"
    MISSING_TOOLS=""
    
    # Check if each tool is available in the system PATH.
    for tool in $TOOLS; do
        # command -v checks if the tool is installed and executable.
        command -v $tool >/dev/null || MISSING_TOOLS="$MISSING_TOOLS $tool"
    done

    if [ -n "$MISSING_TOOLS" ]; then
        echo "Warning: The following tools are missing:$MISSING_TOOLS"
        echo "Please run this command to install them:"
        
        # --- DEPENDENCY CORRECTION FOR CENTOS/RHEL ---
     
        echo "sudo dnf install -y python3 python3-venv nmap wireshark-cli nmap-ncat" 
        
        read -p "Press [Enter] to continue anyway, or [Ctrl+C] to stop and install."
    else
        echo "All system tools are present."
    fi
fi

# 2. Create a Python virtual environment
# Check if the 'venv' directory already exists.
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
# Source the activation script to set up the environment variables.
source venv/bin/activate

# 3. Install Python dependencies
echo "Installing pip dependencies (cryptography)..."
# -q flag means 'quiet', installing packages silently.
pip install -q cryptography
# Check the exit status of the previous command is 0 for success.
if [ $? -ne 0 ]; then
    echo "Error: Failed to install pip dependencies."
    # Deactivate the environment before exiting.
    deactivate
    exit 1
fi

# 4. Generate the encryption key
# Check if the required 'secret.key' file already exists.
if [ ! -f "secret.key" ]; then
    echo "Generating encryption key..."
    # Execute a small Python script to generate a Fernet key and save it.
    python3 -c "from cryptography.fernet import Fernet; key = Fernet.generate_key(); open('secret.key', 'wb').write(key)"
    echo "Generated 'secret.key'."
else
    echo "'secret.key' already exists. Skipping generation."
fi

echo "--- Setup Complete ---"
echo "You can now run './launch.sh' to start the system."

# Exit the virtual environment.
deactivate
