FROM python:3.12-slim

WORKDIR /movieticket

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install setuptools

COPY requirements.txt /movieticket/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /movieticket

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
