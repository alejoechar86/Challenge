from asyncio.windows_events import NULL
from distutils.log import error
#Uso de requests para la funcionalidad de GET
import requests
#Creación de la base de datos a través de SQLite3
import sqlite3
import mailbox
import json

#Llamdo al framework flask
from flask import Flask, jsonify


#Creación de la base de datos
def crearBD():
    conex = sqlite3.connect("Base_Datos.db")
    conex.commit()
    conex.close()

#Creación de la Tabla
def CrearTabla():
    conex = sqlite3.connect("Base_Datos.db")
    cursor = conex.cursor()
    cursor.execute(
        """CREATE TABLE BD_Clientes (fec_alta text, user_name text, codigo_zip text,
     credit_card_num text, credit_card_ccv text, cuenta_numero text, direccion text, geo_latitud text,
     geo_longitud text, color_favorito text, foto_dni text, ip text, auto text, auto_modelo text,
     auto_tipo text, auto_color text, cantidad_compras_realizadas text, avatar text,
     fec_birthday text, iden text)""")
    conex.commit()
    conex.close()

#Creación de la Tabla Usuarios
def CrearTablaUsuarios():
    conex = sqlite3.connect("Base_Datos.db")
    cursor = conex.cursor()
    cursor.execute(
        """CREATE TABLE BD_Usuarios (usuario text, nombre text, apellido text, correo text, perfil int)""")
    conex.commit()
    conex.close()

#Insertar los datos en la base de datos
def InsertarDato():
    conex = sqlite3.connect("Base_Datos.db")
    cursor = conex.cursor()
    cursor.execute("""INSERT INTO BD_Clientes VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}',
    '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
    '{}')""".format(valor[0],valor[1], valor[2], valor[3], valor[4], valor[5], valor[6], valor[7],
    valor[8], valor[9], valor[10], valor[11], valor[12], valor[13], valor[14], valor[15], valor[16],
    valor[17], valor[18], valor[19]))
    conex.commit()
    conex.close()

#Sentencia de obtener toda la información de la base de datos
def SelectDato1(consultaidentidad):
    conex = sqlite3.connect("Base_Datos.db")
    cursor = conex.cursor()
    print (consultaidentidad)
    print ("*******************************")
    #instruccion = 'SELECT * FROM BD_Clientes'
    instruccion = "SELECT * FROM BD_Clientes WHERE iden = '{}'".format(consultaidentidad)
    cursor.execute(instruccion)
    Data = cursor.fetchall()
    #print (Data)
    return (Data)
    conex.commit()
    conex.close()

#Sentencia de obtener alguna información de la base de datos
def SelectDato2(consultaidentidad):
    conex = sqlite3.connect("Base_Datos.db")
    cursor = conex.cursor()
    instruccion = "SELECT fec_alta, user_name, codigo_zip, direccion, auto, auto_modelo, auto_tipo, auto_color, fec_birthday, iden FROM BD_Clientes WHERE iden = '{}'".format(consultaidentidad)
    cursor.execute(instruccion)
    Data = cursor.fetchall()
    #print (Data)
    return (Data)
    conex.commit()
    conex.close()

#Sentencia de obtener otra información de la base de datos
def SelectDato3(consultaidentidad):
    conex = sqlite3.connect("Base_Datos.db")
    cursor = conex.cursor()
    instruccion = "SELECT user_name, credit_card_num, credit_card_ccv, cuenta_numero, color_favorito, foto_dni, ip, cantidad_compras_realizadas, fec_birthday, iden FROM BD_Clientes WHERE iden = '{}'".format(consultaidentidad)
    cursor.execute(instruccion)
    Data = cursor.fetchall()
    #print (Data)
    return (Data)
    conex.commit()
    conex.close()

#Sentencia de obtener el perfil del usaurio de consulta
def SelectUsuario():
    conex = sqlite3.connect("Base_Datos.db")
    cursor = conex.cursor()
    instruccion = 'SELECT perfil FROM BD_Usuarios'
    cursor.execute(instruccion)
    Data = cursor.fetchone()
    #print (Data)
    return (Data)
    conex.commit()
    conex.close()


#llamar la información de la URL
url="https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios"

#Get de la información de la URL
I = requests.get(url)
Info = I.json()
lista = Info[0]
columnas = list(lista.keys())

try:
    #Llamar crear Base de Datos
    crearBD()
    #Llamar crear Tabla
    CrearTabla()
    CrearTablaUsuarios()
    print ("No existía la base de datos y ya se creó")
    print ("Ya se creó la tabla")
    x=0
    for i in Info:
        lista = Info[x]
        valor = list(lista.values())
        x += 1
        InsertarDato()
    print ("Datos guardados con éxito en la base de datos")
except:
    print ("Ya existe la base de datos con los datos cargados") 
    
#Definición de mensaje de error para paginas en rutas no definidas
def pagina_error(error):
    return jsonify({'mensaje' : 'Pagina no encontrada o no existe'})


app = Flask(__name__)

@app.route('/')
def index():
    ### Definición del usuario que se autenticó exitosamente
    
    try:
        usuario = SelectUsuario()
        print (usuario)
        print (type(usuario))
        usuarios = usuario[0]
        perfilusuario = usuarios
        
        #De manera manual se ingresa el valor de identidad que el usuario de consulta quiere visualizar
        #pero esto podría ser una información que nusuario ingresaria en un front
        consultaidentidad = 1   #Numero de identidad que el usuario de consulta quiere visualizar
        
        try:
            if perfilusuario == 1: #Seleccionar la información a mostrar del perfil 1
                dato = SelectDato1(consultaidentidad)
                info_completa = list()
                columnas = list(lista.keys())
                for e in range(len(dato)):
                    dato_lista = dato[e]
                    valor_dato = list(dato_lista)
                    info_completa.append(dict(zip(columnas, valor_dato)))
                return jsonify(info_completa)
            elif perfilusuario == 2: #Seleccionar la información a mostrar del perfil 2
                dato = SelectDato2(consultaidentidad)
                info_completa = list()
                columnas = ["fec_alta", "user_name", "codigo_zip", "direccion", "auto", "auto_modelo", "auto_tipo", "auto_color", "fec_birthday", "iden"]
                for e in range(len(dato)):
                    dato_lista = dato[e]
                    valor_dato = list(dato_lista)
                    info_completa.append(dict(zip(columnas, valor_dato)))
                return jsonify(info_completa)
            elif perfilusuario == 3: #Seleccionar la información a mostrar del perfil 3
                dato = SelectDato3(consultaidentidad)
                info_completa = list()
                columnas = ["user_name", "credit_card_num", "credit_card_ccv", "cuenta_numero", "color_favorito", "foto_dni", "ip", "cantidad_compras_realizadas", "fec_birthday", "iden"]
                for e in range(len(dato)):
                    dato_lista = dato[e]
                    valor_dato = list(dato_lista)
                    info_completa.append(dict(zip(columnas, valor_dato)))
                return jsonify(info_completa)
            else:
                return jsonify("Usuario no valido")
        except Exception as err:
            return "Error"
    except:
        return ("Usuarios de consulta no creados aún en la base de datos")

if __name__ == '__main__':
    app.register_error_handler(404,pagina_error)
    app.run(debug=True, port=8080)
    
