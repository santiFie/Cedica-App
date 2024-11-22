from datetime import datetime
from core import minio
from src.core import database
from flask import flash, redirect, url_for
from src.core import utils
from src.core import team_member as tm
from src.core.models.team_member import TeamMember
from src.core.models.riders_and_horsewomen import File, RiderAndHorsewoman
from src.core.models.riders_and_horsewomen import CaringProfessional, Tutor, WorkInInstitution
from sqlalchemy.orm import aliased
from sqlalchemy import func
from src.web.forms.RiderAndHorsewomanForm import (
    SecondTutorForm,
    FirstTutorForm,
    RiderHorsewomanForm,
    WorkInInstitutionForm,
)

PREFIX="Jinetes y Amazonas"

def create_enums():
    """
    Creates the enums values for riders and horsewomen
    """
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
    """
    Search for the rider or horsewomen with the given parameter
    """

    rider = RiderAndHorsewoman.query.filter_by(dni=dni).first()

    return rider


def create_caring_professional(id_rh, id_tm):
    """
    Create a caring professional
    """
    from src.core.models.riders_and_horsewomen import CaringProfessional

    caring = CaringProfessional(rider_horsewoman_id=id_rh, team_member_id=id_tm)

    database.db.session.add(caring)
    database.db.session.flush()

    return caring


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
        try:
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
            database.db.session.flush()
        except Exception as e:
            database.db.session.rollback()
            flash("Error al crear el primer tutor", "error")
            raise e

    if validation_second_tutor:
        try: 
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
            database.db.session.flush()
        except Exception as e:
            database.db.session.rollback()
            flash("Error al crear el segundo tutor", "error")
            raise e



def create_work_in_institution(form, rider_horsewoman_id):
    """
    Create work in institution and the intermediate table
    """
    work_form = WorkInInstitutionForm(form)
    if work_form.validate():
        try: 
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
            database.db.session.flush()

        except Exception as e:
            database.db.session.rollback()
            flash("Error al crear el trabajo en institución", "error")
            raise e
    else:
        for field, errors in work_form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}")


def create_rider_horsewoman(form, files):
    """
    Create a new rider or horsewoman and dependencys
    """
    from src.core.models.riders_and_horsewomen import RiderAndHorsewoman

    try: 

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
            try:
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
                    pension_situation_observations=form["pension_situation_observations"],
                )

                database.db.session.add(rider_horsewoman)
                database.db.session.flush()
            except Exception as e:
                database.db.session.rollback()
                raise e
        else:
            utils.riders_and_horsewomen_errors(riders_form)
            return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_new"))

        # Use a set in order to avoid duplicates
        professionals_set = set()
        # Add the caring professionals to the set
        for i in range(1, 6):
            id_key = f"select_pro_{i}"
            if form.get(id_key):
                professionals_set.add(form[id_key])
        
        # Create the caring professionals
        for professional_id in professionals_set:
            create_caring_professional(rider_horsewoman.id, professional_id)

        # Tutors
        create_tutors(form, rider_horsewoman.id)

        # Work In Institution
        create_work_in_institution(form, rider_horsewoman.id)

        rider_id = rider_horsewoman.id

        for i in range(1, 4):  # Assuming there are 3 sets of file/link inputs
            link = form.get(f"select_link_{i}")
            filename = form.get(f"file_name_{i}")
            file_type = form.get(f"type_select_file_{i}")
            
            if file_type != "":
                if link != "":
                    new_link(link, filename, rider_id, file_type)
                elif filename != "":
                    file = files[f"select_file_{i}"]
                    new_file(file, filename, file_type, rider_id)

        database.db.session.commit()

    except Exception as e:
        database.db.session.rollback()
        raise(e)
        flash("Error al crear el jinete/Amazona", "error")


def find_all_riders(name=None, last_name=None, dni=None, order_by='asc', professional=None , page=1):
    """
    Search for all riders and horsewomen with the given parameters
    """

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
            query = query.filter(rider_alias_last_name.last_name.ilike(f'%{last_name}%'))

    # filtro por professional
    if professional:
        query = query.join(RiderAndHorsewoman.team_members).filter(TeamMember.id == professional)

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


def update(id, form, selected_professionals, files):
    """
    Update a rider or horsewoman. Returns True if the rider was updated successfully, False otherwise.
    """

    rider = get_rider_by_id(id)

    if not rider:
        return False

    try:
        # Process boolean fields
        lista = process_boolean_fields(form)
        
        # Update main data
        update_rider_main_data(rider, form, lista)

        # Update caring professionals, tutors and work in institution
        update_caring_professionals(selected_professionals, id)
        update_tutors(form, id)
        update_work_in_institution(form, id)

        # Process files and links
        process_files_and_links(form, files, rider.id)

        database.db.session.commit()

        flash("El jinete/Amazona se ha actualizado exitosamente")
    except Exception as e:
        database.db.session.rollback()
        flash("Error al actualizar el jinete/Amazona", "error")
        

    
def process_boolean_fields(form):
    """
    Procesa los campos booleanos y retorna la lista de valores
    """
    lista = []
    
    # Obtener valores booleanos con valor por defecto False
    scholarship_boolean = form.get("scholarship_boolean", False)
    disability_certificate_boolean = form.get("disability_certificate_boolean", False)
    family_allowance_boolean = form.get("family_allowance_boolean", False)
    pension_boolean = form.get("pension_boolean", False)
    
    # Procesar beca
    if scholarship_boolean:
        lista.extend([
            form.get("scholarship_percentage"),
            form.get("observations_scholarship", None)
        ])
    else:
        lista.extend([None, None])
    
    # Procesar certificado de discapacidad
    if disability_certificate_boolean:
        lista.extend([
            form.get("disability_type"),
            form.get("disability_certificate"),
            form.get("disability_certificate_otro") if form.get("disability_certificate") == "OTRO" else None
        ])
    else:
        lista.extend([None, None, None])
    
    # Procesar asignación familiar y pensión
    lista.append(form.get("family_allowance") if family_allowance_boolean else None)
    lista.append(form.get("pension") if pension_boolean else None)
    return lista

def update_rider_main_data(rider, form, lista):
    """
    Actualiza los datos principales del rider
    """
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
    rider.curatela = form.get("curatela") == "on"
    rider.pension_situation_observations = form["observations_institution"]

def process_files_and_links(form, files, rider_id):
    """
    Procesa los archivos y enlaces
    """
    for i in range(1, 4):
        link = form.get(f"select_link_{i}", "")
        filename = form.get(f"file_name_{i}", "")
        file_type = form.get(f"type_select_file_{i}")
        
        if link:
            new_link(link, filename, rider_id, file_type)
        elif filename:
            file = files.get(f"select_file_{i}")
            if file:
                new_file(file, filename, file_type, rider_id)

def update_caring_professionals(new_professionals, id):
    """
    Update caring professionals
    """
    caring_professionals = get_caring_professionals_by_rider_id(id)

    existing_professionals = {cp.id for cp in caring_professionals}

    if new_professionals:
        try:
            # Delete caring professionals that are no longer selected
            for cp in caring_professionals:
                if cp.id not in new_professionals:
                    carring = CaringProfessional.query.filter_by(team_member_id=cp.id).first()
                    database.db.session.delete(carring)

            # Add new caring professionals
            for professional_id in new_professionals - existing_professionals:
                create_caring_professional(id, professional_id)

            database.db.session.flush()
        except Exception as e:
            database.db.session.rollback()
            flash("Error al actualizar los profesionales a cargo", "error")
            raise e

def update_tutors(form, id):
    """
    Update tutors
    """

    first_tutor = Tutor.query.filter(Tutor.rider_and_horsewoman_id == id).first()
    
    if form.get("dni_second_tutor"):
        second_tutor = Tutor.query.filter(Tutor.rider_and_horsewoman_id == id).all()[1]
    else:
        second_tutor = None

    try: 
        first_tutor.dni = form["dni_first_tutor"]
        first_tutor.relationship = form["relationship_first_tutor"]
        first_tutor.name = form["name_first_tutor"]
        first_tutor.last_name = form["last_name_first_tutor"]
        first_tutor.address = form["address_first_tutor"]
        first_tutor.phone = form["phone_first_tutor"]
        first_tutor.email = form["email_first_tutor"]
        first_tutor.education_level = form["education_level_first_tutor"]
        database.db.session.commit()
    except Exception as e:
        database.db.session.rollback()
        flash("Error al actualizar el primer tutor", "error")
        raise e

    if second_tutor:
        try:
            second_tutor.dni = form["dni_second_tutor"]
            second_tutor.relationship = form["relationship_second_tutor"]
            second_tutor.name = form["name_second_tutor"]
            second_tutor.last_name = form["last_name_second_tutor"]
            second_tutor.address = form["address_second_tutor"]
            second_tutor.phone = form["phone_second_tutor"]
            second_tutor.email = form["email_second_tutor"]
            second_tutor.education_level = form["education_level_second_tutor"]

            database.db.session.commit()
        except Exception as e:
            database.db.session.rollback()
            flash("Error al actualizar el segundo tutor", "error")
            raise e



def update_work_in_institution(form, id):
    """
    Update work in institution and the intermediate table
    """
    
    work = get_work_in_institutions_by_rider_id(id)

    try: 
        work.proposal = form["proposal"]
        work.condition = form["condition"]
        work.seat = form["seat"]
        work.therapist = form["therapist"]
        work.rider = form["rider"]
        work.horse = form["horse"]
        work.track_assistant = form["track_assistant"]
        work.days = form.getlist("days")

        database.db.session.flush()

    except Exception as e:
        database.db.session.rollback()
        flash("Error al actualizar el trabajo en institución", "error")
        raise e


    return redirect(url_for("riders_and_horsewomen.riders_and_horsewomen_edit", id=id))


def delete_a_rider(rider):
    """
    Deletes the rider or horsewoman given by parameter and all their related entities from the database
    """

    # Delete associated tutors
    for tutor in rider.tutors:
        database.db.session.delete(tutor)

    # Delete relationships with team_members through caring_professionals
    caring_professionals = CaringProfessional.query.filter_by(
        rider_horsewoman_id=rider.id
    ).all()  # Get all relationships
    for caring_professional in caring_professionals:
        database.db.session.delete(caring_professional)

    # Delete relationships with work_in_institution
    work_in_institutions = WorkInInstitution.query.filter_by(
        rider_horsewoman_id=rider.id
    ).all()  # Get all relationships
    for work_in_institution in work_in_institutions:
        database.db.session.delete(work_in_institution)

    # Delete collections related to the rider
    collections = rider.collections
    for collection in collections:
        database.db.session.delete(collection)

    # Delete files related to the rider
    files = rider.get_files()
    for file in files:
        if file.is_link:
            delete_link(file.id)
        else:
            delete_file(rider.id, file.id)
                    

    # Finally, delete the rider
    database.db.session.delete(rider)
    database.db.session.commit()

    return True



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


def new_file(file, filename, file_type, rider_id):
    """
    Create a new file for a rider
    """

    rider = get_rider_by_id(rider_id)
    if not rider:
        flash("No se encontró el jinete/Amazona", "error")
    
    try:
        user_file = File(filename=filename, file_type=file_type, rider_id=rider_id)

        minio.upload_file(PREFIX, file, rider_id, filename)
        database.db.session.add(user_file)
        database.db.session.flush()
    except Exception as e:
        database.db.session.rollback()
        flash("Error al subir el archivo", "error")
        raise e 
    
def new_link(link, filename, rider_id, file_type):
    """
    Create a new link for a rider
    """

    rider = get_rider_by_id(rider_id)

    if rider:
        file = File(filename=filename,is_link=True,  file_type=file_type, rider_id=rider_id)
        database.db.session.add(file)
        database.db.session.commit()

        minio.upload_link(PREFIX, link, filename, rider_id)

def delete_file(rider_id, file_id):
    """
    Delete the file of a rider
    """
    user_file = File.query.filter_by(id = file_id).first()
    
    if user_file:
        minio.delete_file(PREFIX, user_file.filename, rider_id)
        File.query.filter(File.id == file_id).delete()
        database.db.session.commit()

def get_link(link_id):
    """
    Get the link of a rider
    """
    user_file = File.query.filter_by(id = link_id).first()


    if user_file:
        rider_id = user_file.rider_id
        return minio.get_link(PREFIX, user_file.filename, rider_id)
    
    return None

def order_files(sort_by, file):
    """
    Orders the files with the given parameters
    """
    if sort_by == 'name_asc':
        file.sort(key=lambda x: x['file'].filename)
    elif sort_by == 'name_desc':
        file.sort(key=lambda x: x['file'].filename, reverse=True)
    elif sort_by == 'upload_date_asc':
        file.sort(key=lambda x: x['file'].created_at or datetime.min)
    elif sort_by == 'upload_date_desc':
        file.sort(key=lambda x: x['file'].created_at or datetime.min, reverse=True)
    return file


def list_riders_files(page=1, name=None, initial_date=None, final_date=None, sort_by=None):
    """
    List all the files of the riders that meet the conditions
    """
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
        if not utils.validate_dates(initial_date, final_date):
            flash("Las fechas ingresadas no son válidas")
            return [], 1

    # Iterate over all the riders
    for rider in riders:
        # Get the files of the rider
        rider_files = [file.filename for file in rider.get_files()]
        for file in rider_files:
            if file:
                # Get the date of the file
                user_file = File.query.filter_by(filename = file, rider_id = rider.id).first()
                file_date = user_file.created_at

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
                    'file': get_file_by_name_and_rider_id(file, rider.id),
                    'upload_date': file_date.strftime('%Y-%m-%d %H:%M')
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

def get_file_by_name_and_rider_id(filename, rider_id):
    """
    Search for the file with the given parameters
    """

    user_file = File.query.filter_by(filename = filename, rider_id = rider_id).first()

    if user_file:
        return user_file
    return None

def get_file(file_id):
    """
    Get the file of a rider by file ID
    """
    user_file = File.query.filter_by(id=file_id).first()

    if user_file:
        rider_id = user_file.rider_id
        return  minio.get_file(PREFIX, rider_id, user_file.filename)
    return None

def get_filename(file_id):
    """
    Get the file name of a rider by file ID
    """

    user_file = File.query.filter_by(id=file_id).first()
    
    if user_file:
        return user_file.filename
    return None

def delete_link(link_id):
    """
    Delete link of a rider by link ID
    """
    link_file = File.query.filter_by(id=link_id).first()
    filename = f"{link_file.filename}.txt"
    minio.delete_file(PREFIX, filename, link_file.rider_id)
    File.query.filter(File.id == link_id).delete()
    database.db.session.commit()

def get_days_by_id(id):
    """
    Get the days of a rider by ID
    """
    work = WorkInInstitution.query.filter_by(rider_horsewoman_id = id).first()
    if work:
        return work.days
    
    return None

def get_files_by_rider_id(rider_id):
    """
    Get all the files of a rider by rider ID
    """
    files = File.query.filter_by(rider_id = rider_id).all()

    if files:
        return files
    return None


def get_scolarship():

    riders = RiderAndHorsewoman.query.filter(RiderAndHorsewoman.scholarship_percentage.isnot(None)).count()
    
    return riders

def get_no_scolarship():

    riders = RiderAndHorsewoman.query.filter(RiderAndHorsewoman.scholarship_percentage.is_(None)).count()
    
    return riders

def get_disability_types():

    disabilitys = (
        database.db.session.query(
            RiderAndHorsewoman.disability_type,
            func.count(RiderAndHorsewoman.disability_type).label('count')
        )
        .filter(RiderAndHorsewoman.disability_type.isnot(None))
        .group_by(RiderAndHorsewoman.disability_type)
        )
    
    return disabilitys

def get_debtors():

    debtors = RiderAndHorsewoman.query.filter(RiderAndHorsewoman.debtor.is_(True)).all()

    return debtors