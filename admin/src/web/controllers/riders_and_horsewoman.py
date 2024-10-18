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
)
from src.core import riders_and_horsewomen as rh
from src.core import team_member as tm
from src.core import riders as eq
from src.core import health_insurance as hi
from src.web.forms import RiderHorsewomanForm as riderForm
from src.web.handlers.auth import login_required

bp = Blueprint("riders_and_horsewomen", __name__, url_prefix="/riders_and_horsewomen")


@bp.get("/")
@login_required
def riders_and_horsewomen_list():
    return


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
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
    horses = eq.get_all_riderss()
    track_assistants = tm.get_all_track_assistants()

    form = riderForm(request.form)
    # se checkean todos los campos
    if request.method == "POST":
        if form.validate():
            rider = rh.find_rider(request.form["dni"])
            if not rider:
                rh.create_rider_horsewoman(request.form)
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
    horses = eq.get_all_riderss()
    track_assistants = tm.get_all_track_assistants()

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
    rh.update(id, request.form)
    flash("El jinete/Amazona se ha actualizado exitosamente")

    # ---------------------- Debería ir al index -----------------------
    return redirect(url_for("riders_and_horsewomen.edit", id=id))


@bp.route("/new_institution", methods=["GET", "POST"])
@login_required
def new_institution():
    return render_template("riders_and_horsewomen/new_institution.html")

@bp.post("/add_files")
def riders_and_horsewomen_new_file():
    filename = request.form.get("filename")
    file_type = request.form.get("file_type")
    rider_id = request.form.get("rider_id")
    
    if filename and file_type and rider_id:
        rh.new_file(filename, file_type, rider_id)
    
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

@bp.get("/view_file/<int:id>")
def view_file(id):
    filename = rh.get_file_name(id)
    file_data, content_type  = rh.get_file(id)
    

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
    

#Routes for list all riders files
@bp.get("/list_files")
def list_files():
    # Get the page number or default to 1
    page = request.args.get('page', 1, type=int) 

    # Get the filters from the form
    name = request.args.get('name', None)
    initial_date = request.args.get('initial_date', None)
    final_date = request.args.get('final_date', None)
    sort_by = request.args.get('sort_by', None)

    # find_riderss_files also returns the max number of pages
    all_files, max_pages = rh.list_riders_files(page=page, name=name, initial_date=initial_date, final_date=final_date, sort_by=sort_by)
        
    return render_template("riders_and_horsewomen/list_files.html",files= all_files, page=page, max_pages=max_pages)

@bp.route("/delete_rider/<rider_dni>", methods=["GET", "POST"])
def delete_rider(rider_dni):
    rider = rh.find_rider(rider_dni)

    if not rider:
        flash("El Jinete o Amazona seleccionado no exite", "error")
        return redirect(url_for('riders_and_horsewomen.riders_and_horsewomen_list'))
    
    rh.delete_a_rider(rider)
    
    flash("Jinete o Amazona eliminado exitosamente.")
    return redirect(url_for('riders_and_horsewomen.riders_and_horsewomen_list'))
