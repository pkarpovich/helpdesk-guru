ARG PYTHON_VERSION=3.11.4

FROM python:${PYTHON_VERSION}-slim AS proto-builder

RUN apt-get update \
    && apt-get install -y make

WORKDIR /app

COPY ./protos ./protos

RUN \
    mkdir -p ./lib \
    && pip install grpcio grpcio-tools \
    && pip install --pre "betterproto[compiler]" \
    && python -m grpc_tools.protoc -I /app/protos --python_betterproto_out=/app/lib /app/protos/*.proto

FROM python:${PYTHON_VERSION}-slim AS base

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

RUN \
    set -e \
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser \
    && apt-get update \
    && apt-get upgrade -y \
    && pip install --upgrade pip \
    && pip install poetry==${POETRY_VERSION} \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

FROM base AS builder

RUN pip install poetry==${POETRY_VERSION}

WORKDIR /app

COPY ./services/instagram-service/pyproject.toml ./services/instagram-service/poetry.lock ./

RUN \
    poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root

RUN poetry export -f requirements.txt --output requirements.txt

FROM base AS runtime

ENV PYTHONPATH="/app:${PYTHONPATH}"

WORKDIR /app

COPY --from=proto-builder /app/lib ./lib

COPY --from=builder /app/requirements.txt ./

COPY ./services/instagram-service .

RUN pip install -r /app/requirements.txt

USER appuser

ENTRYPOINT ["python", "instagram_service/main.py"]
