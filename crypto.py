from cryptography.fernet import Fernet, InvalidToken # the specific encryption system used 

KEY_FILE = 'secret.key' # The name of the file that holds the secret key.

# These will be loaded with the key and fernet
key = None
cipher = None

# A function to read the secret key file.
def load_key():
 
    return open(KEY_FILE, 'rb').read() # read bytes since the key is not plain text

# --- This code tries to load the key right when the program starts. ---
try:
    key = load_key()
    cipher = Fernet(key) # 'cipher' is the lockbox tool used to encrypt/decrypt
except FileNotFoundError:
    # Means setup.sh hasn't run or the client/server will load it.
    pass 
except Exception as e:
    # Catch any other error such as a corrupt key
    print(f"Warning: could not load key: {e}")
    cipher = None
# ---

# This function encrypts a messege
def encrypt_message(message_str):
    if cipher is None:
        # Fail if the key was never loaded.
        raise Exception("Cipher not initialized. Run setup.sh and restart.")
    try:
        # Turn the text into bytes and use the "lockbox" to encrypt it.
        return cipher.encrypt(message_str.encode('utf-8'))
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

# This function unlocks a message (decrypts it).
def decrypt_message(encrypted_bytes):
    if cipher is None:
        # Fail if the key was never loaded.
        raise Exception("Cipher not initialized. Run setup.sh and restart.")
    try:
        # Use the fernet to decrypt the bytes and turn them back into text.
        return cipher.decrypt(encrypted_bytes).decode('utf-8')
    except InvalidToken:
        # This error happens if the key is wrong or the data is junk
        raise InvalidToken("Failed to decrypt: Invalid token.")
    except Exception as e:
        print(f"Decryption error: {e}")
        return None
