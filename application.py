#Se importan librerias
import pandas as pd
import json
from urllib.request import urlopen
from flask import Flask, render_template
from api import claves
app = Flask(__name__)
@app.route('/')#
def index():
    acceso=claves()
    consulta=acceso.consultaEstados
    #conUrl=("http://clima.inifap.gob.mx/wapi/api/Estacion?")
    with urlopen(consulta) as response:source=response.read()
    data=json.loads(source)
    df=pd.DataFrame(data['estados'])
    return render_template("index.html", dato=df['Nombre'])
#@app.route('/<string:name>')
#def hello(name):
#    return "<h1>Tu elegiste: {}</h1>".format(name.upper())
@app.route('/<string:name>/<string:id>')
def est(name,id):
    acceso=claves()
    consulta=acceso.consultaEstaciones
    #consulta=("http://clima.inifap.gob.mx/wapi/api/Estacion?idEstado={}".format(id))
    with urlopen("{}idEstado={}".format(consulta,id)) as response:
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
    acceso=claves()
    consulta=acceso.consultaDatos
    print("****",estado,numesta,estacion,numero)
    #llamada="http://clima.inifap.gob.mx/wapi/api/Datos?idEstado={}&IdEstacion={}".format(estacion,numero)
    #print(llamada)
    with urlopen("{}&IdEstado={}&IdEstacion={}".format(consulta,estacion,numero)) as response:
        source=response.read()
    data=json.loads(source)
    dicc=[]
    dicc=dict(data)
    t= dicc['estaciones'][0]['Temt']#temperatura
    h= dicc['estaciones'][0]['Humr']#humedad relativa
    T=(9*int(t)/5)+32#conversion de °c a °f
    HI = -42.379 + 2.04901523*T + 10.14333127*h - .22475541*T*h - .00683783*T*T - .05481717*h*h + .00122874*T*T*h + .00085282*T*h*h - .00000199*T*T*h*h
    Pr= ((h/100)**(1/8))*(112+0.9*t)+0.1*t-112
    #print(df)
    return render_template('estaciones.html',dato2=dicc,dat3=HI,pr=Pr)
