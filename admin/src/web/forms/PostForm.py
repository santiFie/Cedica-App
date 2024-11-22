from wtforms import (
    Form,
    StringField,
    SelectField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
)

DATA_REQUIRED_MESSAGE = "El campo no puede estar vacio."

class NewPostForm(Form):

    def title_exists(form, field):
        from src.core import post as post
        if post.title_exists(field.data):
            raise ValidationError("El título ingresado ya existe.")
        
    title = StringField(
        "Título",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
            title_exists,
        ],
    )

    content = TextAreaField(
        "Contenido",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=2000, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    summary = StringField(
        "Copete",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    state = SelectField(
        "Estado",
        choices=[
            ("Publicado", "Publicado"),
            ("Borrador", "Borrador"),
            ("Archivado", "Archivado"),
        ],
        validators=[DataRequired()],
    )

    
class EditPostForm(Form):
        
    content = TextAreaField(
        "Contenido",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=2000, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    summary = StringField(
        "Copete",
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(max=120, message="El campo supera el limite de caracteres"),
            Length(min=1, message="El campo no puede estar vacio."),
        ],
    )

    state = SelectField(
        "Estado",
        choices=[
            ("Publicado", "Publicado"),
            ("Borrador", "Borrador"),
            ("Archivado", "Archivado"),
        ],
        validators=[DataRequired()],
    )