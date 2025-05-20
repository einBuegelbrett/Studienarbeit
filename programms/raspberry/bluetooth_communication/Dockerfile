FROM python:3.13-slim
WORKDIR /app
RUN pip install bleak cassandra-driver	
COPY . .
CMD ["python", "bluetooth_communication.py"]
