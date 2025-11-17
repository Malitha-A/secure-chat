import socket
import threading
from cryptography.fernet import Fernet, InvalidToken
import crypto # The file for handling the secret key and encryption

# --- Configuration ---
HOST = '127.0.0.1'  # The server's addres
PORT = 9999         # Port number of the server

# This function runs in a separate thread to listen for server messages.
def receive_messages(client_socket):
    while True:
        try:
            # Wait and receive any message from the server
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                # If the message is empty then disconnect from the server
                print("\n[-] Disconnected from server.")
                break
            
            # Use the crypto file to unlock the message
            decrypted_message = crypto.decrypt_message(encrypted_message)
            
            # Print the unlocked message and give the input promt ">" again
            print(f"\r[Received] {decrypted_message}\n> ", end="")
        
        except InvalidToken:
            # Catch junk messeges from attacks
            print(f"\r[Error] Received a corrupt message.\n> ", end="")
        except ConnectionResetError:
            # This happens if the server crashes or closes
            print("\n[-] Server connection lost.")
            break
        except Exception as e:
            # Catch any other unexpected error
            print(f"\n[Error] {e}")
            break
    
    # Clean up the connection if the loop breaks
    client_socket.close()

# This function runs in the main thread to read and send user input.
def send_messages(client_socket):
    try:
        while True:
            # Wait for the user to type something and press Enter
            message = input("> ")
            if message.lower() == 'exit':
                break # Stop the loop if the user types 'exit'
            
            # Use our crypto file to lock the message
            encrypted_message = crypto.encrypt_message(message)
            
            # Send the locked message to the server
            if encrypted_message:
                client_socket.send(encrypted_message)
            
    except (EOFError, KeyboardInterrupt):
        # Handle when the user presses Ctrl+C
        print("\n[+] Quitting...")
    finally:
        # Clean up the connection when the loop stops
        client_socket.close()

# This is the main function that starts everything
def main():
    
    # Check if the 'secret.key' was found and the cipher is ready
    if crypto.cipher is None:
        try:
            crypto.key = crypto.load_key()
            crypto.cipher = Fernet(crypto.key)
        except:
             # Fail if the key is missing
             print("FATAL: 'secret.key' not found. Run setup.sh first.")
             return

    # Create the client's socket to make the connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # connect to server's address and the port
        client_socket.connect((HOST, PORT))
        print(f"[*] Connected to {HOST}:{PORT}. Type 'exit' to quit.")
    except ConnectionRefusedError:
        # If the server is not running
        print(f"[!] Connection refused. Is the server running on {HOST}:{PORT}?")
        return

    # --- Start the two jobs ---

    # 1. Start the 'receive_messages' job in the background
    
    receive_thread = threading.Thread(
        target=receive_messages, 
        args=(client_socket,),
        daemon=True #Thread automatically stops when the main program stops
    )
    receive_thread.start()

    # 2. Use the current main thread for the 'send_messages' job
   
    send_messages(client_socket) #Wait for the user to type
    
# Check if the script is being run directly
# if it is then call the main function to start the program
if __name__ == "__main__":
    main()
