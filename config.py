import os


db_config = {
            "engine": "sqlite+aiosqlite",
            "host": "/db.sqlite3",
            "port": None,
            "user": None,
            "password": None,
            "database": None,
        }
jwt_secret = 'secret'


if os.getenv('DOCKERIZED'):
    db_config = {
            "engine": os.getenv('DB_ENGINE'),
            "host": os.getenv('DB_HOST'),
            "port": os.getenv('DB_PORT'),
            "user": os.getenv('DB_USER'),
            "password": os.getenv('DB_PASSWORD'),
            "database": os.getenv('DB_DATABASE'),
        }
    jwt_secret = os.getenv('JWT_SECRET')
