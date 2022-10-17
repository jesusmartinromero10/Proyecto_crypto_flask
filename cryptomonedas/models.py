from wtforms import HiddenField
import sqlite3
from config import *
import requests
from datetime import *
from cryptomonedas.routes import *


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
    cur.execute("SELECT id, Fecha, Hora, moneda_from, cantidad_from, Moneda_to, Cantidad_to, (cantidad_from/Cantidad_to) as PU from movements order by Fecha;")
    result = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return result


def insert(registro):
  
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("INSERT INTO movements (Fecha, Hora, Moneda_from, Cantidad_from, Moneda_to, cantidad_to) values(?,?,?,?,?,?)", registro)
    conn.commit()
    conn.close()

def peticion_crypto(moneda_from_data, moneda_to_data, apikey):
    url = requests.get(f"https://rest.coinapi.io/v1/exchangerate/{moneda_from_data}/{moneda_to_data}?&apikey={apikey}")
    resultado = url.json()
    return resultado

def invertido():
    conn= sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("SELECT SUM(Cantidad_from) as Cantidad_from FROM movements WHERE Moneda_from = 'EUR'")
    result = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return result

def recuperado():
    conn= sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("SELECT (CASE WHEN SUM(Cantidad_to) IS NULL THEN 0 ELSE SUM(Cantidad_to) end) as Cantidad_to FROM movements WHERE Moneda_to = 'EUR'")
    result = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return result  

def cartera(moneda):
    consulta = f"SELECT ((SELECT (case when (SUM(Cantidad_to)) is null then 0 else SUM(Cantidad_to) end) as tot FROM movements WHERE Moneda_to = '{moneda}') - (SELECT (case when (SUM(Cantidad_from)) is null then 0 else SUM(Cantidad_from) end) as ee FROM movements WHERE Moneda_from = '{moneda}')) AS {moneda}"

    conn= sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute(consulta)
    result = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return result  


def traerTodasCartera(crypto):
    cryptosMonedas = {}
    conn= sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    for moneda in crypto:
        consulta = f"SELECT ((SELECT (case when (SUM(Cantidad_to)) is null then 0 else SUM(Cantidad_to) end) as tot FROM movements WHERE Moneda_to = '{moneda}') - (SELECT (case when (SUM(Cantidad_from)) is null then 0 else SUM(Cantidad_from) end) as ee FROM movements WHERE Moneda_from = '{moneda}')) AS {moneda}"
        cur.execute(consulta)
        fila =cur.fetchall() 
        cryptosMonedas[moneda] = fila[0][0]
    conn.close()
     
    return cryptosMonedas


def totalActivo_una_consulta():    
    total = 0
    monederoActual = traerTodasCartera(cryptos)
    url = requests.get(f"https://rest.coinapi.io/v1/exchangerate/EUR?&apikey={apikey}")
    resultado = url.json()

    for a in monederoActual.keys():
        for b in resultado['rates']:
            if b['asset_id_quote'] == a:
                total += 1/b['rate'] * monederoActual[a]
                
    return total


def validador():
    error = []
    registros = select_all()
    valorCantidad = request.values.get("inputCantidad") 
    valorMonedaFrom = request.values.get('moneda_from')
    valorMonedaTo = request.values.get('moneda_to')
    valorCantidad2 = HiddenField

    if registros == [] and valorMonedaFrom != "EUR":
        error2 = flash("La primera compra de Cryptomonedas tiene que ser compradas con Euros")
        error.append(error2)
        return error
       
    if valorMonedaFrom == valorMonedaTo:
        error2 = flash("Las monedas no pueden ser las mismas")
        error.append(error2)
        return error

    if valorCantidad2._value != valorCantidad:
        error2 = flash("Tienes que calcular el valor en el boton de calculadora antes de comprar pillin")
        error.append(error2)
        return error

    monedero = cartera(valorMonedaFrom)
    if (valorMonedaFrom != 'EUR' and monedero[0][valorMonedaFrom] < float(valorCantidad)):
        error2 = flash(f"No tienes saldo suficiente de {valorMonedaFrom}")
        error.append(error2)
        return error
    
    return error

        

    
    
    
    
    
       
                






  
