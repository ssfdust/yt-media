FROM ssfdust/alpine-python-poetry:latest

ENV FLASK_ENV="production" \
      FLASK_APP="/Application/smorest_sfs/app.py" \
      HOST="0.0.0.0" \
      PYTHONPYCACHEPREFIX="/pycache" \
      LOGURU_LEVEL=INFO \
      APP="web"

RUN mkdir Application

WORKDIR /Application/

COPY pyproject.toml poetry.lock /

RUN /entrypoint.sh \
        -a zlib \
        -a libjpeg \
        -a postgresql-libs \
        -b zlib-dev \
        -b libffi-dev \
        -b jpeg-dev \
        -b freetype-dev \
        -b postgresql-dev

RUN wget https://raw.githubusercontent.com/eficode/wait-for/master/wait-for -O /usr/bin/waitfor \
    && chmod 755 /usr/bin/waitfor

CMD waitfor -t 300 db:5432 redis:6379 rabbitmq:5672 -- bash scripts/initapp.sh
