FROM python:3.8

ENV FLASK_ENV=production

ENV FLASK_APP=/Application/smorest_sfs/app.py

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

ENV PATH="${PATH}:/root/.poetry/bin"

RUN mkdir Application

# set working directory to /app/
WORKDIR /Application/

# add requirements.txt to the image
COPY pyproject.toml poetry.lock /Application/

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

RUN pip install invoke gunicorn eventlet

CMD ["scripts/initapp.sh"]
