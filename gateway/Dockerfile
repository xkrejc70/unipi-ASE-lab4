FROM python:3.8-slim-buster

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

ADD . /gateway
WORKDIR /gateway

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]