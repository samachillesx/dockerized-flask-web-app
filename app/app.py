# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return """Hello from Docker, by Sam!

# Application: Flask
# Environment: Docker
# Status: Running
# Version: 1.0"""

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)


import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    app_env = os.getenv("APP_ENV", "development")
    return f"""Hello from Docker, by Sam Achilles!

Application: Flask
Environment: {app_env}
Status: Running
Version: 1.0"""

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)