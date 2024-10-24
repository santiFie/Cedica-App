from src.core import database   
from datetime import datetime
from src.core.models.equestrian import Equestrian
from src.core.models.team_member import JobEnum
from src.core import team_member as tm
from src.core import utils, minio
from flask import flash


db = database.db
PREFIX="ecuestres"

def equestrian_create(form, files):
    """
    Creates a new equestrian
    """

    # Convert the value of bought to a boolean for the database
    bought = True if form['bought'] == 'true' else False  

    # # Convert the string dates to date objects
    date_of_birth = utils.string_to_date(form['date_of_birth'])
    date_of_entry = utils.string_to_date( form['date_of_entry'])

    # Check if the dates are valid
    if not utils.validate_dates(date_of_birth, date_of_entry):
        return flash("Las fechas ingresadas no son válidas", "info")
    
    # Check if at least one team member is selected
    selected_emails = form.getlist("emails")
    if not selected_emails:
        return flash("Debe seleccionar al menos un entrenador o conductor", "info")
    
    # Check if the equestrian already exists
    equestrian = find_equestrian_by_name(form["name"])
    if equestrian:
        return flash("El equestre ya existe", "info")

    selected_emails = form.getlist("emails")
    if not selected_emails:
        return flash("Debe seleccionar al menos un entrenador o conductor", "info")

    # Create the equestrian
    equestrian = Equestrian(
        name=form["name"],
        date_of_birth=date_of_birth,
        sex=form["sex"],
        race=form["race"],
        coat=form["coat"],
        bought = bought,
        proposals = form.getlist("proposals"),
        date_of_entry=date_of_entry,
        headquarters=form["headquarters"]
    )

    try: # Save the equestrian to the database
        db.session.add(equestrian)
        db.session.flush()
    except:
        db.session.rollback()
        return flash("Error al crear el ecuestre", "info")
    try:
        for key, file in files.items():
            if file:
                minio.upload_file(prefix=PREFIX, file=file , user_id=equestrian.id)
                setattr(equestrian, key, file.filename)

        # Add the selected team members to the equestrianTeamMember table
        # It's possible to do this becourse the relationship between Equestrian and TeamMember is many to many and both have 'secondary' attribute
        
        for email in selected_emails:
            team_member = tm.find_team_member_by_email(email)
            if team_member:
                equestrian.team_members.append(team_member)
        db.session.flush()
    except:
        db.session.rollback()
        return flash("Error al cargar los archivos", "info")
    db.session.commit()

    return flash("Equestre creado exitosamente")


def update_equestrians_files(equestrian_id, files_dict):
    """
    Updates the files of the equestrian given by parameter
    """
    equestrian = find_equestrian_by_id(equestrian_id)

    if not equestrian:
        return flash("El equestre no existe", "info")
    


    for key, file in files_dict.items():
        if file:
            minio.delete_file(PREFIX, getattr(equestrian, key), equestrian.id)
            minio.upload_file(prefix=PREFIX, file=file, user_id=equestrian.id)
            setattr(equestrian, key, file.filename)


def equestrian_update(id, form, files):
    """
    Updates an equestrian
    """


    equestrian = Equestrian.query.filter_by(id=id).first()

    # Check if the equestrian exists
    if not equestrian:
        return flash("El equestre no existe", "info")
    
    # Convert the value of bought to a boolean for the database
    bought = True if form['bought'] == 'true' else False  

    # Convert the string dates to date objects
    date_of_birth = utils.string_to_date(form['date_of_birth'])
    date_of_entry = utils.string_to_date(form['date_of_entry'])

    # Check if the dates are valid
    if not utils.validate_dates(date_of_birth, date_of_entry):
        return flash("Las fechas ingresadas no son válidas", "info")
    
    # Check if at least one team member is selected
    selected_emails = form.getlist("emails")
    if not selected_emails:
        return flash("Debe seleccionar al menos un entrenador o cuidador", "info")
    
    # Add the proposals in the institution to the equestrian
    proposals = form.getlist("proposals")
    if proposals:
        equestrian.proposals = proposals
    

    # Update the equestrian
    equestrian.sex = form["sex"]
    equestrian.headquarters = form["headquarters"]
    equestrian.coat = form["coat"]
    equestrian.race = form["race"]
    equestrian.date_of_birth = date_of_birth
    equestrian.date_of_entry = date_of_entry
    equestrian.bought = bought
    
    update_equestrians_files(equestrian.id, files)

    # Delete all the team members of the equestrian
    equestrian.team_members.clear() 
    
    # Add the selected team members to the equestrianTeamMember table
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
    """
    Search for the equestrian with the given parameter
    """
    equestrian = Equestrian.query.filter_by(id=id).first()

    if not equestrian:
        return None, 404
    
    return equestrian

def list_equestrians(page=1, name=None, proposal=None, date_of_birth=None, date_of_entry= None, sort_by=None):
    """
    Search for all the equestrians with the given parameters
    """
    per_page = 25

    # General query, get all equestrians
    query = Equestrian.query

    # Optional filters
    if name:
        query = query.filter(Equestrian.name.ilike(f'%{name}%'))
    if proposal:
        query = query.filter(Equestrian.proposals.contains([proposal]))

    # Sorting
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
        
    total_files = query.count()

    # If there are no equestrians, ensure page is 1 and there is no pagination
    if total_files == 0:
        return [], 1
    
    max_pages = (total_files + per_page - 1) // per_page  # Round up
        
    # Ensure page is at least 1
    if page < 1:
        page = 1
    
    # Ensure the requested page is not greater than the maximum number of pages
    if page > max_pages:
        page = max_pages
        
    offset = (page - 1) * per_page
    equestrians = query.offset(offset).limit(per_page).all()

    return equestrians, max_pages 


def equestrian_delete(id):
    """
    Deletes the equestrian with the id given by parameter
    """
    equestrian = Equestrian.query.filter_by(id=id).first()
    

    if not equestrian:
        return flash("El equestre no existe", "info")
    
    try:
        # Delete all the files of the equestrian
        files = equestrian.get_files()
        for file in files:
            minio.delete_file(PREFIX,file,equestrian.id)

        # Delete the relationship between the equestrian and the team members
        equestrian.team_members.clear()
        
        # Delete the equestrian
        db.session.delete(equestrian)
        db.session.flush()
    except Exception as e:
        db.session.rollback()
        return flash("Error al eliminar el ecuestre", "info")
    
    db.session.commit()
    return flash("Equestre eliminado exitosamente")

def get_all_equestrians():
    """
    Search for all the equestrians
    """
    return Equestrian.query.all()

def order_files(sort_by, file):
    """
    Orders the files with the given parameters
    """
    if sort_by == 'name_asc':
        file.sort(key=lambda x: x['filename'])
    elif sort_by == 'name_desc':
        file.sort(key=lambda x: x['filename'], reverse=True)
    elif sort_by == 'downloaded_date_asc':
        file.sort(key=lambda x: x['upload_date'] or datetime.min)
    elif sort_by == 'downloaded_date_desc':
        file.sort(key=lambda x: x['upload_date'] or datetime.min, reverse=True)
    return file

def check_dates(initial_date, final_date):
    """
    Checks the dates given by parameter
    """
    # Parse the dates outside the loop
    if initial_date:
        initial_date = datetime.strptime(initial_date, '%Y-%m-%d')
        if initial_date > datetime.now():
            return False
    if final_date:
        final_date = datetime.strptime(final_date, '%Y-%m-%d')

    # Check if the dates are valid
    if not utils.validate_dates(initial_date, final_date):
        return False
    
    return True

def list_equestrians_files(page=1, name=None, initial_date=None, final_date=None, sort_by=None):
    """
    Search for all the files of the equestrians with the given parameters
    """
    per_page = 25

    # Get all the ecuestrians
    equestrians = Equestrian.query.all()
    # Create a list to store the files that meet the conditions
    files_in_conditions = []

    # Parse the dates outside the loop
    if initial_date:
        initial_date = datetime.strptime(initial_date, '%Y-%m-%d')
        if initial_date > datetime.now():
            flash("No se pueden listar archivos que no fueron subidos aún", "info")
            return [], 1
    if final_date:
        final_date = datetime.strptime(final_date, '%Y-%m-%d')

    if final_date and initial_date:
        # Check if the dates are valid
        if not utils.validate_dates(initial_date, final_date):
            flash("Las fechas ingresadas no son válidas", "info")
            return [], 1

    # Iterate over all the equestrians
    for equestrian in equestrians:
        # Get the files of the equest
        equestrian_files = equestrian.get_files()
        for file in equestrian_files:
            if file:
                # Get the date of the file
                file_date = minio.get_file_date(prefix=PREFIX, user_id=equestrian.id, filename=file)
            
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
                    'equestrian_id': equestrian.id,
                    'equestrian_name': equestrian.name,
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
