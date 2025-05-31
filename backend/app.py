from flask import Flask
from flask_cors import CORS
from backend.routes.summaries import summaries_bp
from backend.routes.chat import chat_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(summaries_bp)
app.register_blueprint(chat_bp)

@app.route("/api/test")
def test():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
