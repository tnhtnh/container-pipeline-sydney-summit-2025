# Flask Application with Git SHA Build Variable

A production-ready Flask application that includes the git SHA in responses and provides a health check endpoint.

## Features

- Flask web application with two endpoints:
  - `/`: Returns JSON with a message containing the git SHA
  - `/healthcheck`: Returns status OK for health monitoring
- Pytest tests to verify functionality
- Docker container with build-time git SHA argument

## Prerequisites

- Docker
- Git

## Building the Docker Image

To build the Docker image with the current git SHA:

```bash
# Get the current git SHA
GIT_SHA=$(git rev-parse --short HEAD)

# Build the Docker image
docker build --build-arg GIT_SHA=$GIT_SHA -t flask-app:latest .
```

## Running the Container

To run the container:

```bash
docker run -p 5000:5000 flask-app:latest
```

The application will be available at http://localhost:5000

## API Endpoints

- `GET /`: Returns JSON with git SHA in message field
  - Example response: `{"message": "Application version: abc123"}`
- `GET /healthcheck`: Returns health status
  - Example response: `{"status": "OK"}`

## Running the Tests

To run the tests inside the Docker container:

```bash
docker run --entrypoint "pytest" flask-app:latest
```

Or to run tests locally:

```bash
pip install -r requirements.txt
pytest
```

## Development

To set up local development:

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
export GIT_SHA=$(git rev-parse --short HEAD)  # On Windows: set GIT_SHA=...
python app.py
```

## Project Structure

- `app.py`: Flask application with endpoints for showing git SHA and health check
- `test_app.py`: Pytest tests to verify application functionality
- `requirements.txt`: Python dependencies (Flask and pytest)
- `Dockerfile`: Container setup with git SHA build argument support