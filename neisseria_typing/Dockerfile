FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 curl jq python3-pip ncbi-blast+
RUN pip install biopython urllib3 pandas

COPY ./app /app/
COPY ./bin /bin/

RUN chmod +x /bin/*
