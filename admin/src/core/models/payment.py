from src.core import database
from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM



PaymentType = ENUM (
    'Honorarios',
    'Proveedor',
    'Gastos varios',
    name = 'payment_type_enum',
    create_type = False

)

class Payment(database.db.Model):
    __tablename__ = "payments"

    id = database.db.Column(database.db.Integer, primary_key=True, autoincrement=True)
    
    # si es un beneficiario, osea que trabaja en cedica, apunta a los usuarios del sistema. Los pagos pueden ser a cosas externas tambien
    beneficiary_id = database.db.Column(database.db.String(120), database.db.ForeignKey('users.email'), nullable=True)
    amount = database.db.Column(database.db.Float, nullable = False)
    payment_date = database.db.Column(database.db.DateTime, default=datetime.now, nullable=False)
    payment_type = database.db.Column(PaymentType, nullable=False)
    description = database.db.Column(database.db.String(200), nullable = True)

    # relacione del pago con el beneficiario
    beneficiary = database.db.relationship('User', back_populates = 'payments' )

