#LIbrerias
import pandas as pd
import json
from urllib.request import urlopen
from flask import Flask, render_template
app=Flask(__name__) #asignacion de la página

a=""
@app.route('/') #asignacion del index
def datos():
    with urlopen('http://clima.inifap.gob.mx/wapi/api/Estacion?') as response:
        source=response.read()
    data=json.loads(source)
    df = pd.DataFrame(data['estados'])
    return render_template('index.html',da=df['Nombre'])
#@app.route('/<string:name>')
#def hello(name):
    #return "<h1>Tu elegiste: {}</h1>".format(name.upper())
@app.route('/<string:name>/<string:id>')
def est(name,id):
    with urlopen('http://clima.inifap.gob.mx/wapi/api/Estacion?idEstado={}'.format(id)) as response:
        source=response.read()
    data=json.loads(source)
    df = pd.DataFrame(data['est'])
    a=df['Numero']
    return render_template('estacion.html',da1=df['Nombre'],estado=name,nums=id,estaci=a)

@app.route('/<string:fir>/<string:esta>/<string:estacion>/<string:numes>')
def estacion(fir,esta,estacion,numes):
    print(fir,"  ",esta,"  ",estacion,"  ",numes)

    consulta="http://clima.inifap.gob.mx/wapi/api/Datos?idEstado={}&IdEstacion={}".format(esta,numes)
    print("***** consulta",consulta)
    with urlopen(consulta) as response:
        source=response.read()
    data=json.loads(source)
    d = dict(data)
    return render_template('est.html',da2=d)
