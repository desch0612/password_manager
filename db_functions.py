# todo: get Password entries with Database fetch
import connection_database
from connection_database import *
import sqlite3
import mainpage
from mainpage import *


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

def create_user():
        sql_statement = "CREATE TABLE User( Master_Password STRING)"
        db_cursor.execute(sql_statement)
        db_connection.commit()

def change_master_password():
    pass

def insert_values():
    sql_statement = "INSERT INTO Hash_List VALUES(100, 'testwebsite', 'fjiejfoiew', 2)"
    db_cursor.execute(sql_statement)
    db_connection.commit()

def change_values():
    pass

def delete_values():
    pass

def delete_User():
    """"
    sql_command = DROP TABLE USER;
    db_cursor.execute(sql_command)
    """

# load all passwords from the database
def fetch_all():
    pass

