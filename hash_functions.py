'''
Here the functions are to be added that take a hash value and return a plaintext value
and the other function takes a plaintext value and returns a hash value.
'''

from cryptography.fernet import Fernet

# todo: outsource the generate key from the encrypt function. (Then we have the same key to encrypt and decrypt)
def generate_key():
    key = Fernet.generate_key()  # generate the key.
    return key

# This function takes a plaintext value (password) and returns the hash value.
# The hash value is saved as a hexadecimal value.
def encrypt(password):
    key = generate_key()
    encoded_password = password.encode()
    crypter = Fernet(key)
    crypted_string = crypter.encrypt(encoded_password)
    return crypted_string.decode('utf-8') # convert the hash value into a string!

# todo: The hash value must not be displayed for the user but his plaintext password. This must still be changed.
# This function takes a hash-value and returns the plaintext.
def decrypt(crypted_string):
    key = Fernet.generate_key()
    crypter = Fernet(key)
    crypted_string = crypter.encrypt(bytes(crypted_string, 'utf-8'))
    decrypted_string = crypter.decrypt(crypted_string)

    return decrypted_string













