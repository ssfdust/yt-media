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

CMD [
    "dockerize",
    "-wait", "tcp://db:5432",
    "-wait", "tcp://redis:6379",
    "-wait", "tcp://rabbitmq:5672",
    "scripts/initapp.sh"
]
