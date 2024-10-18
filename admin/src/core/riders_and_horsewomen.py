from src.core import database
from flask import flash, redirect, url_for
from src.core import utils
from src.core import team_member as tm
from src.core.models.team_member import TeamMember
from src.core.models.riders_and_horsewomen import CaringProfessional, RiderAndHorsewoman, Tutor, WorkInInstitution
from sqlalchemy.orm import aliased
from src.web.forms import SecondTutorForm, FirstTutorForm, RiderHorsewomanForm, WorkInInstitutionForm


def create_enums():
    from src.core.models.riders_and_horsewomen import disability_certificate_enum, disability_type_enum, family_allowance_enum, pension_enum, days_enum, condition_enum, seat_enum, proposal_enum, education_level_enum

    disability_certificate_enum.create(database.db.engine, checkfirst=True)
    disability_type_enum.create(database.db.engine, checkfirst=True)
    family_allowance_enum.create(database.db.engine, checkfirst=True)
    pension_enum.create(database.db.engine, checkfirst=True)
    days_enum.create(database.db.engine, checkfirst=True)
    condition_enum.create(database.db.engine, checkfirst=True)
    seat_enum.create(database.db.engine, checkfirst=True)
    proposal_enum.create(database.db.engine, checkfirst=True)
    education_level_enum.create(database.db.engine, checkfirst=True)


def find_rider(dni):

    rider = RiderAndHorsewoman.query.filter_by(dni=dni).first()

    return rider

def create_caring_professional(id_rh, id_tm):
    """
    Create a caring professional
    """
    from src.core.models.riders_and_horsewomen import CaringProfessional

    caring= CaringProfessional(
        rider_horsewoman_id = id_rh,
        team_member_id = id_tm
    )

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
            dni = form["dni_first_tutor"],
            relationship = form["relationship_first_tutor"],
            name = form["name_first_tutor"],
            last_name = form["last_name_first_tutor"],
            address = form["address_first_tutor"],
            phone = form["phone_first_tutor"],
            email = form["email_first_tutor"],
            education_level = form["education_level_first_tutor"],
            occupation = form["occupation_first_tutor"],
            rider_and_horsewoman_id = id,
        )
        database.db.session.add(first_tutor)
        database.db.session.commit()

    
    if validation_second_tutor:
        second_tutor = Tutor(
            dni = form["dni_second_tutor"],
            relationship = form["relationship_second_tutor"],
            name = form["name_second_tutor"],
            last_name = form["last_name_second_tutor"],
            address = form["address_second_tutor"],
            phone = form["phone_second_tutor"],
            email = form["email_second_tutor"],
            education_level = form["education_level_second_tutor"],
            occupation = form["occupation_second_tutor"],
            rider_and_horsewoman_id = id
        )
        database.db.session.add(second_tutor)
        database.db.session.commit()

    if validation_first_tutor and validation_second_tutor:
        flash("Tutores creados exitosamente")
    elif validation_first_tutor:
        flash("Primer tutor creado exitosamente")
    else:
        flash("Segundo tutor creado exitosamente")


def create_work_in_institution(form, rider_horsewoman_id):
    """
    Create work in institution and the intermediate table
    """
    work_form = WorkInInstitutionForm(form)
    if work_form.validate():
        print(work_form.data)
        work = WorkInInstitution(
            proposal = form["proposal"],
            condition = form["condition"],
            seat = form["seat"],
            therapist = form["therapist"],
            rider_id = form["rider"],
            rider_horsewoman_id = rider_horsewoman_id,
            horse = form["horse"],
            track_assistant = form["track_assistant"],
            days = form.getlist("days")
        )

        database.db.session.add(work)
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
            dni = form["dni"],
            name = form["name"],
            last_name = form["last_name"],
            age = form["age"],
            date_of_birth = form["date_of_birth"],
            place_of_birth = form["place_of_birth"],
            address = form["address"],
            phone = form["phone"],
            emergency_contact = form["emergency_contact"],
            emergency_phone = form["emergency_phone"],
            scholarship_percentage = lista[0],
            observations = lista[1],
            disability_certificate = lista[3],
            others = lista[4],
            disability_type = lista[2],
            family_allowance = lista[5],
            pension = lista[6],
            name_institution = form["name_institution"],
            address_institution = form["address_institution"],
            phone_institution = form["phone_institution"],
            current_grade = form["current_grade"],
            observations_institution = form["observations_institution"],
            health_insurance_id = form["health_insurance"],
            membership_number = form["membership_number"],
            curatela = True if curatela == 'on' else False,
            pension_situation_observations = form["observations_institution"]
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

def find_all_riders(name=None, last_name=None, dni=None, order_by='asc', professional=None , page=1):

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
            query = query.filter(rider_alias_name.name.ilike(f'%{name}%'))
        
        # Filtro por apellido del rider
        if last_name:
            query = query.filter(rider_alias_last_name.last_name.ilike(f'%{last_name}%'))

    # filtro por professional
    if professional:
        query = query.join(RiderAndHorsewoman.team_members).filter(TeamMember.id == professional)

    # Ordeno por el campo adecuado
    if order_by == 'asc':
        query = query.order_by(RiderAndHorsewoman.name.asc())  # Puedes cambiarlo por el campo adecuado
    else:
        query = query.order_by(RiderAndHorsewoman.name.desc())  # Puedes cambiarlo por el campo adecuado

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
        rider.curatela = True if curatela == 'on' else False
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

   # Eliminar tutores asociados
    for tutor in rider.tutors:
        database.db.session.delete(tutor)

    # Eliminar relaciones con team_members a través de caring_professionals
    caring_professionals = CaringProfessional.query.filter_by(
        rider_horsewoman_id=rider.id
    ).all()  # Obtener todas las relaciones
    for caring_professional in caring_professionals:
        database.db.session.delete(caring_professional)

    # Eliminar relaciones con work_in_institution
    work_in_institutions = WorkInInstitution.query.filter_by(
        rider_horsewoman_id=rider.id
    ).all()  # Obtener todas las relaciones
    for work_in_institution in work_in_institutions:
        database.db.session.delete(work_in_institution)

    # Eliminar las colecciones relacionadas con el rider
    collections = rider.collections
    for collection in collections:
        database.db.session.delete(collection)

    # Finalmente eliminar el rider
    database.db.session.delete(rider)
    database.db.session.commit()

def get_work_in_institutions_by_rider_id(rider_id):
    """
    Get work in institution by rider id
    """
    work_in_institutions = WorkInInstitution.query.filter(WorkInInstitution.rider_horsewoman_id == rider_id).first()

    return work_in_institutions

def get_caring_professionals_by_rider_id(rider_id):
    """
    Get all caring professionals by rider id
    """
    caring_professionals = TeamMember.query.join(CaringProfessional).filter(CaringProfessional.rider_horsewoman_id == rider_id).all()

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
    num_of_tutors = Tutor.query.filter(Tutor.rider_and_horsewoman_id == rider_id).count()

    if num_of_tutors == 1:
        tutor1 = Tutor.query.filter(Tutor.rider_and_horsewoman_id == rider_id).first()
        tutor2 = None
    elif num_of_tutors == 2:
        tutor1 = Tutor.query.filter(Tutor.rider_and_horsewoman_id == rider_id).first()
        tutor2 = Tutor.query.filter(Tutor.rider_and_horsewoman_id == rider_id).all()[1]

    return tutor1, tutor2