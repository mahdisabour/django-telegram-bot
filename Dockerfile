FROM python:3.8.5

COPY .  /usr/src/app
WORKDIR /usr/src/app
STOPSIGNAL SIGINT
RUN pip install -r requirement.txt
