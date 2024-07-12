FROM python:3.11.2-slim

RUN mkdir /app
WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8000", "--workers", "2"]