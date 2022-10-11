
from flask import redirect, render_template, request, url_for, flash
from cryptomonedas import app
import sqlite3
from cryptomonedas.forms import Moneda
from config import apikey
from cryptomonedas.models import select_all, insert, peticion_crypto, invertido, recuperado, union, valorActual, valorCompra
from datetime import datetime, date
import requests



@app.route("/")
def index():
    try:
        registros = select_all()
        return render_template("index.html", pageTitle = "Cryptomonedas", data =registros, cabecera = 'index.html')
    except sqlite3.Error as e:
        flash("Se a producido error en la base datos")
        return render_template("index.html", pageTitle="Todos", data = [])

        

@app.route("/purchase", methods=["GET", "POST"])
def comprar():
    registros = Moneda()
    if request.method == "GET":
        return render_template("/purchase.html", PageTitle = "Comprar", formulario = registros, cabecera = 'purchase.html')
    
    else:
        try:
            if request.values.get("submitCalcular"):
                resultado = peticion_crypto(registros.moneda_from.data, registros.moneda_to.data, apikey)
                total = resultado['rate'] * float(request.values.get("inputCantidad"))
                tasa = resultado['rate'] 
                return render_template("/purchase.html", resultado = total, Tasa = tasa, formulario = registros)
        
      

            elif request.values.get("submitCompra"):

                try:
                    if request.values.get('moneda_from') == request.values.get('moneda_to'):
                        flash("Las monedas no pueden ser las mismas")
                        return redirect(url_for('comprar'))

                    if registros.validate():
                        resultado = peticion_crypto(registros.moneda_from.data, registros.moneda_to.data, apikey)
                        total = resultado['rate'] * float(request.values.get("inputCantidad"))
                        insert([datetime.now().time(), datetime.now().date(), resultado["asset_id_base"], request.values.get('inputCantidad'), resultado["asset_id_base"], total])
                    flash("Compra realizada correctamente")
                    return redirect(url_for('index'))
                except sqlite3.Error as e:
                    flash("Se a producido error en la base datos")
                    return redirect(url_for('index'))
                
                
            else:
                flash('Ha ocurrido un error inesperado, vuelva a intentarlo')
                return redirect(url_for('index'))
        
        except:
            flash("Has pasado limite de consultas")
            return redirect(url_for("index"))


@app.route("/status")
def estado():
    try:
        return render_template("status.html", inv = invertido(), rec = recuperado(), vComp = valorCompra(), vAct = valorActual(), cabecera = 'status.html')
    except:
        flash("Error de calculo intentelo mas tarde")
        return redirect(url_for('index'))