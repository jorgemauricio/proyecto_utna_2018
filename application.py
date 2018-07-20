#LIbrerias
import pandas as pd
import json
import math
import time
from urllib.request import urlopen
from flask import Flask, render_template
from api import claves
app=Flask(__name__) #asignación de la página


@app.errorhandler(400)
def pageNotFound(error):
    return "los datos enviados por el cliente a través del navegador web no respetan las reglas del protocolo HTTP"

@app.errorhandler(401)
def pageNotFound(error):
    return "la página web que solicita el cliente está protegida con contraseña"

@app.errorhandler(403)
def pageNotFound(error):
    return "el servidor fue capaz de entender la petición del cliente, pero se niega a cumplirla"

@app.errorhandler(404)
def not_found(error):
    return "el host ha sido incapaz de comunicarse",404

@app.errorhandler(408)
def pageNotFound(error):
    return "la solicitud del cliente no se llevó a cabo dentro del plazo de tiempo que el servidor estaba dispuesto a esperar"

@app.errorhandler(410)
def pageNotFound(error):
    return "el recurso solicitado ya no se encuentra disponible y no lo estará nuevamente"

@app.errorhandler(500)
def pageNotFound(error):
    return "La estación no tiene datos o no esta activa"


@app.errorhandler(502)
def pageNotFound(error):
    return "los servidores que se comunican no están de acuerdo sobre el protocolo para intercambiar datos."

@app.errorhandler(503)
def pageNotFound(error):
    return "hay una sobrecarga temporal en el servidor, o se realiza un mantenimiento programado."

@app.errorhandler(504)
def pageNotFound(error):
    return "se agotó el tiempo de respuesta de servidor a servidor"

#RUTAS PARA LA PÁGINA
a=""
@app.route('/') #asignación del index
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
    #diccionario de la consulta

    d = dict(data)
    print(d)
    #F significa el valor en centígrados
    F=d['estaciones'][0]['Temt']
    #RH significa la humedad relativa
    RH=d['estaciones'][0]['Humr']
    #T significa la temperatura de celsius a farenheith
    T =F * 1.8000 + 32.00
    #IC el índice de calor
    IC=  -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH
    IC=("{0:.3f}".format(IC))
    #Pr significa el punto de rocío
    Pr=((RH/100)**(1/8)) *(112+0.9*F)+0.1*F-112
    Pr=("{0:.3f}".format(Pr))
    #fecha obtenida desde python y no desde la computadora, en dia, mes y año, el año es Y por 2018
    fecha=time.strftime("%d/%m/%Y")
    print("temperatura: {}  hum= {} punto de rocio  {}".format(F,RH,Pr))
    fech1=funcionfecha()
    #se almacena el frame enviado desde el metodo de la segunda consulta, y se envian los datos de la primera

    c,suma,promEp,promEt,promHumr,promRadg,promTmax,promTmed,promTmin,promVelv,promVelvMax,promedioDias=funconsulta(esta,numes,fech1,fecha)
        #
    return render_template('pagina3.html',da2=d,c=IC,pr=Pr,f=fecha,f2=fech1,consH=c,sum=suma,pEp=promEp,pEt=promEt,pHumr=promHumr,pRadg=promRadg,pTmax=promTmax,pTmed=promTmed,pTmin=promTmin,pVelv=promVelv,pVelvMax=promVelvMax,pd=promedioDias,estacin=estacion)
        #

#función de la segunda consulta, realizada en otra función para no afectar a la primer consulta
def funconsulta(esta,numes,fech1,fecha):
    print("estación:  {} número  {} fecha1 {}  fecha 2 {}".format(esta,numes,fech1,fecha))
    acceso=claves()
    consulta2= '{}idEstado={}&IdEstacion={}&fch1={}&fch2={}'.format(acceso.consultaDatos,esta,numes,fech1,fecha)
    print(consulta2)
    with urlopen(consulta2) as response:
        source=response.read()
    data=json.loads(source)
    df = pd.DataFrame(data['estaciones'])
    #suma de la precipitación
    sumaPrec=sum(df['Prec'])
    #promedios de las demáss variables
    promEp=df['Ep'].mean()
    promEp=("{0:.3f}".format(promEp))
    promEt=df['Et'].mean()
    promEt=("{0:.3f}".format(promEt))
    promHumr=df['Humr'].mean()
    promHumr=("{0:.3f}".format(promHumr))
    promRadg=df['Radg'].mean()
    promRadg=("{0:.3f}".format(promRadg))
    promTmax=df['Tmax'].mean()
    promTmax=("{0:.3f}".format(promTmax))
    promTmed=df['Tmed'].mean()
    promTmed=("{0:.3f}".format(promTmed))
    promTmin=df['Tmin'].mean()
    promTmin=("{0:.3f}".format(promTmin))
    promVelv=df['Velv'].mean()
    promVelv=("{0:.3f}".format(promVelv))
    promVelvMax=df['VelvMax'].mean()
    promVelvMax=("{0:.3f}".format(promVelvMax))

    #asignacion de v y u por cada uno de los dias
    #después asignacion de la direccion de cada dia
    v1=df['Velv'][0]
    d1=df['Dirv'][0]
    v2=df['Velv'][1]
    d2=df['Dirv'][1]
    v3=df['Velv'][2]
    d3=df['Dirv'][2]
    v4=df['Velv'][3]
    d4=df['Dirv'][3]
    v5=df['Velv'][4]
    d5=df['Dirv'][4]
    d1V=ComponentV(v1,d1)
    d1U=ComponentU(v1,d1)
    pdia1=DiaDir(d1V,d1U)

    d2V=ComponentV(v2,d2)
    d2U=ComponentU(v2,d2)
    pdia2=DiaDir(d2V,d2U)

    d3V=ComponentV(v3,d3)
    d3U=ComponentU(v3,d3)
    pdia3=DiaDir(d3V,d3U)

    d4V=ComponentV(v4,d4)
    d4U=ComponentU(v4,d4)
    pdia4=DiaDir(d4V,d4U)

    d5V=ComponentV(v5,d5)
    d5U=ComponentU(v5,d5)
    pdia5=DiaDir(d5V,d5U)

    promedioDias= (pdia1+pdia2+pdia3+pdia4+pdia5)/5
    promedioDias=("{0:.3f}".format(promedioDias))
    print("promedio de los días {}".format(promedioDias))


    return df,sumaPrec,promEp,promEt,promHumr,promRadg,promTmax,promTmed,promTmin,promVelv,promVelvMax,promedioDias

#descompocisión de la dirección del viento y la velocidad para poder promediar
    #componente V para el promedio de la dirección del viento
def ComponentV(velv, dirv):
        v = velv * math.cos(dirv * math.pi / 180)
        print("variblae v: {}".format(v))
        return v
 #componente U para el promedio de la dirección del viento
def ComponentU(velv, dirv):
    u = velv * math.sin(dirv * math.pi / 180)
    print("variblae u: {}".format(u))
    return u
#regresa el valor en grados
def DiaDir(v,u):
    zRadians = math.atan(u / v) #en radianes  #atan=acotangente
    zDegrees = zRadians * (180.0 / math.pi) #en decimales

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
    #if (u < 0 and v < 0)

    z = zDegrees
    print("dia dirección del viento {}".format(z))
    return z

def funcion(dia,mes,año,r):
    if mes==1:
        if dia<5:
            año=año-1
            mes=12
            dia=r+dia -5
        else:
            dia= dia-5
            if dia==0:
                dia=31
                año=año-1
                mes=12
    else:
        if dia<=5:
            dia=r+dia-5
            mes=mes-1
        else:
            dia=dia-5
    #print(año,mes,dia)
    return año,mes,dia
#función para sacar la fecha de hace cinco días
def funcionfecha():
    fecha=time.strftime("%d/%m/%Y")
    fd=int(time.strftime("%d"))
    fm=int(time.strftime("%m"))
    fa=int(time.strftime("%Y"))
    a=fa
    m=fm
    d=fd
    d1=fd
    m1=fm
    a1=fa
    if m<12:
        if m==5 or m==7 or m==8 or m==10 or m==12:
            rango=30
            if d<=rango:
                a,m,d=funcion(d,m,a,rango)
                fecha1="{}/{}/{}".format(d,m,a)
                print("{}/{}/{}".format(d,m,a))
            else:
                print("este mes solo tiene 30 días")
        else:
            if m==3:
                if a%4==0:
                    if d1<=5:
                        m=m1-1
                        d=d1+29-5
                    else:
                        d=d1-5
                    fecha1="{}/{}/{}".format(d,m,a)
                    print("{}/{}/{}".format(d,m,a))
                else:
                    if d1<=5 and a%4!=0:
                        if d1<=5:
                            d=d1+28-5
                            m=m1-1
                    else:
                        d=d1-5
                    fecha1="{}/{}/{}".format(d,m,a)
                    print("{}/{}/{}".format(d,m,a))
            else:
                rango=31
                if d<=rango:
                    a,m,d=funcion(d,m,a,rango)
                    fecha1="{}/{}/{}".format(d,m,a)
                    print("{}/{}/{}".format(d,m,a))
                else:
                    print("este mes solo tiene 31 días")
    else:
        print("mes no valido")

    return fecha1


if __name__ == "__main__":app.run()
