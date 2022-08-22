import connection_database
import hash_functions
from cryptography.fernet import Fernet


# Returns the maximum ID from the Hash_List table with the pw_id attribute.
def get_maxid():
    sql_statement = "SELECT MAX(pw_id) FROM Hash_List"
    connection_database.db_cursor.execute(sql_statement)
    id_list = connection_database.db_cursor.fetchall()

    # Checks if there are any passwords at all.
    if not id_list[0][0]:
        max_id = 0
    else:
        value = id_list[0][0]
        max_id = value

    return max_id

# load all passwords from the database
def fetch_all():
    hash_list = {}
    entries = []

    connection_database.db_cursor.execute("SELECT * FROM Hash_List")

    for value in connection_database.db_cursor:
        hash_list["id"] = value[0]
        hash_list["website"] = value[1]
        hash_list["password"] = hash_functions.decrypt(value[2])
        entries.append(hash_list)
        hash_list = {}

    return entries


# This function added all information including the hash_value into the database.
def Insert_hash_value(db_id, website, password, security_level):
    security_level = 1
    hash_value = hash_functions.encrypt(password)
    sql_statement = f"INSERT INTO Hash_List (pw_id,Website_Name,Hash_Value,Security_Level) VALUES ({db_id},'{website}','{hash_value}',{security_level})"
    connection_database.db_cursor.execute(sql_statement)
    connection_database.db_connection.commit()


# Updates Password.
def update_password(db_id, website, password):
    if website and password:    # both values changed
        sql_statement = f"UPDATE Hash_List SET Website_Name = '{website}', Hash_Value = '{password}' WHERE pw_id = {db_id}"
    elif not website and password:  # password was changed
        sql_statement = f"UPDATE Hash_List SET Hash_Value = '{password}' WHERE pw_id = {db_id}"
    else:   # website was changed
        sql_statement = f"UPDATE Hash_List SET Website_Name = '{website}' WHERE pw_id = {db_id}"

    connection_database.db_cursor.execute(sql_statement)
    connection_database.db_connection.commit()


# Deletes a password from the database
def delete_password(db_id):
    sql_statement = f"DELETE FROM Hash_LIST WHERE pw_id = {db_id}"
    connection_database.db_cursor.execute(sql_statement)
    connection_database.db_connection.commit()

# Deletes all passwords
def delete_all_passwords():
    sql_statement = "DELETE FROM Hash_List"
    connection_database.db_cursor.execute(sql_statement)
    connection_database.db_connection.commit()


def check_table_existence(tbl):
    sql_statement = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tbl}';"
    connection_database.db_cursor.execute(sql_statement)

    if connection_database.db_cursor.fetchone() is not None:
        # table exists
        return True
    else:   # table doesn't exists
        return False


def create_user_table(mp):
    sql_statement = "CREATE TABLE User (master_password TEXT PRIMARY KEY)"
    connection_database.db_cursor.execute(sql_statement)
    sql_statement = f"INSERT INTO User VALUES ('{mp}')"
    connection_database.db_cursor.execute(sql_statement)
    connection_database.db_connection.commit()


def fetch_mp():
    sql_statement = "SELECT master_password FROM User"
    connection_database.db_cursor.execute(sql_statement)

    return connection_database.db_cursor.fetchone()[0]


def delete_User():
    # Checks if the user is present at all
    if connection_database.db_path.exists():
        sql_command1 = "DROP TABLE Hash_List WHERE pw_id == Master_Password FROM Table User"
        sql_command2 = "DROP TABLE USER"
        connection_database.db_cursor.execute(sql_command1, sql_command2)
        connection_database.db_connection.commit()
        connection_database.db_connection.close()
    else:
        connection_database.db_connection.close()

def change_master_password():
    pass

def change_website():
    pass









