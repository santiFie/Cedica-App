from src.core import contact
from src.web.schema.contact import contact_schema as contact_api
from flask import Blueprint, request, jsonify
import requests

bp = Blueprint("contacts_api", __name__, url_prefix="/api/contacts")

CAPTCHA_SECRET = "6LeGsYIqAAAAANY5iswWl9mEPhPprgvmKeWDzPPQ"


def verify_captcha(token):
    """
    Verifies the provided reCAPTCHA token with Google's reCAPTCHA API.
    Args:
        token (str): The reCAPTCHA token to be verified.
    Returns:
        bool: True if the reCAPTCHA verification is successful, False otherwise.
    Raises:
        requests.RequestException: If there is an error during the request to the reCAPTCHA API.
    """
    url = "https://www.google.com/recaptcha/api/siteverify"
    # campos que se agregan a la url para verificar el captcha
    payload = {"secret": CAPTCHA_SECRET, "response": token}
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("success", False)

    except requests.RequestException as e:
        return False


@bp.post("/register")
def create_contact():
    """
    Endpoint to create a new contact.
    This endpoint expects a JSON payload with the contact details and a captcha token.
    It validates the input data and captcha, creates a new contact if the data is valid,
    and returns the created contact in JSON format.
    Returns:
        Response: JSON response containing the created contact data and HTTP status code 201 if successful.
        Response: JSON response containing error messages and HTTP status code 400 if validation fails.
        Response: JSON response containing an error message and HTTP status code 500 if an exception occurs.
    Raises:
        Exception: If an unexpected error occurs during the contact creation process.
    """
    try:

        if not request.json:
            return jsonify({"error": "Request must be JSON"}), 400

        attrs = request.json
        errors = contact_api.validate(attrs)

        # Verificar el captcha
        captcha_token = request.json.get("captcha")
        if not captcha_token or not verify_captcha(captcha_token):
            return (
                jsonify({"error": "Captcha inválido, por favor inténtalo de nuevo."}),
                400,
            )

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
        return jsonify({"error": str(e)}), 500
