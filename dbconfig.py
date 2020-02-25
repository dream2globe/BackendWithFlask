dbcfg = {
    "user": "root",
    "password": "9838",
    "host": "localhost",
    "port": 3306,
    "database": "mini_twitter",
}

DB_URL = f"mysql+mysqldb://{dbcfg['user']}:{dbcfg['password']}@{dbcfg['host']}:{dbcfg['port']}/{dbcfg['database']}?charset=utf8"
