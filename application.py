#Se importan librerias
import pandas as pd
import json
import time
import math
from urllib.request import urlopen
from flask import Flask, render_template, redirect, url_for
from api import claves
app = Flask(__name__)

#Excepciones
@app.errorhandler(500)
def internal_error(error):
    return "Estación no activa"

@app.errorhandler(404)
def not_found(error):
    return "Error de servidor"


@app.route('/')#Primera página Index
def index():
    acceso=claves()
    consulta=acceso.consultaEstados
    #conUrl=("http://clima.inifap.gob.mx/wapi/api/Estacion?")
    with urlopen(consulta) as response:source=response.read()
    data=json.loads(source)
    df=pd.DataFrame(data['estados'])
    return render_template("index.html", dato=df['Nombre'])


@app.route('/<string:name>/<string:id>')# Segunda página Estación
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
    return render_template('estacion.html',dato1=df['Nombre'],estado=name, num=id,estac=tac)



@app.route('/<string:estado>/<string:estacion>/<string:numesta>/<string:numero>')# Tercera página Estaciones
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
    t= dicc['estaciones'][0]['Temt']#Temperatura
    h= dicc['estaciones'][0]['Humr']#Humedad relativa
    T=(9*int(t)/5)+32#Conversion de °C a °F
    #Indice de calor
    H = -42.379 + 2.04901523*T + 10.14333127*h - .22475541*T*h - .00683783*T*T - .05481717*h*h + .00122874*T*T*h + .00085282*T*h*h - .00000199*T*T*h*h
    HI=("{0:.2f}".format(H))#Imprimir forfato corto
    #Punto de Rocío
    P= ((h/100)**(1/8))*(112+0.9*t)+0.1*t-112
    Pr=("{0:.2f}".format(P))#Imprimir formato corto
    #Función Fecha
    fecha1=fecha()

    fechaC=time.strftime("%d/%m/%Y")
    print(fecha1,"    ",fechaC)
    print("numesta: {}  numero: {} fecha1 {}   fecha2 {}".format(estacion,numero,fecha1,fechaC))
    cons, promEp, promEt, promHumr, promRadg, promTmax, promTmed, promTmin, promVelv, promVelvMax, sumPrec, PromG =consulta1(estacion,numero,fecha1,fechaC)
    return render_template('estaciones.html',dato2=dicc,dat3=HI,pr=Pr,consuf=cons, est=numesta,Ep=promEp, Et=promEt, Humr=promHumr, Radg=promRadg, Tmax=promTmax, Tmed=promTmed, Tmin=promTmin, Velv=promVelv, VelvMax=promVelvMax, sumPrec=sumPrec, promG=PromG)

def consulta1(estacion,numero,fecha,fechaC):
    print("numesta: {}  numero: {} fecha1 {}   fecha2 {}".format(estacion,numero,fecha,fechaC))
    acceso=claves()
    consulta2="{}&IdEstado={}&IdEstacion={}&fch1={}&fch2={}".format(acceso.consultaDatos,estacion,numero,fecha,fechaC)
    print(consulta2)
    with urlopen(consulta2) as response:
        source=response.read()
    data=json.loads(source)
    df=pd.DataFrame(data['estaciones'])
     #promedio EP
    pEp=df['Ep'].mean()
    promEp=("{0:.2f}".format(pEp))
     #promedio ET
    pEt=df['Et'].mean()
    promEt=("{0:.2f}".format(pEt))
    #promedio Humr
    pHumr=df['Humr'].mean()
    promHumr=("{0:.2f}".format(pHumr))
    #promedio Radg
    pRadg=df['Radg'].mean()
    promRadg=("{0:.2f}".format(pRadg))
    #promedio Tmax
    pTmax=df['Tmax'].mean()
    promTmax=("{0:.2f}".format(pTmax))
    #promedio Tmed
    pTmed=df['Tmed'].mean()
    promTmed=("{0:.2f}".format(pTmed))
    #promedio Tmin
    pTmin=df['Tmin'].mean()
    promTmin=("{0:.2f}".format(pTmin))
    #promedio Velv
    pVelv=df['Velv'].mean()
    promVelv=("{0:.2f}".format(pVelv))
    #promedio VelvMax
    pVelvMax=df['VelvMax'].mean()
    promVelvMax=("{0:.2f}".format(pVelvMax))
    #Suma de Precipitación
    sumPrec=df["Prec"].sum()

    #Dirección del viento
    v1=df['Velv'][0]
    d1=df["Dirv"][0]
    v2=df['Velv'][1]
    d2=df["Dirv"][1]
    v3=df['Velv'][2]
    d3=df["Dirv"][2]
    v4=df['Velv'][3]
    d4=df["Dirv"][3]
    v5=df['Velv'][4]
    d5=df["Dirv"][4]

    #Calculo de los componenes U V
    Cv1=componenteV(v1,d1)
    Cu1=componenteU(v1,d1)
    Prom1=diasDir(v1,d1)
    Cv2=componenteV(v2,d2)
    Cu2=componenteU(v2,d2)
    Prom2=diasDir(v2,d2)
    Cv3=componenteV(v3,d3)
    Cu3=componenteU(v3,d3)
    Prom3=diasDir(v3,d3)
    Cv4=componenteV(v4,d4)
    Cu4=componenteU(v4,d4)
    Prom4=diasDir(v4,d4)
    Cv5=componenteV(v5,d5)
    Cu5=componenteU(v5,d5)
    Prom5=diasDir(v5,d5)

    PG= (Prom1+Prom2+Prom3+Prom4+Prom5)/5
    PromG=("{0:.2f}".format(PG))

    return df, promEp, promEt, promHumr, promRadg, promTmax, promTmed, promTmin, promVelv, promVelvMax, sumPrec, PromG

#ComponenteV
def componenteV(velv,dirv):
    v= velv* math.cos(dirv*math.pi/180)
    return v

#ComponenteU
def componenteU(velv,dirv):
    u= velv* math.sin(dirv*math.pi/180)
    return u

#Promedio de direccion de días
def diasDir(v,u):
    zRadians = math.atan(u / v)#atan: acontangente
    zDegrees = zRadians * (180.0 / math.pi)
    if (u == 0 and v > 0):
        zDegrees = 180.0
    if (u == 0 and v < 0):
        zDegrees = 360.0
    if (u > 0 and v == 0):
        zDegrees = 270.0
    if (u < 0 and v == 0):
        zDegrees = 90.0
    if (v > 0):
        zDegrees = zDegrees + 180
    if (u > 0 and v < 0):
        zDegrees = zDegrees + 360

    z = zDegrees
    return z

def fecha():
    dia=int(time.strftime("%d"))#Conversión de tipo de dato para la fecha
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
