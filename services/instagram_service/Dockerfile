ARG PYTHON_VERSION=3.11.4

FROM python:${PYTHON_VERSION}-slim as proto-builder

RUN apt-get update && apt-get install -y make

WORKDIR /app

COPY ./protos ./protos
COPY ./services/instagram_service/Makefile ./Makefile

RUN pip install grpcio-tools
RUN make build_proto

FROM python:${PYTHON_VERSION}-slim as base

ENV \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.5.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR="/var/cache/pypoetry" \
    PYTHONWARNINGS="ignore::DeprecationWarning"

RUN set -ex \
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser \
    && apt-get update \
    && apt-get upgrade -y \
    && pip install --upgrade pip \
    && pip install poetry==${POETRY_VERSION} \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

FROM base as builder

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

COPY . .

RUN poetry export -f requirements.txt --output requirements.txt

COPY services/instagram_service /app/services/instagram_service

RUN pip install -r /app/requirements.txt

FROM base as runtime

ENV PYTHONPATH="/app:${PYTHONPATH}"

WORKDIR /app

COPY --from=proto-builder /app/lib ./lib

COPY --from=builder /app/requirements.txt ./

COPY --from=builder /app/main.py ./main.py

COPY --from=builder /app/services/instagram_service ./services/instagram_service

RUN pip install -r requirements.txt

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

USER appuser

ENTRYPOINT ["python", "./main.py"]
