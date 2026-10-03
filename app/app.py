from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """Hello from Docker, by Sam!

Application: Flask
Environment: Docker
Status: Running
Version: 1.0"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
