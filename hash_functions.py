'''
Here the functions are to be added that take a hash value and return a plaintext value
and the other function takes a plaintext value and returns a hash value.
'''

from cryptography.fernet import Fernet

# todo: outsource the generate key from the encrypt function. (Then we have the same key to encrypt and decrypt)
# Generates a key and save it into a file
def generatekey():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the previously generated key
def load_key():
    return open("secret.key", "rb").read()

# encrypt the password
def encrypt(password):
    key = load_key()
    encoded_password = password.encode()
    crypter = Fernet(key)
    crypted_string = crypter.encrypt(encoded_password)

    return crypted_string.decode('utf-8') # convert the hash value into a string!


# This function takes a hash-value and returns the plaintext.
def decrypt(encrypted_password):
    bytes_encrypted_password = bytes(encrypted_password, 'UTF-8')
    key = load_key()
    crypter = Fernet(key)
    plaintext_Value = crypter.decrypt(bytes_encrypted_password)

    return plaintext_Value










