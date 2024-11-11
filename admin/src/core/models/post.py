from datetime import datetime
from src.core.database import db
from sqlalchemy.dialects.postgresql import ENUM


states_enum = ENUM(
    'Borrador',
    'Publicado',
    'Archivado',
    name='states_enum',
    create_type=False
)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255), nullable=False)  # Mail from the user that made the post
    summary = db.Column(db.String(255), nullable=False)
    state = db.Column(states_enum, nullable=False)  # Consider using an Enum for state
    posted_at = db.Column(db.DateTime, nullable=False) # Preguntar si es igual a la fecha DE CREACción
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())