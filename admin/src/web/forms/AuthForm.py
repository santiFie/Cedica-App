from wtforms import (
    Form,
    StringField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
)

DATA_REQUIRED_MESSAGE = "El campo no puede estar vacio."


class AuthForm(Form):

    email = StringField(
        "email",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Email(message="Se debe ingresar un mail valido"),
            Length(max=50, message="El mail no puede tener mas de 50 caracteres"),
            Length(min=1, message="El mail no puede ser vacio"),
        ],
    )

    password = StringField(
        "password",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )