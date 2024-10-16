from wtforms import Form, StringField, IntegerField, DateField, DecimalField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, Email, ValidationError
from datetime import date


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