#LIbrerias
import pandas as pd
import json
import math
import time
from urllib.request import urlopen
from flask import Flask, render_template
from api import claves
app=Flask(__name__) #asignacion de la página

"""
#control de excepciones
#1XX: Informativo - Solicitud recibida, proceso continuo.
#2XX: Éxito - La acción fue recibida con éxito, comprendida y aceptado.
#3XX: Redirección - Hay que tomar acciones complementarias con el fin de completar la solicitud.
#4XX: Error del lado del cliente - La solicitud contiene una sintaxis incorrecta o no puede cumplirse.
#5XX: Error del lado del servidor - El servidor no pudo cumplir una aparente solicitud válida.
"""
#400 Bad Request
#Este código de error aparece cuando los datos enviados por el cliente a través del navegador web
#no respetan las reglas del protocolo HTTP. El servidor web no puede procesar una solicitud que
#contiene una sintaxis incorrecta. Para verificar que no haya nada malo con tu sistema o con la
#conexión a Internet, abre la misma página web en un navegador diferente y comprueba que la dirección
#sea correcta, borra la caché, y revisa si hay actualizaciones de seguridad pendientes.

@app.errorhandler(400)
def pageNotFound(error):
    return "los datos enviados por el cliente a través del navegador web no respetan las reglas del protocolo HTTP"
#401 Authorization Required
#Cuando la página web que solicita el cliente está protegida con contraseña,
#el servidor responde con un código 401. En este caso, la página no devuelve un mensaje
#de error clásico, sino que aparece una ventana emergente para solicitar al usuario que
#proporcione sus datos de inicio de sesión y su contraseña.
@app.errorhandler(401)
def pageNotFound(error):
    return "la página web que solicita el cliente está protegida con contraseña"

#403 Forbidden
#Aparecerá el código de error 403 cuando el servidor haya sido capaz de entender
#la petición del cliente, pero se niegue a cumplirla. No se trata de un problema
#de sintaxis o de autorización, la razón más común es que el propietario del sitio
#web simplemente no permite a los visitantes ver la página web solicitada.
@app.errorhandler(403)
def pageNotFound(error):
    return "el servidor fue capaz de entender la petición del cliente, pero se niegua a cumplirla"

#404 Not found
#Este es, quizás, el código de error más popular de todos.
#Aparece cuando el servidor no encuentra nada en la ubicación solicitada por el cliente.
#Esto puede deberse a que (1) el cliente escribió mal la URL; (2) a que la estructura de
#enlaces permanentes del sitio ha sido cambiada, por ejemplo, cuando un sitio ha sido trasladado
#a otro servidor web y el DNS todavía apunta a la ubicación anterior; (3) a que la página web
#solicitada no está disponible temporalmente, pero puede intentarlo de nuevo más tarde;
# o (4) a que se eliminó definitivamente la página web.
@app.errorhandler(404)
def not_found(error):
    return "el host ha sido capaz de comunicarse con el servidor  error:",404

#408 Request Timeout
#Cuando la solicitud del cliente no se llevó a cabo dentro del plazo de tiempo que el servidor
#estaba dispuesto a esperar, la conexión se cierra y se muestra un código de error 408.
#Generalmente el tiempo agotado se debe a que había demasiadas personas solicitando el mismo recurso.
#En este caso, el problema puede solucionarse con tan solo refrescar la página (F5).
@app.errorhandler(408)
def pageNotFound(error):
    return "la solicitud del cliente no se llevó a cabo dentro del plazo de tiempo que el servidor estaba dispuesto a esperar"

#410 Gone
#A diferencia del error 404, el código de error 410 indica que el recurso solicitado ya no
#se encuentra disponible y no lo estará nuevamente. Este código es permanente y es activado
#de forma intencional por el administrador del sitio para que los buscadores lo eliminen de sus índices.
@app.errorhandler(410)
def pageNotFound(error):
    return "el recurso solicitado ya no se encuentra disponible y no lo estará nuevamente"
##500 Internal Server Error
#Este error aparece cuando el servidor encuentra una condición inesperada que le impide cumplir
#la solicitud que realizó el cliente, es decir, no se muestra el recurso solicitado.
#El error puede ser resultado del mantenimiento al sitio web, de un error de programación,
#o de un conflicto en los plugins del sitio.
@app.errorhandler(500)
def pageNotFound(error):
    return "La estación no tiene datos o no esta activa"

#502 Bad Gateway
#El error se produce cuando el cliente se conecta a un servidor que actúa como una puerta de
#enlace o proxy para acceder a otro servidor que proporciona servicio adicional a la misma,
#pero este último devuelve una respuesta inválida al primero. En la mayoría de los casos esto
#sucede porque los servidores que se comunican no están de acuerdo sobre el protocolo para intercambiar datos.
@app.errorhandler(502)
def pageNotFound(error):
    return "los servidores que se comunican no están de acuerdo sobre el protocolo para intercambiar datos."

#503 Service Temporarily Unavailable
#El servicio está temporalmente no disponible cuando hay una sobrecarga temporal en el servidor,
#o cuando se realiza un mantenimiento programado. La condición temporal indica que el servicio estará
#disponible nuevamente en otro momento
@app.errorhandler(503)
def pageNotFound(error):
    return "hay una sobrecarga temporal en el servidor, o se realiza un mantenimiento programado."

#504 Gateway Timeout
#Cuando se devuelve el código de estado 504 hay un servidor de nivel superior que se suponía que
#iba a enviar datos al servidor que está conectado a nuestro cliente pero se agotó el tiempo de
#respuesta. En el código 408 la comunicación se realiza de servidor a cliente, en el caso del
#código 504 la comunicación es de servidor a servidor.
@app.errorhandler(504)
def pageNotFound(error):
    return "se agotó el tiempo de respuesta de servidor a servidor"

#RUTAS PARA LA PÁGINA
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
    #diccionario de la consulta

    d = dict(data)
    print(d)
    #F significa el valor en centrigrados
    F=d['estaciones'][0]['Temt']
    #RH significa la humedad relativa
    RH=d['estaciones'][0]['Humr']
    #T significa la temperatura el celsius en farenheith
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

#funcion de la segunda consulta, realizada en otra función para no afectar a la primer consulta
def funconsulta(esta,numes,fech1,fecha):
    print("estacion:  {} numero  {} fecha1 {}  fecha 2 {}".format(esta,numes,fech1,fecha))
    acceso=claves()
    consulta2= '{}idEstado={}&IdEstacion={}&fch1={}&fch2={}'.format(acceso.consultaDatos,esta,numes,fech1,fecha)
    print(consulta2)
    with urlopen(consulta2) as response:
        source=response.read()
    data=json.loads(source)
    df = pd.DataFrame(data['estaciones'])
    #suma de la precipitación
    sumaPrec=sum(df['Prec'])
    #promedios de las demas variables
    promEp=df['Ep'].mean()
    promEt=df['Et'].mean()
    promHumr=df['Humr'].mean()
    promHumr=("{0:.3f}".format(promHumr))
    promRadg=df['Radg'].mean()
    promRadg=("{0:.3f}".format(promRadg))
    promTmax=df['Tmax'].mean()
    promTmed=df['Tmed'].mean()
    promTmin=df['Tmin'].mean()
    promTmin=("{0:.3f}".format(promTmin))
    promVelv=df['Velv'].mean()
    promVelv=("{0:.3f}".format(promVelv))
    promVelvMax=df['VelvMax'].mean()

    #asignacion de v y u por cada uno de los dias
    #despues asignacion de la direccion de cada dia
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
    print("promedio de los dias {}".format(promedioDias))


    return df,sumaPrec,promEp,promEt,promHumr,promRadg,promTmax,promTmed,promTmin,promVelv,promVelvMax,promedioDias

#descompocision de la dirección del viento y la velocidad para poder promediar
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
#funcion para sacar la fecha de hace cinco días
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
                print("este mes solo tiene 30 dias")
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
                    print("este mes solo tiene 31 dias")
    else:
        print("mes no valido")

    return fecha1


if __name__ == "__main__":app.run()
