from wtforms import (
    Form,
    StringField,
    DateField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Regexp,
    Email,
)
from datetime import date

DATA_REQUIRED_MESSAGE = "El campo no puede estar vacio."


class TeamMemberForm(Form):
    name = StringField(
        "name",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    last_name = StringField(
        "last_name",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo supera el limite de caracteres"),
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

    address = StringField(
        "address",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    email = StringField(
        "email",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Email(message="Se debe ingresar un mail valido"),
            Length(max=50, message="El mail no puede tener mas de 50 caracteres"),
            Length(min=1, message="El mail no puede ser vacio"),
        ],
    )

    locality = StringField(
        "locality",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
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

    initial_date = DateField(
        "initial_date",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            lambda form, field: field.data <= date.today(),
        ],
    )

    emergency_contact = StringField(
        "emergency_contact",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
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

    associated_number = StringField(
        "associated_number",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )


class TeamMemberEditForm(Form):

    name = StringField(
        "name",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    last_name = StringField(
        "last_name",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    address = StringField(
        "address",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    locality = StringField(
        "locality",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
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
            Length(max=120, message="El campo supera el limite de caracteres"),
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

    associated_number = StringField(
        "associated_number",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
