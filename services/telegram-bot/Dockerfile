ARG GO_VERSION=1.20

FROM golang:${GO_VERSION} AS base

FROM base AS proto

WORKDIR /app

COPY ./protos ./protos
COPY ./services/telegram-bot/Makefile ./Makefile

RUN apt update \
    && apt install -y protobuf-compiler \
    && go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest \
    && go install google.golang.org/protobuf/cmd/protoc-gen-go@latest

RUN make build_proto


FROM base AS build
WORKDIR /app

RUN --mount=type=cache,target=/go/pkg/mod/ \
    --mount=type=bind,source=/services/telegram-bot/go.sum,target=go.sum \
    --mount=type=bind,source=/services/telegram-bot/go.mod,target=go.mod \
    go mod download -x

COPY ./services/telegram-bot .
COPY --from=proto app/services/telegram-bot/lib ./lib

RUN CGO_ENABLED=0 go build -o /bin/bot .


FROM alpine:latest AS final

RUN --mount=type=cache,target=/var/cache/apk \
    apk --update add \
        ca-certificates \
        tzdata \
        && \
        update-ca-certificates

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

COPY --from=build /bin/bot /bin/


ENTRYPOINT [ "/bin/bot" ]
