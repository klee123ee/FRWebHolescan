from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class OperLog(db.Model):
    oper_id = db.Column(db.Integer, primary_key=True)
    oper_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    oper_type = db.Column(db.String(50), nullable=False)
    oper_content = db.Column(db.String(255), nullable=False)
    oper_ip = db.Column(db.String(50), nullable=False)
    oper_status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)