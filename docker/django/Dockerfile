# This Dockerfile uses multi-stage build to customize DEV and PROD images:
# https://docs.docker.com/develop/develop-images/multistage-build/

FROM python:3.11.1-slim-buster AS development_build

ARG DJANGO_ENV \
  # needed for fixing permissions of files created by Docker:
  UID=1000 \
  GID=1000

ENV DJANGO_ENV=${DJANGO_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.3.1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# system deps:
RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    brotli \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
  # installing poetry:
  && curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version \
  # cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN groupadd -g "${GID}" -r web \
  && useradd -d '/app' -g web -l -r -u "${UID}" web \
  && chown web:web -R '/app'

# copy only requirements, to cache them in docker layer
COPY --chown=web:web ./poetry.lock ./pyproject.toml /app/

# project initialization:
RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
  echo "$DJANGO_ENV" \
  && poetry version \
  # install deps:
  && poetry run pip install -U pip \
  && poetry install \
    $(if [ "$DJANGO_ENV" = 'production' ]; then echo '--only main'; fi) \
    --no-interaction --no-ansi

USER web


# the following stage is only for production:
FROM development_build AS production_build
COPY --chown=web:web . /app
