import os
import pytest
import json
from app import app as flask_app

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_endpoint(client, monkeypatch):
    # Set the GIT_SHA environment variable for testing
    test_sha = "test1234"
    monkeypatch.setenv('GIT_SHA', test_sha)
    
    # Make the request to the index endpoint
    response = client.get('/')
    
    # Check status code
    assert response.status_code == 200
    
    # Parse response data
    data = json.loads(response.data)
    
    # Verify message contains git SHA
    assert "message" in data
    assert test_sha in data["message"]

def test_healthcheck_endpoint(client):
    # Make the request to the healthcheck endpoint
    response = client.get('/healthcheck')
    
    # Check status code
    assert response.status_code == 200
    
    # Parse response data
    data = json.loads(response.data)
    
    # Verify response content
    assert data == {"status": "OK"}