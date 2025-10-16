FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY
RUN python manage.py collectstatic --noinput

EXPOSE 8000
