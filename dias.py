año= int(input("Ingresa el año: "))
mes=int(input("Ingresa el mes[1:12]: "))
if mes==4 or mes==6 or mes==9 or mes==11:
    dia=int(input("Ingresa el día[1:30]: "))
elif mes==2 and año%4==0:
    dia=int(input("Ingresa el día[1:29]: "))
elif mes==2:
        dia=int(input("Ingresa el día[1:28]: "))
else:
    dia=int(input("Ingresa el día[1:31]: "))
dia1=dia
mes1=mes
año1=año
if mes<=12:
    if mes==1:
        if dia<=5:
            año=año-1
            mes=12
            dia=dia1-5+31
            print("el día a partir de la fecha ingresada es: [aaaa-mm-dd] {} - {} - {}".format(año,mes,dia))
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
                    print("el día a partir de la fecha ingresada es: [aaaa-mm-dd] {} - {} - {}".format(año,mes,dia))
                else:
                    dia= dia-5
                    print("el día a partir de la fecha ingresada es: [aaaa-mm-dd] {} - {} - {}".format(año,mes,dia))
        else:

            if mes1==3:
                if año1%4==0:
                    if dia<=5:
                        dia=29+dia1-5
                        mes=mes1-1
                        print("el  día a partir de la fecha ingresada es: [aaaa-mm-dd] {} - {} - {}".format(año,mes,dia))
                    else:
                        dia=dia1-5
                        print("el  día a partir de la fecha ingresada es: [aaaa-mm-dd] {} - {} - {}".format(año,mes,dia))

                else:
                    if dia1<=28 and año1%4!=0:
                        if dia<=5:
                            dia=28+dia1-5
                            mes=mes1-1
                        else:
                            dia=dia-5
                        print("el día a partir de la fecha ingresada es: [aaaa-mm-dd] {} - {} - {}".format(año,mes,dia))
                    else:
                        print("Este mes solo 28 dias")
            else:

                if dia>31:
                    print("Este mes solo tiene 31 dias")
                else:
                    if dia<=5:
                        mes=mes-1
                        dia=dia-5+30
                        print("el día a partir de la fecha ingresada es:[aaaa-mm-dd] {} - {} - {}".format(año,mes,dia))
                    else:
                        dia= dia-5
                        print("el día a partir de la fecha ingresada es: [aaaa-mm-dd] {} - {} - {}".format(año,mes,dia))




else:
    print("Mes no valido")
