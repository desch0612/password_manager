# Connection (API) between the database and the password_manager

import sqlite3

# connection (database)
db_path = "/Users/dennisschafer/lazydata/Passwort_Manager/pw_manager/Password_Manager_DB.db"
db_connection = sqlite3.connect(db_path)
db_cursor = db_connection.cursor()
db_cursor.execute("Select * From User")
found_data = db_cursor.fetchall()

print(found_data)













