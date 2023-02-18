FROM python:3.10

RUN apt-get update && apt-get install -y default-mysql-client

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL mysql://mariadb:mariadb@db:9051/mariadb

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./ ./
 
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
