import mimetypes
from core import minio
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    flash,
    send_file,
    url_for,
)

from src.core.models.riders_and_horsewomen import (
    File,
    disability_certificate_enum,
    disability_type_enum,
    family_allowance_enum,
    pension_enum,
    days_enum,
    condition_enum,
    seat_enum,
    proposal_enum,
    education_level_enum,
    files_enum,
)
from src.core import riders_and_horsewomen as rh
from src.core import team_member as tm
from src.core import equestrian as eq
from src.core import health_insurance as hi
from src.web.forms.RiderAndHorsewomanForm import FirstTutorForm, RiderHorsewomanForm as riderForm, RiderHorsewomanEditForm, SecondTutorForm, WorkInInstitutionForm
from src.web.handlers.auth import login_required
from src.web.handlers.users import check_permissions

bp = Blueprint("riders_and_horsewomen", __name__,
               url_prefix="/riders_and_horsewomen")


@bp.get("/")
@check_permissions("riders_and_horsewomen_index")
@login_required
def riders_and_horsewomen_index():
    """
    Displays the list of riders and horsewomen with optional search filters and pagination
    """
    # obtengo parametros de busqueda del formulario
    team_members = tm.get_all()
    name = request.args.get("name")
    last_name = request.args.get("last_name")
    dni = request.args.get("dni")
    order_by = request.args.get("order_by", "asc")
    professional = request.args.get("professionenum")
    page = request.args.get("page", 1, type=int)
    all_riders, max_pages = rh.find_all_riders(
        name, last_name, dni, order_by, professional, page
    )

    return render_template(
        "riders_and_horsewomen/show_riders.html",
        pro_member_options=team_members,
        riders=all_riders,
        max_pages=max_pages,
        page=page,
    )


@bp.route("/new", methods=["GET", "POST"])
@check_permissions("riders_and_horsewomen_new")
@login_required
def riders_and_horsewomen_new(form=None):
    """
    Register a new rider or horsewomen with the information of the form
    """
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
        flash(
            "No hay caballos cargados en el sistema y son necesarios para registrar/modificar un jinete/amazona",
            "error",
        )
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))

    if not riders:
        flash(
            "No hay manejadores de caballos cargados en el sistema y son necesarios para registrar/modificar un jinete/amazona",
            "error",
        )
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))

    if not team_members:
        flash(
            "No hay miembros de equipo cargados en el sistema y son necesarios para registrar/modificar un jinete/amazona",
            "error",
        )
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))

    if not track_assistants:
        flash(
            "No hay asistentes de pista cargados en el sistema y son necesarios para registrar/modificar un jinete/amazona",
            "error",
        )
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))

    if not therapists:
        flash(
            "No hay terapeutas cargados en el sistema y son necesarios para registrar/modificar un jinete/amazona",
            "error",
        )
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
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error: {error}", 'info')

        #return riders_and_horsewomen_new(request.form)

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
        form=request.form,
    )


@bp.get("/edit/<int:id>")
@check_permissions("riders_and_horsewomen_edit")
@login_required
def riders_and_horsewomen_edit(id, form=None):
    """
    Renders the riders and horsewomen edit form page
    """

    rider = rh.get_rider_by_id(id)
    tutor1, tutor2 = rh.get_tutors_by_rider_id(id)
    caring_professionals = rh.get_caring_professionals_by_rider_id(id)
    work_in_institutions = rh.get_work_in_institutions_by_rider_id(id)
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
    therapist = tm.find_team_member_by_id(work_in_institutions.therapist)
    track_assistant = tm.find_team_member_by_id(
        work_in_institutions.track_assistant)
    horse_handler = tm.find_team_member_by_id(work_in_institutions.rider_id)
    horse = eq.find_equestrian_by_id(work_in_institutions.horse)

    if not horses:
        flash(
            "No hay caballos cargados en el sistema y son necesarios para registrar/modificar a este jinete/amazona",
            "error",
        )
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))

    if not riders:
        flash(
            "No hay manejadores de caballos cargados en el sistema y son necesarios para registrar/modificar a este jinete/amazona",
            "error",
        )
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))

    if not team_members:
        flash(
            "No hay miembros de equipo cargados en el sistema y son necesarios para registrar/modificar a este jinete/amazona",
            "error",
        )
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))

    if not track_assistants:
        flash(
            "No hay asistentes de pista cargados en el sistema y son necesarios para registrar/modificar a este jinete/amazona",
            "error",
        )
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))

    if not therapists:
        flash(
            "No hay terapeutas cargados en el sistema y son necesarios para registrar/modificar a este jinete/amazona",
            "error",
        )
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))
    
    return render_template(
        "riders_and_horsewomen/edit.html",
        rider=rider,
        tutor1=tutor1,
        tutor2=tutor2,
        caring_professionals=caring_professionals,
        work=work_in_institutions,
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
        rider_therapist=therapist,
        track_assistants=track_assistants,
        health_insurance_options=health_insurances,
        rider_track_assistant=track_assistant,
        horse_handler=horse_handler,
        work_horse = horse,
        rider_condition = work_in_institutions.condition,
        rider_seat = work_in_institutions.seat,
        form=form,
        file_type=file_type,
    )


def validate_tutors(tutor1_form, tutor2_form):
    validation_tutor1 = tutor1_form.validate()
    validation_tutor2 = True
    if tutor2_form:
        validation_tutor2 = tutor2_form.validate()

    return validation_tutor1 and validation_tutor2

def show_tutors_errors(tutor1_form, tutor2_form):
    for field, errors in tutor1_form.errors.items():
        for error in errors:
            flash(f"Error: {error}", 'info')
    if tutor2_form:
        for field, errors in tutor2_form.errors.items():
            for error in errors:
                flash(f"Error: {error}", 'info')

def validate_forms(form, first_tutor_form, second_tutor_form, work_form):



    if not form.validate():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error: {error}", 'info')
        return False

    if not validate_tutors(first_tutor_form, second_tutor_form):
        show_tutors_errors(first_tutor_form, second_tutor_form)
        return False
        
    if not work_form.validate():
        for field, errors in work_form.errors.items():
            for error in errors:
                flash(f"Error: {error}", 'info')
        return False
    
    return True
        


@bp.post("/update/<int:id>")
@check_permissions("riders_and_horsewomen_update")
@login_required
def riders_and_horsewomen_update(id):
    """
    Updates the rider or horsewomen given by parameter
    """
    # Get forms
    form = RiderHorsewomanEditForm(request.form)
    first_tutor_form = FirstTutorForm(request.form)
    work_form = WorkInInstitutionForm(request.form)

    second_tutor_form = None
    if request.form.get('dni_second_tutor'):
        second_tutor_form = SecondTutorForm(request.form)

    # Validate forms
    if validate_forms(form, first_tutor_form, second_tutor_form, work_form):
        # Update rider
        professionals ={int(pro) for pro in request.form.getlist("select_pro") if pro != ""}
        rh.update(id, request.form, professionals, request.files)
    else:
        return riders_and_horsewomen_edit(id, form=request.form)

    return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))


@bp.route("/new_institution", methods=["GET", "POST"])
@check_permissions("riders_and_horsewomen_new_institution")
@login_required
def riders_and_horsewomen_new_institution():
    return render_template("riders_and_horsewomen/new_institution.html")


@bp.get("/view/<int:id>")
@check_permissions("riders_and_horsewomen_view")
@login_required
def riders_and_horsewomen_view(id):
    rider = rh.get_rider_by_id(id)
    tutor1, tutor2 = rh.get_tutors_by_rider_id(id)
    work_in_institutions = rh.get_work_in_institutions_by_rider_id(id)
    days = rh.get_days_by_id(id)
    if days:
        days_str = "-".join(days)
    else:
        days_str = ""
    # Get the files of the rider
    rider_files = rider.get_files()
    health_insurance = hi.get_by_id(rider.health_insurance_id)
    therapist = tm.find_team_member_by_id(work_in_institutions.therapist)
    track_assistant = tm.find_team_member_by_id(
        work_in_institutions.track_assistant)
    driver = eq.find_equestrian_by_id(work_in_institutions.rider_id)
    horse = eq.find_equestrian_by_id(work_in_institutions.horse)

    return render_template(
        "riders_and_horsewomen/view_rider.html",
        therapist=therapist,
        track_assistant=track_assistant,
        driver=driver,
        horse=horse,
        rider=rider,
        tutor1=tutor1,
        tutor2=tutor2,
        work=work_in_institutions,
        days=days_str,
        files=rider_files,
        health_insurance=health_insurance,
    )


@bp.post("/add_files")
@check_permissions("riders_and_horsewomen_new_file")
@login_required
def riders_and_horsewomen_new_file():
    file = request.files.get("select_file_1")
    link = request.form.get("select_link_1")
    file_type = request.form.get("file_type")
    rider_id = request.form.get("rider_id")

    if file:
        filename = file
        rh.new_file(file, file_type, rider_id)
    elif link:
        rh.new_link(link, rider_id, file_type)

    return redirect(
        url_for("riders_and_horsewomen.riders_and_horsewomen_new", id=rider_id)
    )


@bp.post("/delete_file/<int:file_id>")
@check_permissions("riders_and_horsewomen_delete_file")
@login_required
def riders_and_horsewomen_delete_file(file_id):

    rider_id = File.query.filter_by(id=file_id).first().rider_id

    if file_id:
        rh.delete_file(rider_id, file_id)

    return redirect(
        url_for("riders_and_horsewomen.riders_and_horsewomen_index_files", id=rider_id)
    )


@bp.post("/add_link")
@check_permissions("riders_and_horsewomen_new_link")
@login_required
def riders_and_horsewomen_new_link():
    link = request.form.get("link")
    file_type = request.form.get("file_type")
    rider_id = request.form.get("rider_id")

    if link:
        rh.new_link(link, rider_id, file_type)

    return redirect(
        url_for("riders_and_horsewomen.riders_and_horsewomen_new", id=rider_id)
    )


@bp.post("/delete_link/<int:file_id>")
@check_permissions("riders_and_horsewomen_delete_link")
@login_required
def riders_and_horsewomen_delete_link(file_id):

    if file_id:
        rh.delete_link(file_id)

    return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index_files"))


@bp.get("/view_file/<int:file_id>")
@check_permissions("riders_and_horsewomen_view_file")
@login_required
def riders_and_horsewomen_view_file(file_id):
    filename = rh.get_filename(file_id)
    file_data, content_type = rh.get_file(file_id)

    if not file_data:
        return "Archivo no encontrado", 404

    # If the content type is not provided, try to guess it from the filename
    if not content_type:
        content_type, _ = mimetypes.guess_type(filename)

    # For PDF files
    if content_type == "application/pdf":
        return send_file(
            file_data,
            mimetype="application/pdf",
            as_attachment=False,
            download_name=filename,
        )

    # For images
    elif content_type.startswith("image/"):
        return send_file(
            file_data,
            mimetype=content_type,
            as_attachment=False,
            download_name=filename,
        )

    # For other files, force download
    else:
        return send_file(
            file_data, mimetype=content_type, as_attachment=True, download_name=filename
        )


@bp.get("/view_link/<int:link_id>")
@check_permissions("riders_and_horsewomen_view_link")
@login_required
def riders_and_horsewomen_view_link(link_id):

    link, data = rh.get_link(link_id)
    if not link:
        return "Archivo no encontrado", 404
    return redirect(link)


@bp.get("/dowload_file/<int:file_id>")
@check_permissions("riders_and_horsewomen_download_file")
@login_required
def riders_and_horsewomen_download_file(file_id):
    file_data, content_type = rh.get_file(file_id)

    if not file_data:
        return "Archivo no encontrado", 404

    return send_file(
        file_data,
        mimetype=content_type,
        as_attachment=True,
        download_name=rh.get_filename(file_id),
    )


@bp.get("/dowload_link/<int:file_id>")
@check_permissions("riders_and_horsewomen_download_link")
@login_required
def riders_and_horsewomen_download_link(file_id):
    file_data, content_type = rh.get_link(file_id)

    if not file_data:
        return "Archivo no encontrado", 404

    return send_file(
        file_data,
        mimetype=content_type,
        as_attachment=True,
        download_name=rh.get_filename(file_id),
    )


# Routes for listing all riders' files
@bp.get("/list_files")
@check_permissions("riders_and_horsewomen_index_files")
@login_required
def riders_and_horsewomen_index_files():
    # Get the page number or default to 1
    page = request.args.get("page", 1, type=int)

    # Get the filters from the form
    name = request.args.get("name", None)
    initial_date = request.args.get("initial_date", None)
    final_date = request.args.get("final_date", None)
    sort_by = request.args.get("sort_by", None)

    # find_riders_files also returns the max number of pages
    all_files, max_pages = rh.list_riders_files(
        name=name,
        initial_date=initial_date,
        final_date=final_date,
        sort_by=sort_by,
        page=page,
    )

    # all_files should be a dictionary with filename, file_type, rider_id, created_at
    return render_template(
        "riders_and_horsewomen/list_files.html",
        files=all_files,
        page=page,
        max_pages=max_pages,
    )


@bp.route("/delete_rider/<rider_dni>", methods=["GET", "POST"])
@check_permissions("riders_and_horsewomen_delete_rider")
@login_required
def riders_and_horsewomen_delete_rider(rider_dni):
    rider = rh.find_rider(rider_dni)

    if not rider:
        flash("El Jinete o Amazona seleccionado no exite", "error")
        return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))

    rh.delete_a_rider(rider)

    flash("Jinete o Amazona eliminado exitosamente.")
    return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_index"))
