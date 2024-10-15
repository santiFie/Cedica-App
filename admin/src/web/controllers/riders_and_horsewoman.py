from flask import Blueprint, render_template, request, flash
from src.core.models.riders_and_horsewomen import disability_certificate_enum, disability_type_enum, family_allowance_enum, pension_enum, days_enum, condition_enum, seat_enum, proposal_enum, education_level_enum 
from src.core import riders_and_horsewomen as rh
from src.core import health_insurance as hi
from src.web.handlers.auth import login_required

bp = Blueprint('riders_and_horsewomen',__name__,url_prefix="/riders_and_horsewomen")


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
    
    #donde van funciones aux de checkeo de datos.
    if request.method == "POST":
        rider = rh.find_rider(request.form["dni"])

        if not rider:
            #se checkean todos los campos
            flash("El jinete/Amazona se creado exitosamente")
        else:
            flash("El dni ingresado ya existe", "info")
    
    
    return render_template("riders_and_horsewomen/new.html", disability_certificate_options=disability_certificate_options, disability_type_options=disability_type_options, family_allowance_options=family_allowance_options, pension_options=pension_options)

@bp.route("/new/tutor", methods=["GET", "POST"])
@login_required
def new_tutor():
    education_level_options = education_level_enum.enums
    return render_template("riders_and_horsewomen/new_tutor.html", education_level_options= education_level_options)

@bp.route("/new/institution", methods=["GET", "POST"])
@login_required
def new_institution():
    return render_template("riders_and_horsewomen/new_institution.html")