# todo: get Password entries with Database fetch
import connection_database
import sqlite3

'''
def get_entries():
    entry1 = {"id": 1, "website": "Amazon", "password": "123456"}
    entry2 = {"id": 2, "website": "ebay", "password": "test123"}
    entry3 = {"id": 3, "website": "website1", "password": "daskjca"}
    entry4 = {"id": 4, "website": "website2", "password": "pjpaf"}
    entry5 = {"id": 5, "website": "website3", "password": "lcksdnl"}
    entry6 = {"id": 6, "website": "website4", "password": "kdjak"}
    entry7 = {"id": 7, "website": "website4", "password": "kdjak"}
    entry8 = {"id": 8, "website": "website4", "password": "kdjak"}
    entry9 = {"id": 9, "website": "website4", "password": "kdjak"}
    entry11 = {"id": 11, "website": "website4", "password": "kdjak"}
    entry10 = {"id": 10, "website": "website4", "password": "kdjak"}
    entry12 = {"id": 12, "website": "website4", "password": "kdjak"}

    entries = [entry1, entry2, entry3, entry4, entry5, entry6, entry7, entry8, entry9, entry10, entry11, entry12]
    return entries
'''

# Returns the maximum ID from the Hash_List table with the pw_id attribute.
def get_maxid():
    sql_statement = "SELECT MAX(pw_id) FROM Hash_List"
    connection_database.db_cursor.execute(sql_statement)
    id_list = connection_database.db_cursor.fetchall()
    max_id = int

    # Checks if there are any passwords at all.
    if id_list:
        value = id_list[0]
        value = list(value)
    max_id = value[0]
    return max_id

# load all passwords from the database
def fetch_all():
    hash_list = {}
    entries = []

    connection_database.db_cursor.execute("SELECT * FROM Hash_List")

    for value in connection_database.db_cursor:
        hash_list["id"] = value[0]
        hash_list["website"] = value[1]
        hash_list["password"] = value[2]
        entries.append(hash_list)
        hash_list = {}
    return entries

# Adds password to the database.
def Insert_password(zahl1, website, password, zahl2):
    # test values.
    sql_statement = "INSERT INTO Hash_List (pw_id,Website_Name,Hash_Value,Security_Level) VALUES ('zahl1',website,password,'zahl2')"
    connection_database.db_cursor.execute(sql_statement)
    connection_database.db_connection.commit()


# Deletes a password from the database
def delete_password():
    sql_statement = "DELETE FROM Hash_LIST WHERE pw_id =  102"
    connection_database.db_cursor.execute(sql_statement)
    connection_database.db_connection.commit()

# Deletes all passwords
def delete_all_passwords():
    sql_statement = "DELETE FROM Hash_List"
    connection_database.db_cursor.execute(sql_statement)
    connection_database.db_connection.commit()

def create_user():
    # test if the user already created
    # create a new "user"
    if not connection_database.db_path.exists():
        sql_statement1 = "CREATE TABLE User(Master_Password STRING PRIMARY KEY)"
        sql_statement2 = "CREATE TABLE Hash_List (pw_id INT PRIMARY KEY, Website_Name STRING, " \
                         "Hash_Value STRING, Security_Level INT)"
        connection_database.db_cursor.execute(sql_statement1, sql_statement2)
        connection_database.db_connection.commit()

def delete_User():
    # Checks if the user is present at all
    if connection_database.db_path.exists():
        sql_command1 = "DROP TABLE Hash_List WHERE pw_id == Master_Password FROM Table User"
        # todo: connection between User and the Hash-List (which User has to be deleted?)
        sql_command2 = "DROP TABLE USER"
        connection_database.db_cursor.execute(sql_command1, sql_command2)
        connection_database.db_connection.commit()
        connection_database.db_connection.close()
    else:
        connection_database.db_connection.close()

def change_password():
    pass

def change_master_password():
    pass

def change_website():
    pass









