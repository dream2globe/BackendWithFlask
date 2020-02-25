db = {
    "user": "root",
    "password": "9838",
    "host": "localhost",
    "port": 3306,
    "database": "mini_twitter",
}

DB_URL = f"mysql+mysqlconnetor://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
