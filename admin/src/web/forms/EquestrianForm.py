from wtforms import (
    Form,
    StringField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    Length,
)

DATA_REQUIRED_MESSAGE = "El campo no puede estar vacio."

class EquestrianForm(Form):

    name = StringField(
        "name",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    sex = SelectField(
        "sex",
        choices=[
            ("M", "Macho"),
            ("F", "Hembra"),
        ],
        validators=[DataRequired()],
    )

    race = StringField(
        "rce",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    coat = StringField(
        "coat",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    headquarters = StringField(
        "headquarters",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )