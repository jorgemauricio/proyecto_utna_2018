#LIbrerias
import pandas as pd
import json
from urllib.request import urlopen
from flask import Flask, render_template
app=Flask(__name__) #asignacion de la página

id=""
@app.route('/') #asignacion del index
def datos():
    arr=[]
    with urlopen('http://clima.inifap.gob.mx/wapi/api/Estacion?') as response:
        source=response.read()
    data=json.loads(source)
    df = pd.DataFrame(data['estados'])
    return render_template('index.html',dato=df['Nombre'])

@app.route('/<string:name>/<string:id>')

def est(name,id):
    with urlopen('http://clima.inifap.gob.mx/wapi/api/Estacion?idEstado={}'.format(id)) as response:
        source=response.read()
    data=json.loads(source)
    df = pd.DataFrame(data['est'])
    return render_template('estacion.html',dato=df['Nombre'])

@app.route('/<string:name>/<string:Numero>')
def estaciones(name,numero):
    with urlopen('http://clima.inifap.gob.mx/wapi/api/Datos?idEstado=1&IdEstacion={}'.format(numero)) as response:
        source=response.read()
    data=json.loads(source)
    df = pd.DataFrame(data['estaciones'])
    return render_template('estaciones.html',dato=df['Nombre'])
