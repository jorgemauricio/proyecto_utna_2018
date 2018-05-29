#librerias
import pandas as pd
import json
from urllib.request import urlopen
from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    with urlopen("http://clima.inifap.gob.mx/wapi/api/Estacion?") as response:source=response.read()
    data=json.loads(source)
    df=pd.DataFrame(data['estados'])
    return render_template("index.html", dato=df['Nombre'])
#@app.route('/<string:name>')
#def hello(name):
#    return "<h1>Tu elegiste: {}</h1>".format(name.upper())
@app.route('/<string:name>/<string:id>')
def est(name,id):
    with urlopen("http://clima.inifap.gob.mx/wapi/api/Estacion?idEstado={}".format(id)) as response:
        source=response.read()
    data=json.loads(source)
    df=pd.DataFrame(data['est'])
    df
    tac=df['Numero']
    tac
#estac=tac
    #print(df)
    return render_template('estacion.html',dato1=df['Nombre'],estado=name, num=id,estac=tac)


@app.route('/<string:estado>/<string:estacion>/<string:numesta>/<string:numero>')
def estacion(estado,numesta,estacion,numero):
    print("****",estado,numesta,estacion,numero)
    llamada="http://clima.inifap.gob.mx/wapi/api/Datos?idEstado={}&IdEstacion={}".format(estacion,numero)
    print(llamada)
    with urlopen(llamada) as response:
        source=response.read()
    data=json.loads(source)
    dicc=[]
    dicc=dict(data)

    #print(df)
    return render_template('estaciones.html',dato2=dicc)
