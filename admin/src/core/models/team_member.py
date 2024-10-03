from src.core import database
from enum import Enum

class ProfessionEnum(Enum):
        PSYCHOLOGIST = "Psicólogo/a"
        PSYCHOMOTRICIAN = "Psicomotricista"
        DOCTOR = "Médico/a"
        PHYSIOTHERAPIST = "Kinesiólogo/a"
        OCCUPATIONAL_THERAPIST = "Terapista Ocupacional"
        EDUCATIONAL_PSYCHOLOGIST = "Psicopedagogo/a"
        TEACHER = "Docente"
        PROFESSOR = "Profesor"
        SPEECH_THERAPIST = "Fonoaudiólogo/a"
        VETERINARIAN = "Veterinario/a"
        OTHER = "Otro"

        def __str__(self):
            return self.value
        
class Job(Enum):
    ADMINISTRATIVE = "Administrativo/a"
    THERAPIST = "Terapeuta"
    DRIVER = "Conductor"
    TRACK_ASSISTANT = "Auxiliar de pista"
    BLACKSMITH = "Herrero"
    VETERINARIAN = "Veterinario"
    HORSE_TRAINER = "Entrenador de Caballos"
    HORSE_TAMER = "Domador"
    EQUESTRIAN_TEACHER = "Profesor de Equitación"
    TRAINING_TEACHER = "Docente de Capacitación"
    MAINTENANCE_ASSISTANT = "Auxiliar de mantenimiento"
    OTHER = "Otro"

    def __str__(self):
        return self.value
    
class Condition(Enum):
    VOLUNTEER = "Voluntario"
    PAID_STAFF = "Personal Rentado"

    def __str__(self):
        return self.value

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
    end_date = database.db.Column(database.db.DateTime, nullable=True)
    emergency_contact = database.db.Column(database.db.String(120), nullable=False)
    emergency_phone = database.db.Column(database.db.String(120), nullable=False)
    active = database.db.Column(database.db.Boolean, nullable=False, default=True)
    health_insurance_id = database.db.Column(database.db.Integer, database.db.ForeignKey('health_insurances.id'), nullable=False)

    condition = database.db.Column(database.db.Enum(Condition), nullable=False)
    job_position = database.db.Column(database.db.Enum(Job), nullable=False)
    proffesion = database.db.Column(database.db.Enum(ProfessionEnum), nullable=False)
    health_insurance = database.db.relationship('HealthInsurance', back_populates='team_members')

    def __repr__(self):
        return self.name