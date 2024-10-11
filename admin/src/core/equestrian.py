from src.core import database   
from src.core.models.equestrian import Equestrian
from src.core.models.team_member import JobEnum
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
   
    # Add the proposals in the institution to the equestrian    
    proposals = form.getlist("proposals")
    if proposals:
        equestrian.proposals = proposals

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
    
    # Add the proposals in the institution to the equestrian
    proposals = form.getlist("proposals")
    if proposals:
        equestrian.proposals = proposals
    
    # Check if the name already exists for other equestrian
    equestrian = find_equestrian_by_name(form["name"])
    if equestrian.id != id:
        return flash("El equestre ya existe")

    # Update the equestrian
    equestrian.name = form["name"]
    equestrian.sex = form["sex"]
    equestrian.headquarters = form["headquarters"]
    equestrian.coat = form["coat"]
    equestrian.race = form["race"]
    equestrian.date_of_birth = date_of_birth
    equestrian.date_of_entry = date_of_entry
    equestrian.bought = bought

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

def list_equestrians(page=1, name=None, proposal=None, date_of_birth=None, date_of_entry= None, sort_by=None):
    per_page = 25

    # consulta general, obtengo todos los usuarios
    query = Equestrian.query

    # Filtros opcionales
    if name:
        query = query.filter(Equestrian.name.ilike(f'%{name}%'))
    if proposal:
        query = query.filter(Equestrian.proposals.contains([proposal]))

    # Ordenamiento
    if sort_by == 'name_asc':
        query = query.order_by(Equestrian.name.asc())
    elif sort_by == 'name_desc':
        query = query.order_by(Equestrian.name.desc())
    elif sort_by == 'date_of_birth_asc':
        query = query.order_by(Equestrian.date_of_birth.asc())
    elif sort_by == 'date_of_birth_desc':
        query = query.order_by(Equestrian.date_of_birth.desc())
    elif sort_by == 'date_of_entry_asc':
        query = query.order_by(Equestrian.date_of_entry.asc())
    elif sort_by == 'date_of_entry_desc':
        query = query.order_by(Equestrian.date_of_entry.desc())
        
    total_equestrians = query.count()

    # Si no hay usuarios, aseguramos que page sea 1 y no haya paginación
    if total_equestrians == 0:
        return [], 1
    
    max_pages = (total_equestrians + per_page - 1) // per_page  # Redondeo hacia arriba
        
    # Aseguramos que page sea al menos 1
    if page < 1:
        page = 1
    
    # Aseguramos que la página solicitada no sea mayor que el número máximo de páginas
    if page > max_pages:
        page = max_pages
        
    offset = (page - 1) * per_page
    equestrians = query.offset(offset).limit(per_page).all()

    return equestrians, max_pages 