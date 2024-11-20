from flask import Blueprint, request, render_template, flash, redirect, url_for
from src.web.handlers.auth import login_required
from src.web.handlers.users import check_permissions
from src.core.contact import find_contacts, find_contact, delete_contact, block, add_comment


bp = Blueprint("contacts", __name__, url_prefix="/contacts")

@bp.get("/")
@check_permissions("contact_index")
@login_required
def contacts_index():

    # obtener parametros de busqueda del formulario
    page = request.args.get("page", 1, type=int)
    order = request.args.get("order", "asc")
    state = request.args.get("state")

    contacts, max_pages = find_contacts(page=page, order=order, state=state)  

    return render_template("contacts/show_contacts.html", contacts=contacts, max_pages=max_pages, current_page=page)

@bp.get("/contact_detail/<int:contact_id>")
@check_permissions("contact_detail")
@login_required
def contact_show_detail(contact_id):

    contact = find_contact(contact_id)

    if not contact:
        flash("La consulta no existe", "error")
        return render_template("contacts/show_contacts.html")

    return render_template("contacts/show_contact_detail.html", contact=contact)


@bp.route("/contact_delete/<int:contact_id>", methods=["POST", "GET"])
@check_permissions("contact_delete")
@login_required
def contact_delete(contact_id):

    contact = find_contact(contact_id)

    if not contact:
        flash("La consulta no existe", "error")
        return redirect(url_for("contacts.contacts_index"))

    delete_contact(contact)

    flash("Consulta eliminada correctamente")
    return redirect(url_for("contacts.contacts_index"))

@bp.post("/contact_answer/<int:contact_id>")
@check_permissions("contact_answer")
@login_required
def contact_answer(contact_id):

    contact = find_contact(contact_id)

    if not contact:
        flash("La consulta no existe", "error")
        return redirect(url_for("contacts.contacts_index"))
    
    # capturar el mensaje de respuesta
    comment = request.form.get("comment")

    if not comment:
        flash("Debe ingresar un comentario", "error")
        return redirect(url_for("contacts.contact_show_detail", contact_id=contact_id))

    # settear el comentario en el contacto
    commented_contact = add_comment(contact, comment)

    flash("Se guardo la respuesta correctamente")

    return redirect(url_for("contacts.contact_show_detail", contact_id=commented_contact.id))


@bp.post("/contact_block/<int:contact_id>")
@check_permissions("contact_block")
@login_required
def contact_block(contact_id):

    contact = find_contact(contact_id)

    if not contact:
        flash("La consulta no existe", "error")
        return redirect(url_for("contacts.contacts_index"))
    
    if contact.state == "Bloqueado":
        blocked_contact = block(contact, "Pendiente")
        flash("Consulta desbloqueada correctamente")
    else:
        blocked_contact = block(contact, "Bloqueado")
        flash("Consulta bloqueada correctamente")

    return redirect(url_for("contacts.contact_show_detail", contact_id=blocked_contact.id))
