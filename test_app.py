import os
import pytest
import json
from app import app as flask_app
from unittest.mock import patch, Mock

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

@patch('subprocess.check_output')
def test_run_command_endpoint(mock_check_output, client):
    """
    Test the vulnerable command injection endpoint.
    This test mocks subprocess.check_output to avoid actually executing commands.
    """
    # Mock the subprocess call to return a known value
    mock_check_output.return_value = "command output"
    
    # Prepare the test data with a simple command
    test_data = {"command": "ls -la"}
    
    # Make the request to the vulnerable endpoint
    response = client.post('/run_command', 
                          json=test_data,
                          content_type='application/json')
    
    # Check status code
    assert response.status_code == 200
    
    # Parse response data
    data = json.loads(response.data)
    
    # Verify response content
    assert data == {"result": "command output"}
    
    # Verify that subprocess was called with the expected command
    mock_check_output.assert_called_once_with("ls -la", shell=True, text=True)

@patch('subprocess.check_output')
def test_run_command_injection_scenario(mock_check_output, client):
    """
    Test that demonstrates the potential command injection vulnerability.
    This test shows how a malicious command could be injected.
    """
    # Mock the subprocess call to return a known value
    mock_check_output.return_value = "sensitive data"
    
    # Prepare test data with a command that includes command injection
    # This would be caught by security scanners
    malicious_command = "echo 'hello' && cat /etc/passwd"
    test_data = {"command": malicious_command}
    
    # Make the request to the vulnerable endpoint
    response = client.post('/run_command', 
                          json=test_data,
                          content_type='application/json')
    
    # Check status code
    assert response.status_code == 200
    
    # Verify that subprocess was called with the malicious command
    mock_check_output.assert_called_once_with(malicious_command, shell=True, text=True)

@patch('requests.get')
def test_fetch_url_endpoint(mock_get, client):
    """
    Test the vulnerable SSRF endpoint.
    This test mocks requests.get to avoid actually making HTTP requests.
    """
    # Create a mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><body>Example response</body></html>"
    mock_get.return_value = mock_response
    
    # Prepare the test data with a simple URL
    test_data = {"url": "https://example.com"}
    
    # Make the request to the vulnerable endpoint
    response = client.post('/fetch_url', 
                          json=test_data,
                          content_type='application/json')
    
    # Check status code
    assert response.status_code == 200
    
    # Parse response data
    data = json.loads(response.data)
    
    # Verify response content
    assert data["status_code"] == 200
    assert data["content"] == "<html><body>Example response</body></html>"
    
    # Verify that requests.get was called with the expected URL
    mock_get.assert_called_once_with("https://example.com")

@patch('requests.get')
def test_fetch_url_ssrf_scenario(mock_get, client):
    """
    Test that demonstrates the potential SSRF vulnerability.
    This test shows how internal resources could be accessed via the SSRF vulnerability.
    """
    # Create a mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "AWS metadata content"
    mock_get.return_value = mock_response
    
    # Prepare test data with a URL that could access AWS instance metadata
    # This would be caught by security scanners
    internal_url = "http://169.254.169.254/latest/meta-data/"
    test_data = {"url": internal_url}
    
    # Make the request to the vulnerable endpoint
    response = client.post('/fetch_url', 
                          json=test_data,
                          content_type='application/json')
    
    # Check status code
    assert response.status_code == 200
    
    # Verify that requests.get was called with the internal URL
    mock_get.assert_called_once_with(internal_url)