from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core.collections import find_collections, create_collection, find_collection, delete_a_collection, edit_a_collection, find_debtors, calculate_debt
from src.core.team_member import find_team_member_by_email 
from src.web.handlers.auth import login_required
from src.core.riders_and_horsewomen import find_rider
from datetime import datetime


bp = Blueprint('collections',__name__,url_prefix="/collections")


@bp.get('/')
@login_required
def index_collections():

    # Obtener parámetros de búsqueda del formulario
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    payment_method = request.args.get('payment_method')
    name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    order_by = request.args.get('order_by', 'asc')
    page = request.args.get('page', 1, type=int)

    all_collections, max_pages = find_collections(start_date, end_date, payment_method, name, last_name, order_by, page)

    return render_template("collections/show_collections.html", collections = all_collections, max_pages = max_pages, current_page = page)


@bp.get('/collection_register_form')
@login_required
def collection_register_form():
    return render_template("collections/collection_register_form.html")


@bp.post('/register_collection')
@login_required
def register_collection():
        
        # Obtener los datos del formulario
        amount = request.form.get('amount')
        payment_date = request.form.get('payment_date')
        payment_method = request.form.get('payment_method')
        observations = request.form.get('observations', '')
        team_member_id = request.form.get('team_member_id')
        rider_dni = request.form.get('rider_dni')
        
        # convierto el parametro de la fecha a un datetime para poder comparar con la fecha actual
        obj_payment_date = datetime.strptime(payment_date, "%Y-%m-%d").date()

        if obj_payment_date > datetime.today().date() :
            flash("La fecha de pago no puede ser una fecha futura.", "error")
            return render_template('collections/collection_register_form.html')
        
        # chequeo si al cargar el team_member se ingresa un usuario cargado en el sistema
        if team_member_id:
            team_member = find_team_member_by_email(team_member_id)
            if not team_member:
                flash("El miembro de equipo no existe.", "error")
                return render_template('collections/collection_register_form.html')

        # chequeo si al cargar el rider se ingresa un usuario cargado en el sistema
        if rider_dni:
             rider = find_rider(rider_dni)
             if not rider:
                flash("El jinete o amazona no existe.", "error")
                return render_template('collections/collection_register_form.html')
        
        new_collection = create_collection(
             amount=amount,
             payment_date = payment_date,
             payment_method = payment_method,
             observations = observations,
             team_member_id = team_member.email,
             rider_dni = rider.dni
        )


         # Mostrar mensaje de éxito
        flash("Cobro registrado exitosamente", "success")

        # Renderiza la misma página con un mensaje de éxito o en caso de error
        return render_template("collections/collection_register_form.html")


@bp.get('/collection_detail/<int:collection_id>')
@login_required
def show_detail_collection(collection_id):
     
    collection = find_collection(collection_id)
    
    if not collection:
        flash("El cobro seleccionado no exite", "error")
        return render_template('collections/show_collections.html')
        
    #renderizo html y le mando el payment
    return render_template("collections/show_detail_collection.html", collection=collection)


@bp.get('/edit_collection_form/<int:collection_id>')
@login_required
def edit_collection_form(collection_id):
    collection = find_collection(collection_id)
    return render_template("collections/edit_collection_form.html", collection=collection)

@bp.post('/edit_collection/<int:collection_id>')
@login_required
def edit_collection(collection_id):

    collection = find_collection(collection_id)

    # para hacer el chequeo por fecha
    payment_date = request.form.get('payment_date')

    # para buscar J&A y team_member en el sistema
    rider_dni = request.form.get('rider_dni')
    team_member_id = request.form.get('team_member_id')

    # convierto el parametro de la fecha a un datetime para poder comparar con la fecha actual
    obj_payment_date = datetime.strptime(payment_date, "%Y-%m-%d").date()

    if obj_payment_date > datetime.today().date() :
        flash("La fecha de cobro no puede ser una fecha futura.", "error")
        return render_template('collectios/edit_collection_form.html', collection=collection)
    
     # chequeo si al cargar el team_member se ingresa un usuario cargado en el sistema
    if team_member_id:
        team_member = find_team_member_by_email(team_member_id)
        if not team_member:
            flash("El miembro de equipo no existe.", "error")
            return render_template('collections/edit_collection_form.html', collection=collection)

    # chequeo si al cargar el rider se ingresa un usuario cargado en el sistema
    if rider_dni:
        rider = find_rider(rider_dni)
        if not rider:
            flash("El jinete o amazona no existe.", "error")
            return render_template('collections/edit_collection_form.html', collection=collection)
        
    collection = edit_a_collection(
        collection_id=collection_id,
        rider_dni = request.form.get('rider_dni'),
        team_member_id = request.form.get('team_member_id'),
        amount = float(request.form.get('amount')),
        payment_date = request.form.get('payment_date'),
        payment_method = request.form.get('payment_method'),
        observations = request.form.get('observations', ''),

    )
    

    if not collection:
        flash("El cobro seleccionado no exite", "error")
    else:
        flash("Datos del cobro actualizado")
    return redirect(url_for('collections.index_collections'))



@bp.post('/delete_collection/<int:collection_id>')
@login_required
def delete_collection(collection_id):

    collection = find_collection(collection_id)

    if not collection:
        flash("El cobro seleccionado no exite", "error")
        return redirect(url_for('collections.index_collections'))
    
    delete_a_collection(collection)
    
    flash("Cobro eliminado exitosamente.")
    return redirect(url_for('collections.index_collections')) 


@bp.get('/index_debts')
@login_required
def index_debts():
    # obtengo parametros del filtro
    # Obtener parámetros de búsqueda del formulario
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    dni = request.args.get('dni')
    order_by = request.args.get('order_by', 'asc')
    page = request.args.get('page', 1, type=int)

    # busco deudores
    debtors, max_pages = find_debtors(start_date, end_date, dni, order_by, page)
    
    return render_template("collections/show_debtors.html", debtors=debtors, max_pages=max_pages, current_page=page)

@bp.get('/detail_debt/<string:debtor_dni>')
@login_required
def show_detail_debt(debtor_dni):
    # muestro detalle de que meses debe ese rider
    debt_details, debtor = calculate_debt(debtor_dni)

    return render_template("collections/show_debt_detail.html", debt_details=debt_details, debtor=debtor)