# Connection (API) between the database and the password_manager

import sqlite3

# connection (database)
db_path = "/Users/dennisschafer/lazydata/Passwort_Manager/Datenbank/password_manager/Password_DB.db"
db_connection = sqlite3.connect.connect(db_path)
db_cursor = db_connection.cursor()
db_cursor.execute("SELECT * FROM user")
found_data = db_cursor.fetchall()

print(str(found_data))










