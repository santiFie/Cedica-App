from src.core import database
from sqlalchemy.dialects.postgresql import ARRAY

db = database.db

class Equestrian(database.Model):
    __tablename__ = 'equestrian'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    race = db.Column(db.String(100), nullable=False)
    coat = db.Column(db.String(100), nullable=False)
    bought = db.Column(db.Boolean, nullable=False)
    date_of_entry = db.Column(db.DateTime, nullable=False)
    headquarters  = db.Column(db.String(100), nullable=False)

    #job_in_institution = db.Column(ARRAY(job_in_institution_enum), nullable=False)

    team_member = db.relationship('TeamMember', secondary="equestrian_team_members", back_populates='equestrians')

class EquestrianTeamMember(database.Model):
    __tablename__ = 'equestrian_team_members'

    equestrian_id = db.Column(db.Integer, db.ForeignKey('equestrian.id'), primary_key=True)
    team_member_id = db.Column(db.Integer, db.ForeignKey('team_member.id'), primary_key=True)

    # Relaciones para vincular la tabla intermedia con Equestrian y TeamMember
    equestrian = db.relationship('Equestrian', back_populates='team_members')
    team_member = db.relationship('TeamMember', back_populates='equestrians')