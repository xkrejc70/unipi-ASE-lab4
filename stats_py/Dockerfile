FROM python:3.8-slim-buster

RUN apt-get update && \
    apt-get install -y \
        python3-dev \
        default-libmysqlclient-dev \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt && rm /requirements.txt

ADD . /stats_py
WORKDIR /stats_py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]