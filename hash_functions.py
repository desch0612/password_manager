'''
Here the functions are to be added that take a hash value and return a plaintext value
and the other function takes a plaintext value and returns a hash value.
he encryption is to be based on sha-256.
'''
import hashlib
import pandas as pd
import db_functions

# with the dataframe, we load all data from the database into a dataframe.
df = pd.DataFrame.from_dict(db_functions.fetch_all())

# This function takes a plaintext value (password) and returns the hash value.
# The hash value is saved as a hexadecimal value.
def hash_function(password):
 return hashlib.sha256(password.encode('utf-8')).hexdigest()

# hash_value is the new column in the df with the hash_values.
df['hash_value'] = df['password'].apply(hash_function)
print(df.head())
# todo: the hash-value has to be saved in the database.

# This function takes a hash-value and returns the plaintext.
def plaintext_function(hash_value):
 pass


