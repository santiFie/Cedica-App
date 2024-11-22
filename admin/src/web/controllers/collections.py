from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core.collections import (
    find_collections,
    create_collection,
    find_collection,
    delete_a_collection,
    edit_a_collection,
    find_debtors,
    calculate_debt,
)
from src.core.team_member import find_team_member_by_email
from src.web.handlers.auth import login_required
from src.core.riders_and_horsewomen import find_rider
from src.web.handlers.auth import login_required
from src.web.handlers.users import check_permissions
from src.web.forms.CollectionForm import CollectionForm
from datetime import datetime


bp = Blueprint("collections", __name__, url_prefix="/collections")


@bp.get("/")
@check_permissions("collection_index")
@login_required
def collection_index():
    """
    Displays the list of collections with optional search filters and pagination
    """

    # Get search parameters from the form
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    payment_method = request.args.get("payment_method")
    name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    order_by = request.args.get("order_by", "asc")
    page = request.args.get("page", 1, type=int)

    all_collections, max_pages = find_collections(
        start_date, end_date, payment_method, name, last_name, order_by, page
    )

    return render_template(
        "collections/show_collections.html",
        collections=all_collections,
        max_pages=max_pages,
        page=page,
    )


@bp.get("/collection_register_form")
@check_permissions("collection_register")
@login_required
def collection_register_form():
    """
    Renders the collection register form page
    """
    form = CollectionForm()
    return render_template("collections/collection_register_form.html", form=form)


@bp.route("/register_collection", methods=["GET", "POST"])
@check_permissions("collection_register")
@login_required
def collection_register():
    """
    Register a new collection with the information of the form
    """

    form = CollectionForm(request.form)

    if request.method == "POST":
        if form.validate():
            team_member = (
                find_team_member_by_email(form.team_member_id.data)
                if form.team_member_id.data
                else None
            )
            rider = find_rider(form.rider_dni.data) if form.rider_dni.data else None

            # Verify if the team member exists
            if form.team_member_id.data and not team_member:
                flash("El miembro de equipo no existe.", "error")
                return render_template(
                    "collections/collection_register_form.html", form=form
                )

            # Verify if the rider exists
            if form.rider_dni.data and not rider:
                flash("El jinete o amazona no existe.", "error")
                return render_template(
                    "collections/collection_register_form.html", form=form
                )
            
            
            try:
                # Convert the format "{month_name} de {year}" to a datetime object
                month_name, year = calculate_debt(rider.dni)[0][0].split(" de ")
            except Exception as e:
                flash("El jinete o amazona no tiene deudas", "error")
                return render_template(
                    "collections/collection_register_form.html", form=form
                )  

            # Dictionary to map month names in Spanish to month numbers
            month_mapping = {
                "Enero": 1,
                "Febrero": 2,
                "Marzo": 3,
                "Abril": 4,
                "Mayo": 5,
                "Junio": 6,
                "Julio": 7,
                "Agosto": 8,
                "Septiembre": 9,
                "Octubre": 10,
                "Noviembre": 11,
                "Diciembre": 12,
            }

            # Get the month number from the Spanish name
            month_number = month_mapping.get(month_name)

            if month_number is None:
                raise ValueError(f"Nombre de mes no válido: {month_name}")

            first_payment_date = datetime.strptime(
                f"{year}-{month_number:02d}-01", "%Y-%m-%d"
            ).date()

            if form["payment_date"].data < first_payment_date:
                flash("No posee deudas en esa fecha", "error")
                return render_template(
                    "collections/collection_register_form.html", form=form
                )

            # Create the new collection
            new_collection = create_collection(
                amount=form.amount.data,
                payment_date=form.payment_date.data,
                payment_method=form.payment_method.data,
                observations=form.observations.data,
                team_member_id=team_member.email if team_member else "",
                rider_dni=rider.dni if rider else "",
            )

            if new_collection:
                flash("Cobro registrado exitosamente")
            else:
                flash("Error al registrar el cobro", "error")
            return redirect(url_for("collections.collection_register_form"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error: {error}", "info")
    # If the form has errors or is GET, render the page with the form
    return render_template("collections/collection_register_form.html", form=form)


@bp.get("/collection_detail/<int:collection_id>")
@check_permissions("collection_show_detail")
@login_required
def collection_show_detail(collection_id):
    """
    Renders the collection detail page
    """

    collection = find_collection(collection_id)

    if not collection:
        flash("El cobro seleccionado no exite", "error")
        return render_template("collections/show_collections.html")

    # Render HTML and send the payment
    return render_template(
        "collections/show_detail_collection.html", collection=collection
    )


@bp.get("/edit_collection_form/<int:collection_id>")
@check_permissions("collection_edit_form")
@login_required
def collection_edit_form(collection_id):
    """
    Renders the collection edit form page
    """
    collection = find_collection(collection_id)
    form = CollectionForm()
    return render_template(
        "collections/edit_collection_form.html", form=form, collection=collection
    )


@bp.route("/edit_collection/<int:collection_id>", methods=["GET", "POST"])
@check_permissions("collection_edit")
@login_required
def collection_edit(collection_id):
    """
    Updates the collection given by parameter with the information of the form
    """

    collection = find_collection(collection_id)
    form = CollectionForm(request.form)

    if request.method == "POST":
        if form.validate():

            # Find the team member and rider with the validated data
            team_member = (
                find_team_member_by_email(form.team_member_id.data)
                if form.team_member_id.data
                else None
            )
            rider = find_rider(form.rider_dni.data) if form.rider_dni.data else None

            # Verify if the team member exists
            if form.team_member_id.data and not team_member:
                flash("El miembro de equipo no existe.", "error")
                return render_template(
                    "collections/edit_collection_form.html",
                    form=form,
                    collection=collection,
                )

            # Verify if the rider exists
            if form.rider_dni.data and not rider:
                flash("El jinete o amazona no existe.", "error")
                return render_template(
                    "collections/edit_collection_form.html",
                    form=form,
                    collection=collection,
                )

            # Update the collection with the form data
            updated_collection = edit_a_collection(
                collection_id=collection_id,
                rider_dni=form.rider_dni.data,
                team_member_id=team_member.email if team_member else "",
                amount=form.amount.data,
                payment_date=form.payment_date.data,
                payment_method=form.payment_method.data,
                observations=form.observations.data,
            )

            if not updated_collection:
                flash("El cobro seleccionado no existe", "error")
            else:
                flash("Datos del cobro actualizados")

            return redirect(url_for("collections.collection_index"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error: {error}", "info")

    # If the form has errors or is a GET, render the form with the errors
    return render_template(
        "collections/edit_collection_form.html", form=form, collection=collection
    )


@bp.post("/delete_collection/<int:collection_id>")
@check_permissions("collection_delete")
@login_required
def collection_delete(collection_id):
    """
    Deletes the collection with the id given by parameter
    """

    collection = find_collection(collection_id)

    if not collection:
        flash("El cobro seleccionado no exite", "error")
        return redirect(url_for("collections.collection_index"))

    delete_a_collection(collection)

    flash("Cobro eliminado exitosamente.")
    return redirect(url_for("collections.collection_index"))


@bp.get("/index_debts")
@check_permissions("collection_index_debts")
@login_required
def collection_index_debts():
    """
    Displays the list of debtors with optional search filters and pagination
    """
    # Get search parameters from the form
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    dni = request.args.get("dni")
    order_by = request.args.get("order_by", "asc")
    page = request.args.get("page", 1, type=int)

    # Find debtors
    debtors, max_pages = find_debtors(start_date, end_date, dni, order_by, page)

    return render_template(
        "collections/show_debtors.html",
        debtors=debtors,
        max_pages=max_pages,
        page=page,
    )


@bp.get("/detail_debt/<string:debtor_dni>")
@check_permissions("collection_show_detail_debt")
@login_required
def collection_show_detail_debt(debtor_dni):
    """
    Renders the debtor detail page
    """
    # Show detail of which months the rider owes
    debt_details, debtor = calculate_debt(debtor_dni)

    return render_template(
        "collections/show_debt_detail.html", debt_details=debt_details, debtor=debtor
    )
