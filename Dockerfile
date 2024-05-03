# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .
CMD alembic upgrade head && python3 -m bot && arq bot.worker.settings.WorkerSettings && uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 8000
