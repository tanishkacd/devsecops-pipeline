from flask import Flask, jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "DevSecOps Pipeline Demo App",
        "status": "running",
        "timestamp": str(datetime.datetime.now())
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/version')
def version():
    return jsonify({"version": "1.0.0"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
