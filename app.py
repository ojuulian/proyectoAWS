import os
import modelo
import utils
import functools
import random
from datetime import datetime
import yagmail as yagmail
from db import get_db, close_db
from werkzeug.utils import secure_filename     #verifica el nombre del archivo,  generalmente /las cambiara por _ 

from flask import Flask, render_template, request, redirect ,url_for, flash, jsonify, session, send_file, current_app, \
    g, make_response, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from formularios import FormInicio, FormContrasena, FormNuevaContrasena, FormRegistro, FormBuscar


app= Flask(__name__)
app.secret_key = os.urandom(24)
now = datetime.now()

#-----------
@app.route("/",methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect( url_for( 'galeria' ) )    
  #try: 
    if  request.method == "GET": #Si la ruta es accedida a través del método GET entonces
      form = FormInicio()
      return render_template('login.html', form=form)
    if  request.method == "POST":
      us = request.form["usuario"]
      cont= request.form["password"]
      db = get_db()
      error = None

      if not us:
        error = 'Debes ingresar el usuario'
        flash(error)
        return redirect(url_for('login'))

      if not cont:
        error = 'Contraseña requerida'
        flash( error )
        return redirect(url_for('login'))

      user = db.execute(
          'SELECT * FROM usuarios WHERE usuario = ?', (us,)
      ).fetchone()

      if user is None:
        error = 'Usuario o contraseña inválidos'
      else:
        if check_password_hash( user['contrasena'], cont ):
            session.clear()
            session['user_id'] = user[0]
            resp = make_response( render_template( 'galeria.html' ) )   #redirect( url_for( 'personal' ) )
            #resp.set_cookie('usuario', us)
            return resp
            #return redirect( url_for( 'personal' ) )
        else:
            error = 'Usuario o contraseña inválidos'
      flash(error)
    return redirect(url_for('login'))
  #except:
    return render_template( 'login.html' )
#-----------




#-----------
@app.route("/registro", methods=['GET', 'POST'])
def registro():
  if g.user:
        return redirect( url_for( 'login' ) )  
  try:     
    if  request.method == "GET": #Si la ruta es accedida a través del método GET entonces
      form = FormRegistro()
      return render_template('registro.html', form=form)
    if  request.method == "POST":
      nom = request.form["nombre"]
      us = request.form["usuario"]
      email = request.form["email"] 
      cont= request.form["password"]
      error = None
      db = get_db()

      if not utils.isUsernameValid(us):
        error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
        flash( error )
        return redirect(url_for('registro'))

      if not utils.isPasswordValid(cont):
        error = 'La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres'
        flash( error )
        return redirect(url_for('registro'))

      if not utils.isEmailValid(email):
        error = 'Correo invalido'
        flash( error )
        return redirect(url_for('registro'))

      if db.execute( 'SELECT id FROM usuarios WHERE correo = ?', (email,) ).fetchone() is not None:
        error = 'El correo ya existe'.format( email )
        flash( error )
        return redirect(url_for('registro'))

      if db.execute( 'SELECT id FROM usuarios WHERE usuario = ?', (us,) ).fetchone() is not None:
        error = 'El usuario ya existe, escribe otro'.format(us)
        flash( error )
        return redirect(url_for('registro'))

      yag = yagmail.SMTP('misiontic2022grupo11@gmail.com', '2022Grupo11') #modificar con tu informacion personal
      yag.send(to=email, subject='Activa tu cuenta', contents='Bienvenido, usa este link para activar tu cuenta ')
      flash( 'Revisa tu correo para activar tu cuenta' )

      hashContraseña = generate_password_hash(cont)
      modelo.sql_insert(nom, us, email, hashContraseña ,now) 

      return redirect(url_for('login'))
  except:
    return render_template( 'login.html' )
#-----------
    #flash('Inicio de sesión solicitado por el usuario {}'.format(form.nombre.data))
    #return redirect(url_for('index2'))
    #return render_template('Registro.html', form=form)

#-----------


#-----------

@app.route("/recuperacion",methods=['GET', 'POST'])
def recuperacion():
  if g.user:
        return redirect( url_for( 'login' ) )  
  try:     
    if  request.method == "GET": #Si la ruta es accedida a través del método GET entonces
      form = FormContrasena()
      return render_template('recuperacion.html', form=form)
    if  request.method == "POST":
      email = request.form["email"] 
      error = None
      db = get_db()

      if not utils.isEmailValid(email):
        error = 'Correo invalido!'
        flash( error )
        return redirect(url_for('recuperacion'))

      if db.execute( 'SELECT id FROM usuarios WHERE correo = ?', (email,) ).fetchone() is not None:
        codigo = random.randint(0, 10000)
        error ='Revisa tu correo {} para cambiar tu contraseña'.format( email )
        yag = yagmail.SMTP('misiontic2022grupo11@gmail.com', '2022Grupo11') #modificar con tu informacion personal
        yag.send(to=email, subject='Cambia tu contraseña PIXELUNI', contents='Bienvenido, ingresa a www.pixeluni.com/nuevacontrasena para cambiar tu contraseña. \
          Además, usa el código {} para hacer cambios.  CODIGO VÁLIDO EN 24 HORAS!!'.format(codigo))
        #flash( 'Revisa tu correo para cambiar tu contraseña' )
        modelo.sql_update_codigo_autenticar(email , codigo)
        flash( error )
        return redirect(url_for('login'))

      return redirect(url_for('nuevacontrasena'))
  except:
    return render_template( 'login.html' )
#-----------


#-----------
@app.route("/nuevacontrasena",methods=['GET', 'POST'])
def nuevacontrasena():
  if g.user:
        return redirect( url_for( 'login' ) )  
  try:     
    if  request.method == "GET": #Si la ruta es accedida a través del método GET entonces
      form = FormNuevaContrasena()
      return render_template('nuevacontrasena.html', form=form)
    if  request.method == "POST":
      codigo= request.form["codigo"] 
      email = request.form["email"]
      cont= request.form["password"]
      error = None
      db = get_db()

      if not utils.isPasswordValid(cont):
        error = 'La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres'
        flash( error )
        return redirect(url_for('nuevacontrasena'))

      if not utils.isEmailValid(email):
        error = 'Correo invalido, ingresa el correo asociado a tu cuenta.'
        flash( error )
        return redirect(url_for('nuevacontrasena'))

      if db.execute( 'SELECT id FROM usuarios WHERE correo = ? AND cod_autenticacion = ?', (email,codigo) ).fetchone() is not None:
        error ='La contraseña asociada a la cuenta {} ha sido cambiada.'.format( email )
        error2 = 'Ingresa tus nuevas credenciales a PIXELUNI!!'
        #flash( 'Revisa tu correo para cambiar tu contraseña' )
        modelo.sql_update_contrasena(email , cont)
        flash( error )
        flash( error2 )
        return redirect(url_for('login'))

      if db.execute( 'SELECT id FROM usuarios WHERE correo = ? AND cod_autenticacion = ?', (email,codigo) ).fetchone() is None:
        error ='Las credenciales asociadas a la cuenta {} no coinciden'.format( email )
        error2 = 'Verifica las credenciales seguras generadas, puede que hayan expirado.'
        #flash( 'Revisa tu correo para cambiar tu contraseña' )
        flash( error )
        flash( error2 )
        return redirect(url_for('login'))

      return redirect(url_for('nuevacontrasena'))
  except:
    return render_template( 'login.html' )



#---------------------------
#generando un decorador para usar el loggeo del usuario en todas las páginas
def login_required(view):
    @functools.wraps( view )
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect( url_for( 'login' ) )
        return view( **kwargs )

    return wrapped_view



#------------------------------    


UPLOAD_FOLDER = os.path.abspath("./static/images/")
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpge"])

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER     #donde queremos que se guarden  nuestras fotos

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_file():
    if  request.method == "GET": #Si la ruta es accedida a través del método GET entonces
        return render_template('upload.html')
    if request.method == "POST":
        if not "file" in request.files:
            return "Sin parte de archivo en el formulario."
        f = request.files["file"]
        if f.filename == "":
            return "No exite archivo seleccionado."
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("get_file", filename=filename))
        return "Archivo no permitido."

    return render_template("upload.html")

@app.route("/images/<filename>")
def get_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)













#----------------------------------
@app.route("/galeria", methods=["GET","POST"])
@login_required
def galeria():
    if  request.method == "GET": #Si la ruta es accedida a través del método GET entonces
        return render_template('galeria.html')
    return render_template("galeria.html")

@app.route("/personal", methods=["GET","POST"])
@login_required
def personal():
    #session.clear()
    return render_template("personal.html")

@app.route("/crear", methods=["GET","POST"])
@login_required
def crear():
    session.clear()
    return render_template("crear.html")

@app.route("/descargar", methods=["GET","POST"])
def descargar():
    session.clear()
    return render_template("descargar.html")



@app.route("/buscar", methods=["GET","POST"])
@login_required
def buscar():
  if g.user:
        return redirect( url_for( 'galeria2' ) )  
  try:     
    if  request.method == "GET": #Si la ruta es accedida a través del método GET entonces
      form = FormRegistro()
      return render_template('buscar.html', form=form)
    if  request.method == "POST":
      nom = request.form["nombre"]
      error = None
      db = get_db()

      if not utils.isUsernameValid(nom):
        error = "El nombre que buscarte no existe"
        flash( error )
        return redirect(url_for('buscar'))


      return redirect(url_for('buscar'))
  except:
    return render_template("buscar.html",form=form)















@app.route("/eliminar", methods=["GET","POST"])
def eliminar():
    session.clear()
    return render_template("eliminar.html")

@app.route("/actualizar", methods=["GET","POST"])
def actualizar():
    session.clear()
    return render_template("actualizar.html")





"""
@app.route( '/downloadpdf', methods=('GET', 'POST') )
@login_required
def downloadpdf():
    return send_file( "resources/doc.pdf", as_attachment=True )


@app.route( '/downloadimage', methods=('GET', 'POST') )
@login_required
def downloadimage():
    return send_file( "resources/image.png", as_attachment=True )


@app.route( '/send', methods=('GET', 'POST') )
@login_required
def send():
    if request.method == 'POST':
        from_id = g.user['id']
        to_username = request.form['para']
        subject = request.form['asunto']
        body = request.form['mensaje']
        db = get_db()
        username=request.cookies.get('username')
        if not to_username:
            flash( username+': Para es un campo requerido' );
            return render_template( 'send.html' )

        if not subject:
            flash( username+': Asunto es un campo requerido' );
            return render_template( 'send.html' )

        if not body:
            flash( username+': Mensaje es un campo requerido' );
            return render_template( 'send.html' )

        error = None
        userto = None

        userto = db.execute(
            'SELECT * FROM usuarios WHERE usuario = ?', (to_username,)
        ).fetchone()

        if userto is None:
            error = username+': usuario digitado en el campo Para no existe'

        if error is not None:
            flash( error )

        else:
            db = get_db()
            query =  'INSERT INTO mensajes (from_id, to_id, asunto, mensaje) VALUES (?, ?, ?, ?)'
            db.execute(query, (g.user['id'], userto['id'], subject, body))
            db.commit()
            flash( "Mensaje Enviado" )

    return render_template( 'send.html')
"""


#uno de los decoradores más importantes
@app.before_request
def load_logged_in_user():
    user_id = session.get( 'user_id' )

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM usuarios WHERE id = ?', (user_id,)
        ).fetchone()


#limpia todo lo de la sesion y redirige a la página que se quiera
@app.route( '/logout' )
def logout():
    session.clear()
    return redirect( url_for( 'login' ) )


#-----------

if __name__ == '__main__':
    app.run( host='127.0.0.1', port =443, ssl_context=('micertificado.pem', 'llaveprivada.pem')  )