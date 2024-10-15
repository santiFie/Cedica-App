from datetime import datetime
from src.core import database
from src.core import minio
from sqlalchemy.dialects.postgresql import ARRAY
from src.core.models.team_member import TeamMember
from src.core.models.riders_and_horsewomen import proposal_enum
db = database.db


class Equestrian(db.Model):
    __tablename__ = "equestrians"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    race = db.Column(db.String(100), nullable=False)
    coat = db.Column(db.String(100), nullable=False)
    bought = db.Column(db.Boolean, nullable=False)
    date_of_entry = db.Column(db.DateTime, nullable=False)
    headquarters = db.Column(db.String(100), nullable=False)
    inserted_at = database.db.Column(database.db.DateTime, default=datetime.now())
    proposals = db.Column(ARRAY(proposal_enum), nullable=True)
    evolution_report = db.Column(db.String(100), nullable=True)
    veterinary_record = db.Column(db.String(100), nullable=True)
    training_plan = db.Column(db.String(100), nullable=True)
    images = db.Column(db.String(100), nullable=True)
    horse_sheet = db.Column(db.String(100), nullable=True)

    team_members = db.relationship(
        "TeamMember", secondary="equestrian_team_members", back_populates="equestrians"
    )

    def get_files(self):
        return [self.evolution_report, self.veterinary_record, self.training_plan, self.images, self.horse_sheet]
    
    def get_file_date(self, filename, user_id):
        prefix="ecuestres"
        return minio.get_file_date(prefix, user_id, filename)



class EquestrianTeamMember(db.Model):
    __tablename__ = "equestrian_team_members"

    equestrian_id = db.Column(
        db.Integer, db.ForeignKey("equestrians.id"), primary_key=True
    )
    team_member_id = db.Column(
        db.Integer, db.ForeignKey("team_members.id"), primary_key=True
    )

    # # Relaciones para vincular la tabla intermedia con Equestrian y TeamMember
    # equestrians = db.relationship('Equestrian', back_populates='team_members')
    # team_members = db.relationship('TeamMember', back_populates='equestrians')