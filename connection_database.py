import sqlite3

# todo: db_path has to save not in a local path!

# Connection (API) between the database and the password_manager
db_path = "/Users/dennisschafer/lazydata/Passwort_Manager/pw_manager/Password_Manager_DB.db"
db_connection = sqlite3.connect(db_path)
db_cursor = db_connection.cursor()
found_data = db_cursor.fetchall()















