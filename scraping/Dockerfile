FROM python:3.7-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc libpq-dev && \
    apt-get clean

RUN env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib"

RUN mkdir /app/
WORKDIR /app/
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt

# COPY . /app/scraping/.

CMD tail -f /dev/null
