from src.core import database, minio
from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM

ProfessionEnum = ENUM(
    'PSICOLOGO',
    'PSICOMOTRICISTA',
    'MEDICO',
    'FISIOTERAPEUTA',
    'TERAPEUTA_OCUPACIONAL',
    'PSICOLOGO_EDUCATIVO',
    'MAESTRO',
    'PROFESOR',
    'FONOAUDIOLOGO',
    'VETERINARIO',
    'OTRO',
    name='professionenum',
    create_type=False
)
        
JobEnum = ENUM(
    'ADMINISTRATIVO',
    'TERAPEUTA',
    'MANEJADOR',
    'ASISTENTE_DE_PISTA',
    'HERRERO',
    'VETERINARIO',
    'ENTRENADOR_DE_CABALLOS',
    'DOMADOR_DE_CABALLOS',
    'PROFESOR_DE_EQUITACION',
    'PROFESOR_DE_ENTRENAMIENTO',
    'ASISTENTE_DE_MANTENIMIENTO',
    'OTRO',
    name='jobenum',
    create_type=False
)

ConditionEnum = ENUM(
    'VOLUNTARIO',
    'PERSONAL_PAGADO',
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
    health_insurance_id = database.db.Column(database.db.Integer, database.db.ForeignKey('health_insurances.id'), nullable=False)
    asocciated_number = database.db.Column(database.db.String(120), nullable=False)

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

    def __repr__(self):
        return self.name