#Se importan librerias
import pandas as pd
import json
import time
from urllib.request import urlopen
from flask import Flask, render_template, redirect, url_for
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
    T=(9*int(t)/5)+32#Conversion de °c a °f
    HI = -42.379 + 2.04901523*T + 10.14333127*h - .22475541*T*h - .00683783*T*T - .05481717*h*h + .00122874*T*T*h + .00085282*T*h*h - .00000199*T*T*h*h
    Pr= ((h/100)**(1/8))*(112+0.9*t)+0.1*t-112

    fecha1=fecha()

    fechaC=time.strftime("%d/%m/%Y")
    print(fecha1,"    ",fechaC)
    #print(df)
    print("numesta: {}  numero: {} fecha1 {}   fecha2 {}".format(estacion,numero,fecha1,fechaC))
    cons=consulta1(estacion,numero,fecha1,fechaC)
    return render_template('estaciones.html',dato2=dicc,dat3=HI,pr=Pr,consuf=cons, est=numesta)

def consulta1(estacion,numero,fecha,fechaC):
    print("numesta: {}  numero: {} fecha1 {}   fecha2 {}".format(estacion,numero,fecha,fechaC))
    acceso=claves()
    consulta2="{}&IdEstado={}&IdEstacion={}&fch1={}&fch2={}".format(acceso.consultaDatos,estacion,numero,fecha,fechaC)
    print(consulta2)
    with urlopen(consulta2) as response:
        source=response.read()
    data=json.loads(source)
    df=pd.DataFrame(data['estaciones'])
    return df


def fecha():
    dia=int(time.strftime("%d"))
    mes=int(time.strftime("%m"))
    año=int(time.strftime("%Y"))

    dia1=dia
    mes1=mes
    año1=año
    if mes<=12:
        if mes==1:
            if dia<=5:
                año=año-1
                mes=12
                dia=dia1-5+31
                fech1=("{}/{}/{}".format(dia,mes,año))
                #print("{}/{}/{}".format(dia,mes,año))
            else:
                dia=dia-5
        else:
            if mes==2 or mes==4 or mes==6 or mes==9 or mes==11:
                if dia>30:
                    print("Este mes solo tiene 30 dias")

                else:
                    if dia<=5:
                        mes=mes-1
                        dia=dia-5+31
                        fech1=("{}/{}/{}".format(dia,mes,año))
                        #print("{}/{}/{}".format(dia,mes,año))
                    else:
                        dia= dia-5
                        fech1=("{}/{}/{}".format(dia,mes,año))
                        #print("{}/{}/{}".format(dia,mes,año))
            else:

                if mes1==3:
                    if año1%4==0:
                        if dia<=5:
                            dia=29+dia1-5
                            mes=mes1-1
                            fech1=("{}/{}/{}".format(dia,mes,año))
                            #print("{}/{}/{}".format(dia,mes,año))
                        else:
                            dia=dia1-5
                            fech1=("{}/{}/{}".format(dia,mes,año))
                            #print("{}/{}/{}".format(dia,mes,año))

                    else:
                        if dia1<=28 and año1%4!=0:
                            if dia<=5:
                                dia=28+dia1-5
                                mes=mes1-1
                            else:
                                dia=dia-5
                            fech1=("{}/{}/{}".format(dia,mes,año))
                            #print("{}/{}/{}".format(dia,mes,año))
                        else:
                            print("Este mes solo 28 dias")
                else:

                    if dia>31:
                        print("Este mes solo tiene 31 dias")
                    else:
                        if dia<=5:
                            mes=mes-1
                            dia=dia-5+30
                            fech1=("{}/{}/{}".format(dia,mes,año))
                            #print("{}/{}/{}".format(dia,mes,año))
                        else:
                            dia= dia-5
                            fech1=("{}/{}/{}".format(dia,mes,año))
                            #print("{}/{}/{}".format(dia,mes,año))

    else:
        print("Mes no valido")

    return fech1

if __name__=="__main__":app.run()
