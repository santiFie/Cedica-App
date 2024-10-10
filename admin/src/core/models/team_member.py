from src.core import database

class TeamMember(database.db.Model):
    __tablename__ = "team_members"
    id = database.db.Column(database.db.Integer, primary_key=True, autoincrement=True)
    name = database.db.Column(database.db.String(120), nullable=False)
    last_name = database.db.Column(database.db.String(120), nullable=False)
    address = database.db.Column(database.db.String(120), nullable=False)
    email = database.db.Column(database.db.String(120), nullable=False, unique=True)
    locality = database.db.Column(database.db.String(120), nullable=False)
    phone = database.db.Column(database.db.String(120), nullable=False)
    proffesion = database.db.Column(database.db.String(120), nullable=False)
    job_position = database.db.Column(database.db.String(120), nullable=False)
    initial_date = database.db.Column(database.db.DateTime, nullable=False)
    end_date = database.db.Column(database.db.DateTime, nullable=True)
    emergency_contact = database.db.Column(database.db.String(120), nullable=False)
    emergency_phone = database.db.Column(database.db.String(120), nullable=False)
    condition = database.db.Column(database.db.String(120), nullable=False)
    active = database.db.Column(database.db.Boolean, nullable=False, default=True)
    health_insurance_id = database.db.Column(database.db.Integer, database.db.ForeignKey('health_insurances.id'), nullable=False)

    health_insurance = database.db.relationship('HealthInsurance', back_populates='team_members')
    equestrians = database.db.relationship('Equestrian', secondary='equestrian_team_members', back_populates='team_members')

    def __repr__(self):
        return self.name