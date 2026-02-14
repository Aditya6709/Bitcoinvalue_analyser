FROM apache/spark:latest

USER root

RUN apt-get update && apt-get install -y python3 python3-pip curl && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install requests kafka-python


WORKDIR /opt/spark/jars
RUN curl -O https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.28/mysql-connector-java-8.0.28.jar

WORKDIR /app
COPY . .
