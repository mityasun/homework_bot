FROM python:3.9.8-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt --no-cache-dir

COPY .. /app

LABEL project='homework_bot' version=1.0

CMD ["python", "homework.py"]