# Go Application with Git SHA Build Variable

A production-ready Go application that includes the git SHA in responses and provides a health check endpoint.

## Features

- Go web application with four endpoints:
  - `/`: Returns JSON with a message containing the git SHA
  - `/healthcheck`: Returns status OK for health monitoring
  - `/summit`: Returns a specific message
  - `/run_command`: A deliberately vulnerable endpoint for demonstration purposes
- Go tests to verify functionality
- Docker container with build-time git SHA argument

## Prerequisites

- Docker
- Git
- Go 1.22 or later (for local development)

## Building the Docker Image

To build the Docker image with the current git SHA:

```bash
# Get the current git SHA
GIT_SHA=$(git rev-parse --short HEAD)

# Build the Docker image
docker build --build-arg GIT_SHA=$GIT_SHA -t go-app:latest .
```

## Running the Container

To run the container:

```bash
docker run -p 80:80 go-app:latest
```

The application will be available at http://localhost:80

## API Endpoints

- `GET /`: Returns JSON with git SHA in message field
  - Example response: `{"message": "Application version: abc123"}`
- `GET /healthcheck`: Returns health status
  - Example response: `{"status": "OK"}`
- `GET /summit`: Returns a specific message
  - Example response: `{"message": "I hope you are enjoying this talk"}`
- `POST /run_command`: Executes a shell command (deliberately vulnerable)
  - Example request: `{"command": "ls -la"}`
  - Example response: `{"result": "total 24\ndrwxr-xr-x..."}`

## Running the Tests

To run the tests inside the Docker container:

```bash
docker build --target builder -t go-app-tests .
```

Or to run tests locally:

```bash
go test -v ./...
```

## Development

To set up local development:

```bash
# Clone the repository
git clone https://github.com/yourusername/aws-ecs-deployment-demo.git
cd aws-ecs-deployment-demo

# Run the tests
go test -v ./...

# Run the application
export GIT_SHA=$(git rev-parse --short HEAD)
go run main.go
```

## Project Structure

- `main.go`: Go application with endpoints for showing git SHA and health check
- `main_test.go`: Go tests to verify application functionality
- `go.mod`: Go module definition
- `Dockerfile`: Container setup with git SHA build argument support