from wtforms import Form, StringField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, Email
from datetime import date


class RiderHorsewomanForm(Form):
    name = StringField(
        "name",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    dni = StringField(
        "dni",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{8,9}$", message="El DNI debe tener entre 8 y 9 dígitos numéricos."
            ),
        ],
    )
    last_name = StringField(
        "last_name",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    age = IntegerField("age", validators=[DataRequired(), NumberRange(min=0, max=99)])
    place_of_birth = StringField(
        "place_of_birth",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    date_of_birth = DateField(
        "date_of_birth",
        validators=[DataRequired(), lambda form, field: field.data <= date.today()],
    )
    address = StringField(
        "address",
        validators=[
            DataRequired(),
            Length(max=80, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    phone = StringField(
        "phone",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    emergency_contact = StringField(
        "emergency_contact",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    emergency_phone = StringField(
        "emergency_phone",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    name_institution = StringField(
        "name_intitution",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    address_institution = StringField(
        "address_institution",
        validators=[
            DataRequired(),
            Length(max=80, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    phone_institution = StringField(
        "phone_institution",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    current_grade = StringField(
        "current_grade",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    dni_first_tutor = StringField(
        "dni_first_tutor",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{8,9}$", message="El DNI debe tener entre 8 y 9 dígitos numéricos."
            ),
        ],
    )
    relationship_first_tutor = StringField(
        "relationship_first_tutor",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    name_first_tutor = StringField(
        "name_first_tutor",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    last_name_first_tutor = StringField(
        "last_name_first_tutor",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    address_first_tutor = StringField(
        "address_first_tutor",
        validators=[
            DataRequired(),
            Length(max=80, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    phone_first_tutor = StringField(
        "phone_first_tutor",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    email_first_tutor = StringField(
        "email_first_tutor",
        validators=[
            DataRequired(),
            Email(message="Ingresa una dirección de correo válida."),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    occupation_first_tutor = StringField(
        "occupation_first_tutor",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    membership_number = StringField(
        "membership_number",
        validators=[
            DataRequired(),
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
            DataRequired(),
            Regexp(
                r"^\d{8,9}$", message="El DNI debe tener entre 8 y 9 dígitos numéricos."
            ),
        ],
    )
    relationship_first_tutor = StringField(
        "relationship_first_tutor",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    name_first_tutor = StringField(
        "name_first_tutor",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    last_name_first_tutor = StringField(
        "last_name_first_tutor",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    address_first_tutor = StringField(
        "address_first_tutor",
        validators=[
            DataRequired(),
            Length(max=80, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    phone_first_tutor = StringField(
        "phone_first_tutor",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    email_first_tutor = StringField(
        "email_first_tutor",
        validators=[
            DataRequired(),
            Email(message="Ingresa una dirección de correo válida."),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    occupation_first_tutor = StringField(
        "occupation_first_tutor",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

class SecondTutorForm(Form):
    dni_second_tutor = StringField(
        "dni_second_tutor",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{8,9}$", message="El DNI debe tener entre 8 y 9 dígitos numéricos."
            ),
        ],
    )
    relationship_second_tutor = StringField(
        "relationship_second_tutor",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    name_second_tutor = StringField(
        "name_second_tutor",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    last_name_second_tutor = StringField(
        "last_name_second_tutor",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    address_second_tutor = StringField(
        "address_second_tutor",
        validators=[
            DataRequired(),
            Length(max=80, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    phone_second_tutor = StringField(
        "phone_second_tutor",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{7,15}$",
                message="El numero de telefono debe tener entre 7 y 15 digitos.",
            ),
        ],
    )
    email_second_tutor = StringField(
        "email_second_tutor",
        validators=[
            DataRequired(),
            Email(message="Ingresa una dirección de correo válida."),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    occupation_second_tutor = StringField(
        "occupation_second_tutor",
        validators=[
            DataRequired(),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
