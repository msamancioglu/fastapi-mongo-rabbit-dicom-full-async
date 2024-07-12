FROM python:3.11.2-slim

RUN mkdir /app
WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN pip install --upgrade pip
RUN pip install poetry

COPY requirements.txt .

RUN pip install -r requirements.txt


CMD ["python", "consumer.py"]