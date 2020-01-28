FROM python:3.7-slim

RUN mkdir /app/
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY /scraping/. /app/scraping/.

CMD /bin/bash
