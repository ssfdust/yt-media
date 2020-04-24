FROM jfloff/alpine-python:3.8

ENV FLASK_ENV=production

ENV FLASK_APP=/Application/smorest_sfs/app.py

ENV HOST=0.0.0.0

ENV PYTHONPYCACHEPREFIX=/pycache

RUN apk --no-cache add curl zlib-dev

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

ENV PATH="${PATH}:/root/.poetry/bin"

RUN pip install --upgrade pip

RUN apk --no-cache add jpeg-dev

RUN pip install pillow

RUN mkdir Application

# set working directory to /app/
WORKDIR /Application/

# add requirements.txt to the image
COPY pyproject.toml poetry.lock /Application/

RUN pip install -U setuptools wheel poetry
RUN pip install --no-build-isolation pendulum

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

CMD ["scripts/initapp.sh"]
