FROM python:3.10.12-bullseye

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]
FROM python:3.10.12-bullseye

COPY . /app

RUN mkdir /app/data

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]
