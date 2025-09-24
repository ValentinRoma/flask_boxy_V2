from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Boxy

class RegistrationBoxy(FlaskForm):
    clave_boxy = StringField('Clave boxy', validators=[DataRequired(), Length(1, 64)])
    sala = StringField('Sala')
    submit = SubmitField('Sumar Boxy')

    
    def validate_clave_boxy(self, field):
         if Boxy.query.filter_by(clave_boxy=field.data).first():
             raise ValidationError('Esta clave ya existe')
    
