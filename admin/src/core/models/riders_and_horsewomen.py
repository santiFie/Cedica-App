from src.core import database

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
#Faltan certificado discapacidad para abajo.

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
