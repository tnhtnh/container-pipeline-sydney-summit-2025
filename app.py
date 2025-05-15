import os
import subprocess
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    git_sha = os.environ.get('GIT_SHA', 'unknown')
    return jsonify({"message": f"Application version: {git_sha}"})

@app.route('/healthcheck')
def healthcheck():
    return jsonify({"status": "OK"})

@app.route('/summit')
def summit():
    return jsonify({"message": "I hope you are enjoying this talk"})

@app.route('/run_command', methods=['POST'])
def run_command():
    """
    SECURITY VULNERABILITY: Command Injection
    This endpoint executes shell commands from user input without validation,
    creating a command injection vulnerability.
    """
    command = request.json.get('command', '')
    # Vulnerable code: directly executing user input
    result = subprocess.check_output(command, shell=True, text=True)
    return jsonify({"result": result})

@app.route('/fetch_url', methods=['POST'])
def fetch_url():
    """
    SECURITY VULNERABILITY: Server-Side Request Forgery (SSRF)
    This endpoint makes HTTP requests to URLs provided by user input without validation,
    creating an SSRF vulnerability that could allow access to internal resources.
    """
    url = request.json.get('url', '')
    # Vulnerable code: making requests to user-provided URLs without validation
    response = requests.get(url)
    return jsonify({
        "status_code": response.status_code,
        "content": response.text[:500]  # Return first 500 chars to avoid large responses
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)