import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        con=sqlite3.connect('dbproyecto.db')   #sql_conection me da un objeto tipo connect, que me da un cursos - en java=statement
        return con
    except Error:
        print(Error)


def sql_insert(nombre, usuario, correo, contrasena, fecha_ingreso):
    #query = """ INSERT INTO PRODUCTOS (CODIGO, NOMBRE,CANTIDAD) VALUES('{}' , '{}' , '{}')""".format(codigo,nombre,cantidad)
    query=f"""INSERT INTO USUARIOS (NOMBRE, USUARIO, CORREO, CONTRASENA, FECHA_INGRESO) VALUES ( '{nombre}' , '{usuario}' , '{correo}' , '{contrasena}','{fecha_ingreso}')"""
    con = sql_connection()
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    con.close()


def sql_select():
    query=f"""SELECT * FROM USUARIOS"""
    con = sql_connection()
    cursor = con.cursor()
    cursor.execute(query)           #al realizar execute todos los datos quedan almacenados en el cursosr
    usuarios= cursor.fetchall()  #fetchall permite gestionar los datos del cursos devolviendome un matriz
    #print(usuarios)
    return usuarios
    con.close()
    #cabe decir que el fetchall trae de a 5 obs, asi sucesivamente


def sql_update_usuario(id, usuario):
    query=f"""UPDATE USUARIOS SET 
    USUARIO = '{usuario}'
    WHERE ID = {id}
    """
    print(query)
    con = sql_connection()
    cursor = con.cursor()
    cursor.execute(query)          
    con.commit()
    con.close()


def sql_update_contrasena(correo, contrasena):
    query=f"""UPDATE USUARIOS SET 
    CONTRASENA = '{contrasena}'
    WHERE CORREO = '{correo}'
    """
    print(query)
    con = sql_connection()
    cursor = con.cursor()
    cursor.execute(query)          
    con.commit()
    con.close()

def sql_update_codigo_autenticar(correo, cod):
    query=f"""UPDATE USUARIOS SET 
    cod_autenticacion = '{cod}'
    WHERE CORREO = '{correo}'
    """
    print(query)
    con = sql_connection()
    cursor = con.cursor()
    cursor.execute(query)          
    con.commit()
    con.close()

def sql_delete(id):
    query=f"""DELETE FROM USUARIOS WHERE ID = {id} """
    con=sql_connection()
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    con.close()


#----------------------------------------
 # TABLA IMAGENES
#--------------------------------------
def sql_insert_imagen(titulo, id_usuario, fecha_creacion, link):
        #query = """ INSERT INTO PRODUCTOS (CODIGO, NOMBRE,CANTIDAD) VALUES('{}' , '{}' , '{}')""".format(codigo,nombre,cantidad)
    query=f"""INSERT INTO IMAGENES (TITULO, ID_USUARIO, FECHA_CREACION, LINK) VALUES ( '{titulo}' , '{id_usuario}' , '{fecha_creacion}' , '{link}')"""
    con = sql_connection()
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    con.close()


def sql_select_imagen():
    query=f"""SELECT * FROM IMAGENES"""
    con = sql_connection()
    cursor = con.cursor()
    cursor.execute(query)           #al realizar execute todos los datos quedan almacenados en el cursosr
    usuarios= cursor.fetchall()  #fetchall permite gestionar los datos del cursos devolviendome un matriz
    #print(usuarios)
    return usuarios
    con.close()
    #cabe decir que el fetchall trae de a 5 obs, asi sucesivamente


def sql_update_imagen(id, titulo):
    query=f"""UPDATE IMAGENES SET 
    TITULO = '{titulo}'
    WHERE ID = {id}
    """
    print(query)
    con = sql_connection()
    cursor = con.cursor()
    cursor.execute(query)          
    con.commit()
    con.close()


def sql_update_link(id, link):
    query=f"""UPDATE IMAGENES SET 
    LINK = '{link}'
    WHERE ID = {id}
    """
    print(query)
    con = sql_connection()
    cursor = con.cursor()
    cursor.execute(query)          
    con.commit()
    con.close()
    

def sql_delete_imagenes(id):
    query=f"""DELETE FROM IMAGENES WHERE ID = {id} """
    con=sql_connection()
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    con.close()   



