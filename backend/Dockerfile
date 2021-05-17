FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

# collect static files
RUN python manage.py collectstatic --noinput

# apply migrate
RUN python manage.py migrate

# add and run as non-root user
RUN adduser -D django
USER django

# exec command
CMD gunicorn semctra.wsgi:application --bind 0.0.0.0:$PORT
