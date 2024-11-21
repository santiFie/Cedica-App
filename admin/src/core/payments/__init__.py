from src.core.database import db
from src.core.models.payment import Payment, PaymentType
from src.core.models.users import User
from datetime import datetime

def find_payments(start_date=None, end_date=None, payment_type=None, order_by='asc', page=1):
    """
    Search for all payments with the given parameters
    """
    # similar to find users
    # I will show 25 per page
    per_page = 25

    # general query, get all payments
    query = Payment.query

    # Filter by date range
    if start_date:
        query = query.filter(Payment.payment_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Payment.payment_date <= datetime.strptime(end_date, '%Y-%m-%d'))

    # Filter by payment type
    if payment_type:
        query = query.filter(Payment.payment_type == payment_type)

    # Order by payment date
    if order_by == 'asc':
        query = query.order_by(Payment.payment_date.asc())
    else:
        query = query.order_by(Payment.payment_date.desc())

    total_payments = query.count()

    # Handle the case where there are no payments
    if total_payments == 0:
        return [], 0

    max_pages = (total_payments + per_page - 1) // per_page  # Round up

    # Ensure the requested page is not less than 1
    if page < 1:
        page = 1
        
    # Ensure the requested page is not greater than the maximum number of pages
    if page > max_pages:
        page = max_pages
        
        
    offset = (page - 1) * per_page
    payments = query.offset(offset).limit(per_page).all()

    return payments, max_pages 



def create_payment(**kwargs):
    """
    Create a new payment with the given parameter
    """
    
    payment_type_str = kwargs["payment_type"]  # Capture the payment type string

    beneficiary_id = kwargs.get("beneficiary_id", None)
    
    # if there is no beneficiary because it is another type of payment, send empty
    if beneficiary_id == '':
        beneficiary_id = None

    payment = Payment(
        amount=kwargs["amount"],
        payment_date=kwargs["payment_date"],
        payment_type=payment_type_str,
        description=kwargs.get("description", ""),
        beneficiary_id=beneficiary_id
    )
    try:
        # Add the payment to the database
        db.session.add(payment)
        db.session.flush()
    except:
        db.session.rollback()
        return None
    
    db.session.commit()

    return payment


def create_enums():
    """
    Creates the enums values for payments
    """

    PaymentType.create(db.engine, checkfirst=True)


def find_payment(id):
    """
    Search for the payment by the given parameter
    """

    # retrieve payment by id
    payment = Payment.query.get(id)

    return payment


def delete_a_payment(payment):
    """
    Deletes the payment given by parameter
    """

    db.session.delete(payment)
    db.session.commit()

    return True

def edit_a_payment(**kwargs):
    """
    Updates a payment with the given parameters
    """

    # get the payment to edit
    payment = find_payment(kwargs["payment_id"])
    # if it exists, modify the data and return the updated payment
    if payment:
        beneficiary_id = kwargs.get('beneficiary_id', payment.beneficiary_id)

         # If the beneficiary is "External", assign None so the field is NULL
        if beneficiary_id == 'Externo':
            payment.beneficiary_id = None
        else:
            payment.beneficiary_id = beneficiary_id

        # check if the date is a datetime object, if not, convert it
        payment.payment_date = kwargs.get('payment_date')
        payment.amount = kwargs.get('amount', payment.amount)
        payment.payment_type = kwargs.get('payment_type', payment.payment_type)
        payment.description = kwargs.get('description', payment.description)

        db.session.commit()
        return payment
    return None


def get_payments_on_date(date):
    
    payments = Payment.query.filter(Payment.payment_date == date).all()

    return payments
