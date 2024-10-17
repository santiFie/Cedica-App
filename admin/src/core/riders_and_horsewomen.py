from datetime import datetime
from core import minio
from src.core import database
from flask import flash, redirect, url_for
from src.core import utils
from src.core import team_member as tm
from src.core.models.team_member import TeamMember
from src.core.models.riders_and_horsewomen import File, RiderAndHorsewoman
from src.core.models.riders_and_horsewomen import (
    CaringProfessional,
    RiderAndHorsewoman,
    Tutor,
    WorkInInstitution,
    RiderHorsewomanInstitution,
)
from sqlalchemy.orm import aliased
from src.web.forms import (
    SecondTutorForm,
    FirstTutorForm,
    RiderHorsewomanForm,
    WorkInInstitutionForm,
)

PREFIX="Jinetes y Amazonas"

def create_enums():
    from src.core.models.riders_and_horsewomen import (
        disability_certificate_enum,
        disability_type_enum,
        files_enum,
        family_allowance_enum,
        pension_enum,
        days_enum,
        condition_enum,
        seat_enum,
        proposal_enum,
        education_level_enum,
    )

    disability_certificate_enum.create(database.db.engine, checkfirst=True)
    disability_type_enum.create(database.db.engine, checkfirst=True)
    family_allowance_enum.create(database.db.engine, checkfirst=True)
    pension_enum.create(database.db.engine, checkfirst=True)
    days_enum.create(database.db.engine, checkfirst=True)
    condition_enum.create(database.db.engine, checkfirst=True)
    seat_enum.create(database.db.engine, checkfirst=True)
    proposal_enum.create(database.db.engine, checkfirst=True)
    education_level_enum.create(database.db.engine, checkfirst=True)
    files_enum.create(database.db.engine, checkfirst=True)


def find_rider(dni):

    rider = RiderAndHorsewoman.query.filter_by(dni=dni).first()

    return rider


def create_caring_professional(id_rh, id_tm):
    """
    Create a caring professional
    """
    from src.core.models.riders_and_horsewomen import CaringProfessional

    caring = CaringProfessional(rider_horsewoman_id=id_rh, team_member_id=id_tm)

    database.db.session.add(caring)
    database.db.session.commit()


def create_tutors(form, id):
    """
    Create tutor/s
    """
    from src.core.models.riders_and_horsewomen import Tutor

    first_tutor_form = FirstTutorForm(form)
    second_tutor_form = None
    if form["dni_second_tutor"]:
        second_tutor_form = SecondTutorForm(form)

    validation_first_tutor = first_tutor_form.validate()
    validation_second_tutor = False
    if second_tutor_form:
        validation_second_tutor = second_tutor_form.validate()

    if validation_first_tutor:
        first_tutor = Tutor(
            dni=form["dni_first_tutor"],
            relationship=form["relationship_first_tutor"],
            name=form["name_first_tutor"],
            last_name=form["last_name_first_tutor"],
            address=form["address_first_tutor"],
            phone=form["phone_first_tutor"],
            email=form["email_first_tutor"],
            education_level=form["education_level_first_tutor"],
            occupation=form["occupation_first_tutor"],
            rider_and_horsewoman_id=id,
        )
        database.db.session.add(first_tutor)
        database.db.session.commit()

    if validation_second_tutor:
        second_tutor = Tutor(
            dni=form["dni_second_tutor"],
            relationship=form["relationship_second_tutor"],
            name=form["name_second_tutor"],
            last_name=form["last_name_second_tutor"],
            address=form["address_second_tutor"],
            phone=form["phone_second_tutor"],
            email=form["email_second_tutor"],
            education_level=form["education_level_second_tutor"],
            occupation=form["occupation_second_tutor"],
            rider_and_horsewoman_id=id,
        )
        database.db.session.add(second_tutor)
        database.db.session.commit()

    if validation_first_tutor and validation_second_tutor:
        flash("Tutores creados exitosamente")
    elif validation_first_tutor:
        flash("Primer tutor creado exitosamente")
    else:
        flash("Segundo tutor creado exitosamente")


def create_work_in_institution(form, id):
    """
    Create work in institution and the intermediate table
    """
    work_form = WorkInInstitutionForm(form)
    if work_form.validate():
        work = WorkInInstitution(
            proposal=form["proposal"],
            condition=form["condition"],
            seat=form["seat"],
            therapist=form["therapist"],
            rider=form["rider"],
            horse=form["horse"],
            track_assistant=form["track_assistant"],
            days=form.getlist("days"),
        )

        database.db.session.add(work)
        database.db.session.commit()

        rider_institution = RiderHorsewomanInstitution(
            rider_horsewoman_id=id, work_in_institution_id=work.id
        )

        database.db.session.add(rider_institution)
        database.db.session.commit()

        flash("Trabajo en institución creado exitosamente", "success")
    else:
        for field, errors in work_form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}")

        return redirect(url_for("riders_and_horsewomen.new"))


def create_rider_horsewoman(form):
    """
    Create a new rider or horsewoman and dependencys
    """
    from src.core.models.riders_and_horsewomen import RiderAndHorsewoman
    from src.core.team_member import check_team_member_by_email

    lista = []
    scholarship_boolean = form.get("scholarship_boolean", False)
    disability_certificate_boolean = form.get("disability_certificate_boolean", False)
    family_allowance_boolean = form.get("family_allowance_boolean", False)
    pension_boolean = form.get("pension_boolean", False)
    curatela = form.get("curatela", False)

    if scholarship_boolean:
        lista.append(form["scholarship_percentage"])
        if form["observations_scholarship"]:
            lista.append(form["observations_scholarship"])
        else:
            lista.append(None)
    else:
        lista.append(None)
        lista.append(None)

    if disability_certificate_boolean:
        lista.append(form["disability_type"])
        lista.append(form["disability_certificate"])
        if form["disability_certificate"] == "OTRO":
            lista.append(form["disability_certificate_otro"])
        else:
            lista.append(None)
    else:
        lista.append(None)
        lista.append(None)
        lista.append(None)

    if family_allowance_boolean:
        lista.append(form["family_allowance"])
    else:
        lista.append(None)
    if pension_boolean:
        lista.append(form["pension"])
    else:
        lista.append(None)

    riders_form = RiderHorsewomanForm(form)
    if riders_form.validate():
        rider_horsewoman = RiderAndHorsewoman(
            dni=form["dni"],
            name=form["name"],
            last_name=form["last_name"],
            age=form["age"],
            date_of_birth=form["date_of_birth"],
            place_of_birth=form["place_of_birth"],
            address=form["address"],
            phone=form["phone"],
            emergency_contact=form["emergency_contact"],
            emergency_phone=form["emergency_phone"],
            scholarship_percentage=lista[0],
            observations=lista[1],
            disability_certificate=lista[3],
            others=lista[4],
            disability_type=lista[2],
            family_allowance=lista[5],
            pension=lista[6],
            name_institution=form["name_institution"],
            address_institution=form["address_institution"],
            phone_institution=form["phone_institution"],
            current_grade=form["current_grade"],
            observations_institution=form["observations_institution"],
            health_insurance_id=form["health_insurance"],
            membership_number=form["membership_number"],
            curatela=True if curatela == "on" else False,
            pension_situation_observations=form["observations_institution"],
        )

        database.db.session.add(rider_horsewoman)
        database.db.session.commit()
    else:
        utils.riders_and_horsewomen_errors(riders_form)
        return redirect(url_for("riders_and_horsewomen.new"))

    # Caring professionals
    for i in range(1, 6):
        id_key = f"select_pro_{i}"
        if form.get(id_key):
            create_caring_professional(rider_horsewoman.id, form[id_key])

    # Tutors
    create_tutors(form, rider_horsewoman.id)

    # Work In Institution
    create_work_in_institution(form, rider_horsewoman.id)


# FALTA EL PARAM Y FILTRO DE PROFESIONALES QUE LO ATIENDEN !!!!!!!!!!
def find_all_riders(name=None, last_name=None, dni=None, order_by="asc", page=1):

    per_page = 25

    query = RiderAndHorsewoman.query

    # Filtro por DNI
    if dni:
        query = query.filter(RiderAndHorsewoman.dni == dni)

    if name or last_name:
        # para poder buscar por ambos campos al mismo tiempo
        rider_alias_name = aliased(RiderAndHorsewoman)
        rider_alias_last_name = aliased(RiderAndHorsewoman)

        # Filtro por nombre del rider
        if name:
            query = query.filter(rider_alias_name.name.ilike(f"%{name}%"))

        # Filtro por apellido del rider
        if last_name:
            query = query.filter(
                rider_alias_last_name.last_name.ilike(f"%{last_name}%")
            )

    # Ordeno por el campo adecuado
    if order_by == "asc":
        query = query.order_by(
            RiderAndHorsewoman.name.asc()
        )  # Puedes cambiarlo por el campo adecuado
    else:
        query = query.order_by(
            RiderAndHorsewoman.name.desc()
        )  # Puedes cambiarlo por el campo adecuado

    total_riders = query.count()

    # Manejo del caso en el que no haya jinetes
    if total_riders == 0:
        return [], 0

    max_pages = (total_riders + per_page - 1) // per_page  # Redondeo hacia arriba

    # Aseguramos que la página solicitada no sea menor que 1
    if page < 1:
        page = 1

    # Aseguramos que la página solicitada no sea mayor que el número máximo de páginas
    if page > max_pages:
        page = max_pages

    offset = (page - 1) * per_page
    riders = query.offset(offset).limit(per_page).all()

    return riders, max_pages


def update(id, form):
    """
    Update a rider or horsewoman. Returns True if the rider was updated successfully, False otherwise.
    """

    rider = get_rider_by_id(id)

    if not rider:
        return False

    lista = []
    scholarship_boolean = form.get("scholarship_boolean", False)
    disability_certificate_boolean = form.get("disability_certificate_boolean", False)
    family_allowance_boolean = form.get("family_allowance_boolean", False)
    pension_boolean = form.get("pension_boolean", False)
    curatela = form.get("curatela", False)

    if scholarship_boolean:
        lista.append(form["scholarship_percentage"])
        if form["observations_scholarship"]:
            lista.append(form["observations_scholarship"])
        else:
            lista.append(None)
    else:
        lista.append(None)
        lista.append(None)

    if disability_certificate_boolean:
        lista.append(form["disability_type"])
        lista.append(form["disability_certificate"])
        if form["disability_certificate"] == "OTRO":
            lista.append(form["disability_certificate_otro"])
        else:
            lista.append(None)
    else:
        lista.append(None)
        lista.append(None)
        lista.append(None)

    if family_allowance_boolean:
        lista.append(form["family_allowance"])
    else:
        lista.append(None)
    if pension_boolean:
        lista.append(form["pension"])
    else:
        lista.append(None)

    riders_form = RiderHorsewomanForm(form)
    if riders_form.validate():

        rider.name = form["name"]
        rider.last_name = form["last_name"]
        rider.age = form["age"]
        rider.date_of_birth = form["date_of_birth"]
        rider.place_of_birth = form["place_of_birth"]
        rider.address = form["address"]
        rider.phone = form["phone"]
        rider.emergency_contact = form["emergency_contact"]
        rider.emergency_phone = form["emergency_phone"]
        rider.scholarship_percentage = lista[0]
        rider.observations = lista[1]
        rider.disability_certificate = lista[3]
        rider.others = lista[4]
        rider.disability_type = lista[2]
        rider.family_allowance = lista[5]
        rider.pension = lista[6]
        rider.name_institution = form["name_institution"]
        rider.address_institution = form["address_institution"]
        rider.phone_institution = form["phone_institution"]
        rider.current_grade = form["current_grade"]
        rider.observations_institution = form["observations_institution"]
        rider.health_insurance_id = form["health_insurance"]
        rider.membership_number = form["membership_number"]
        rider.curatela = True if curatela == "on" else False
        rider.pension_situation_observations = form["observations_institution"]

        database.db.session.commit()
    else:
        utils.riders_and_horsewomen_errors(riders_form)
        return redirect(url_for("riders_and_horsewomen.new"))

    update_caring_professionals(form, id)
    update_tutors(form, id)
    update_work_in_institution(form, id)

    return True


def update_caring_professionals(form, id):
    """
    Update caring professionals
    """
    caring_professionals = get_caring_professionals_by_rider_id(id)

    for caring_professional in caring_professionals:
        database.db.session.delete(caring_professional)
        database.db.session.commit()

    for i in range(1, 6):
        id_key = f"select_pro_{i}"
        if form.get(id_key):
            create_caring_professional(id, form[id_key])


def update_tutors(form, id):
    """
    Update tutors
    """
    first_tutor_form = FirstTutorForm(form)
    second_tutor_form = None
    if form["dni_second_tutor"]:
        second_tutor_form = SecondTutorForm(form)

    first_tutor = Tutor.query.filter(Tutor.rider_and_horsewoman_id == id).first()
    second_tutor = Tutor.query.filter(Tutor.rider_and_horsewoman_id == id).all()[1]

    validation_first_tutor = first_tutor_form.validate()
    validation_second_tutor = False
    if second_tutor_form:
        validation_second_tutor = second_tutor_form.validate()

    if validation_first_tutor:
        first_tutor.dni = form["dni_first_tutor"]
        first_tutor.relationship = form["relationship_first_tutor"]
        first_tutor.name = form["name_first_tutor"]
        first_tutor.last_name = form["last_name_first_tutor"]
        first_tutor.address = form["address_first_tutor"]
        first_tutor.phone = form["phone_first_tutor"]
        first_tutor.email = form["email_first_tutor"]
        first_tutor.education_level = form["education_level_first_tutor"]

        database.db.session.commit()

    if validation_second_tutor:
        second_tutor.dni = form["dni_second_tutor"]
        second_tutor.relationship = form["relationship_second_tutor"]
        second_tutor.name = form["name_second_tutor"]
        second_tutor.last_name = form["last_name_second_tutor"]
        second_tutor.address = form["address_second_tutor"]
        second_tutor.phone = form["phone_second_tutor"]
        second_tutor.email = form["email_second_tutor"]
        second_tutor.education_level = form["education_level_second_tutor"]

        database.db.session.commit()

    if validation_first_tutor and validation_second_tutor:
        flash("Tutores actualizados exitosamente")
    elif validation_first_tutor:
        flash("Primer tutor actualizado exitosamente")
    else:
        flash("Segundo tutor actualizado exitosamente")


def update_work_in_institution(form, id):
    """
    Update work in institution and the intermediate table
    """
    work_form = WorkInInstitutionForm(form)
    if work_form.validate():
        work = get_work_in_institutions_by_rider_id(id)

        work.proposal = form["proposal"]
        work.condition = form["condition"]
        work.seat = form["seat"]
        work.therapist = form["therapist"]
        work.rider = form["rider"]
        work.horse = form["horse"]
        work.track_assistant = form["track_assistant"]
        work.days = form.getlist("days")

        database.db.session.commit()
    else:
        for field, errors in work_form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}")

        return redirect(url_for("riders_and_horsewomen.new"))


#!!!!!!!!
def delete_a_rider(rider):

    database.db.session.delete(rider)
    database.db.session.commit()

    return True


def get_work_in_institutions_by_rider_id(rider_id):
    """
    Get work in institution by rider id
    """
    work_in_institutions = (
        WorkInInstitution.query.join(RiderHorsewomanInstitution)
        .filter(RiderHorsewomanInstitution.rider_horsewoman_id == rider_id)
        .first()
    )

    return work_in_institutions


def get_caring_professionals_by_rider_id(rider_id):
    """
    Get all caring professionals by rider id
    """
    caring_professionals = (
        TeamMember.query.join(CaringProfessional)
        .filter(CaringProfessional.rider_horsewoman_id == rider_id)
        .all()
    )

    return caring_professionals


def get_rider_by_id(rider_id):
    """
    Get a rider by id
    """
    rider = RiderAndHorsewoman.query.get(rider_id)

    return rider


def get_tutors_by_rider_id(rider_id):
    """
    Get all tutors by rider id
    """
    num_of_tutors = Tutor.query.filter(
        Tutor.rider_and_horsewoman_id == rider_id
    ).count()

    if num_of_tutors == 1:
        tutor1 = Tutor.query.filter(Tutor.rider_and_horsewoman_id == rider_id).first()
        tutor2 = None
    elif num_of_tutors == 2:
        tutor1 = Tutor.query.filter(Tutor.rider_and_horsewoman_id == rider_id).first()
        tutor2 = Tutor.query.filter(Tutor.rider_and_horsewoman_id == rider_id).all()[1]

    return tutor1, tutor2


def new_file(filename, file_type, rider_id):
    """
    Create a new file for a rider
    """

    rider = get_rider_by_id(rider_id)

    if rider:

        file = File(filename=filename, file_type=file_type, rider_id=rider_id)

        minio.upload_file(PREFIX, filename, rider_id)
        database.db.session.add(file)
        database.db.session.commit()

def new_link(link, rider_id, file_type):
    """
    Create a new file for a rider
    """

    rider = get_rider_by_id(rider_id)

    if rider:
        file = File(filename=link, file_type=file_type, rider_id=rider_id)
        minio.upload_link(PREFIX, link, rider_id)
        database.db.session.add(file)
        database.db.session.commit()

def delete_file(rider_id, file_id):
    """
    Delete the file of a rider
    """
    user_file = File.query.filter(File.id == file_id).first()
    
    if user_file:
        minio.upload_file(PREFIX, user_file.filename, rider_id)
        File.query.filter(File.id == file_id).delete()
        database.db.session.commit()

def delete_link(rider_id, link_id):
    """
    Delete the link of a rider
    """
    user_file = File.query.filter(File.id == link_id).first()
    
    if user_file:
        minio.upload_link(PREFIX, user_file.filename, rider_id)
        File.query.filter(File.id == link_id).delete()
        database.db.session.commit()

def get_link(link_id):
    """
    Get the link of a rider
    """
    user_file = File.query.filter(File.id == link_id).first()


    if user_file:
        rider_id = user_file.rider_id
        return minio.get_link(PREFIX, user_file.filename, rider_id)
    return None

def order_files(sort_by, file):
    if sort_by == 'name_asc':
        file.sort(key=lambda x: x['filename'])
    elif sort_by == 'name_desc':
        file.sort(key=lambda x: x['filename'], reverse=True)
    elif sort_by == 'downloaded_date_asc':
        file.sort(key=lambda x: x['upload_date'] or datetime.min)
    elif sort_by == 'downloaded_date_desc':
        file.sort(key=lambda x: x['upload_date'] or datetime.min, reverse=True)
    return file


def list_riders_files(page=1, name=None, initial_date=None, final_date=None, sort_by=None):
    per_page = 25

    # Get all the riders
    riders = RiderAndHorsewoman.query.all()
    # Create a list to store the files that meet the conditions
    files_in_conditions = []

    # Parse the dates outside the loop
    if initial_date:
        initial_date = datetime.strptime(initial_date, '%Y-%m-%d')
        if initial_date > datetime.now():
            flash("No se pueden listar archivos que no fueron subidos aún")
            return [], 1
    if final_date:
        final_date = datetime.strptime(final_date, '%Y-%m-%d')

    if final_date and initial_date:
        # Check if the dates are valid
        if not utils.validate_dates(initial_date, final_date)filename:
            flash("Las fechas ingresadas no son válidas")
            return [], 1

    # Iterate over all the riders
    for rider in riders:
        # Get the files of the rider
        rider_files = [rider.filename for rider in rider.get_files()]
        for file in rider_files:
            if file:
                # Get the date of the file
                file_date = minio.get_file_date(prefix=PREFIX, user_id=rider.id, filename=file)
            
                # Apply the name filter
                if name and name not in file:
                    # If the name is not in the file name, continue with the next file
                    continue
                
                # Apply the date filter
                if initial_date and final_date:
                    if not (file_date and initial_date <= file_date <= final_date):
                        continue
                
                # Add the file to the list
                files_in_conditions.append({
                    'rider_id': rider.id,
                    'rider_name': rider.name,
                    'filename': file,
                    'upload_date': file_date
                })

    # Order the files
    files_in_conditions = order_files(sort_by, files_in_conditions)

    # Calcular la paginación
    total = len(files_in_conditions)
    max_pages = (total + per_page - 1) // per_page  # Redondeo hacia arriba
    
    # Asegurar que la página sea válida
    page = max(1, min(page, max_pages))
    
    start = (page - 1) * per_page
    end = start + per_page
    files = files_in_conditions[start:end]

    return files, max_pages 


def get_file(file_id):
    """
    Get the file of a rider by file ID
    """
    user_file = File.query.filter(File.id == file_id).first()

    if user_file:
        rider_id = user_file.rider_id
        return minio.get_file(PREFIX, user_file.filename, rider_id)
    return None

def get_file_name(file_id):
        """
        Get the file name of a rider by file ID
        """
        user_file = File.query.filter(File.id == file_id).first()

        if user_file:
            return user_file.filename
        return None