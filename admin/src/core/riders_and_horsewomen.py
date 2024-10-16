from src.core import database
from flask import flash
from src.core import utils

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
    from src.core.models.riders_and_horsewomen import RiderAndHorsewoman

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

def create_tutor(form, id):
    """
    Create tutor
    """
    from src.core.models.riders_and_horsewomen import Tutor

    tutor = Tutor(
        dni = form["dni_first_tutor"],
        relationship = form["relationship_first_tutor"],
        name = form["name_first_tutor"],
        last_name = form["last_name_first_tutor"],
        address = form["address_first_tutor"],
        phone = form["phone_first_tutor"],
        email = form["email_first_tutor"],
        education_level = form["education_level_first_tutor"],
        occupation = form["occupation_first_tutor"],
        rider_and_horsewoman_id = id
    )

    database.db.session.add(tutor)
    database.db.session.commit()

    return flash("tutor creado exitosamente")


def create_rider_horsewoman(form):
    """
    Create a new rider or horsewoman and dependencys
    """
    from src.core.models.riders_and_horsewomen import RiderAndHorsewoman
    from src.core.team_member import check_team_member_by_email

    lista = []
    if form["scholarship_boolean"]:
        lista.append(form["scholarship_percentage"])
        if form["observations_scholarship"]:
            lista.append(form["observations_scholarship"])
        else:
            lista.append(None)
    else:
        lista.append(None)
        lista.append(None)

    if form["disability_certificate_boolean"]:
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

    if form["family_allowance_boolean"]:
        lista.append(form["family_allowance"])
    else:
        lista.append(None)
    if form["pension_boolean"]:
        lista.append(form["pension"])
    else:
        lista.append(None)

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
    )

    database.db.session.add(rider_horsewoman)
    database.db.session.commit()

    rider = find_rider(form["dni"])
    member = check_team_member_by_email(form["email_member"])
    create_caring_professional(rider.id,member.id)
    create_tutor(form, rider.id)
    return flash("Miembro de equipo creado exitosamente")