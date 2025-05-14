import os
from flask import Flask, jsonify

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)