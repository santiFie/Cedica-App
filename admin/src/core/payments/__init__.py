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


def find_payment(id):

    # recupero pago por id
    payment = Payment.query.get(id)

    return payment


def delete_a_payment(payment):

    db.session.delete(payment)
    db.session.commit()

    return True

def edit_a_payment(**kwargs):

    # agarro el payment a editar
    payment = find_payment(kwargs["payment_id"])
    print(payment)
    # si existe modifico los datos y devuelvo el payment actualizado
    if payment:
        beneficiary_id = kwargs.get('beneficiary_id', payment.beneficiary_id)

         # Si el beneficiario es "Externo", asignar None para que el campo sea NULL
        if beneficiary_id == 'Externo':
            payment.beneficiary_id = None
        else:
            payment.beneficiary_id = beneficiary_id

        # chequeo si la fecha es un objeto datetime, si no lo es, convertirla
        payment.payment_date = kwargs.get('payment_date')
        payment.amount = kwargs.get('amount', payment.amount)
        payment.payment_type = kwargs.get('payment_type', payment.payment_type)
        payment.description = kwargs.get('description', payment.description)

        db.session.commit()
        return payment
    return None
