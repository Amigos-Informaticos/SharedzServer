FROM python:3.9.5-buster

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN pip install gunicorn==20.1.0

RUN apt update && apt install nano

CMD ["gunicorn", "-b", "0.0.0.0:42071", "--certfile", "cert.pem", "--ca-certs", "chain.pem", "--keyfile", "privkey.pem", "--workers", "2", "app:app"]
