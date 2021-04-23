FROM python:3.8.5


COPY .  /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirement.txt
