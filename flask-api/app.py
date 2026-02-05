from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/status")
def status():
    return jsonify({
        "service": "Flask API",
        "status": "running"
    })

if __name__ == "__main__":
    app.run(debug=True)
