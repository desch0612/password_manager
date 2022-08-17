'''
Here the functions are to be added that take a hash value and return a plaintext value
and the other function takes a plaintext value and returns a hash value.
he encryption is to be based on sha-256.
'''

from cryptography.fernet import Fernet

# This function takes a plaintext value (password) and returns the hash value.
# The hash value is saved as a hexadecimal value.
def encrypt(password):
    key = Fernet.generate_key()
    crypter = Fernet(key)
    pw = crypter.encrypt()
    return str(pw, encoding = 'utf8')


# todo: The hash value must not be displayed for the user but his plaintext password. This must still be changed.
# This function takes a hash-value and returns the plaintext.
def decrypt(hash_value):
    pass






