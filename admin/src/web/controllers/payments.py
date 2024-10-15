from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core.payments import find_payments, create_payment, find_payment, delete_a_payment, edit_a_payment
from src.core.auth import find_user_by_email
from src.web.handlers.auth import login_required
from datetime import datetime

bp = Blueprint('payments',__name__,url_prefix="/payments")

@bp.get('/')
@login_required
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
@login_required
def payment_register_form():
    return render_template("payments/payment_register.html")

@bp.route("/payment_register", methods=["GET", "POST"])
@login_required
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
        
        # chequeo si al cargar el beneficiario se ingresa un usuario cargado en el sistema
        if beneficiary_id:
            beneficiary = find_user_by_email(beneficiary_id)
            if not beneficiary:
                flash("El beneficiario no existe.", "error")
                return render_template('payments/payment_register.html')

        new_payment = create_payment(amount = amount,
                                     payment_date = payment_date,
                                     payment_type = payment_type,
                                     description = description,
                                     beneficiary_id = beneficiary.email if beneficiary else '')

    # Mostrar mensaje de éxito
    flash("Pago registrado exitosamente", "success")

    # Renderiza la misma página con un mensaje de éxito o en caso de error
    return render_template("payments/payment_register.html")


@bp.get('/payment_detail/<int:payment_id>')
@login_required
def show_detail_payment(payment_id):

    #recupero payment que quiero ver 
    payment = find_payment(payment_id)

    if not payment:
        flash("El pago seleccionado no exite", "error")
        return render_template('payments/show_payments.html')
        
    #renderizo html y le mando el payment
    return render_template("payments/show_detail_payment.html", payment=payment)
    
@bp.get('edit_payment_form/<int:payment_id>')
@login_required
def edit_payment_form(payment_id):
    payment = find_payment(payment_id)
    return render_template("payments/edit_payment_form.html", payment=payment)


@bp.post('/edit_payment/<int:payment_id>')
@login_required
def edit_payment(payment_id):
    print(payment_id)
    # agarro el payment para el edit payment form
    payment = find_payment(payment_id)

    # agarro fecha para hacer chequeo de fecha futura
    payment_date = request.form.get('payment_date')
    beneficiary_id = request.form.get('beneficiary_id')

    # convierto el parametro de la fecha a un datetime para poder comparar con la fecha actual
    obj_payment_date = datetime.strptime(payment_date, "%Y-%m-%d").date()

    if obj_payment_date > datetime.today().date() :
        flash("La fecha de pago no puede ser una fecha futura.", "error")
        return render_template('payments/edit_payment_form.html', payment=payment)
    
    # chequeo si al cambiar el beneficiario se ingresa un usuario cargado en el sistema
    if beneficiary_id:
            beneficiary = find_user_by_email(beneficiary_id)
            if not beneficiary:
                flash("El beneficiario no existe.", "error")
                return render_template('payments/edit_payment_form.html', payment=payment)
    
    payment = edit_a_payment(
        payment_id=payment_id,
        beneficiary_id = request.form.get('beneficiary_id'),
        amount = float(request.form.get('amount')),
        payment_date = request.form.get('payment_date'),
        payment_type = request.form.get('payment_type'),
        description = request.form.get('description', ''),
    )

    if not payment:
        flash("El pago seleccionado no exite", "error")
    else:
        flash("Datos del pago actualizado")
    return redirect(url_for('payments.index_payments'))



   
@bp.post('/delete_payment/<int:payment_id>', endpoint='delete_payment')
@login_required
def delete_payment(payment_id):

    #obtengo pago a eliminar
    payment = find_payment(payment_id)

    if not payment:
        flash("El pago seleccionado no exite", "error")
        return redirect(url_for('payments.index_payments'))
    
    delete_a_payment(payment)
    
    flash("Pago eliminado exitosamente.")
    return redirect(url_for('payments.index_payments')) 
    