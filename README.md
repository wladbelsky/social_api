# Установка

Для установки необходимо выполнить следующие команды:

```bash
pip install -r requirements.txt
```

# Запуск

Для установки параметров подключения к базе данных необходимо изменить файл `config.py` в корне проекта.

Для запуска необходимо выполнить следующие команды:

```bash
python main.py
```

или для запуска через uvicorn

```bash
uvicorn main:app
```

# Запуск через docker-compose

Для установки параметров подключения к базе данных необходимо создать файл `.env` в корне проекта и заполнить его следующим образом:

```yaml
      - DB_ENGINE=sqlite+aiosqlite
      - DB_HOST=data/db.sqlite3
      - DB_PORT
      - DB_USER
      - DB_PASSWORD
      - DB_DATABASE
      - JWT_SECRET=secret
```

Для запуска через docker-compose необходимо выполнить следующую команду:

```bash
docker-compose up
```

# Документация

Документация доступна по адресу `http://{host}:{port}/docs`


