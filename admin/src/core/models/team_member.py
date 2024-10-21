from src.core import database, minio
from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime


ProfessionEnum = ENUM(
    'Psicologo',
    'Psicomotricista',
    'Medico',
    'Fisioterapeuta',
    'Terapeuta ocupacional',
    'Psicologoeducativo',
    'Maestro',
    'Profesor',
    'Fonoaudiologo',
    'Veterinario',
    'Otro',
    name='professionenum',
    create_type=False
)
        
JobEnum = ENUM(
    'Administrativo',
    'Terapeuta',
    'Manejador',
    'Asistente de pista',
    'Herrero',
    'Veterinario',
    'Entrenador de caballos',
    'Domador de caballos',
    'Profesor de equitacion',
    'Profesor de entrenamiento',
    'Asistente de mantenimiento',
    'Otro',
    name='jobenum',
    create_type=False
)

ConditionEnum = ENUM(
    'Voluntario',
    'Personal pagado',
    name='conditionenum',
    create_type=False
)

class TeamMember(database.db.Model):
    __tablename__ = "team_members"
    id = database.db.Column(database.db.Integer, primary_key=True, autoincrement=True)
    name = database.db.Column(database.db.String(120), nullable=False)
    last_name = database.db.Column(database.db.String(120), nullable=False)
    dni = database.db.Column(database.db.String(8), unique=True)
    address = database.db.Column(database.db.String(120), nullable=False)
    email = database.db.Column(database.db.String(120), nullable=False, unique=True)
    locality = database.db.Column(database.db.String(120), nullable=False)
    phone = database.db.Column(database.db.String(120), nullable=False)
    initial_date = database.db.Column(database.db.DateTime, nullable=False)
    end_date = database.db.Column(database.db.DateTime, nullable=True, default=None)
    emergency_contact = database.db.Column(database.db.String(120), nullable=False)
    emergency_phone = database.db.Column(database.db.String(120), nullable=False)
    active = database.db.Column(database.db.Boolean, nullable=False, default=True)
    inserted_at = database.db.Column(database.db.DateTime, default=datetime.now())
    health_insurance_id = database.db.Column(database.db.Integer, database.db.ForeignKey('health_insurances.id'), nullable=False)
    associated_number = database.db.Column(database.db.String(120), nullable=False)

    ##Archivos
    
    title = database.db.Column(database.db.String(100), nullable=True)
    dni_copy = database.db.Column(database.db.String(100), nullable=True)
    cv = database.db.Column(database.db.String(100), nullable=True)


    def get_files(self):
        return [self.title, self.dni_copy, self.cv]
    
    def get_file_date(self, filename, user_id):
        prefix="team_members"
        return minio.get_file_date(prefix, user_id, filename)

    condition = database.db.Column(ConditionEnum, nullable=False)
    job_position = database.db.Column(JobEnum, nullable=False)
    profession = database.db.Column(ProfessionEnum, nullable=False)
    health_insurance = database.db.relationship('HealthInsurance', back_populates='team_members')
    equestrians = database.db.relationship('Equestrian', secondary='equestrian_team_members', back_populates='team_members')

    # relacion con Collection
    collections = database.db.relationship('Collection', back_populates='teammember')

    riders_and_horsewomen = database.db.relationship('RiderAndHorsewoman', secondary='caring_professionals', back_populates='team_members')

    def __repr__(self):
        return self.name