from src.core import database
from sqlalchemy.dialects.postgresql import ENUM


disability_certificate_enum = ENUM(
    'ECNE', 
    'Lesión post-traumática', 
    'Mielomeningocele', 
    'Esclerosis Múltiple', 
    'Escoliosis Leve', 
    'Secuelas de ACV', 
    'Discapacidad Intelectual', 
    'Trastorno del Espectro Autista', 
    'Trastorno del Aprendizaje', 
    'Trastorno por Déficit de Atención/Hiperactividad', 
    'Trastorno de la Comunicación', 
    'Trastorno de Ansiedad', 
    'Síndrome de Down', 
    'Retraso Madurativo', 
    'Psicosis',     
    'Trastorno de Conducta', 
    'Trastornos del ánimo y afectivos', 
    'Trastorno Alimentario', 
    'OTRO',
    name='disability_certificate_enum',
    create_type=False  # Para no crear el tipo si ya existe
)

disability_type_enum= ENUM(
    'Mental',
    'Motora',
    'Sensorial',
    'Visceral',
    name='disability_type_enum',
    create_type= False
)

#Asignacion familiar
family_allowance_enum= ENUM( 
    'Asignación Universal por hijo',
    'Asignación Universal por hijo con Discapacidad',
    'Asignación por ayuda escolar anual',
    name='family_allowance_enum',
    create_type= False
)

pension_enum= ENUM(
    'Provincial',
    'Nacional',
    name='pension_enum',
    create_type= False
)

# Definimos el ENUM para los días de la semana
days_enum = ENUM(
    'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo',
    name='days_of_week_enum',  # Nombre del tipo ENUM en PostgreSQL
    create_type=False  # Creamos el tipo si no existe
)

# nombre del modelo dudas plural?
class RidersAndHorsewoman(database.db.Model):
    __tablename__ = 'riders_and_horsewomens'
    dni = database.db.Column(database.db.String(8), primary_key=True)
    name = database.db.Column(database.db.String(120), nullable=False)
    age = database.db.Column(database.db.Integer, nullable=False)
    date_of_birth = database.db.Column(database.db.Date, nullable=False)
    place_of_birth = database.db.Column(database.db.String(120), nullable=False)
    address = database.db.Column(database.db.String(120), nullable=False)
    phone = database.db.Column(database.db.String(13), nullable=False)
    emergency_contact = database.db.Column(database.db.String(120), nullable=False)
    emergency_phone = database.db.Column(database.db.String(13), nullable=False)
    scholarship = database.db.Column(database.db.Boolean, nullable=False)
    observations = database.db.Column(database.db.String(120), nullable=True)
    disability_certificate = database.db.Column(disability_certificate_enum, nullable=True, default=None)
    others = database.db.Column(database.db.String(120), nullable=True)
    disability_type = database.db.Column(disability_type_enum, nullable=False)
    family_allowance = database.db.Column(family_allowance_enum, nullable= True, default= None)
    pension = database.db.Column(pension_enum, nullable= True, default= None)

class Tutor(database.db.Model):
    __tablename__ = 'tutors'
    dni = database.db.Column(database.db.String(8), primary_key=True)
    relationship = database.db.Column(database.db.String(120), nullable=False)
    name = database.db.Column(database.db.String(120), nullable=False)
    address = database.db.Column(database.db.String(120), nullable=False)
    phone = database.db.Column(database.db.String(13), nullable=False)
    email = database.db.Column(database.db.String(120), nullable=False)
    education_level = database.db.Column(database.db.String(120), nullable=False)
    occupation = database.db.Column(database.db.String(120), nullable=False)

#tabla intermedia entre tutor y jinetes

# class WorkDays(database.db.Model):
#     __tablename__ = 'work_days'

#     day = database.db.Column(days_enum, nullable=False, primary_key=True)
#     work_in_institution_id = database.db.Column(database.db.BigInteger, database.db.ForeignKey('work_in_institutions.id'), nullable=False, primary_key=True)

# class WorkInInstitution(database.db.Model):
#     __tablename__ = 'work_in_institutions'
#     proposal = database.db.Column(database.db.String(120), nullable=False)
#     condition = database.db.Column(database.db.String(120), nullable=False)
#     seat = database.db.Column(database.db.String(120), nullable=False)
#     #therapist = 
#     #rider =
#     #horse =
#     #track_assistant=

#     # Relación many-to-many con los días
#     days = database.db.relationship('Day', secondary=WorkDays, back_populates='tasks')
