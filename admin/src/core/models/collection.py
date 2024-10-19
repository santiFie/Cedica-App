from src.core import database
from datetime import datetime
from sqlalchemy.dialects.postgresql import ENUM



PaymentMethod = ENUM(
    'Efectivo',
    'Tarjeta de credito',
    'Tarjeta de debito',
    'Transferencia',
    name='payment_method_enum',
    create_type=False
)


class Collection(database.db.Model):
    __tablename__ = "collections"

    id = database.db.Column(database.db.Integer, primary_key=True, autoincrement=True)

    # rider o horsewomen que hizo el pago. 
    rider_dni = database.db.Column(database.db.String(100), database.db.ForeignKey('riders_and_horsewomen.dni'), nullable=True)
    # fecha en la que hizo el pago
    payment_date = database.db.Column(database.db.DateTime, default=datetime.now, nullable=False)
    payment_method = database.db.Column(PaymentMethod, nullable=False)
    amount = database.db.Column(database.db.Float, nullable = False)
    observations = database.db.Column(database.db.String(120), nullable=True)
    # miembro del equipo que recibe el pago
    team_member_id = database.db.Column(database.db.String(100), database.db.ForeignKey('team_members.email'), nullable=True)

    # si debe el pago
    #debt = database.db.Column(database.db.Boolean, default=True)

    # relaciones entre quien recibe el pago y quien lo hace 
    teammember = database.db.relationship('TeamMember', back_populates = 'collections' )
    rider = database.db.relationship('RiderAndHorsewoman', back_populates = 'collections' )
