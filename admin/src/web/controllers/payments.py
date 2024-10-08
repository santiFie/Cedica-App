from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core.payments import find_payments, create_payment
from datetime import datetime

bp = Blueprint('payments',__name__,url_prefix="/payments")

@bp.get('/')
def index_payments():

    # Obtener parámetros de búsqueda del formulario
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    payment_type = request.args.get('payment_type')
    order_by = request.args.get('order_by', 'asc')
    page = request.args.get('page', 1, type=int)

    all_payments, max_pages = find_payments(start_date, end_date, payment_type, order_by, page)

    return render_template("payments/show_payments.html", payments = all_payments, max_pages = max_pages, current_page=page)

@bp.get('/payment_register_form')
def payment_register_form():
    return render_template("payments/payment_register.html")

@bp.route("/payment_register", methods=["GET", "POST"])
def payment_register():

    if request.method == "POST":
        # Obtener los datos del formulario
        amount = request.form.get('amount')
        payment_date = request.form.get('payment_date')
        payment_type = request.form.get('payment_type')
        description = request.form.get('description', '')
        beneficiary_id = request.form.get('beneficiary_id')  # Este campo puede ser opcional

        if not amount or not payment_type or not payment_date:
            flash("Todos los campos obligatorios deben ser completados", "error")
            return redirect(url_for('payments.payment_form'))  # Redirige al formulario si faltan datos
        
        # convierto el parametro de la fecha a un datetime para poder comparar con la fecha actual
        obj_payment_date = datetime.strptime(payment_date, "%Y-%m-%d").date()

        if obj_payment_date > datetime.today().date() :
            flash("La fecha de pago no puede ser una fecha futura.", "error")
            return render_template('payments/payment_register.html')

        new_payment = create_payment(amount = amount,
                                     payment_date = payment_date,
                                     payment_type = payment_type,
                                     description = description,
                                     beneficiary_id = beneficiary_id)

    # Mostrar mensaje de éxito
    flash("Pago registrado exitosamente", "success")

    # Renderiza la misma página con un mensaje de éxito o en caso de error
    return render_template("payments/payment_register.html")



    
   
    