from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core.payments import find_payments, create_payment, find_payment, delete_a_payment, edit_a_payment
from src.core.auth import find_user_by_email
from src.web.handlers.auth import login_required
from src.web.handlers.users import check_permissions
from src.web.forms.PaymentForm import PaymentForm
from datetime import datetime

bp = Blueprint('payments',__name__,url_prefix="/payments")

@bp.get('/')
@check_permissions('payment_index')
@login_required
def payment_index():
    """
    Displays the list of payments with optional search filters and pagination 
    """

    # Obtener parámetros de búsqueda del formulario
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    payment_type = request.args.get('payment_type')
    order_by = request.args.get('order_by', 'asc')
    page = request.args.get('page', 1, type=int)

    all_payments, max_pages = find_payments(start_date, end_date, payment_type, order_by, page)

    return render_template("payments/show_payments.html", payments = all_payments, max_pages = max_pages, current_page=page)

@bp.get('/payment_register_form')
@check_permissions('payment_register_form')
@login_required
def payment_register_form():
    """
    Renders the payment register form page
    """
    form = PaymentForm()
    return render_template("payments/payment_register.html", form=form)

@bp.route("/payment_register", methods=["GET", "POST"])
@check_permissions('payment_register')
@login_required
def payment_register():
    """
    Register a new payment with the information of the form
    """
    
    form = PaymentForm(request.form)
    
    if request.method == "POST":
        if form.validate():
            # Crear el nuevo pago con los datos validados del formulario
            beneficiary = find_user_by_email(form.beneficiary_id.data) if form.beneficiary_id.data else None

            # Si se ingreso un beneficiario y no se encontro en la bd
            if form.beneficiary_id.data and not beneficiary:
                flash("El beneficiario no existe.", "error")
                return render_template('payments/payment_register.html', form=form)
            
            # Validar si el tipo de pago es "Honorarios" y no hay beneficiario
            if form.payment_type.data == "Honorarios" and not beneficiary:
                flash("El beneficiario es obligatorio para pagos de Honorarios.", "error")
                return render_template('payments/payment_register.html', form=form)

            new_payment = create_payment(
                amount=form.amount.data,
                payment_date=form.payment_date.data,
                payment_type=form.payment_type.data,
                description=form.description.data,
                beneficiary_id=beneficiary.email if beneficiary else None
            )

            flash("Pago registrado exitosamente")
            return redirect(url_for('payments.payment_register'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error: {error}", 'info')

    # Si el formulario tiene errores o es GET, renderizar la página con el formulario
    return render_template("payments/payment_register.html", form=form)


@bp.get('/payment_detail/<int:payment_id>')
@check_permissions('payment_show_detail')
@login_required
def payment_show_detail(payment_id):
    """
    Renders the payment detail page
    """

    #recupero payment que quiero ver 
    payment = find_payment(payment_id)

    if not payment:
        flash("El pago seleccionado no exite", "error")
        return render_template('payments/show_payments.html')
        
    #renderizo html y le mando el payment
    return render_template("payments/show_detail_payment.html", payment=payment)
    
@bp.get('edit_payment_form/<int:payment_id>')
@check_permissions('payment_edit_form') 
@login_required
def payment_edit_form(payment_id):
    """
    Renders the payment edit form page
    """
    payment = find_payment(payment_id)
    form = PaymentForm(obj=payment)

    return render_template("payments/edit_payment_form.html", payment=payment, form=form)


@bp.route('/edit_payment/<int:payment_id>', methods=["GET", "POST"])
@check_permissions('payment_edit')
@login_required
def payment_edit(payment_id):
    """
    Updates the payment given by parameter with the information of the form
    """
    # agarro el payment para el edit payment form
    payment = find_payment(payment_id)
    form = PaymentForm(request.form) 
    # validate_on_submit chequea el tipo de solicitud, en este caso que sea post  
    if request.method == 'POST':
        
        if form.validate():
        
            # Si el tipo de pago es "Honorarios", se requiere un beneficiario válido
            if form.payment_type.data == "Honorarios":
                # Verificar si el beneficiary_id es válido y no "Externo"
                if form.beneficiary_id.data == 'Externo' or not form.beneficiary_id.data:
                    flash("El beneficiario es obligatorio para pagos de Honorarios.", "error")
                    return render_template('payments/edit_payment_form.html', form=form, payment=payment)

                # Buscar el beneficiario en la base de datos
                beneficiary = find_user_by_email(form.beneficiary_id.data)
                if not beneficiary:
                    flash("El beneficiario no existe.", "error")
                    return render_template('payments/edit_payment_form.html', form=form, payment=payment)

            # Si el formulario es válido, actualizamos los datos
            payment = edit_a_payment(
                payment_id=payment_id,
                beneficiary_id=form.beneficiary_id.data,
                amount=form.amount.data,
                payment_date=form.payment_date.data,
                payment_type=form.payment_type.data,
                description=form.description.data,
            )
            
            if payment:
                flash("Datos del pago actualizado")
                return redirect(url_for('payments.payment_index'))
            else:
                flash("El pago seleccionado no existe", "error")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error: {error}", 'info')
    
    # Si el formulario tiene errores o es GET, renderizar la página con el formulario
    return render_template('payments/edit_payment_form.html', form=form, payment=payment)



   
@bp.post('/delete_payment/<int:payment_id>')#, endpoint='delete_payment')
@check_permissions('payment_delete')
@login_required
def payment_delete(payment_id):
    """
    Deletes the payment with the id given by parameter
    """

    #obtengo pago a eliminar
    payment = find_payment(payment_id)

    if not payment:
        flash("El pago seleccionado no exite", "error")
        return redirect(url_for('payments.payment_index'))
    
    delete_a_payment(payment)
    
    flash("Pago eliminado exitosamente.")
    return redirect(url_for('payments.payment_index')) 
    