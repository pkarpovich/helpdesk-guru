ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim-buster as base

ENV \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.5.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_VENV=/opt/poetry-venv \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONWARNINGS="ignore::DeprecationWarning"

RUN set -ex \
    # Create a non-root user
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser \
    # Upgrade the package index and install security upgrades
    && apt-get update \
    && apt-get upgrade -y \
    # Install dependencies \
    && pip install --upgrade pip \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*


FROM base as proto-builder

RUN apt-get update && apt-get install -y make
WORKDIR /app
COPY ./protos ./protos
RUN mkdir -p ./lib
RUN pip install grpcio grpcio-tools
RUN pip install --pre "betterproto[compiler]"
RUN python -m grpc_tools.protoc -I /app/protos --python_betterproto_out=/app/lib /app/protos/*.proto


FROM base as builder

RUN pip install poetry==${POETRY_VERSION}

WORKDIR /app
COPY ./services/gpt-context/pyproject.toml ./services/gpt-context/poetry.lock ./
RUN poetry config virtualenvs.create false
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-dev --no-root
RUN poetry export -f requirements.txt --output requirements.txt


FROM base as runtime

ENV PYTHONPATH="/app:${PYTHONPATH}"

WORKDIR /app

COPY ./services/gpt-context .
COPY --from=proto-builder /app/lib ./lib
COPY --from=builder /app/requirements.txt ./

RUN pip install -r requirements.txt

USER appuser

EXPOSE 50051

CMD python gpt_context/main.py