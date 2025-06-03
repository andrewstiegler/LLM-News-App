from flask import Flask
from flask_cors import CORS
from backend.routes.summaries import summaries_bp
from backend.routes.chat import chat_bp
from backend.utils.config import POSTGRES_URL
from backend.models import db
from backend.routes.pipeline import pipeline_bp

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with app
db.init_app(app)

print(f"🔌 Connected to DB: {app.config['SQLALCHEMY_DATABASE_URI']}")

app.register_blueprint(summaries_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(pipeline_bp)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)