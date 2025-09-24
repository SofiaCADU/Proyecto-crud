from base.models.cita_model import Cita  # desde la carpeta base, traeme el modelo donde citas ya esta definida la forma de trabajar con la tabla citas
from base.models.usuario_model import Usuario
from flask import render_template, redirect, request, session, Blueprint, flash  # sesion: Mantiene los datos almecenados de un usuario. El render con el redirect, te redirige entre paginas, request: hace que sea obligatoria una accion, flash: permite mostrar mensajes al usuario, blueprint: permite organizar las rutas y vistas de la aplicacion.

bp = Blueprint('citas', __name__, url_prefix ='/citas')

# Controlador de citas
# Todas las rutas relacionadas con la gestion de citas y favoritos.

# Creamos el blueprint para agrupar las rutas de citas.
bp = Blueprint('citas', __name__, url_prefix='/citas') # Prefix muestra las rutas mas rapido

bp.route("/agregar", methods=['POST'])
# Ruta para agregar una nueva cita. Solo usuarios autentificados pueden agregar.
# Valida la cita y muestra si es necesario.
def agregar_cita():
    if 'usuario_id' not in session:
        return redirect('/')
    if not Cita.validar_cita(request.form):
        return redirect('/citas')  
    data = {
        'cita': request.form['cita'],
        'autor_id': session['usuario_id']
    }
    Cita.guardar_cita(data)
    return redirect('/citas')

@bp.route('/editar/<int:id>')
def pagina_editar(id):
    # Ruta para mostrar el formulario de edicion de una cita.
    # Solo el autor de la cita puede editar.
    if 'usuario_id' not in session:
        return redirect('/')
    cita = Cita.obtener_por_id(id)
    if not cita or cita.autor_id != session['usuario_id']:
        flash("No tienes permiso para editar esta cita.", 'error')  # El error es la palabra que utilizaremos para llamarlo desde el html.
        return redirect('/citas')
    return render_template('editar_cita.html', cita=cita)  # Render_template = redirige los html de la carpeta templates.


@bp.route('/procesar_editar', methods=['POST'])  # POST: porque quien entrega la inforemacion viene desde fuera, no esta en la base de datos.
def procesar_editar():
    # Procesa la edicion de una cita. 
    # Solo el autor puede editar y se valida los datos.
    if 'usuario_id' not in session:
        return redirect('/')
    cita_a_editar = Cita.obtener_por_id(request.form['id'])
    if not cita_a_editar or cita_a_editar.autor_id != session['usuario_id']:
        flash("No tienes permisos para editar esta cita.", 'error')
        return redirect('/citas')
    if not Cita.validar_cita(request.form):
        return redirect(f"/citas/editar/{request.form['id']}")
    Cita.actualizar_cita(request.form)
    return redirect('/citas')

@bp.route('/borrar/<int:id>')
def borrar_citas(id):
    # Ruta para borrar una cita.
    #Solo el ususario puede borara su cita.
    if 'usuario_id' not in session:
        return redirect('/')
    cita_a_borrar = Cita.obtener_por_id(id)
    if not cita_a_borrar or cita_a_borrar.autor_id != session['usuario_id']:
        flash("No tienes permiso para borrar esta cita.", 'error')
        return redirect('/citas')
    Cita.eliminar_cita(id)
    return redirect('/citas')

@bp.route('/perfil')
def perfil():
    # Ruta la cual muestra el perfil del usuario actual.
    # Su cita y el total de publicaciones.
    if 'usuario_id' not in session:
        return redirect('/')
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    citas_usuario = Cita.obtener_citas_usuario(session['usuario_id'])
    total_citas = len(citas_usuario)
    return render_template('perfil.html', usuario=usuario, citas=citas_usuario, total_citas=total_citas)

@bp.route('/')
def dashboard():
    # Esta ruta muestra el dashboard principal con todas las citas y las favoritas del usuario.
    if 'usuario_id' not in session:
        return redirect('/')
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    return render_template('dashboard.html', usuario=usuario)