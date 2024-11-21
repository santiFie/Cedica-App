from src.core.database import db
from src.core.models.contact import Contact


def create_contact(**kwargs):
    # Crear una instancia de Contacto usando los datos pasados como kwargs
    new_contact = Contact(
        name=kwargs.get('name'),
        last_name=kwargs.get('last_name'),
        email=kwargs.get('email'),
        message=kwargs.get('message'),
        state=kwargs.get('state', 'Pendiente'),  # Estado por defecto si no se pasa
        comment=kwargs.get('comment', '')  # Comentario vacío si no se pasa
    )

    # Agregar el nuevo contacto a la sesión y guardar en la base de datos
    db.session.add(new_contact)
    db.session.commit()

    return new_contact


def list_contacts():
    # Obtener todos los contactos de la base de datos
    return Contact.query.all()


def find_contacts(page=1, order='asc', state=None):
    
    per_page = 25

    query = Contact.query

    if state:
        query = query.filter(Contact.state == state)
    
    if order == 'asc':
        query = query.order_by(Contact.created_at.asc())
    else:
        query = query.order_by(Contact.created_at.desc())

    total_contacts = query.count()

    if total_contacts == 0:
        return [], 0
    
    max_pages = (total_contacts + per_page - 1) // per_page

    if page < 1:
        page = 1
    
    if page > max_pages:
        page = max_pages

    offset = (page - 1) * per_page
    contacts = query.offset(offset).limit(per_page).all()
    
    return contacts, max_pages

def find_contact(contact_id):
    return Contact.query.filter_by(id=contact_id).first()

def delete_contact(contact):
    db.session.delete(contact)
    db.session.commit()

    return True
    

def add_comment(contact, comment):
    contact.comment = comment
    contact.state = 'Resuelto'
    db.session.commit()

    return contact

def block(contact, block):
    contact.state = block
    db.session.commit()

    return contact