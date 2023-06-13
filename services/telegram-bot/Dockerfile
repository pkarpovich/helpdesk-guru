ARG GO_VERSION=1.20

FROM onosproject/protoc-go:v1.3.0 AS proto

WORKDIR /src

COPY ./protos ./protos
COPY ./Makefile ./Makefile

RUN make build_proto


FROM golang:${GO_VERSION} AS build
WORKDIR /src

RUN --mount=type=cache,target=/go/pkg/mod/ \
    --mount=type=bind,source=/services/telegram-bot/go.sum,target=go.sum \
    --mount=type=bind,source=/services/telegram-bot/go.mod,target=go.mod \
    go mod download -x

COPY ./services/telegram-bot .
COPY --from=proto src/services/telegram-bot/lib ./lib

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
