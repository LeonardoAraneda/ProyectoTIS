from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    id = StringField('RUT', validators=[DataRequired()])
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrar')
    
class SignInForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(),Length(max=30)])
    password = StringField("Contraseña", validators=[DataRequired(),Length(max=30)])
    submit = SubmitField('Ingresar')
    
class ReservaCancha(FlaskForm):
    cliente = SelectField('Cliente', validators=[DataRequired()], choices=[])
    cancha = SelectField('Cancha', validators=[DataRequired()], choices=[])
    bloque = SelectField('Bloque', validators=[DataRequired()], choices=[])
    dia = StringField('Día', validators=[DataRequired()])
    tipo_pago = SelectField('Tipo pago', validators=[DataRequired()], choices=[])
    id_pago = StringField('N° Pago', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class crear_cancha(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Título slug', validators=[Length(max=128)])
    content = TextAreaField('Descripcion')
    id_cancha = StringField('ID Cancha', validators=[DataRequired(), Length(max = 3)])
    tipo_cancha  = StringField('Tipo de Cancha', validators=[DataRequired(), Length(max = 200)])
    submit = SubmitField('Crear reserva')

class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Título slug', validators=[Length(max=128)])
    content = TextAreaField('Contenido')
    submit = SubmitField('Enviar')
    
class Cliente(FlaskForm):
    idc = StringField('RUT', validators=[DataRequired()])
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')