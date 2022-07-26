# todo: get Password entries with Database fetch
import connection_database
import sqlite3
db_path = "/Users/dennisschafer/lazydata/Passwort_Manager/pw_manager/Password_Manager_DB.db"
db_connection = sqlite3.connect(db_path)
db_cursor = db_connection.cursor()

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

def delete_password():
    pass

def insert_password():
    pass

def delete_User():
    """"
    sql_command = DROP TABLE USER;
    db_cursor.execute(sql_command)
    """

def change_password():
    pass

# a new user need a new database to create some passwords
def create_database():
    """"
    sql_command = CREATE TABLE "User" (
    "Master_Password"	TEXT,
	PRIMARY KEY("Master_Password")
); CREATE TABLE "Hash_List" (
	"pw_id"	INTEGER,
	"Website_Name"	TEXT,
	"Hash_Value"	TEXT,
	"Security_Level"	INTEGER
    );

    db_cursor.execute(sql_command)"""

# load all passwords from the database
def fetch_all():
    pass

