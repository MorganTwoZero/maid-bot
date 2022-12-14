FROM python:3.10-alpine

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

CMD ["python", "src/main.py"]
