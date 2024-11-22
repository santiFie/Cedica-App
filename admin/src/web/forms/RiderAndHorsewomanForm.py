from wtforms import (
    Form,
    StringField,
    IntegerField,
    DateField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Regexp,
    NumberRange,
    Email,
)
from datetime import date

DATA_REQUIRED_MESSAGE = "El campo no puede estar vacio."

class RiderHorsewomanForm(Form):
    name = StringField(
        "name",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    dni = StringField(
        "dni",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{8}$", message="El DNI debe tener 8 dígitos numéricos."
            ),
        ],
    )
    last_name = StringField(
        "last_name",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    age = IntegerField(
        "age",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            NumberRange(min=0, max=99),
        ],
    )
    place_of_birth = StringField(
        "place_of_birth",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    date_of_birth = DateField(
        "date_of_birth",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            lambda form, field: field.data <= date.today(),
        ],
    )
    address = StringField(
        "address",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=80, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    phone = StringField(
        "phone",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    emergency_contact = StringField(
        "emergency_contact",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    emergency_phone = StringField(
        "emergency_phone",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    name_institution = StringField(
        "name_intitution",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    address_institution = StringField(
        "address_institution",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=80, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    phone_institution = StringField(
        "phone_institution",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    current_grade = StringField(
        "current_grade",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    dni_first_tutor = StringField(
        "dni_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{8}$", message="El DNI debe tener 8 dígitos numéricos."
            ),
        ],
    )
    relationship_first_tutor = StringField(
        "relationship_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    name_first_tutor = StringField(
        "name_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    last_name_first_tutor = StringField(
        "last_name_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    address_first_tutor = StringField(
        "address_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=80, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    phone_first_tutor = StringField(
        "phone_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    email_first_tutor = StringField(
        "email_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Email(message="Ingresa una dirección de correo válida."),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    occupation_first_tutor = StringField(
        "occupation_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    membership_number = StringField(
        "membership_number",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{1,20}$",
                message="El numero de afiliado debe tener entre 1 y 20 digitos.",
            ),
        ],
    )

class RiderHorsewomanEditForm(Form):
    name = StringField(
        "name",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    last_name = StringField(
        "last_name",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    age = IntegerField(
        "age",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            NumberRange(min=0, max=99),
        ],
    )
    place_of_birth = StringField(
        "place_of_birth",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    date_of_birth = DateField(
        "date_of_birth",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            lambda form, field: field.data <= date.today(),
        ],
    )
    address = StringField(
        "address",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=80, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    phone = StringField(
        "phone",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    emergency_contact = StringField(
        "emergency_contact",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    emergency_phone = StringField(
        "emergency_phone",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    name_institution = StringField(
        "name_intitution",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    address_institution = StringField(
        "address_institution",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=80, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    phone_institution = StringField(
        "phone_institution",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    current_grade = StringField(
        "current_grade",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    dni_first_tutor = StringField(
        "dni_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{8}$", message="El DNI debe tener 8 dígitos numéricos."
            ),
        ],
    )
    relationship_first_tutor = StringField(
        "relationship_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    name_first_tutor = StringField(
        "name_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    last_name_first_tutor = StringField(
        "last_name_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    address_first_tutor = StringField(
        "address_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=80, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    phone_first_tutor = StringField(
        "phone_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    email_first_tutor = StringField(
        "email_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Email(message="Ingresa una dirección de correo válida."),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    occupation_first_tutor = StringField(
        "occupation_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    membership_number = StringField(
        "membership_number",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{1,20}$",
                message="El numero de afiliado debe tener entre 1 y 20 digitos.",
            ),
        ],
    )

class FirstTutorForm(Form):
    dni_first_tutor = StringField(
        "dni_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{8}$", message="El DNI debe tener 8 dígitos numéricos."
            ),
        ],
    )
    relationship_first_tutor = StringField(
        "relationship_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    name_first_tutor = StringField(
        "name_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    last_name_first_tutor = StringField(
        "last_name_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    address_first_tutor = StringField(
        "address_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=80, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    phone_first_tutor = StringField(
        "phone_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    email_first_tutor = StringField(
        "email_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Email(message="Ingresa una dirección de correo válida."),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    occupation_first_tutor = StringField(
        "occupation_first_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )


class SecondTutorForm(Form):
    dni_second_tutor = StringField(
        "dni_second_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{8}$", message="El DNI debe tener entre 8 dígitos numéricos."
            ),
        ],
    )
    relationship_second_tutor = StringField(
        "relationship_second_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    name_second_tutor = StringField(
        "name_second_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    last_name_second_tutor = StringField(
        "last_name_second_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    address_second_tutor = StringField(
        "address_second_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=80, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    phone_second_tutor = StringField(
        "phone_second_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    email_second_tutor = StringField(
        "email_second_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Email(message="Ingresa una dirección de correo válida."),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    occupation_second_tutor = StringField(
        "occupation_second_tutor",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

class WorkInInstitutionForm(Form):
    proposal = StringField(
        "proposal",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo 'proposal' no puede estar vacio."),
        ],
    )
    condition = StringField(
        "condition",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo 'condition' no puede estar vacio."),
        ],
    )
    seat = StringField(
        "seat",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo 'seat' no puede estar vacio."),
        ],
    )
    therapist = IntegerField(
        "therapist", validators=[DataRequired(message="terapista")]
    )
    rider = IntegerField(
        "rider", validators=[DataRequired(message="rideame los huevos")]
    )
    horse = IntegerField(
        "horse", validators=[DataRequired(message="horseee")]
    )
    track_assistant = IntegerField(
        "track_assistant", validators=[DataRequired(message="asistente track")]
    )
    days = StringField(
        "days",
        validators=[
            DataRequired(message="dias"),
        ],
    )

