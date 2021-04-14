# FROM python:3

# ENV PATH="/scripts:${PATH}"

# COPY . /usr/src/app

# COPY ./scripts /scripts

# RUN chmod +x /scripts/*

# WORKDIR /usr/src/app
# RUN pip install -r requirement.txt
# CMD ["entrypoint.sh"]



FROM python:3
COPY .  /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirement.txt
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

CMD [ "python3", "manage.py", "runbot" ]