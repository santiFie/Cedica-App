from src.core.database import db
from src.core.models.payment import Payment, PaymentType
from src.core.models.users import User
from datetime import datetime

def find_payments(start_date=None, end_date=None, payment_type=None, order_by='asc', page=1):
    # similar a find users
    # voy a mostrar 25 por pagina
    per_page = 25

    #consulta general, agarro todos los payments
    query = Payment.query

    # Filtro por rango de fechas
    if start_date:
        query = query.filter(Payment.payment_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Payment.payment_date <= datetime.strptime(end_date, '%Y-%m-%d'))

    # Filtro por tipo de pago
    if payment_type:
        query = query.filter(Payment.payment_type == payment_type)

    # Ordeno por fecha de pago
    if order_by == 'asc':
        query = query.order_by(Payment.payment_date.asc())
    else:
        query = query.order_by(Payment.payment_date.desc())

    total_payments = query.count()

    # Manejo del caso en el que no haya pagos
    if total_payments == 0:
        return [], 0

    max_pages = (total_payments + per_page - 1) // per_page  # Redondeo hacia arriba

    # Aseguramos que la página solicitada no sea menor que 1
    if page < 1:
        page = 1
        
    # Aseguramos que la página solicitada no sea mayor que el número máximo de páginas
    if page > max_pages:
        page = max_pages
        
        
    offset = (page - 1) * per_page
    payments = query.offset(offset).limit(per_page).all()

    return payments, max_pages 



def create_payment(**kwargs):
    """
     Crea un nuevo Payment con los parámetros dados
    """
    
    payment_type_str = kwargs["payment_type"]  # Captura el string del tipo de pago

    beneficiary_id = kwargs.get("beneficiary_id", None)
    
    # si no hay beneficiario por que es otro tipo de pago, le mando vacio
    if beneficiary_id == '':
        beneficiary_id = None
    else:
        # Verificar si el beneficiario existe
        if not User.query.filter_by(email=beneficiary_id).first():
            raise ValueError("El beneficiario no existe en la base de datos.")

    payment = Payment(
        amount=kwargs["amount"],
        payment_date=kwargs["payment_date"],
        payment_type=payment_type_str,
        description=kwargs.get("description", ""),
        beneficiary_id=beneficiary_id
    )

    # Agregar el pago a la base de datos
    db.session.add(payment)
    db.session.commit()

    return payment


def create_enums():
   # from src.core.models.payment import PaymentType

    PaymentType.create(db.engine, checkfirst=True)
