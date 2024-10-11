from src.core import database
from sqlalchemy.dialects.postgresql import ENUM, ARRAY


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

days_enum = ENUM(
        'LUNES',
        'MARTES',
        'MIERCOLES',
        'JUEVES',
        'VIERNES',
        'SABADO',
        'DOMINGO',
        name='days_of_week_enum',
        create_type=False
    )

condition_enum = ENUM(
    'REGULAR',
    'DE BAJA',
    name='condition_enum',
    create_type=False
)

seat_enum = ENUM( 
    'CASJ',
    'HLP',
    'OTRO',
    name='seat_enum',
    create_type= False
)

proposal_enum = ENUM(
    'Hipoterapia',
    'Monta Terapeutica',
    'Deporte Ecuestre Adaptado',
    'Actividades Recreativas',
    'Equitacion',
    name='proposal_enum',
    create_type= False
)


education_level_enum = ENUM(
    'Primario',
    'Secundario',
    'Terciario',
    'Universitario',
    name= 'education_level_enum',
    create_type= False
)

class RiderAndHorsewoman(database.db.Model):
    __tablename__ = 'riders_and_horsewomen'
    id = database.db.Column(database.db.Integer, primary_key=True, autoincrement=True)
    dni = database.db.Column(database.db.String(8), unique=True)
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
    tutors = database.db.relationship('Tutor', back_populates='rider_and_horsewoman')
    institution = database.db.relationship('WorkInInstitution', secondary= 'riders_horsewomen_institution', back_populates='riders_and_horsewomen')

class WorkInInstitution(database.db.Model):
    __tablename__ = 'work_in_institutions'
    id = database.db.Column(database.db.Integer, primary_key=True, autoincrement=True)
    proposal = database.db.Column(proposal_enum, nullable=False)
    condition= database.db.Column(condition_enum, nullable=False)
    seat = database.db.Column(seat_enum, nullable=False)
    therapist = database.db.Column(database.db.BigInteger, database.db.ForeignKey('team_members.id'), nullable=False )
    rider = database.db.Column(database.db.BigInteger, database.db.ForeignKey('team_members.id'), nullable=False )
    horse = database.db.Column(database.db.BigInteger, database.db.ForeignKey('equestrians.id'), nullable=False )
    track_assistant= database.db.Column(database.db.BigInteger, database.db.ForeignKey('team_members.id'), nullable=False )
    days = database.db.Column(ARRAY(days_enum), nullable=False)
    riders_horsewoman = database.db.relationship('RiderAndHorsewoman', secondary= 'riders_horsewomen_institution', back_populates='work_in_institutions')

class RiderHorsewomanInstitution(database.db.Model):
    __tablename__ = 'riders_horsewomen_institution'
    rider_horsewoman = database.db.Column(database.db.BigInteger, database.db.ForeignKey('riders_and_horsewomen.id'), primary_key=True, nullable=False )
    institution = database.db.Column(database.db.BigInteger, database.db.ForeignKey('work_in_institutions.id'), primary_key=True, nullable=False )


class Tutor(database.db.Model):
    __tablename__ = 'tutors'
    id = database.db.Column(database.db.Integer, primary_key=True, autoincrement=True)
    dni = database.db.Column(database.db.String(8), nullable=False)
    relationship = database.db.Column(database.db.String(120), nullable=False)
    name = database.db.Column(database.db.String(120), nullable=False)
    address = database.db.Column(database.db.String(120), nullable=False)
    phone = database.db.Column(database.db.String(13), nullable=False)
    email = database.db.Column(database.db.String(120), nullable=False)
    education_level = database.db.Column(education_level_enum, nullable=False)
    occupation = database.db.Column(database.db.String(120), nullable=False)
    rider_and_horsewoman_id = database.db.Column(database.db.BigInteger, database.db.ForeignKey('riders_and_horsewomen.id'), nullable=False)
    rider_and_horsewoman = database.db.relationship('RiderAndHorsewoman', back_populates='tutors')
