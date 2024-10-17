from src.core import database

class HealthInsurance(database.db.Model):
    __tablename__ = "health_insurances"
    id = database.db.Column(database.db.Integer, primary_key=True, autoincrement=True)
    name = database.db.Column(database.db.String(120), nullable=False)
    team_members = database.db.relationship('TeamMember', back_populates='health_insurance')
    
    def __repr__(self):
        return self.name