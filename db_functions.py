# todo: get Password entries with Database fetch
import connection_database
from connection_database import *
import sqlite3
import mainpage
from mainpage import *
import os  # includes functions to interact with the file system.


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

# load all passwords from the database
def fetch_all():
    # The variables can used outside of the function.
    global master_password
    global pw_id, website_name, hash_value, secuity_level

    hash_list = {}
    entries = []

    db_cursor.execute("SELECT * FROM Hash_List ")

    for element in db_cursor:
        hash_list["id"] = element[0]
        hash_list["website"] = element[1]
        hash_list["password"] = element[2]
        entries.append(hash_list)
        hash_list = {}
        #if element[0] == hash_list["id"]:
        #    return entries

    # hash_list has the entries with all attributes (id, website, password)
    #return entries

print(fetch_all())

def Insert_password():
    # test values.
    sql_statement = "INSERT INTO Hash_List VALUES(99 , 'TEST_WEBSITE', 'TEST_PASSWORT', 45)"
    db_cursor.execute(sql_statement)
    db_connection.commit()

def Delete_password():
    pass

def Create_user():
    # test if the user already created
    # create a new "user"
    if not db_path.exists():
        sql_statement1 = "CREATE TABLE User(Master_Password STRING PRIMARY KEY)"
        sql_statement2 = "CREATE TABLE Hash_List (pw_id INT PRIMARY KEY, Website_Name STRING, " \
                         "Hash_Value STRING, Security_Level INT)"
        db_cursor.execute(sql_statement1, sql_statement2)
        db_connection.commit()


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









