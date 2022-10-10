import sqlite3
from config import *


def filas_to_diccionario(filas, columnas):

    resultado = []
    for fila in filas:  
        posicion_columna = 0
        d = {}
        for campo in columnas:
            d[campo[0]] = fila[posicion_columna]
            posicion_columna += 1
        resultado.append(d)
    
    return resultado


def select_all():
    conn= sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("SELECT id, Fecha, Hora, moneda_from, cantidad_from, Moneda_to, Cantidad_to, (cantidad_from/Cantidad_to) as PU from movements;")
    result = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return result