from flask import Blueprint
from src.core import team_member as tm
from src.core.models.riders_and_horsewomen import proposal_enum
from src.core import equestrian as eq
from flask import render_template, request, flash, url_for, redirect, send_file, abort
from src.core import utils, minio
import mimetypes
from src.web.forms.EquestrianForm import EquestrianForm
from src.web.handlers.auth import login_required
from src.web.handlers.users import check_permissions

bp = Blueprint("equestrian", __name__, url_prefix="/equestrians")


# Routes for create a new equestrian
@bp.get("/new")
@check_permissions("equestrian_new")
@login_required
def equestrian_new():
    email_lists = tm.list_emails_from_trainers_and_handlers()
    proposals = proposal_enum.enums

    if not email_lists:
        flash("No hay entrenadores ni cuidadores registrados y son necesarios para crear un ecuestre", "info")
        return redirect(url_for("equestrian.equestrian_index"))

    return render_template("equestrians/new.html", email_list=email_lists, proposals=proposals)

@bp.post("/create")
@check_permissions("equestrian_create")
@login_required
def equestrian_create():

    equestrian_form = EquestrianForm(request.form)
    if equestrian_form.validate():
        equestrian = eq.find_equestrian_by_name(request.form["name"])
        if equestrian:
            flash("El equestre ya existe", "info")
            return redirect(url_for("equestrian.equestrian_new"))

        file_keys = ['evolution_report', 'veterinary_record', 'training_plan', 'images', 'horse_sheet']
        files = {key: request.files[key] for key in file_keys if key in request.files}
        
        eq.equestrian_create(request.form, files)
    else:
        flash("Hay campos inválidos", "error")
    return redirect(url_for("equestrian.equestrian_new"))

    

# Routes for update a equestrian
@bp.get("/edit<int:id>")
@check_permissions("equestrian_edit")
@login_required
def equestrian_edit(id):
    equestrian = eq.find_equestrian_by_id(id)
    equestrian.date_of_birth = utils.date_to_string(equestrian.date_of_birth)
    equestrian.date_of_entry = utils.date_to_string(equestrian.date_of_entry)

    proposals = proposal_enum.enums
    email_lists = tm.list_emails_from_trainers_and_handlers()

    if not email_lists:
        flash("No hay entrenadores ni cuidadores registrados y son necesarios para editar este ecuestre", "info")
        return redirect(url_for("equestrian.equestrian_index"))


    selected_emails = [team_member.email for team_member in equestrian.team_members]

    if equestrian.proposals:
        selected_proposals = [proposal for proposal in equestrian.proposals]
    else:
        selected_proposals = []

    return render_template("equestrians/edit.html", equestrian=equestrian, proposals=proposals, email_list=email_lists, selected_emails=selected_emails, selected_proposals=selected_proposals)

@bp.post("/update<int:id>")
@check_permissions("equestrian_update")
@login_required
def equestrian_update(id):
    file_keys = ['evolution_report', 'veterinary_record', 'training_plan', 'images', 'horse_sheet']
    files = {key: request.files[key] for key in file_keys if key in request.files}

    eq.equestrian_update(id, request.form, files)
    return redirect(url_for("equestrian.equestrian_index"))


# Routes for list all equestrians
@bp.get("/list")
@check_permissions("equestrian_index")
@login_required
def equestrian_index():
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name', None)
    proposal = request.args.get('proposal', None)
    date_of_birth = request.args.get('date_of_birth', None)
    date_of_entry = request.args.get('date_of_entry', None)
    sort_by = request.args.get('sort_by', None)

    all_proposals = proposal_enum.enums
    all_users, max_pages = eq.list_equestrians(page=page, name=name, proposal=proposal, date_of_birth=date_of_birth, date_of_entry=date_of_entry, sort_by=sort_by)
        
    return render_template("equestrians/list.html", list=all_users, page=page, max_pages=max_pages, all_proposals=all_proposals)

# Routes for delete a equestrian
@bp.post("/delete/<int:id>")
@check_permissions("equestrian_delete")
@login_required
def equestrian_delete(id):
    eq.equestrian_delete(id)
    return redirect(url_for("equestrian.equestrian_index"))

# Routes for show a equestrian
@bp.get("/show<int:id>")
@check_permissions("equestrian_show")
@login_required
def equestrian_show(id):
    equestrian = eq.find_equestrian_by_id(id)
    return render_template("equestrians/show.html", equestrian=equestrian)

# Routes for list all equestrian files
@bp.get("/list_files")
@check_permissions("equestrian_list_files")
@login_required
def equestrian_index_files():
    equestrians = eq.get_all_equestrians()
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name', None)
    initial_date = request.args.get('initial_date', None)
    final_date = request.args.get('final_date', None)
    sort_by = request.args.get('sort_by', None)

    all_files, max_pages = eq.list_equestrians_files(page=page, name=name, initial_date=initial_date, final_date=final_date, sort_by=sort_by)
        
    return render_template("equestrians/list_files.html", files=all_files, page=page, max_pages=max_pages)

# Routes for files management
@bp.get("/view_file/<int:id>/<string:filename>")
@check_permissions("equestrian_view_file")
@login_required
def equestrian_view_file(id, filename):
    file_data, content_type = minio.get_file("ecuestres", id, filename)
    if not file_data:
        return "Archivo no encontrado", 404

    if not content_type:
        content_type, _ = mimetypes.guess_type(filename)

    if content_type == 'application/pdf':
        return send_file(
            file_data,
            mimetype='application/pdf',
            as_attachment=False,
            download_name=filename
        )
    elif content_type.startswith('image/'):
        return send_file(
            file_data,
            mimetype=content_type,
            as_attachment=False,
            download_name=filename
        )
    else:
        return send_file(
            file_data,
            mimetype=content_type,
            as_attachment=True,
            download_name=filename
        )

@bp.get("/dowload_file/<int:id>/<string:filename>")
@check_permissions("equestrian_download_file")
@login_required
def equestrian_download_file(id, filename):
    file_data, content_type = minio.get_file("ecuestres", id, filename)
    if not file_data:
        return "Archivo no encontrado", 404

    return send_file(
        file_data,
        mimetype=content_type,
        as_attachment=True,
        download_name=filename
    )
