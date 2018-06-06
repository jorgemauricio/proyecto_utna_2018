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
    with urlopen(cons) as response:
        source=response.read()
    data=json.loads(source)
    df = pd.DataFrame(data['estados'])
    return render_template('pagina.html',da=df['Nombre'])
#@app.route('/<string:name>')
#def hello(name):
    #return "<h1>Tu elegiste: {}</h1>".format(name.upper())
@app.route('/<string:name>/<string:id>')
def est(name,id):
    acceso=claves()
    cons=acceso.consultaEstaciones
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
    cons= '{}idEstado={}&IdEstacion={}'.format(acceso.consultaDatos,esta,numes)
    print("***** consulta",cons)
    with urlopen(cons) as response:
        source=response.read()
    data=json.loads(source)
    d = dict(data)
    F=d['estaciones'][0]['Temt']
    RH=d['estaciones'][0]['Humr']
    T =F * 1.8000 + 32.00
#IC = (-42.379 + (2.04901523 * T) + (10.14333127 * R) - (0.22475541 * (T*R))  - (6.83783e-3 * (T*T)) - (5.481717e-2 * (R*R)) + ( 1.22874e-3 * (T*T*R)) + (8.5282e-4 * (T*R*R)) - (1.99e-6 * (T*T*R*R)))
    IC=  -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH
    Pr= ((RH/100)*(100+F)-100)/8
    return render_template('pagina3_1.html',da2=d,c=IC,pr=Pr)
