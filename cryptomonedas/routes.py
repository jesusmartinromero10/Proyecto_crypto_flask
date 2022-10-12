
from flask import redirect, render_template, request, url_for, flash
from cryptomonedas import app
import sqlite3
from cryptomonedas.forms import Moneda
from config import apikey, cryptos
from cryptomonedas.models import select_all, insert, peticion_crypto, invertido, recuperado, union, valorActual, valorCompra, cartera
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
    moneda = Moneda()
    registros = select_all()
    valorCantidad = request.values.get("inputCantidad") 
    valorMonedaFrom = request.values.get('moneda_from')
    valorMonedaTo = request.values.get('moneda_to')
    if request.method == "GET":
        return render_template("/purchase.html", PageTitle = "Comprar", formulario = moneda, cabecera = 'purchase.html')
    
    else:
        try:
            if request.values.get("submitCalcular"):
                
                try:
                    resultado = peticion_crypto(moneda.moneda_from.data, moneda.moneda_to.data, apikey)
                    total = resultado['rate'] * float(valorCantidad)
                    total = ("{:.8f}".format(total))
                    tasa = resultado['rate']
                    tasa = ("{:.8f}".format(tasa))
                    return render_template("/purchase.html", resultado = total, Tasa = tasa, formulario = moneda, cabecera = "purchase.html")
                except:
                    flash("Error conexion con Api, intentelo pasados unos minutos")
                    return redirect(url_for("index"))
        
      

            elif request.values.get("submitCompra"):
                
                try:
                    
                    if registros == [] and valorMonedaFrom != "EUR":
                        flash("La primera compra de Cryptomonedas tiene que ser compradas con Euros")
                        return redirect(url_for("purchase.html"))
                    if valorMonedaFrom == valorMonedaTo:
                        flash("Las monedas no pueden ser las mismas")
                        return redirect(url_for('comprar'))

                    monedero = cartera(valorMonedaFrom)
                    if valorMonedaFrom != 'EUR' and monedero[0][valorMonedaFrom] < float(valorCantidad):
                        flash(f"No tienes saldo suficiente de {valorMonedaFrom}")
                        return redirect(url_for('purchase.html'))
                    

                    if moneda.validate():
                        resultado = peticion_crypto(moneda.moneda_from.data, moneda.moneda_to.data, apikey)
                        total = resultado['rate'] * float(valorCantidad)
                        insert([datetime.now().time(), datetime.now().date(), resultado["asset_id_base"], valorCantidad, resultado["asset_id_quote"], total])
                    flash("Compra realizada correctamente")
                    return redirect(url_for('index'))
                except sqlite3.Error as e:
                    flash("Se a producido error en la base datos2")
                    return redirect(url_for('index'))
                
                
            else:
                flash('Ha ocurrido un error inesperado, vuelva a intentarlo')
                return redirect(url_for('index'))
        
        except:
            flash("Error, vuelva a intentarlo")
            return redirect(url_for("index"))


@app.route("/status")
def estado():
    try:
        return render_template("status.html", inv = invertido(), rec = recuperado(), vComp = valorCompra(), vAct = valorActual(), cabecera = 'status.html')
    except:
        flash("Error de calculo intentelo mas tarde")
        return redirect(url_for('index'))