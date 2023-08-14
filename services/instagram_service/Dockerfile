ARG PYTHON_VERSION=3.11.4

FROM python:${PYTHON_VERSION}-slim as proto-builder

RUN apt-get update && apt-get install -y make

WORKDIR /app

COPY ./protos ./protos
COPY ./services/instagram_service/Makefile ./Makefile
RUN pip install google
RUN pip install grpcio-tools
RUN make build_proto

FROM python:${PYTHON_VERSION}-slim as base

# Set environment variables
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
    # Create a non-root user
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser \
    # Upgrade the package index and install security upgrades
    && apt-get update \
    && apt-get upgrade -y \
    # Install dependencies \
    && pip install --upgrade pip \
    && pip install poetry==${POETRY_VERSION} \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

FROM base as builder

# Set the working directory
WORKDIR /app

# Copy poetry files and install dependencies
COPY ./services/instagram_service/pyproject.toml ./services/instagram_service/poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

# Copy the application files
COPY . .
#COPY ./services/instagram_service .
# Export runtime dependencies to requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt

# Copy the Instagram service files
COPY services/instagram_service /app/services/instagram_service
COPY services/instagram_service/main.py /app/main.py
# Install dependencies for the Instagram service
RUN pip install -r /app/requirements.txt

FROM base as runtime

# Set the environment variables
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Set the working directory
WORKDIR /app

# Copy the protos library
COPY --from=proto-builder /app/lib ./lib

# Copy the requirements.txt file
COPY --from=builder /app/requirements.txt ./

# Copy the application files
COPY --from=builder /app/main.py ./main.py

# Copy the Instagram service files
COPY --from=builder /app/services/instagram_service ./services/instagram_service
COPY ./services/instagram_service .
# Install the runtime dependencies
#RUN pip install google
RUN pip install -r requirements.txt

# Switch to the non-root user
USER appuser

# Set the entrypoint
ENTRYPOINT ["python", "./main.py"]
#VOLUME /usr/data