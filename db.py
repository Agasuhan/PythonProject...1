import mysql.connector
dbconfig = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'aliik0555@#$',
    'database': 'sakila'
}

# Функция для подключения к базе данных
def connect_to_db():
    return mysql.connector.connect(**dbconfig)
