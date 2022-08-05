import sqlite3
import os.path


# Creates Table for Password Entries if .db File is new
def create_table():
    sql_statement = "CREATE TABLE Hash_List (pw_id INT PRIMARY KEY, Website_Name STRING, " \
                     "Hash_Value STRING, Security_Level INT)"
    db_cursor.execute(sql_statement)
    db_connection.commit()


db_create = False
if not os.path.exists("Password_Manager_DB.db"):
    file = open("Password_Manager_DB.db", "w+")
    file.close()
    db_create = True


# Connection (API) between the database and the password_manager
db_path = "Password_Manager_DB.db"
db_connection = sqlite3.connect(db_path)
db_cursor = db_connection.cursor()
if db_create:
    create_table()
found_data = db_cursor.fetchall()















