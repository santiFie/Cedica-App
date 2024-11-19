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
    author = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    state = db.Column(states_enum, nullable=False) 
    posted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())