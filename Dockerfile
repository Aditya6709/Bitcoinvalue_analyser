FROM apache/spark:latest

USER root

RUN apt-get update && apt-get install -y python3 python3-pip curl && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install requests kafka-python

WORKDIR /app
COPY . .