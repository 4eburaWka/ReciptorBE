FROM python:3.10.9-slim

RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY . .
RUN python manage.py migrate

EXPOSE 80
CMD ["python", "manage.py", "runserver"]