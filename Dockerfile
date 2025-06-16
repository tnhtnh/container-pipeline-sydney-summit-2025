FROM golang:1.22-alpine AS builder

WORKDIR /app
COPY go.mod main.go main_test.go ./
RUN go test -v ./...
RUN go build -o app .

FROM alpine:latest
RUN apk --no-cache add curl

WORKDIR /app
COPY --from=builder /app/app .

ARG GIT_SHA=unknown
ENV GIT_SHA=$GIT_SHA

HEALTHCHECK --interval=15s --timeout=3s \
  CMD curl -f http://localhost/healthcheck || exit 1

LABEL git_sha=$GIT_SHA
LABEL maintainer="your-email@example.com"
LABEL version="1.0"
LABEL description="Example container with AWS Inspector scanning"

EXPOSE 80

CMD ["./app"]