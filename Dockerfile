# syntax=docker/dockerfile:1
FROM python:3.12-alpine
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .
CMD alembic upgrade head && python3 -m bot && arq bot.worker.settings.WorkerSettings
