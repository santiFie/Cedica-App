from datetime import datetime
from src.core import database

class User(database.db.Model):
    __tablename__ = "users"
    email = database.db.Column(database.db.String(120), primary_key=True)
    nickname = database.db.Column(database.db.String(120), nullable=False)
    password = database.db.Column(database.db.String(120), nullable=False)
    active = database.db.Column(database.db.Boolean, default=True)
    system_admin = database.db.Column(database.db.Boolean, default=False)
    #role_id = database.db.Column(database.db.Integer, database.db.ForeignKey("role.id"), default=1)
    iserted_at = database.db.Column(database.db.DateTime, default=datetime.now())
    updated_at = database.db.Column(database.db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return f"<Usuario {self.email}>"
