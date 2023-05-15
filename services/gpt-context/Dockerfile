ARG PYTHON_VERSION=3.11.3
FROM python:${PYTHON_VERSION}-slim as base

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev


RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=./services/gpt-context/requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY . .

WORKDIR /app/services/gpt-context

RUN mkdir -p lib
RUN make build_proto
RUN python ingest.py

USER appuser

EXPOSE 50051

CMD python main.py
