FROM python:3.8.5-alpine

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
# RUN addgroup -S app && adduser -S app -G app
# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt $APP_HOME

WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
RUN pip install --upgrade pip
RUN apk update \
    && apk add --virtual .build-deps gcc rust cargo libffi-dev openssl-dev libressl-dev python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && pip install -r requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps
COPY . $APP_HOME

# RUN chown -R app:app $APP_HOME
# RUN chown -R app:app $HOME


# USER app