
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import Optional, Any

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'

class UserPrompt(db.Model):
    __tablename__ = 'user_prompts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    prompt_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserPrompt {self.id}>'

class UserResult(db.Model):
    __tablename__ = 'user_results'
    id: int = db.Column(db.Integer, primary_key=True)
    user_id: str = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    result_json: Any = db.Column(db.JSON, nullable=False)  # JSON type can be complex, so Any is safe here
    created_at: Optional[datetime] = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserResult {self.id}>'