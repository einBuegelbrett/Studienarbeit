FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install cassandra-driver

CMD ["python", "/app/init-service/init_database.py"]