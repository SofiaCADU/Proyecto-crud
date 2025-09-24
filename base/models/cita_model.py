# base/models/cita_model.py

# Modelo de cita
# Encapsulamos la logica de las citas y favoritos en la base de datos.

from base.config.mysqlconnection import connectToMySQL 
from flask import flash, session

class Cita:
    @classmethod  # es un construcctor de clase
    def obtener_citas_usuarios(cls, usuario_id):
        # Obtener todas las citas creadas por un usuario.
        query = "SELECT * FROM citas WHERE autor_id = %(usuario_id)s;"
        data = {'usuario_id': usuario_id}  # Uno es de la base de tados y otro es de la variable que le pasamos.
        resultado = connectToMySQL(cls.dl).query_db(query, data)
        citas = []  # se dejan los corchetes vacios esperando que se llenen despues y vallan a la base de datos.
        for row in resultado: # Se necesita iterar solo la información del usuario.
            citas.append(cls(row))   #cls: hace referencia a la clase
        return citas
    
# Clase que representa una cita y sus operaciones en la base de datos.

db = "proyecto_crud"

def __init__(self, data):
    #  Constructor: Inicializacion de los atributos de la clase.
    self.id = data['id']
    self.cita = data['cita']
    self.autor_id = data['autor_id']
    self.usuario_id = data['usuario_id']
    self.creado_en = data['creado_en']
    self.actualizado_en = data['actualizado_en']
     
@classmethod
def guardar_cita(cls, data):
    # Guardar una nueva cita en la base de datos.
    
    query = "INSERT INTO citas (cita, autor_id) VALUES (%(cita)s, %(autor_id)s);"
    resultado = connectToMySQL(cls.db).query_db(query, data)
    return resultado 

@classmethod
def obtener_por_id(cls, cita_id):
    # Busca una cita por su id.
    query = "SELECT * FROM citas WHERE id = %(id)s;"
    data = {'id': cita_id}
    resultado = connectToMySQL(cls.db).query_db(query, data)
    if not resultado:
        return None
    return cls(resultado[0])

@classmethod
def obtener_todas(cls):
    # Obtiene todas las citas de la base de datos.
    query = "SELECT * FROM citas;"  #El ; esta iniciando y terminendo un componente
    resultado = connectToMySQL(cls.db).query_db(query)
    citas = []
    for row in resultado:
        citas.append(cls(row))
    return citas

@classmethod
def actualizar_cita(cls, data):
    # Actualiza los datos de una cita exiatente.
    query = "UPDATE citas SET cita = %(cita)s WHERE id = %(id)s;"
    resultado = connectToMySQL(cls.db).query_db(query, data)  # query.db: llama a la base de datos.
    
@classmethod
def eliminar_cita(cls, cita_id):
    # Elimina una cita de la base de datos por su id.
    query = "DELETE FROM citas WHERE id = %(id)s;"
    data = {'id': cita_id}
    return connectToMySQL(cls.db).query_db(query, data)

@staticmethod
def validar_cita(cita):
    # Validar los darosa de la cita.
    # Devuelve verdadero si todo es valido y falso si hay errores ( mostramos un flah).
    is_valid = True
    if len(cita['cita']) < 5:
        flash("La cita debe tener al menos 5 caracteres.", "alerta")
        is_valid = False
    return is_valid