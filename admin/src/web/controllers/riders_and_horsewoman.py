import mimetypes
from core import minio
from flask import Blueprint, redirect, render_template, request, flash, send_file, url_for
from src.core.models.riders_and_horsewomen import (
    disability_certificate_enum,
    disability_type_enum,
    family_allowance_enum,
    pension_enum,
    days_enum,
    condition_enum,
    seat_enum,
    proposal_enum,
    education_level_enum,
    files_enum
)
from src.core import riders_and_horsewomen as rh
from src.core import team_member as tm
from src.core import equestrian as eq
from src.core import health_insurance as hi
from src.web.forms import RiderHorsewomanForm as riderForm
from src.web.handlers.auth import login_required

bp = Blueprint("riders_and_horsewomen", __name__, url_prefix="/riders_and_horsewomen")


@bp.get("/")
@login_required
def riders_and_horsewomen_index():
    # obtengo parametros de busqueda del formulario
    team_members = tm.get_all()
    name = request.args.get('name') 
    last_name = request.args.get('last_name')
    dni = request.args.get('dni')
    order_by = request.args.get('order_by', 'asc')
    professional = request.args.get('professionenum')
    page = request.args.get('page', 1, type=int)
    all_riders, max_pages = rh.find_all_riders(name, last_name, dni, order_by, professional, page)

    return render_template('riders_and_horsewomen/show_riders.html',
                           pro_member_options=team_members ,riders = all_riders, max_pages = max_pages, current_page = page)

@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    disability_certificate_options = disability_certificate_enum.enums
    disability_type_options = disability_type_enum.enums
    family_allowance_options = family_allowance_enum.enums
    pension_options = pension_enum.enums
    education_level_options = education_level_enum.enums
    days_options = days_enum.enums
    file_type = files_enum.enums
    health_insurances = hi.get_all()
    team_members = tm.get_all()
    therapists = tm.get_all_therapists()
    riders = tm.get_all_riders()
    horses = eq.get_all_equestrians()
    track_assistants = tm.get_all_track_assistants()

    if not horses:
        flash("No hay caballos cargados en el sistema y son necesarios para registrar un jinete/amazona", "error")
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))
    
    if not riders:
        flash("No hay manejadores de caballos cargados en el sistema y son necesarios para registrar un jinete/amazona", "error")
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))

    if not team_members:
        flash("No hay miembros de equipo cargados en el sistema y son necesarios para registrar un jinete/amazona", "error")
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))
    
    if not track_assistants:
        flash("No hay asistentes de pista cargados en el sistema y son necesarios para registrar un jinete/amazona", "error")
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))
    
    if not therapists:
        flash("No hay terapeutas cargados en el sistema y son necesarios para registrar un jinete/amazona", "error")
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))


    form = riderForm(request.form)
    # se checkean todos los campos
    if request.method == "POST":
        if form.validate():
            rider = rh.find_rider(request.form["dni"])
            if not rider:
    
                rh.create_rider_horsewoman(request.form, request.files)
                flash("El jinete/Amazona se creado exitosamente")
            else:
                flash("El dni ingresado ya existe", "info")
        else:
            flash("faltan datos para completar", "error")

        return redirect(url_for("riders_and_horsewomen.new"))

    return render_template(
        "riders_and_horsewomen/new.html",
        days_options=days_options,
        disability_certificate_options=disability_certificate_options,
        disability_type_options=disability_type_options,
        family_allowance_options=family_allowance_options,
        pension_options=pension_options,
        education_level_options=education_level_options,
        pro_member_options=team_members,
        therapists=therapists,
        condition_options=condition_enum.enums,
        seat_options=seat_enum.enums,
        proposal_options=proposal_enum.enums,
        riders=riders,
        horses=horses,
        track_assistants=track_assistants,
        health_insurance_options=health_insurances,
        file_type=file_type,
    )


@bp.get("/edit/<int:id>")
@login_required
def edit(id):
    rider = rh.get_rider_by_id(id)
    first_tutor, second_tutor = rh.get_tutors_by_rider_id(id)
    caring_professionals = rh.get_caring_professionals_by_rider_id(id)
    work_in_institutions = rh.get_work_in_institutions_by_rider_id(id)
    disability_certificate_options = disability_certificate_enum.enums
    disability_type_options = disability_type_enum.enums
    family_allowance_options = family_allowance_enum.enums
    pension_options = pension_enum.enums
    education_level_options = education_level_enum.enums
    days_options = days_enum.enums
    health_insurances = hi.get_all()
    team_members = tm.get_all()
    therapists = tm.get_all_therapists()
    riders = tm.get_all_riders()
    horses = eq.get_all_equestrians()
    track_assistants = tm.get_all_track_assistants()

    if not horses:
        flash("No hay caballos cargados en el sistema y son necesarios para registrar a este jinete/amazona", "error")
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))
    
    if not riders:
        flash("No hay manejadores de caballos cargados en el sistema y son necesarios para registrar a este jinete/amazona", "error")
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))

    if not team_members:
        flash("No hay miembros de equipo cargados en el sistema y son necesarios para registrar a este jinete/amazona", "error")
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))
    
    if not track_assistants:
        flash("No hay asistentes de pista cargados en el sistema y son necesarios para registrar a este jinete/amazona", "error")
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))
    
    if not therapists:
        flash("No hay terapeutas cargados en el sistema y son necesarios para registrar a este jinete/amazona", "error")
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))

    return render_template(
        "riders_and_horsewomen/edit.html",
        rider=rider,
        first_tutor=first_tutor,
        second_tutor=second_tutor,
        caring_professionals=caring_professionals,
        work_in_institutions=work_in_institutions,
        days_options=days_options,
        disability_certificate_options=disability_certificate_options,
        disability_type_options=disability_type_options,
        family_allowance_options=family_allowance_options,
        pension_options=pension_options,
        education_level_options=education_level_options,
        pro_member_options=team_members,
        therapists=therapists,
        condition_options=condition_enum.enums,
        seat_options=seat_enum.enums,
        proposal_options=proposal_enum.enums,
        riders=riders,
        horses=horses,
        track_assistants=track_assistants,
        health_insurance_options=health_insurances,
    )

@bp.post("/update/<int:id>")
@login_required
def riders_and_horsewomen_update(id):
    rh.update(id, request.form, request.files)
    flash("El jinete/Amazona se ha actualizado exitosamente")

    # ---------------------- Debería ir al index -----------------------
    return redirect(url_for("riders_and_horsewomen.edit", id=id))


@bp.route("/new_institution", methods=["GET", "POST"])
@login_required
def new_institution():
    return render_template("riders_and_horsewomen/new_institution.html")

@bp.post("/add_files")
def riders_and_horsewomen_new_file():
    file = request.files.get("select_file_1")
    link = request.form.get("select_link_1")
    file_type = request.form.get("file_type")
    rider_id = request.form.get("rider_id")

    if file:
        print(file)
        filename = file
        rh.new_file(file, file_type, rider_id)
    elif link:
        rh.new_link(link, rider_id, file_type)

    return redirect(url_for("riders_and_horsewomen.new", id=rider_id))

@bp.post("/delete_file")
def riders_and_horsewomen_delete_file(rider_id):

    if request.args.get("file_id"):
        file_id = request.args.get("file_id")
        rh.delete_file(rider_id, file_id)
    
    return redirect(url_for("riders_and_horsewomen.new", id=rider_id))

@bp.post("/add_link")
def riders_and_horsewomen_new_link():
    link = request.form.get("link")
    file_type = request.form.get("file_type")
    rider_id = request.form.get("rider_id")

    if link:
        rh.new_link(link, rider_id, file_type)
    
    return redirect(url_for("riders_and_horsewomen.new", id=rider_id))

@bp.post("/delete_link")
def riders_and_horsewomen_delete_link(rider_id):

    if request.args.get("link_id"):
        link_id = request.args.get("link_id")
        rh.delete_link(link_id)
    
    return redirect(url_for("riders_and_horsewomen.new", id=rider_id))

@bp.get("/view_file/<int:file_id>")
def riders_and_horsewomen_view_file(file_id):
    filename = rh.get_filename(file_id)
    file_data, content_type  = rh.get_file(file_id)
    

    if not file_data:
        return "Archivo no encontrado", 404

     # If the content type is not provided, try to guess it from the filename
    if not content_type:
        content_type, _ = mimetypes.guess_type(filename)

    
    # For PDF files
    if content_type == 'application/pdf':
        return send_file(
            file_data,
            mimetype='application/pdf',
            as_attachment=False,
            download_name=filename
        )
    
    # For images
    elif content_type.startswith('image/'):
        return send_file(
            file_data,
            mimetype=content_type,
            as_attachment=False,
            download_name=filename
        )
    
    # For other files, force download
    else:
        return send_file(
            file_data,
            mimetype=content_type,
            as_attachment=True,
            download_name=filename
        )
    

@bp.get("/view_link/<int:link_id>")
def riders_and_horsewomen_view_link(link_id):

    link, data = rh.get_link(link_id)
    return redirect(link)

@bp.get("/dowload_file/<int:file_id>")
#@check_permissions("equestrian_download_file")
@login_required
def riders_and_horsewomen_download_file(file_id):
    file_data, content_type = rh.get_file(file_id)

    if not file_data:
        return "Archivo no encontrado", 404

    return send_file(
        file_data,
        mimetype=content_type,
        as_attachment=True,
        download_name=rh.get_filename(file_id)
    )


# Routes for listing all riders' files
@bp.get("/list_files")
@login_required
def riders_and_horsewomen_index_files():
    # Get the page number or default to 1
    page = request.args.get('page', 1, type=int)

    # Get the filters from the form
    name = request.args.get('name', None)
    initial_date = request.args.get('initial_date', None)
    final_date = request.args.get('final_date', None)
    sort_by = request.args.get('sort_by', None)

    # find_riders_files also returns the max number of pages
    all_files, max_pages = rh.list_riders_files(page=page, name=name, initial_date=initial_date, final_date=final_date, sort_by=sort_by)

    for file in all_files:
        print(file["file"].is_link)

    # all_files should be a dictionary with filename, file_type, rider_id, created_at
    return render_template("riders_and_horsewomen/list_files.html", files=all_files, page=page, max_pages=max_pages)

@bp.route("/delete_rider/<rider_dni>", methods=["GET", "POST"])
def delete_rider(rider_dni):
    rider = rh.find_rider(rider_dni)

    if not rider:
        flash("El Jinete o Amazona seleccionado no exite", "error")
        return redirect(url_for('riders_and_horsewomen.riders_and_horsewomen_index'))
    
    rh.delete_a_rider(rider)
    
    flash("Jinete o Amazona eliminado exitosamente.")
    return redirect(url_for('riders_and_horsewomen.riders_and_horsewomen_index'))

 