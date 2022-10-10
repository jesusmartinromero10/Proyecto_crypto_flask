
from flask import redirect, render_template, request, url_for, flash
from cryptomonedas import app
import sqlite3
from cryptomonedas.forms import Moneda
from config import apikey
from cryptomonedas.models import select_all
from datetime import datetime, date
import requests



@app.route("/")
def index():
    try:
        registros = select_all()
        return render_template("index.html", pageTitle = "Cryptomonedas", data =registros)
    except sqlite3.Error as e:
        flash("Se a producido error en la base datos")
        return render_template("index.html", pageTitle="Todos", data = [])

@app.route("/purchase", methods=["GET", "POST"])
def comprar():
    registros = Moneda()
    if request.method == "GET":
        return render_template("/purchase.html", PageTitle = "Comprar", formulario = registros)
    
    else:
        time = datetime.now()
        url = requests.get(f"https://rest.coinapi.io/v1/exchangerate/{registros.moneda_from.data}/{registros.moneda_to.data}?&apikey={apikey}")
        resultado = url.json()
        tasa = resultado['rate'] * float(request.values.get("inputCantidad"))
        total = resultado['rate'] 
        return render_template("/purchase.html", resultado = tasa, Total = total, formulario = registros)