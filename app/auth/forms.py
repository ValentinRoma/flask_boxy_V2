from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
 'El nombre de usuario no debe tener espacios '
 )])
    password = PasswordField('Password', validators=[
 DataRequired(), EqualTo('confirm', message='La contraseñas deben coincidir.')])
    confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Registrarse')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Este email ya está registrado.')


    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('El nombre de usuario ya está en uso.')
        


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password  = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Mantenme en la sesión')
    submit = SubmitField('Iniciar sesión')
    
