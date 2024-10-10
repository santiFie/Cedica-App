from src.core import database   
from src.core.models.equestrian import Equestrian
from src.core import team_member as tm


db = database.db


def equestrian_create(form):
    """
    Creates a new equestrian
    """
    
    bought = form['bought'] # O cualquier fuente de datos
    bought = True if bought == 'true' else False  # Convertir el valor

    

    equestrian = Equestrian(
        name=form["name"],
        date_of_birth=form["date_of_birth"],
        sex=form["sex"],
        race=form["race"],
        coat=form["coat"],
        bought = bought,
        date_of_entry=form["date_of_entry"],
        headquarters=form["headquarters"]
    )

    db.session.add(equestrian)
    db.session.commit()

    emails = form.getlist("emails")

    # Añadir el equipo a los entrenadores relacionados de una manera más directa
    # Esto se puede hacer así porque los modelos de Equestrian y TeamMember están relacionados mediante una relación many-to-many usnado secondary
    for email in emails:
        team_member = tm.find_team_member_by_email(email)
        if team_member:
            equestrian.team_members.append(team_member)

    db.session.commit()
    
    return equestrian

def find_equestrian_by_name(name):
    """
    Find an equestrian by name
    """
    return Equestrian.query.filter_by(name=name).first()