# syntax=docker/dockerfile:1
FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD alembic upgrade head && python3 -m bot && arq bot.worker.settings.WorkerSettings
