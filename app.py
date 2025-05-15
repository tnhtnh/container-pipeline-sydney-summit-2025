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

@app.route('/ping', methods=['GET'])
def ping():
    """
    Insecure endpoint that executes a ping command with user-provided input.
    This creates a command injection vulnerability.
    """
    hostname = request.args.get('hostname', 'localhost')
    # SECURITY VULNERABILITY: Direct use of user input in shell command
    try:
        output = subprocess.check_output(f"ping -c 1 {hostname}", shell=True)
        return jsonify({"output": output.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)