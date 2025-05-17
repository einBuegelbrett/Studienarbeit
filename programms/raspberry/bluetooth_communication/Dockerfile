FROM python:3.11-slim
WORKDIR /app
RUN pip install bleak cassandra-driver	
COPY . .
CMD ["python", "bluetooth_reader.py"]
