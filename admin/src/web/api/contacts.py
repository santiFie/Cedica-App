from src.core import contact
from src.web.schema.contact import contact_schema as contact_api
from flask import Blueprint, request, jsonify

bp = Blueprint('contacts_api', __name__, url_prefix='/api/contacts')


@bp.post('/register')
def create_contact():
    try:

        if not request.json:
            return jsonify({"error": "Request must be JSON"}), 400

        attrs = request.json
        errors = contact_api.validate(attrs)

        if errors:
            return jsonify(errors), 400
        
        # cargo los datos ya validados
        kwars = contact_api.load(attrs)
        # creo el contacto
        new_contact = contact.create_contact(**kwars)
        # serializo el contacto creado para que sea mas facil de enviar en formato json
        data = contact_api.dump(new_contact)
        
        return jsonify(data), 201
    
    except Exception as e:
        return jsonify({"error":str(e)}), 500