import sqlite3

# Connection (API) between the database and the password_manager
db_path = "Password_Manager_DB.db"
db_connection = sqlite3.connect(db_path)
db_cursor = db_connection.cursor()
found_data = db_cursor.fetchall()















