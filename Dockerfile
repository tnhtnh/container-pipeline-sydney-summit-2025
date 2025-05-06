FROM python:3.9-slim

WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py test_app.py ./

# Set build argument for git SHA
ARG GIT_SHA=unknown
ENV GIT_SHA=$GIT_SHA

# Expose port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]