'''
Here the functions are to be added that take a hash value and return a plaintext value
and the other function takes a plaintext value and returns a hash value.
he encryption is to be based on sha-256.
'''
import hashlib



# This function takes a plaintext value (password) and returns the hash value.
# The hash value is saved as a hexadecimal value.
def hash_function(password):
 hash_value = hashlib.sha256(password.encode('utf-8')).hexdigest()
 return hash_value

# todo: The hash value must not be displayed for the user but his plaintext password. This must still be changed.
# This function takes a hash-value and returns the plaintext.
def plaintext_function(hash_value):
 pass


