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
    create_type=False
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
    create_type=False
)

# nombre del modelo dudas plural? mal declarado
class RiderAndHorsewoman(database.db.Model):
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
    scholarship_percentage = database.db.Column(database.db.String(2), nullable=True)
    observations = database.db.Column(database.db.String(120), nullable=True)
    disability_certificate = database.db.Column(disability_certificate_enum, nullable=True, default=None)
    others = database.db.Column(database.db.String(120), nullable=True)
    disability_type = database.db.Column(disability_type_enum, nullable=False)
    family_allowance = database.db.Column(family_allowance_enum, nullable= True, default= None)
    pension = database.db.Column(pension_enum, nullable= True, default= None)
    name_institution = database.db.Column(database.db.String(120), nullable=False)
    address_institution = database.db.Column(database.db.String(120), nullable=False)
    phone_institution = database.db.Column(database.db.String(13), nullable=False)
    current_grade = database.db.Column(database.db.String(2), nullable=False)
    observations_institution = database.db.Column(database.db.String(120), nullable=True)

    tutors = database.db.relationship('Tutor', back_poulates='rider_and_horsewomen')

class Tutor(database.db.Model):
    __tablename__ = 'tutors'
    dni = database.db.Column(database.db.String(8), nullable=False)
    relationship = database.db.Column(database.db.String(120), nullable=False)
    name = database.db.Column(database.db.String(120), nullable=False)
    address = database.db.Column(database.db.String(120), nullable=False)
    phone = database.db.Column(database.db.String(13), nullable=False)
    email = database.db.Column(database.db.String(120), nullable=False)
    education_level = database.db.Column(database.db.String(120), nullable=False)
    occupation = database.db.Column(database.db.String(120), nullable=False)

    rider_and_horsewoman_id = database.db.Column(database.db.Integer, database.db.ForeignKey('riders_and_horsewomens'), nullable=False)

    # Relación con el modelo User
    #riders_and_horsewoman = database.db.relationship('RidersAndHorsewoman', backref=database.db.backref('tutors', lazy=True))
    rider_and_horsewoman = database.db.relationship('RiderAndHorsewoman', back_populates='tutors')


# class WorkInInstitution(database.db.Model):
#     __tablename__ = 'work_in_institutions'
#     proposal = database.db.Column(database.db.String(120), nullable=False)
#     condition = database.db.Column(database.db.String(120), nullable=False)
#     seat = database.db.Column(database.db.String(120), nullable=False)
#     #therapist = clave foranea
#     #rider = clave foranea
#     #horse = clave foranea
#     #track_assistant= clave foranea

#     days =
