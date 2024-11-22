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
    NumberRange,
    ValidationError,
    Optional,
)
from datetime import date

DATA_REQUIRED_MESSAGE = "El campo no puede estar vacio."

# Validador personalizado para fechas futuras
def validate_date_not_in_future(form, field):
    if field.data > date.today():
        raise ValidationError("La fecha de pago no puede ser una fecha futura.")
    
def validate_beneficiary_if_honorarios(form, field):
    if form.payment_type.data == "Honorarios" and not field.data:
        raise ValidationError("El beneficiario es obligatorio para pagos de Honorarios.")


class PaymentForm(Form):
    # Monto del pago (debe ser un número positivo)
    amount = DecimalField(
        "amount",
        validators=[
            DataRequired(message="El monto es obligatorio."),
            NumberRange(min=0, message="El monto debe ser un valor positivo."),
        ],
    )

    # Fecha del pago (no puede ser futura)
    payment_date = DateField(
        "payment_date",
        validators=[
            DataRequired(message="La fecha de pago es obligatoria."),
            validate_date_not_in_future,
        ],
    )

    # Tipo de pago (puedes usar SelectField si hay opciones específicas)
    payment_type = SelectField(
        "payment_type",
        choices=[
            ("Honorarios", "Honorarios"),
            ("Proveedor", "Proveedor"),
            ("Gastos varios", "Gastos Varios"),
        ],
        validators=[DataRequired(message="El tipo de pago es obligatorio.")],
    )

    # Descripción (opcional, pero con límite de caracteres)
    description = TextAreaField(
        "description",
        validators=[
            Length(
                max=200, message="La descripción no puede tener más de 200 caracteres."
            )
        ],
        default="",
    )

    # Beneficiario (opcional, pero si se ingresa, debe ser un email válido)
    beneficiary_id = StringField(
        "beneficiary_id",
        validators=[
            Optional(),
            Length(max=50, message="El email no puede superar los 50 caracteres."),
            validate_beneficiary_if_honorarios,
        ],
        default="",
    )