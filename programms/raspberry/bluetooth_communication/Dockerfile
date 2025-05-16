FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r bleak
COPY . .
CMD ["python", "bluetooth_reader.py"]
