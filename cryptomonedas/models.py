from lib2to3.pytree import convert
import sqlite3
from config import *
import requests
from datetime import *
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


def insert(registro):
  
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("INSERT INTO movements (Fecha, Hora, Moneda_from, Cantidad_from, Moneda_to, cantidad_to) values(?,?,?,?,?,?)", [datetime.now(), datetime.now(),registro[2],registro[3],registro[4],registro[5]])
    conn.commit()
    conn.close()

def peticion_crypto(moneda_from_data, moneda_to_data, apikey):
    url = requests.get(f"https://rest.coinapi.io/v1/exchangerate/{moneda_from_data}/{moneda_to_data}?&apikey={apikey}")
    resultado = url.json()
    return resultado