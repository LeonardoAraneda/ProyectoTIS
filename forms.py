from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    id = StringField('RUT', validators=[DataRequired(), Length(max=8), Length(min=7)])
    dv = StringField('Digito Verificador', validators=[DataRequired(), Length(max=1)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')
    
class SignInForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(),Length(max=30)])
    password = StringField("Contraseña", validators=[DataRequired(),Length(max=30)])
    submit = SubmitField('Ingresar')
    
class Cancha(FlaskForm):
    cancha = SelectField('Cancha', choices=[('0', 'Cancha 1 - Pasto'), ('1', 'Cancha 2 - Tierra'), ('2', 'Cancha 3 - Sintético')])
    dia = StringField('Dia', validators=[DataRequired(), Length(max = 10)])
    hora = StringField('Hora', validators=[DataRequired(), Length(max = 5)])
    submit = SubmitField('Registrar')

class crear_cancha(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Título slug', validators=[Length(max=128)])
    content = TextAreaField('Descripcion')
    id_cancha = StringField('ID Cancha', validators=[DataRequired(), Length(max = 3)])
    tipo_cancha  = StringField('Tipo de Cancha', validators=[DataRequired(), Length(max = 200)])
    submit = SubmitField('Registrar')

class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Título slug', validators=[Length(max=128)])
    content = TextAreaField('Contenido')
    submit = SubmitField('Enviar')