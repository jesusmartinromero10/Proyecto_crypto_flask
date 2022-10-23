
from flask import redirect, render_template, request, url_for, flash
from cryptomonedas import app
import sqlite3
from cryptomonedas.forms import Moneda
from config import apikey
from cryptomonedas.models import select_all, insert, peticion_crypto, invertido, recuperado, totalActivo_una_consulta, validador
from datetime import datetime
from wtforms import HiddenField



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
    valorCantidad = request.values.get("inputCantidad") 
    valorCantidad2 = HiddenField
    if request.method == "GET":
        return render_template("/purchase.html", PageTitle = "Comprar", formulario = moneda, cabecera = 'purchase.html', cantidad = "input")
    
    else:
        try:
            if request.values.get("submitCalcular"):
                
                try:
                    if moneda.inputCantidad.data == None:
                        flash("Introduce en la casilla de Cantidad un dato numerico. O si es decimal usa el . (Punto) no la ,(Coma) para los decimales")
                        return redirect(url_for("comprar"))
                    resultado = peticion_crypto(moneda.moneda_from.data, moneda.moneda_to.data, apikey)
                    total = resultado['rate'] * float(valorCantidad)
                    total = ("{:.8f}".format(total))
                    tasa = resultado['rate']
                    tasa = ("{:.8f}".format(tasa))
                    valorCantidad2._value = valorCantidad
                    
                    return render_template("/purchase.html", resultado = total, Tasa = tasa, formulario = moneda, cabecera = "purchase.html", cantidad = "texto", valorinput = valorCantidad, texmoneda = moneda.moneda_to.data)
                except Exception as e:
                    print(e)
                    flash("Error conexion con Api, intentelo pasados unos minutos")
                    return redirect(url_for("index"))
        
      
            elif request.values.get("submitCompra"):
                
                try:
                    validat = validador()
                    if validat != []:
                        return redirect (url_for('comprar'))
                   
                    if moneda.validate():
                        resultado = peticion_crypto(moneda.moneda_from.data, moneda.moneda_to.data, apikey)
                        total = resultado['rate'] * float(valorCantidad)
                        insert([datetime.now().date().isoformat(), str(datetime.now().time().isoformat())[:8], resultado["asset_id_base"], valorCantidad, resultado["asset_id_quote"], total])
                        flash("Compra realizada correctamente")
                        return redirect(url_for('index'))
                except sqlite3.Error as e:
                    print(e)
                    flash("Se a producido error en la base datos")
                    return redirect(url_for('index'))
                
                
            else:
                flash('Ha ocurrido un error inesperado, vuelva a intentarlo')
                return redirect(url_for('index'))
        
        except Exception as e:
            print(e)
            flash("Error, vuelva a intentarlo")
            return redirect(url_for("index"))


@app.route("/status")
def estado():
    inver = invertido()
    if inver[0]['Cantidad_from'] == None:
        flash("No hay compras de Cryptomonedas")
        return render_template("status.html", inv = [{'Cantidad_from': 0}], rec = [{'Cantidad_to': 0}], vComp = 0, vAct = 0, ganancia = 0, cabecera = 'status.html')
        
    else:   
        
        try:
            inv = invertido()
            rec = recuperado()
            vComp = inv[0]['Cantidad_from'] - rec[0]['Cantidad_to']
            vActi = totalActivo_una_consulta()
        
            return render_template("status.html", inv = inv, rec = rec, vComp = vComp , vAct = vActi, ganancia = vActi - vComp, cabecera = 'status.html')
        except Exception as e:
            print(e)
            flash("Error de calculo intentelo mas tarde")
            return redirect(url_for('index'))

