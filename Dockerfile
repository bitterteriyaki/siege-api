FROM python:3.11.1

ENV \
  # python:
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  # poetry:
  POETRY_VERSION=1.3.1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_HOME="/usr/local"

RUN \
  apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    curl \
    build-essential \
  # installing poetry:
  && curl -sSL "https://install.python-poetry.org" | python - \
  && poetry --version

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN \
  poetry version \
  # install deps:
  && poetry run pip install -U pip \
  && poetry install --only main --no-interaction --no-ansi
