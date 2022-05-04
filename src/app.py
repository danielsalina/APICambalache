from flask import Flask, jsonify, request, redirect, url_for
from flask_mysqldb import MySQL
from config import config
from dotenv import load_dotenv
from routes.auth import routes_auth

app = Flask(__name__)
app.register_blueprint(routes_auth)

# CONEXIÓN A MYSQL
conexion = MySQL(app)


@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return "<h1>Estas en la página de inicio</h1>"

#GET TODOS LOS USUARIOS
@app.route('/usuarios')
def mostrar_usuarios():
    try:
        cursor = conexion.connection.cursor()
        query = "SELECT * FROM usuarios"
        cursor.execute(query)
        data = cursor.fetchall()
        users = []
        for row in data:
            user = {'Nombre': row[1], 'email': row[2], 'Fecha de nacimiento': row[3], 'Lenguaje de programacion favorito': row[4]}
            users.append(user)
        return jsonify({'Users': users, 'Mensaje': "Usuarios existentes"})
    except Exception as ex:
        return jsonify({'Mensaje': "Hubo tremendo Error"})



#GET UN USUARIOS 
@app.route('/usuarios/<id_usuario>')
def mostrar_usuario(id_usuario):
    try:
        cursor = conexion.connection.cursor()
        query = "SELECT * FROM usuarios WHERE id_usuario = '{0}'".format(id_usuario)
        cursor.execute(query)
        data = cursor.fetchone()
        if data != None:
            user = {'Nombre': data[1], 'email': data[2], 'Fecha de nacimiento': data[3], 'Lenguaje de programacion favorito': data[4]}
            return jsonify({'Usuario': user, 'Mensaje': "Mostrando usuario encontrado"})
        else:
            return jsonify({'Mensaje': "Usuario no encontrado"})
    except Exception as ex:
        return jsonify({'Mensaje': "Hubo tremendo Error"})




#GET TODOS LOS LOG'S 
@app.route('/historial')
def historial_de_login():
    try:
        cursor = conexion.connection.cursor()
        query = 'SELECT * FROM historial_de_login'
        cursor.execute(query)
        data = cursor.fetchall()
        stories = []
        for row in data:
            history = {'Id del Usuario': row[2], 'Tipo': row[1], 'Fecha y hora': row[0], 'Nombre de proyecto consultado': row[3]}
            stories.append(history)
        return jsonify({'Historial': stories, 'Mensaje': "Historial de login del usuario"})
    except Exception as ex:
        return jsonify({'Mensaje': "Hubo tremendo Error"})



#GET UN LOG EN ESPECIFICO
@app.route('/historial/<id_usuario>')
def un_historial_de_login(id_usuario):
    try:
        cursor = conexion.connection.cursor()
        query = "SELECT * FROM historial_de_login WHERE id_usuario = '{0}'".format(id_usuario)
        cursor.execute(query)
        data = cursor.fetchone()
        if data != None:
            history = {'Id del Usuario': data[2], 'Tipo': data[1], 'Fecha y hora': data[0], 'Nombre de proyecto consultado': data[3]}
            return jsonify({'Historial': history, 'Mensaje': "Mostrando historial encontrado"})
        else:
            return jsonify({'Mensaje': "Historial no encontrado"})
    except Exception as ex:
        return jsonify({'Mensaje': "Hubo tremendo Error"})



#GET TODOS LOS REPOSITORIOS
@app.route('/repositorios')
def repositorios():
    try:
        cursor = conexion.connection.cursor()
        query = 'SELECT * FROM repositorios'
        cursor.execute(query)
        data = cursor.fetchall()
        repositorios = []
        for row in data:
            repositorio = {'Nombre del proyecto': row[1], 'Lenguaje': row[2], 'Descripcion': row[4], 'Fecha de creacion': row[3], 'Creado por': row[6]}
            repositorios.append(repositorio)
        return jsonify({'Repositorio': repositorios, 'Mensaje': "Repositorios del usuario"})
    except Exception as ex:
        return jsonify({'Mensaje': "Hubo tremendo Error"})



#GET REPOSITORIO EN ESPECIFICO
@app.route('/repositorios/<id_repositorio>')
def repositorio(id_repositorio):
    try:
        cursor = conexion.connection.cursor()
        query = "SELECT * FROM repositorios WHERE id_repositorio = '{0}'".format(id_repositorio)
        cursor.execute(query)
        data = cursor.fetchone()
        if data != None:
            repositorio = {'Nombre del proyecto': data[1], 'Lenguaje': data[2], 'Descripcion': data[4], 'Fecha de creacion': data[3], 'Creado por': data[6]}
            return jsonify({'Repositorio': repositorio, 'Mensaje': "Mostrando repositorios encontrado"})
        else:
            return jsonify({'Mensaje': "Repositorio no encontrado"})
    except Exception as ex:
        return jsonify({'Mensaje': "Hubo tremendo Error"})




#POST USUARIOS
@app.route('/usuarios', methods=['POST'])
def alta_usuario():
    try:
        cursor = conexion.connection.cursor()
        query = """INSERT INTO usuarios (nombre, email, fecha_de_nacimiento, lenguaje_de_programacion_favorito, password) 
                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(request.json['nombre'], request.json['email'], 
                request.json['fecha_de_nacimiento'], request.json['lenguaje_de_programacion_favorito'], request.json['password'])
        cursor.execute(query)
        conexion.connection.commit()
        return jsonify({'Mensaje': "Usuario registrado."})
        # print(request.json["fecha_de_nacimiento"])
    except Exception as ex:
        return jsonify({"Mensaje": "Hubo tremendo Error"})



#POST REPOSITORIOS
@app.route('/repositorios', methods=['POST'])
def subir_repositorio():
    try:
        cursor = conexion.connection.cursor()
        query = """INSERT INTO repositorios (nombre_de_proyecto, lenguaje, fecha_de_creacion, descripcion, id_usuario, usuario) 
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""".format(request.json['nombre_de_proyecto'], request.json['lenguaje'], 
            request.json['fecha_de_creacion'], request.json['descripcion'], request.json['id_usuario'], request.json['usuario'])
        cursor.execute(query)
        conexion.connection.commit()
        return jsonify({'Mensaje': "Repositorio subido completamente."})
    except Exception as ex:
        return jsonify({"Mensaje": "Hubo tremendo Error"})



#POST HISTORIAL
@app.route('/historial', methods=['POST'])
def registrar_log():
    try:
        cursor = conexion.connection.cursor()
        query = """INSERT INTO historial_de_login (fecha_y_hora, tipo, id_usuario, nombre_de_proyecto) 
            VALUES ('{0}', '{1}', '{2}', '{3}')""".format(request.json['fecha_y_hora'], request.json['tipo'], 
            request.json['id_usuario'], request.json['nombre_de_proyecto'])
        cursor.execute(query)
        conexion.connection.commit()
        print(request.json)
        return jsonify({'Mensaje': "Login registrado."})
    except Exception as ex:
        return jsonify({"Mensaje": "Hubo tremendo Error"})




#DELETE USUARIOS
@app.route('/usuarios/<id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    try:
        cursor = conexion.connection.cursor()
        query = "DELETE FROM usuarios WHERE id_usuario = '{0}'".format(id_usuario)
        cursor.execute(query)
        conexion.connection.commit()
        return jsonify({'Mensaje': "Usuario eliminado."})
    except Exception as ex:
        return jsonify({'Mensaje': "Usuario no encontrado."})




#DELETE REPOSITORIOS
@app.route('/repositorios/<id_repositorio>', methods=['DELETE'])
def eliminar_repositorio(id_repositorio):
    try:
        cursor = conexion.connection.cursor()
        query = "DELETE FROM repositorios WHERE id_repositorio = '{0}'".format(id_repositorio)
        cursor.execute(query)
        conexion.connection.commit()
        return jsonify({'Mensaje': "Repositorio eliminado."})
    except Exception as ex:
        return jsonify({'Mensaje': "Repositorio no encontrado."})




#DELETE HISTORIAL
@app.route('/historial/<id_usuario>', methods=['DELETE'])
def eliminar_historial(id_usuario):
    try:
        cursor = conexion.connection.cursor()
        query = "DELETE FROM historial_de_login WHERE id_usuario = '{0}'".format(id_usuario)
        cursor.execute(query)
        conexion.connection.commit()
        return jsonify({'Mensaje': "Historial eliminado."})
    except Exception as ex:
        return jsonify({'Mensaje': "Historial no encontrado."})




#PUT USUARIOS
@app.route('/usuarios/<id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    try:
        cursor = conexion.connection.cursor()                                    
        query = """UPDATE usuarios SET nombre = '{0}', email = '{1}',  fecha_de_nacimiento = '{2}',  lenguaje_de_programacion_favorito = '{3}',  
            password = '{4}'  WHERE id_usuario = {5}""".format(request.json['nombre'], request.json['email'], request.json['fecha_de_nacimiento'], 
            request.json['lenguaje_de_programacion_favorito'], request.json['password'], id_usuario)
        cursor.execute(query)
        conexion.connection.commit()
        return jsonify({'Mensaje': "Usuario actualizado."})
    except Exception as ex:
        return jsonify({'Mensaje': "Usuario no encontrado."})




#PUT HISTORIAL
@app.route('/historial/<id_usuario>', methods=['PUT'])
def actualizar_historial(id_usuario):
    try:
        cursor = conexion.connection.cursor()                                    
        query = """UPDATE historial_de_login SET fecha_y_hora = '{0}', tipo = '{1}',  nombre_de_proyecto = '{2}' 
            WHERE id_usuario = {3}""".format(request.json['fecha_y_hora'], request.json['tipo'], request.json['nombre_de_proyecto'], id_usuario)
        cursor.execute(query)
        conexion.connection.commit()
        print(request.json)
        print(id_usuario)
        return jsonify({'Mensaje': "Historial actualizado."})
    except Exception as ex:
        print(request.json)
        print(id_usuario)
        return jsonify({'Mensaje': "Historial no encontrado."})




#PUT REPOSITORIOS
@app.route('/repositorios/<id_repositorio>', methods=['PUT'])
def actualizar_respositorio(id_repositorio):
    try:
        cursor = conexion.connection.cursor()
        query = """UPDATE repositorios SET nombre_de_proyecto = '{0}', lenguaje = '{1}',  fecha_de_creacion = '{2}',  descripcion = '{3}',  id_usuario = '{4}',  
            usuario = '{5}' WHERE id_repositorio = {6}""".format( request.json['nombre_de_proyecto'], request.json['lenguaje'], request.json['fecha_de_creacion'], 
            request.json['descripcion'], request.json['id_usuario'], request.json['usuario'], id_repositorio)
        cursor.execute(query)
        conexion.connection.commit()
        print(request.json)
        print(id_repositorio)
        return jsonify({'Mensaje': "Historial actualizado."})
    except Exception as ex:
        print(request.json)
        print(id_repositorio)
        return jsonify({'Mensaje': "Historial no encontrado."})



#PÁGINA NO ENCONTRADA
def pagina_no_encontrada(error):
    return "<h1>La página que buscas no se encuentra</h1>", 404

if __name__ == '__main__':
    load_dotenv()
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()

