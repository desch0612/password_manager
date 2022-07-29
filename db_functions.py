# todo: get Password entries with Database fetch
import connection_database
from connection_database import *
import sqlite3
import mainpage
from mainpage import *
import os  # includes functions to interact with the file system.


def get_entries():
    entry1 = {"id": 1, "name": "Amazon", "pw": "123456"}
    entry2 = {"id": 2, "name": "ebay", "pw": "test123"}
    entry3 = {"id": 3, "name": "website1", "pw": "daskjca"}
    entry4 = {"id": 4, "name": "website2", "pw": "pjpaf"}
    entry5 = {"id": 5, "name": "website3", "pw": "lcksdnl"}
    entry6 = {"id": 6, "name": "website4", "pw": "kdjak"}
    entry7 = {"id": 7, "name": "website4", "pw": "kdjak"}
    entry8 = {"id": 8, "name": "website4", "pw": "kdjak"}
    entry9 = {"id": 9, "name": "website4", "pw": "kdjak"}
    entry10 = {"id": 10, "name": "website4", "pw": "kdjak"}
    entry11 = {"id": 11, "name": "website4", "pw": "kdjak"}
    entry12 = {"id": 12, "name": "website4", "pw": "kdjak"}

    entries = [entry1, entry2, entry3, entry4, entry5, entry6, entry7, entry8, entry9, entry10, entry11, entry12]
    return entries

# load all passwords from the database
def fetch_all():
    # The variables can used outside of the function.
    global master_password
    global pw_id, website_name, hash_value, secuity_level

    # todo: remove "get_entries"
    # todo: save the data into lists?
    user_list = []
    hash_list = []

    sql_statment1 = "SELECT * FROM User"
    sql_statement2 = "SELECT * FROM Hash_List "
    db_cursor.execute(sql_statment1, sql_statement2)
    db_connection.commit()
    db_connection.close()

def Insert_password():
    # test values.
    sql_statement = "INSERT INTO Hash_List VALUES(99 , 'TEST_WEBSITE', 'TEST_PASSWORT', 45)"
    db_cursor.execute(sql_statement)
    db_connection.commit()
    db_connection.close()

def Create_user():
    # test if the user already created
    # create a new "user"
    if not db_path.exists():
        sql_statement1 = "CREATE TABLE User(Master_Password STRING PRIMARY KEY)"
        sql_statement2 = "CREATE TABLE Hash_List (pw_id INT PRIMARY KEY, Website_Name STRING, " \
                         "Hash_Value STRING, Security_Level INT)"
        db_cursor.execute(sql_statement1, sql_statement2)
        db_connection.commit()
        db_connection.close()

def Delete_User():
    if db_path.exists():
        sql_command1 = "DROP TABLE Hash_List WHERE pw_id == Master_Password FROM Table User"
        # todo: connection between User and the Hash-List (which User has to be deleted?)
        sql_command2 = "DROP TABLE USER"
        db_cursor.execute(sql_command1, sql_command2)
        db_connection.commit()
        db_connection.close()
    else:
        db_connection.close()

def Change_master_password():
    pass

def Change_password():
    pass

def Change_website():
    pass

# delete password/website
def Delete_values():
    pass






