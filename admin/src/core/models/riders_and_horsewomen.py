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
    create_type=False
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

# nombre del modelo dudas plural?
class RidersAndHorsewoman(database.db.Model):
    __tablename__ = 'riders_and_horsewomens'
    dni = database.db.Column(database.db.String(8), primary_key=True)
    name = database.db.Column(database.db.String(120), nullable=False)
    age = database.db.Column(database.db.Integer(2), nullable=False)
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

class WorkInInstitution(database.db.Model):
    __tablename__ = 'work_in_institutions'
    proposal = database.db.Column(database.db.String(120), nullable=False)
    condition = database.db.Column(database.db.String(120), nullable=False)
    seat = database.db.Column(database.db.String(120), nullable=False)
    #day = 
    #therapist = 
    #rider =
    #horse =
    #track_assistant=
