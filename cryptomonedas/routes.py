from cryptomonedas import app




@app.route("/")
def index():
    return "hola"