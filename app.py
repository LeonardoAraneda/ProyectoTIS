from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
import psycopg2
import psycopg2.extras
from forms import Cliente, DeleteCount, DeleteReserva,  SignupForm, SignInForm, ReservaCancha, crear_cancha
from datetime import datetime

conn = psycopg2.connect(
    user = "riwbncvvdzqyza",
    password = "9be398d70978c9b443d619eb0c969f361ec927edc559d1df10a70851fa76dc27",
    host = "ec2-52-72-252-211.compute-1.amazonaws.com",
    port = "5432",
    database = "ddtnat73bqjn52"
)

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

posts = []
@app.route("/")
def index():
    if not session.get("id"):
        return redirect("/signin/")

    return render_template("index.html", posts=posts)

@app.route("/reserva_completa/")
def reserva_completa():
    form = ReservaCancha()

    cur = conn.cursor()
    cur.execute("SELECT r.fecha_ingreso, p.nombre_personal, cl.nombre_cliente, r.dia, tp.nombre_pago, tc.nombre_tipo, b.hora FROM reserva r, tipo_pago tp, canchas ca, tipo_cancha tc, bloques b, cliente cl, personal p WHERE r.a_cargo=p.id_personal AND r.cancha=ca.id_cancha AND ca.id_cancha=tc.id_tipo AND r.tipo_pago=tp.id_pago AND r.hora=b.id_bloque AND r.cliente=cl.id_cliente")
    datos = cur.fetchall()

    return render_template("reserva_completa.html", canchas = datos)

@app.route("/p/<string:slug>/")
def show_post(slug):
    return render_template("post_view.html", slug_title=slug)

@app.route("/bienvenido_personal/")
def bienvenido_personal():
    if 'id' in session:
        id_sesion = session['id']

    cur = conn.cursor()
    cur.execute("SELECT CONCAT(p.id_personal, '-', p.dv_personal), p.nombre_personal, p.mail_personal, r.nombre_rol FROM personal p, roles r WHERE p.rol=r.id_rol AND id_personal=%s", id_sesion)
    datos = cur.fetchall()

    return render_template("index.html", datos=datos)

@app.route("/admin/agregar_canchas/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/agregar_canchas/<int:post_id>/", methods=['GET', 'POST'])
def post_form(post_id):
    form = crear_cancha()
    if form.validate_on_submit():
        title       = form.title.data
        title_slug  = form.title_slug.data
        content     = form.content.data
        id_cancha   = form.id_cancha.data
        tipo_cancha = form.tipo_cancha.data

        post = {'title': title, 'title_slug': title_slug, 'content': content, 'id_cancha': id_cancha, 'tipo_cancha': tipo_cancha}
        posts.append(post)

        return redirect(url_for('index'))
    return render_template("admin/agregar_canchas.html", form=form)


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm()
    cur = conn.cursor()
    cur.execute("SELECT id_rol, nombre_rol FROM roles")
    form.rol.choices = cur.fetchall()
    cur.close()
    if form.validate_on_submit():
        id       = form.id.data
        name     = form.name.data
        email    = form.email.data
        password = form.password.data
        rol      = form.rol.data

        next = request.args.get('next', None)

        ingresos = {
            'id'      : id[0 : id.find('-')],
            'dv'      : id[8 : 9],
            'name'    : name,
            'email'   : email,
            'password': password,
            'rol'     : rol
        }
        print("dv: ",id[8:9])
        if id[8:9] == '':
            return redirect(url_for('show_signup_form'))

        cur = conn.cursor()
        cur.execute("INSERT INTO personal(id_personal, dv_personal, nombre_personal, mail_personal, pass, rol) VALUES (%(id)s, %(dv)s, %(name)s, %(email)s, %(password)s, %(rol)s)", ingresos)
        conn.commit()
        cur.close()
        if next:
            return redirect(next)
        return redirect(url_for('ver_perfil'))
    return render_template("signup_form.html", form=form)

@app.route("/signin/", methods=["GET", "POST"])
def show_signin_form():
    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        next = request.args.get('next', None)

        query = "SELECT * FROM personal WHERE id_personal = %s AND pass = %s"
        vals = (username[0 : username.find('-')], password)
        cur = conn.cursor()
        cur.execute(query,vals)
        datos = cur.fetchall()
        print(datos)
        cur.close()


        while True:
            try:
                session["id"] = datos[0][0]
                session["name"] = datos[0][2]
                session["rol"] = datos[0][5]
                break
            except IndexError:
                print("algo no esta bien")
                return redirect(url_for('show_signin_form'))

        if datos == []:
            print("algo anda mal")

        if next:
            return redirect(next)
        else:
            return render_template("index.html", datos=datos)
    return render_template("signin_form.html", form=form)

@app.route("/reserva/", methods=["GET", "POST"])
def show_reserva_form():
    form = ReservaCancha()

    cur = conn.cursor()
    cur.execute("SELECT c.id_cancha, CONCAT('Cancha ', c.id_cancha+1, ' - ', tc.nombre_tipo) FROM canchas c, tipo_cancha tc WHERE c.tipo_cancha=tc.id_tipo")
    form.cancha.choices = cur.fetchall()
    cur.close()
    
    cur = conn.cursor()
    cur.execute("SELECT id_bloque, CONCAT('Bloque: ', hora) FROM bloques")
    form.bloque.choices = cur.fetchall()
    cur.close()

    cur = conn.cursor()
    cur.execute("SELECT id_cliente, CONCAT(id_cliente, '-', dv_cliente, ' - ', nombre_cliente) FROM cliente")
    form.cliente.choices = cur.fetchall()
    cur.close()
    
    cur = conn.cursor()
    cur.execute("SELECT id_pago, nombre_pago FROM tipo_pago")
    form.tipo_pago.choices = cur.fetchall()
    cur.close()

    if form.validate_on_submit():
        cliente = form.cliente.data
        cancha  = form.cancha.data
        bloque  = form.bloque.data
        dia     = form.dia.data
        pago    = form.tipo_pago.data
        id_pago = form.id_pago.data

        next = request.args.get('next', None)
        if "id" in session:
            session_id = session['id']

        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM reserva")
        id_reserva = cur.fetchall()
        
        cur.execute("SELECT * FROM reserva")
        reserva = cur.fetchall()
        
        #for i in reserva:
        #    if id_reserva[0][0] == reserva[0][i]:
        #        id_reserva += 1

        ingresos = {
            'reserva': id_reserva[0][0]+1,
            'ingreso': datetime.today().strftime('%Y-%m-%d'),
            'cliente': cliente,
            'admin'  : session_id,
            'pago'   : pago,
            'id_pago': id_pago,
            'cancha' : cancha,
            'dia'    : dia,
            'hora'   : bloque
        }
        cur.execute("INSERT INTO reserva(id_reserva, fecha_ingreso, cliente, a_cargo, tipo_pago, numero_pago, cancha, dia, hora) VALUES (%(reserva)s, %(ingreso)s, %(cliente)s, %(admin)s, %(pago)s, %(id_pago)s, %(cancha)s, %(dia)s, %(hora)s)", ingresos)
        conn.commit()
        cur.close()
        if next:
            return redirect(next)
        return redirect(url_for('show_reserva_completa'))

    return render_template("reserva_cancha.html", form=form)

@app.route("/listareservas/", methods=["GET","POST"])
def show_reserva_completa():
    form = ReservaCancha()

    if 'id' in session:
        n = session['id']
        print(n)

    valores = {'val1':n}
    cur = conn.cursor()
    cur.execute("SELECT r.fecha_ingreso, cl.nombre_cliente, r.dia, tp.nombre_pago, tc.nombre_tipo, b.hora FROM reserva r, tipo_pago tp, canchas ca, tipo_cancha tc, bloques b, cliente cl WHERE r.cancha=ca.id_cancha AND ca.id_cancha=tc.id_tipo AND r.tipo_pago=tp.id_pago AND r.hora=b.id_bloque AND r.cliente=cl.id_cliente AND a_cargo=%(val1)s", valores)
    datos = cur.fetchall()

    return render_template("reservas_canchas.html", canchas=datos)

@app.route("/logout")
def logout():
    session["id"] = None

    return redirect("/")

@app.route("/perfil/")
def ver_perfil():
    id = session["id"]
    valores = {'val1':id}
    cur = conn.cursor()
    print(id)
    cur.execute("SELECT * FROM personal WHERE id_personal = %(val1)s",valores)
    datos = cur.fetchall()
    print(datos)
    return render_template("post_view.html", datos = datos)

@app.route("/crear_cliente/", methods=["GET","POST"])
def crear_cliente():
    form = Cliente()
    if form.validate_on_submit():
        idc = form.idc.data
        name = form.name.data
        email = form.email.data
        
        next = request.args.get('next', None)
        
        if 'idc' in session:
            idc = session['idc']

        cur = conn.cursor()
        ingresos = {
            'id'      : idc[0 : idc.find('-')],
            'dv'      : idc[8 : 9],
            'name' : name,
            'email': email
        }
        cur.execute("INSERT INTO cliente(id_cliente, dv_cliente, nombre_cliente, mail_cliente) VALUES (%(id)s, %(dv)s, %(name)s, %(email)s)", ingresos)
        conn.commit()
        cur.close()
        if next:
            return redirect(next)
        return redirect(url_for('ver_cliente'))

    return render_template("crear_cliente.html", form=form)
    
@app.route("/ver_clientes/")
def ver_cliente():
    cur = conn.cursor()
    print(id)
    cur.execute("SELECT * FROM cliente")
    datos = cur.fetchall()
    print(datos)
    return render_template("ver_cliente.html", datos = datos)

@app.route("/eliminar_cuenta/",  methods=["GET","POST"])
def eliminar_cuenta():
    form = DeleteCount()
    
    cur = conn.cursor()
    cur.execute("SELECT id_personal, CONCAT(id_personal, '-', dv_personal, ' - ', nombre_personal) FROM personal")
    form.id.choices = cur.fetchall()
    cur.close()
    
    #if form.validate_on_submit():
    if request.method == 'POST':
        print(form.id.choices)
        id = form.id.data
        print(id)
        
        next = request.args.get('next', None)
        cur = conn.cursor()
        
        valores = {'val1':id}
        cur.execute("DELETE FROM personal WHERE id_personal = %(val1)s",valores)
        conn.commit()
        cur.close()
        if next:
            return redirect(next)
        return redirect(url_for('eliminar_cuenta'))
        
    return render_template("eliminar_cuenta.html", form=form)
    
@app.route("/eliminar_reserva/",  methods=["GET","POST"])
def eliminar_reserva():
    form = DeleteReserva()
    
    cur = conn.cursor()
    cur.execute("SELECT r.id_reserva, CONCAT('Reserva: ', cl.nombre_cliente, ', ', tc.nombre_tipo, ' - ', r.dia, '  ', b.hora) FROM reserva r, cliente cl, tipo_cancha tc, canchas ca, bloques b WHERE r.cliente=cl.id_cliente AND r.cancha=ca.id_cancha AND ca.tipo_cancha=tc.id_tipo AND r.hora=b.id_bloque")
    form.id_reserva.choices = cur.fetchall()
    cur.close()
    
    #if form.validate_on_submit():
    if request.method == 'POST':
        print(form.id_reserva.choices)
        id = form.id_reserva.data
        print(id)
        
        next = request.args.get('next', None)
        cur = conn.cursor()
        
        valores = {'val1':id}
        cur.execute("DELETE FROM reserva WHERE id_reserva = %(val1)s",valores)
        conn.commit()
        cur.close()
        if next:
            return redirect(next)
        return redirect(url_for('eliminar_reserva'))
        
    return render_template("eliminar_reserva.html", form=form)
    
if __name__ == "__main__":
    app.run(debug=True)