# Dockerfile

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . /app/
COPY .env /app/.env

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "src.wsgi:application", "--bind", "0.0.0.0:8000"]
