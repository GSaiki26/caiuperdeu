FROM python:3.8-alpine

WORKDIR /app

RUN 'apt install gcc'
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

CMD python3 -u src/main.py
