from wtforms import Form, StringField, IntegerField, DateField, DecimalField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, Email, ValidationError
from datetime import date

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
       # Email(message='Ingresa una dirección de correo válida.'), 
        Length(max=50, message='El email no puede superar los 50 caracteres.')
    ], default='')

