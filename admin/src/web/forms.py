from wtforms import Form, StringField, IntegerField, DateField, DecimalField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, Email, ValidationError
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
                r"^\d{8,9}$", message="El DNI debe tener entre 8 y 9 dígitos numéricos."
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
    age = IntegerField("age", validators=[DataRequired(message=DATA_REQUIRED_MESSAGE), NumberRange(min=0, max=99)])
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
        validators=[DataRequired(message=DATA_REQUIRED_MESSAGE), lambda form, field: field.data <= date.today()],
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
                r"^\d{8,9}$", message="El DNI debe tener entre 8 y 9 dígitos numéricos."
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
                r"^\d{8,9}$", message="El DNI debe tener entre 8 y 9 dígitos numéricos."
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
                r"^\d{8,9}$", message="El DNI debe tener entre 8 y 9 dígitos numéricos."
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
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    condition = StringField(
        "condition",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    seat = StringField(
        "seat",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=50, message="El campo ingresado supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )
    therapist = IntegerField("therapist", validators=[DataRequired(message=DATA_REQUIRED_MESSAGE)])
    rider = IntegerField("rider", validators=[DataRequired(message=DATA_REQUIRED_MESSAGE)])
    horse = IntegerField("horse", validators=[DataRequired(message=DATA_REQUIRED_MESSAGE)])
    track_assistant = IntegerField("track_assistant", validators=[DataRequired(message=DATA_REQUIRED_MESSAGE)])
    days = StringField(
        "days",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
        ],
    )
# Validador personalizado para fechas futuras
def validate_date_not_in_future(form, field):
    if field.data > date.today():
        raise ValidationError("La fecha de pago no puede ser una fecha futura.")

class PaymentForm(Form):
    # Monto del pago (debe ser un número positivo)
    amount = DecimalField('amount', validators=[
        DataRequired(message='El monto es obligatorio.'),
        NumberRange(min=0, message='El monto debe ser un valor positivo.')
    ])

    # Fecha del pago (no puede ser futura)
    payment_date = DateField('payment_date', validators=[
        DataRequired(message='La fecha de pago es obligatoria.'),
        validate_date_not_in_future
    ])

    # Tipo de pago (puedes usar SelectField si hay opciones específicas)
    payment_type = SelectField('payment_type', choices=[
        ('HONORARIOS', 'Honorarios'), 
        ('PROVEEDOR', 'Proveedor'), 
        ('GASTOS VARIOS', 'Gastos Varios')
    ], validators=[DataRequired(message='El tipo de pago es obligatorio.')])

    # Descripción (opcional, pero con límite de caracteres)
    description = TextAreaField('description', validators=[
        Length(max=200, message='La descripción no puede tener más de 200 caracteres.')
    ], default='')

    # Beneficiario (opcional, pero si se ingresa, debe ser un email válido)
    beneficiary_id = StringField('beneficiary_id', validators=[
       # REVISAR POR QUE NO ANDA EMAIL
        Email(message='Ingresa una dirección de correo válida.'), 
        Length(max=50, message='El email no puede superar los 50 caracteres.')
    ], default='')


class CollectionForm(Form):
    amount = DecimalField('Monto', validators=[DataRequired(), NumberRange(min=0, message="El monto debe ser positivo.")])
    payment_date = DateField('Fecha de pago', validators=[DataRequired()])
    payment_method = SelectField('Método de pago', 
        choices=[
            ('EFECTIVO', 'Efectivo'), 
            ('TARJETA DE CREDITO', 'Tarjeta de Credito'),
            ('TARJETA DE DEBITO', 'Tarjeta de Debito'),
            ('TRANSFERENCIA', 'Transferencia')], 
        validators=[DataRequired()])
    
    observations = TextAreaField('Observaciones', validators=[Length(max=200)])
    team_member_id = StringField('ID de miembro del equipo', validators=[DataRequired()])
    rider_dni = StringField('DNI de jinete', validators=[DataRequired(),Regexp(r'^\d{8,9}$', message='El DNI debe tener entre 8 y 9 dígitos numéricos.')])

    def validate_payment_date(form, field):
        if field.data > date.today():
            raise ValidationError("La fecha de pago no puede ser una fecha futura.")
