FROM ssfdust/alpine-python-poetry:latest

ENV FLASK_ENV="production" \
      FLASK_APP="/Application/smorest_sfs/app.py" \
      HOST="0.0.0.0" \
      PYTHONPYCACHEPREFIX="/pycache" \
      LOGURU_LEVEL=INFO \
      DOCKERIZE_VERSION="v0.6.1" \
      APP="web"

RUN mkdir Application

WORKDIR /Application/

COPY pyproject.toml poetry.lock /

RUN /entrypoint.sh \
        -a zlib \
        -a libjpeg \
        -a openssl \
        -a postgresql-libs \
        -b zlib-dev \
        -b libffi-dev \
        -b jpeg-dev \
        -b freetype-dev \
        -b postgresql-dev

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

CMD dockerize -wait tcp://db:5432 -wait tcp://redis:6379 -wait tcp://rabbitmq:5672 bash scripts/initapp.sh
