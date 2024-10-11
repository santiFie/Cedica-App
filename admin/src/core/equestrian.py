from src.core import database   
from src.core.models.equestrian import Equestrian
from src.core import team_member as tm
from src.core import utils
from flask import flash


db = database.db

def equestrian_create(form):
    """
    Creates a new equestrian
    """

    # Convert the value of bought to a boolean for the database
    bought = True if form['bought'] == 'true' else False  

    # Convert the string dates to date objects
    date_of_birth = utils.string_to_date(form['date_of_birth'])
    date_of_entry = utils.string_to_date( form['date_of_entry'])

    # Check if the dates are valid
    if not utils.validate_dates(date_of_birth, date_of_entry):
        return flash("Las fechas ingresadas no son válidas")
    
    # Check if at least one team member is selected
    selected_emails = form.getlist("emails")
    if not selected_emails:
        return flash("Debe seleccionar al menos un entrenador o conductor")
    
    # Check if the equestrian already exists
    equestrian = find_equestrian_by_name(form["name"])
    if equestrian:
        return flash("El equestre ya existe")
   
    # Add the jobs in the institution to the equestrian    
    jobs_in_institution = form.getlist("jobs_in_institution")
    if jobs_in_institution:
        equestrian.jobs_in_institution = jobs_in_institution

    # Create the equestrian
    equestrian = Equestrian(
        name=form["name"],
        date_of_birth=date_of_birth,
        sex=form["sex"],
        race=form["race"],
        coat=form["coat"],
        bought = bought,
        date_of_entry=date_of_entry,
        headquarters=form["headquarters"]
    )

    # Save the equestrian to the database
    db.session.add(equestrian)
    db.session.commit()

    

    # Add the selected team members to the equestrianTeamMember table
    # It's possible to do this becourse the relationship between Equestrian and TeamMember is many to many and both have 'secondary' attribute
    for email in selected_emails:
        team_member = tm.find_team_member_by_email(email)
        if team_member:
            equestrian.team_members.append(team_member)

    db.session.commit()
    
    return flash("Equestre creado exitosamente")



def equestrian_update(id, form):
    """
    Updates an equestrian
    """

    equestrian = Equestrian.query.filter_by(id=id).first()

    # Check if the equestrian exists
    if not equestrian:
        return flash("El equestre no existe")
    
    # Convert the value of bought to a boolean for the database
    bought = True if form['bought'] == 'true' else False  

    # Convert the string dates to date objects
    date_of_birth = utils.string_to_date(form['date_of_birth'])
    date_of_entry = utils.string_to_date(form['date_of_entry'])

    # Check if the dates are valid
    if not utils.validate_dates(date_of_birth, date_of_entry):
        return flash("Las fechas ingresadas no son válidas")
    
    # Check if at least one team member is selected
    selected_emails = form.getlist("emails")
    if not selected_emails:
        return flash("Debe seleccionar al menos un entrenador o cuidador")
    
    # Add the jobs in the institution to the equestrian
    jobs_in_institution = form.getlist("jobs")
    if jobs_in_institution:
        equestrian.jobs_in_institution = jobs_in_institution
    
    # Check if the name already exists for other equestrian
    equestrian = find_equestrian_by_name(form["name"])
    if equestrian.id != id:
        return flash("El equestre ya existe")

    # Update the equestrian
    equestrian.date_of_birth = date_of_birth

    # Eliminar todos los miembros del equipo del equestre
    equestrian.team_members.clear() 
    
    # Agregar los miembros del equipo seleccionados
    for email in selected_emails:
        team_member = tm.find_team_member_by_email(email)
        if team_member:
            equestrian.team_members.append(team_member)
    
    # Save the equestrian to the database
    db.session.commit()
    
    return flash("Equestre actualizado exitosamente")

def find_equestrian_by_name(name):
    """
    Find an equestrian by name
    """
    return Equestrian.query.filter_by(name=name).first()

def find_equestrian_by_id(id):
    equestrian = Equestrian.query.filter_by(id=id).first()

    if not equestrian:
        return None, 404
    
    return equestrian