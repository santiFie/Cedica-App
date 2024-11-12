from flask import Blueprint, request, render_template, flash
from src.web.handlers.auth import login_required, cheack_permissions
from src.core.contact import find_contacts, find_contact, delete_contact 


bp = Blueprint("contact", __name__, url_prefix="/contacts")

@bp.get("/list_contacts")
#@cheack_permissions("contact_index")
#@login_required
def index_contacts():

    # obtener parametros de busqueda del formulario
    page = request.args.get("page", 1, type=int)
    order = request.args.get("order_by", "asc")
    state = request.args.get("state")

    contacts, max_pages = find_contacts(page=page, order=order, state=state)  

    return render_template("contacts/show_contacts.html", contacts=contacts, max_pages=max_pages, current_page=page)

@bp.get("/contact_detail/<int:contact_id>")
@cheack_permissions("contact_detail")
@login_required
def contact_show_detail(contact_id):

    contact = find_contact(contact_id)

    if not contact:
        flash("La consulta no existe", "error")
        return render_template("contacts/show_contacts.html")

    return render_template("contacts/contact_detail.html", contact=contact)


bp.post("/delete_contact/<int:contact_id>")
@cheack_permissions("contact_delete")
@login_required
def contact_delete(contact_id):

    contact = find_contact(contact_id)

    if not contact:
        flash("La consulta no existe", "error")
        return render_template("contacts/show_contacts.html")

    delete_contact(contact)

    flash("Consulta eliminada correctamente", "success")
    return render_template("contacts/show_contacts.html")