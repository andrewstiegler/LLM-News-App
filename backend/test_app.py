from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/test")
def test():
    return jsonify({"message": "Test route working!"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
