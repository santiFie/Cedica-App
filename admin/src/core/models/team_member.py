from src.core import database
from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM

ProfessionEnum = ENUM(
    'PSYCHOLOGIST',
    'PSYCHOMOTRICIAN',
    'DOCTOR',
    'PHYSIOTHERAPIST',
    'OCCUPATIONAL_THERAPIST',
    'EDUCATIONAL_PSYCHOLOGIST',
    'TEACHER',
    'PROFESSOR',
    'SPEECH_THERAPIST',
    'VETERINARIAN',
    'OTHER',
    name='professionenum',
    create_type=False
)
        
JobEnum = ENUM(
    'ADMINISTRATIVE',
    'THERAPIST',
    'DRIVER',
    'TRACK_ASSISTANT',
    'BLACKSMITH',
    'VETERINARIAN',
    'HORSE_TRAINER',
    'HORSE_TAMER',
    'EQUESTRIAN_TEACHER',
    'TRAINING_TEACHER',
    'MAINTENANCE_ASSISTANT',
    'OTHER',
    name='jobenum',
    create_type=False
)

ConditionEnum = ENUM(
    'VOLUNTEER',
    'PAID_STAFF',
    name='conditionenum',
    create_type=False
)

class TeamMember(database.db.Model):
    __tablename__ = "team_members"
    id = database.db.Column(database.db.Integer, primary_key=True, autoincrement=True)
    name = database.db.Column(database.db.String(120), nullable=False)
    last_name = database.db.Column(database.db.String(120), nullable=False)
    address = database.db.Column(database.db.String(120), nullable=False)
    email = database.db.Column(database.db.String(120), nullable=False, unique=True)
    locality = database.db.Column(database.db.String(120), nullable=False)
    phone = database.db.Column(database.db.String(120), nullable=False)
    initial_date = database.db.Column(database.db.DateTime, nullable=False)
    end_date = database.db.Column(database.db.DateTime, nullable=True, default=None)
    emergency_contact = database.db.Column(database.db.String(120), nullable=False)
    emergency_phone = database.db.Column(database.db.String(120), nullable=False)
    active = database.db.Column(database.db.Boolean, nullable=False, default=True)
    health_insurance_id = database.db.Column(database.db.Integer, database.db.ForeignKey('health_insurances.id'), nullable=False)

    condition = database.db.Column(ConditionEnum, nullable=False)
    job_position = database.db.Column(JobEnum, nullable=False)
    profession = database.db.Column(ProfessionEnum, nullable=False)
    health_insurance = database.db.relationship('HealthInsurance', back_populates='team_members')

    def __repr__(self):
        return self.name