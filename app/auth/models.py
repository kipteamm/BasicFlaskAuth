from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from typing import Optional

from app.extensions import db

import uuid


def get_uuid():
    return str(uuid.uuid4())


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    # Authentication
    id = db.Column(db.String(128), primary_key=True, default=get_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.set_password(password)
    
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    
    
    @staticmethod
    def authenticate(email, password) -> Optional['User']:
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            return user
        
        return None
