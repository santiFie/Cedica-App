from wtforms import (
    Form,
    StringField,
    DateField,
    DecimalField,
    SelectField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Regexp,
    NumberRange,
    ValidationError,
)
from datetime import date

DATA_REQUIRED_MESSAGE = "El campo no puede estar vacio."

class CollectionForm(Form):
    amount = DecimalField(
        "Monto",
        validators=[
            DataRequired(),
            NumberRange(min=0, message="El monto debe ser positivo."),
        ],
    )
    payment_date = DateField("Fecha de pago", validators=[DataRequired()])
    payment_method = SelectField(
        "Método de pago",
        choices=[
            ("Efectivo", "Efectivo"),
            ("Tarjeta de credito", "Tarjeta de credito"),
            ("Tarjeta de debito", "Tarjeta de debito"),
            ("Transferencia", "Transferencia"),
        ],
        validators=[DataRequired()],
    )

    observations = TextAreaField("Observaciones", validators=[Length(max=200)])
    team_member_id = StringField(
        "ID de miembro del equipo", validators=[DataRequired()]
    )
    rider_dni = StringField(
        "DNI de jinete",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{8}$", message="El DNI debe tener 8 dígitos numéricos."
            ),
        ],
    )

    def validate_payment_date(form, field):
        if field.data > date.today():
            raise ValidationError("La fecha de pago no puede ser una fecha futura.")
