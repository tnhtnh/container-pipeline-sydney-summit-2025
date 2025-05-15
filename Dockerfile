FROM python:3.5.0b3-slim AS builder

WORKDIR /app
COPY requirements.txt requirements-dev.txt ./
COPY app.py test_app.py ./
RUN pip install --no-cache-dir -r requirements-dev.txt
RUN pytest test_app.py

FROM python:3.5.0b3-slim
RUN apt-get update && apt-get install -y curl

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy only app.py from builder stage (forces builder to succeed)
COPY --from=builder /app/app.py ./
ARG GIT_SHA=unknown
ENV GIT_SHA=$GIT_SHA

HEALTHCHECK --interval=15s --timeout=3s \
  CMD curl -f http://localhost/healthcheck || exit 1

LABEL git_sha=$GIT_SHA
LABEL maintainer="your-email@example.com"
LABEL version="1.0"
LABEL description="Example container with AWS Inspector scanning"

EXPOSE 80

CMD ["python", "app.py"]