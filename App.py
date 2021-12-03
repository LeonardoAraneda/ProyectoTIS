from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import psycopg2
import psycopg2.extras
from forms import SignupForm, Cancha, PostForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'



posts = []
@app.route("/")
def index():
    return render_template("index.html", posts=posts)

@app.route("/reserva_completa/")
def reserva_completa():
    return render_template("reserva_completa.html")

@app.route("/p/<string:slug>/")
def show_post(slug):
    return render_template("post_view.html", slug_title=slug)

@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        title_slug = form.title_slug.data
        content = form.content.data

        post = {'title': title, 'title_slug': title_slug, 'content': content}
        posts.append(post)

        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        id = form.id.data
        dv = form.dv.data
        email = form.email.data
        password = form.password.data
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('index'))
    return render_template("signup_form.html", form=form)

@app.route("/reserva/", methods=["GET", "POST"])
def show_reserva_form():
    form = Cancha()
    if form.validate_on_submit():
        id_cancha = form.id_cancha.data
        tipo_cancha = form.tipo_cancha.data
        id_block = form.id_block.data
        dia = form.dia.data
        hora = form.hora.data
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('reserva_completa'))
    return render_template("reserva_cancha.html", form=form)