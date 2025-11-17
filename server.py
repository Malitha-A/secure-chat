import socket
import threading
import logging
from cryptography.fernet import InvalidToken, Fernet
import crypto # Our custom module for encryption

# --- Configuration ---
HOST = '127.0.0.1'  # Localhost
PORT = 9999         # The port the server will listen on.
LOG_FILE = 'logs/chat.log' # Log for all activities

# --- Logging Setup ---
# Configure the logging system to write to LOG_FILE.
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO, # Log all messages at the INFO level or higher.
    # Define the format for each log entry.
    format='%(asctime)s [%(levelname)s] (%(threadName)s) %(message)s'
)

# --- Global Client List ---
clients = [] # Store all active client sockets for broadcasting.

# Broadcasts a message to all clients except the original sender.
def broadcast(message_bytes, sender_socket):
    # Iterate over a copy of the list in case it changes during iteration.
    for client in clients:
        client_socket = client[0] # Get the socket object from the tuple
        if client_socket != sender_socket:
            try:
                # Send the raw encrypted bytes to the other client.
                client_socket.send(message_bytes)
            except Exception as e:
                # Log if sending fail
                logging.error(f"Failed to broadcast to {client[1]}: {e}")

# Manages a single client connection in its own thread.
def handle_client(client_socket, addr):
    logging.info(f"New connection from {addr}")
    print(f"[+] New connection from {addr}")
    clients.append((client_socket, addr)) # Add this new client to the global list.

    try:
        # Main loop to receive messages from this client.
        while True:
            # This is a blocking call to wait until data is received.
        
            encrypted_message = client_socket.recv(1024) #1024 is the buffer size
            if not encrypted_message:
                # If recv returns an empty string disconnect the client
                break 

            # --- SECURITY & LOGGING ---
            try:
                # Attempt to decrypt the message using our crypto module.
                decrypted_message = crypto.decrypt_message(encrypted_message)
                
                # If decryption is successful, log the plain text.
                logging.info(f"Received from {addr}: {decrypted_message}")
                print(f"[{addr}] {decrypted_message}")
                
                # Relay the original encrypted message to all other clients.
                broadcast(encrypted_message, client_socket)

            except InvalidToken:
                # --- THIS IS THE SECURITY ALERT ---
                # This exception is raised if the data is not valid suck as junk or wrong key
                # This is triggered by simulate_attack.sh.
                logging.warning(f"Failed decryption attempt from {addr}. Possible attack.")
            
            except Exception as e:
                # Catch any other decryption or processing errors.
                logging.error(f"Error processing message from {addr}: {e}")

    except ConnectionResetError:
        # This happens if the client connection is forcibly closed.
        logging.warning(f"Connection lost from {addr}")
    except Exception as e:
        # Catch any other unhandled errors.
        logging.error(f"Unhandled error with {addr}: {e}")
    finally:
        # --- Cleanup ---
        # This code always runs whether the client disconnected cleanly or crashed
        logging.info(f"Closing connection for {addr}")
        print(f"[-] Connection closed for {addr}")
        clients.remove((client_socket, addr)) # Remove client from the broadcast list.
        client_socket.close() # Close the socket connection.

# Main function to initialize and start the server.
def main():
    # Re-check the cipher, in case setup.sh was run after the script was first imported.
    if crypto.cipher is None:
        print("Waiting for 'secret.key'...")
        try:
            # Manually load the key and initialize the cipher.
            crypto.key = crypto.load_key()
            crypto.cipher = Fernet(crypto.key)
            print("Cipher initialized.")
        except Exception:
             # Fail if the key is still not found.
             logging.critical("FATAL: Cipher not initialized. Run setup.sh first.")
             return

    # Create the main server socket object.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Bind the socket to our host and port.
        server_socket.bind((HOST, PORT))
        # Set the socket to listen for incoming connections
        server_socket.listen(5) #5 is the backlog queue
        logging.info(f"Server started. Listening on {HOST}:{PORT}")
        print(f"[*] Server listening on {HOST}:{PORT}")

        # Main loop to accept new connections.
        while True:
            # This is a blocking call. It waits for a new client to connect.
            client_socket, addr = server_socket.accept()
            
            # --- Threading ---
            # Create a new thread to manage this connection independently.
            client_thread = threading.Thread(
                target=handle_client,  # The function this thread will run.
                args=(client_socket, addr), # The arguments to pass to that function.
                daemon=True # Set as daemon so thread auto-exits when main program does.
            )
            # Set a useful name for the thread (visible in logs).
            client_thread.name = f"Client-{addr[1]}"
            client_thread.start() # Start the thread's execution.

    except OSError as e:
        # This can happen if the port is already in use.
        logging.critical(f"Server socket error: {e}")
    except KeyboardInterrupt:
        # This happens when you press Ctrl+C.
        logging.info("Server shutting down.")
    finally:
        # --- Server Cleanup ---
        # Close all active client connections.
        for client in clients:
            client[0].close()
        # Close the main server socket.
        server_socket.close()
        print("\n[*] Server shut down.")

# This check ensures the main() function only runs when the script is executed directly
if __name__ == "__main__":
    main()
