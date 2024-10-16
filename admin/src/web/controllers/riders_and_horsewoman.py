from flask import Blueprint, render_template, request, flash
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
from src.core import equestrian as eq
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
    team_members = tm.get_all()
    therapists = tm.get_all_therapists()
    riders = tm.get_all_riders()
    horses = eq.get_all_equestrians()
    track_asistenaces = tm.get_all_track_asistances()
    days_options = days_enum.enums

    form = riderForm(request.form)
    # se checkean todos los campos
    if request.method == "POST":
        if form.validate():
            # chckeo que no este cargado en la base de datos
            rider = rh.find_rider(request.form["dni"])
            if not rider:
                # cargo en la base de datos
                flash("El jinete/Amazona se creado exitosamente")
            else:
                flash("El dni ingresado ya existe", "info")
        else:
            flash("faltan datos para completar", "error")


    return render_template(
        "riders_and_horsewomen/new.html",
        days_options=days_options,
        disability_certificate_options=disability_certificate_options,
        disability_type_options=disability_type_options,
        family_allowance_options=family_allowance_options,
        pension_options=pension_options,
        education_level_options=education_level_options,
        pro_members_options = team_members,
        therapists=therapists,
        condition_options=condition_enum.enums,
        seat_options = seat_enum.enums,
        porposal_options = proposal_enum.enums,
        riders=riders,
        horses=horses,
        track_asistenaces=track_asistenaces,
    )


@bp.route("/new/institution", methods=["GET", "POST"])
@login_required
def new_institution():
    return render_template("riders_and_horsewomen/new_institution.html")
