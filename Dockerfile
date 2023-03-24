FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app

RUN python -m venv venv

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]