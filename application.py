#LIbrerias
import pandas as pd
import json
from urllib.request import urlopen
from flask import Flask, render_template
from api import claves
app=Flask(__name__) #asignacion de la página

a=""
@app.route('/') #asignacion del index
def datos():
    acceso=claves()
    cons=acceso.consultaEstados
    #consulta='http://clima.inifap.gob.mx/wapi/api/Estacion?'
    with urlopen(cons) as response:
        source=response.read()
    data=json.loads(source)
    df = pd.DataFrame(data['estados'])
    return render_template('pagina.html',da=df['Nombre'])

@app.route('/<string:name>/<string:id>')
def est(name,id):
    acceso=claves()
    cons=acceso.consultaEstaciones
    #consulta="http://clima.inifap.gob.mx/wapi/api/Estacion?idEstado={}".format(id)
    with urlopen("{}idEstado={}".format(cons,id)) as response:
        source=response.read()
    data=json.loads(source)
    df = pd.DataFrame(data['est'])
    a=df['Numero']
    return render_template('pagina2.html',da1=df['Nombre'],estado=name,nums=id,estaci=a)

@app.route('/<string:fir>/<string:esta>/<string:estacion>/<string:numes>')
def estacion(fir,esta,estacion,numes):
    print(fir,"  ",esta,"  ",estacion,"  ",numes)
    acceso=claves()
    cons=acceso.consultaDatos
    #consulta="http://clima.inifap.gob.mx/wapi/api/Datos?idEstado={}&IdEstacion={}".format(esta,numes)
    print("***** consulta",cons)
    with urlopen('{}idEstado={}&IdEstacion={}'.format(cons,esta,numes)) as response:
        source=response.read()
    data=json.loads(source)
    d = dict(data)
    return render_template('est.html',da2=d)
