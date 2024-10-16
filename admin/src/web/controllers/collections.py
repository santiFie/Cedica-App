from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core.collections import find_collections, create_collection, find_collection, delete_a_collection, edit_a_collection, find_debtors, calculate_debt
from src.core.team_member import find_team_member_by_email 
from src.core.riders_and_horsewomen import find_rider
from src.web.handlers.auth import login_required
from src.web.forms import CollectionForm
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
    form = CollectionForm()
    return render_template("collections/collection_register_form.html", form=form)


@bp.route('/register_collection', methods=["GET", "POST"])
@login_required
def register_collection():
    
    form = CollectionForm(request.form)
        
    if request.method == "POST" and form.validate():
        team_member = find_team_member_by_email(form.team_member_id.data) if form.team_member_id.data else None
        rider = find_rider(form.rider_dni.data) if form.rider_dni.data else None

        # Verificar si el miembro del equipo existe
        if form.team_member_id.data and not team_member:
            flash("El miembro de equipo no existe.", "error")
            return render_template('collections/collection_register_form.html', form=form)

        # Verificar si el jinete existe
        if form.rider_dni.data and not rider:
            flash("El jinete o amazona no existe.", "error")
            return render_template('collections/collection_register_form.html', form=form)

        # Crear la nueva colección
        new_collection = create_collection(
            amount=form.amount.data,
            payment_date=form.payment_date.data,
            payment_method=form.payment_method.data,
            observations=form.observations.data,
            team_member_id=team_member.email if team_member else '',
            rider_dni=rider.dni if rider else ''
        )

        flash("Cobro registrado exitosamente", "success")
        return redirect(url_for('collections.collection_register_form'))

    # Si el formulario tiene errores o es GET, renderizar la página con el formulario
    return render_template('collections/collection_register_form.html', form=form)


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
    form = CollectionForm()
    return render_template("collections/edit_collection_form.html", form=form, collection=collection)

@bp.route('/edit_collection/<int:collection_id>', methods=["GET", "POST"])
@login_required
def edit_collection(collection_id):

    collection = find_collection(collection_id)
    form = CollectionForm(request.form)

    if request.method == 'POST' and form.validate():

    # Buscar el miembro del equipo y el jinete con los datos validados
        team_member = find_team_member_by_email(form.team_member_id.data) if form.team_member_id.data else None
        rider = find_rider(form.rider_dni.data) if form.rider_dni.data else None

        # Verificar si el miembro del equipo existe
        if form.team_member_id.data and not team_member:
            flash("El miembro de equipo no existe.", "error")
            return render_template('collections/edit_collection_form.html', form=form, collection=collection)

        # Verificar si el jinete existe
        if form.rider_dni.data and not rider:
            flash("El jinete o amazona no existe.", "error")
            return render_template('collections/edit_collection_form.html', form=form, collection=collection)

        # Actualizar la colección con los datos del formulario
        updated_collection = edit_a_collection(
            collection_id=collection_id,
            rider_dni=form.rider_dni.data,
            team_member_id=team_member.email if team_member else '',
            amount=form.amount.data,
            payment_date=form.payment_date.data,
            payment_method=form.payment_method.data,
            observations=form.observations.data,
        )

        if not updated_collection:
            flash("El cobro seleccionado no existe", "error")
        else:
            flash("Datos del cobro actualizados", "success")

        return redirect(url_for('collections.index_collections'))

    # Si el formulario tiene errores o es un GET, renderiza el formulario con los errores
    return render_template('collections/edit_collection_form.html', form=form, collection=collection)



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