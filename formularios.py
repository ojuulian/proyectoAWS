from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class FormInicio(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')])
    password = PasswordField('password', validators=[ DataRequired(message='No dejar vacío, completar')] )
    #recordar = BooleanField('Recordar usuario')
    enviar = SubmitField('ACCEDER')

class FormContrasena(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(message='No dejar vacío, completar')]) #[validators.Length(min=4, max=25)]
    #recordar = BooleanField('Recordar usuario')
    enviar = SubmitField('RECUPERAR')

class FormNuevaContrasena(FlaskForm):
    codigo=IntegerField('codigo', validators=[NumberRange(min=1, max=5, message='Invalid length'), DataRequired(message='No dejar vacío, completar')])
    email = StringField('Email Address', validators=[DataRequired(message='No dejar vacío, completar')]) #[validators.Length(min=4, max=25)]
    password = PasswordField('password', validators=[ DataRequired(message='No dejar vacío, completar')] )
    #recordar = BooleanField('Recordar usuario')
    enviar = SubmitField('GUARDAR')

class FormRegistro(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(message='No dejar vacío, completar')])
    usuario = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')]) #[validators.Length(min=4, max=25)]
    email = StringField('Email Address', validators=[DataRequired(message='No dejar vacío, completar')])
    password = PasswordField('password', validators=[ DataRequired(message='No dejar vacío, completar')] )
    #recordar = BooleanField('Recordar usuario')
    enviar = SubmitField('REGISTRAR')

class Personal(FlaskForm):
    enviar1 = SubmitField('DESCARGAR')
    enviar2 = SubmitField('ACTUALIZAR')
    enviar3 = SubmitField('CREAR')
    #recordar = BooleanField('Recordar usuario')
    enviar4 = SubmitField('REGISTRAR')


class FormBuscar(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(message='No dejar vacío, completar')])
    buscar = SubmitField('BUSCAR')

