from datetime import datetime
from src.core import database

class User(database.db.Model):
    __tablename__ = "users"
    email = database.db.Column(database.db.String(120), primary_key=True)
    nickname = database.db.Column(database.db.String(120), nullable=False)
    password = database.db.Column(database.db.String(120), nullable=False)
    active = database.db.Column(database.db.Boolean, default=True)
    system_admin = database.db.Column(database.db.Boolean, default=False)
    role_id = database.db.Column(database.db.BigInteger, database.db.ForeignKey('roles.id'), nullable=True)
    inserted_at = database.db.Column(database.db.DateTime, default=datetime.now())
    updated_at = database.db.Column(database.db.DateTime, default=datetime.now(), onupdate=datetime.now())
    
    # Relación con roles
    role = database.db.relationship('Role', back_populates='users')

    # Relación con pagos
    payments = database.db.relationship('Payment', back_populates='beneficiary')


# Modelo Role
class Role(database.db.Model):
    __tablename__ = 'roles'
    
    id = database.db.Column(database.db.BigInteger, primary_key=True)
    name = database.db.Column(database.db.String, nullable=False)
    
    # Relación con usuarios
    users = database.db.relationship('User', back_populates='role')
    
    # Relación con permisos a través de RolePermission
    permissions = database.db.relationship('Permission', secondary='role_permissions', back_populates='roles')


# Modelo Permission
class Permission(database.db.Model):
    __tablename__ = 'permissions'
    
    id = database.db.Column(database.db.BigInteger, primary_key=True)
    name = database.db.Column(database.db.String, nullable=False)
    
    # Relación con roles a través de RolePermission
    roles = database.db.relationship('Role', secondary='role_permissions', back_populates='permissions')


# Modelo RolePermission (Tabla intermedia)
class RolePermission(database.db.Model):
    __tablename__ = 'role_permissions'
    
    role_id = database.db.Column(database.db.BigInteger, database.db.ForeignKey('roles.id'), primary_key=True)
    permission_id = database.db.Column(database.db.BigInteger, database.db.ForeignKey('permissions.id'), primary_key=True)