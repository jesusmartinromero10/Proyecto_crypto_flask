# WEB CRYPTOMONEDAS
- Proyecto Final BootCamp Zero - IV Edición | KeepCoding

- Aplicación web en Flask

- Simulador de conversión e inversión en Criptomonedas

# Compra-ventas y tradeo de Cryptomonedas

Programa hecho en como lenguaje principal python. Tambien se a usado Flask, Html5, CSS3 y Jinja.
Para recuperar el valor de las criptos a sido desde Coinapi.io

## Instalación 🔧

- Obtener la apikey en Coinapi.io.
- Obtener una Scret Key en https://randomkeygen.com/ 
- Hacer una copia del fichero `config_template.py`:
        - En la clave apikey  poner tu clave

```
apikey = "45gt76u67ii8i"
```
        - En el SECRET_KEY poner tu Secret Key
```
SECRET_KEY = "4rfEw65hg45y6h4g4"
```

- renombrar al fichero copia como `config.py`
- Descargar la app DB Browser for SQLite
- En la carpeta data hay un fichero llamado create.sql que tiene la estructura para crear la tabla de la base de datos en DB Browser
- hacer una copia del fichero `.env_template` y el FLASK_DEBUG poner True o False


### Instalacion de dependencias

- Ejecutar `pip install -r requirements.txt``

Por ultimo ejecutar

```
flask run
```
o tambien
```
python tasaintercambio.py
```