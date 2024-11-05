from datetime import datetime
from src.core.database import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255), nullable=False)  # Mail from the user that made the post
    summary = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(50), nullable=False)  # Consider using an Enum for state
    posted_at = db.Column(db.DateTime, nullable=False) # Preguntar si es igual a la fecha DE CREACción
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())