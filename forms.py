from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    id = StringField('RUT', validators=[DataRequired(), Length(max=7), Length(min=8)])
    dv = StringField('Digito Verificador', validators=[DataRequired(), Length(max=1)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')
    
class Cancha(FlaskForm):
    id_cancha = StringField('ID', validators=[DataRequired(), Length(max = 3)])
    tipo_cancha  = StringField('Tipo de Cancha', validators=[DataRequired(), Length(max = 200)])
    
class Block(FlaskForm):
    id_block = StringField('ID', validators=[DataRequired(), Length(max = 3)])
    dia = StringField('Dia', validators=[DataRequired(), Length(max = 8)])
    hora = StringField('Hora', validators=[DataRequired(), Length(max = 5)])
    