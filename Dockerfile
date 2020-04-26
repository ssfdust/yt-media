FROM ccr.ccs.tencentyun.com/ssfdust/alpine-poetry:latest

ENV FLASK_ENV="production" \
      FLASK_APP="/Application/smorest_sfs/app.py" \
      HOST="0.0.0.0" \
      PYTHONPYCACHEPREFIX="/pycache"

RUN mkdir Application

WORKDIR /Application/

COPY pyproject.toml poetry.lock /

RUN /entrypoint.sh \
        -a zlib \
        -a libjpeg \
        -a freetype \
        -a postgresql-libs \
        -b zlib-dev \
        -b libffi-dev \
        -b jpeg-dev \
        -b postgresql-dev

CMD ["scripts/initapp.sh"]
