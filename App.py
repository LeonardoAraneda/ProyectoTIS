from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
import psycopg2
import psycopg2.extras
from forms import SignupForm,SignInForm, Cancha, crear_cancha

conn = psycopg2.connect(user = "postgres",
        password = "f3l1p312",
        host = "localhost",
        port = "5432",
        database = "reserva_canchas")

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

posts = []
@app.route("/")
def index():
    return render_template("index.html", posts=posts)

@app.route("/reserva_completa/")
def reserva_completa():
    form = Cancha()
    cur = conn.cursor()
    cur.execute('SELECT * FROM reserva')
    datos = cur.fetchall()
#    print(datos)
    return render_template("reserva_completa.html", canchas = datos)

@app.route("/p/<string:slug>/")
def show_post(slug):
    return render_template("post_view.html", slug_title=slug)

@app.route("/bienvenido_personal/")
def bienvenido_personal():
    if 'name' in session:
        n = session['name']
    cur = conn.cursor()
    username = str(session["name"])
    valores = {'val1':n}
#    print(type(n))
    cur.execute("SELECT * FROM personal WHERE id_personal = %(val1)s",valores)
    datos = cur.fetchall()
    conn.commit()
    return render_template("bienvenido_personal.html", datos = datos)

@app.route("/admin/agregar_canchas/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/agregar_canchas/<int:post_id>/", methods=['GET', 'POST'])
def post_form(post_id):
    form = crear_cancha()
    if form.validate_on_submit():
        title = form.title.data
        title_slug = form.title_slug.data
        content = form.content.data
        id_cancha = form.id_cancha.data
        tipo_cancha = form.tipo_cancha.data

        post = {'title': title, 'title_slug': title_slug, 'content': content, 'id_cancha': id_cancha, 'tipo_cancha': tipo_cancha}
        posts.append(post)

        return redirect(url_for('index'))
    return render_template("admin/agregar_canchas.html", form=form)


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
        cur = conn.cursor()
        query = "INSERT INTO personal(id_personal, dv_personal, nombre_personal, mail_personal, pass, rol) values (%s,%s,%s,%s,%s,%s)"
        val = (id, dv, name, email, password, 0)
        cur.execute(query,val)
        conn.commit()
        if next:
            return redirect(next)
        return redirect(url_for('index'))
    return render_template("signup_form.html", form=form)

@app.route("/signin/", methods=["GET", "POST"])
def show_signin_form():
    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        next = request.args.get('next', None)
        query = "SELECT * FROM personal WHERE id_personal = %s AND pass = %s"
        query2 = "SELECT * FROM  personal"
        vals = (username, password)
        cur = conn.cursor()
        cur.execute(query,vals)
        datos = cur.fetchall()
        cur.close()
        cur = conn.cursor()
        cur.execute(query2)
        datos2 = cur.fetchall()
        session["name"] = username
#        print(datos2)
        if next:
            return redirect(next)
        if datos == []:
            print("algo anda mal")
        else:
            return render_template("bienvenido_personal.html", datos=datos, datos2=datos2)
    return render_template("signin_form.html", form=form)

@app.route("/reserva/", methods=["GET", "POST"])
def show_reserva_form():
    form = Cancha()
    if form.validate_on_submit():
        cancha = form.cancha.data
        dia = form.dia.data
        hora = form.hora.data
        next = request.args.get('next', None)
        if "name" in session:
            n = session['name']
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM reserva")
        contador = [contador[0] for contador in cur.fetchall()]
        print(contador[0])
        valores = {
            'val2': cancha,
            'val3': dia, 
            'val4': hora,
            'val1': n,
            'val5': contador[0]
        }
        cur.execute("INSERT INTO reserva(id_reserva, fecha_ingreso, cliente, a_cargo, tipo_pago, numero_pago, cancha, dia, hora) VALUES (%(val5)s, '2021-12-03', '12345678', %(val1)s, 0, 0, %(val2)s, %(val3)s, %(val4)s)", valores)
        conn.commit()
        cur.close()
        if next:
            return redirect(next)
        return redirect(url_for('reserva_completa'))

    return render_template("reserva_cancha.html", form = form)

@app.route("/listareservas/", methods=["GET","POST"])
def show_reserva_completa():
    form = Cancha()
    cur = conn.cursor()
    cur.execute('SELECT * FROM reserva')
    datos = cur.fetchall()
#    print(datos)
    return render_template("reservas_canchas.html", canchas = datos) 

if __name__ == "__main__":
    app.run(debug=True)