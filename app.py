import os
import subprocess
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)