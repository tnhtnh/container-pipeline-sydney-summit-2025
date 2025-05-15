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
    
def test_summit_endpoint(client):
    # Make the request to the summit endpoint
    response = client.get('/summit')
    
    # Check status code
    assert response.status_code == 200
    
    # Parse response data
    data = json.loads(response.data)
    
    # Verify response content
    assert data == {"message": "I hope you are enjoying this talk"}

def test_ping_endpoint_with_safe_input(client, monkeypatch):
    """Test the ping endpoint with safe input."""
    # Mock subprocess.check_output to avoid actual command execution
    class MockSubprocess:
        def check_output(self, cmd, shell=False):
            return b"PING localhost (127.0.0.1): 56 data bytes\n64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.037 ms\n"
    
    monkeypatch.setattr('app.subprocess', MockSubprocess())
    
    # Make the request to the ping endpoint with safe input
    response = client.get('/ping?hostname=localhost')
    
    # Check status code
    assert response.status_code == 200
    
    # Parse response data
    data = json.loads(response.data)
    
    # Verify response contains output
    assert "output" in data
    assert "PING localhost" in data["output"]

def test_ping_endpoint_with_unsafe_input(client, monkeypatch):
    """Test the ping endpoint with unsafe input that could lead to command injection."""
    # Mock subprocess.check_output to avoid actual command execution
    class MockSubprocess:
        def check_output(self, cmd, shell=False):
            # Here we're just verifying the command contains our injected code
            # In reality, this would be a security vulnerability
            if "; ls" in cmd:
                return b"This command could allow arbitrary code execution\n"
            return b"Normal output"
    
    monkeypatch.setattr('app.subprocess', MockSubprocess())
    
    # Make the request to the ping endpoint with unsafe input
    # This input attempts command injection with ; to execute a second command
    response = client.get('/ping?hostname=localhost;%20ls%20-la')
    
    # Check status code - this should still "work" which demonstrates the vulnerability
    assert response.status_code == 200
    
    # In a real-world scenario, this would execute both the ping and the ls command
    # Here we're just verifying our mocked response
    data = json.loads(response.data)
    assert "output" in data