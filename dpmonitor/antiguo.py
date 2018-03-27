# -*- coding: utf-8 -*-
import csv
# import re
import codecs
# from flask import url_for

from flask import render_template

import time
from time import mktime

from subprocess import Popen, PIPE, STDOUT
import locale

locale.setlocale(locale.LC_ALL,'en_US.utf8')
#Obtencion de dichos archivos:
#La info esta partida: El contenido caliente esta en el archivo contenidocaliente.csv
# y el unico dato que tengo adicional es la sesion que lo genero.
# Para lo cual tengo que invocar a la sesion objetivo para obtener su nombre y fecha.
#####################################################


#Archivos de salidas de DP (originales)
calientecsvori = '/var/www/flask/dpmonitor/data/contenidocaliente.csv'
listsessionsori = '/var/www/flask/dpmonitor/data/list_sessions'

#Archivos modificados para poder trabajarlos (saltos de linea DOS a Ux)
calientecsv =  calientecsvori + '_ux'
listsessions = listsessionsori + '_ux'

#Primero hay que convertir la codificacion de los archivos de entrada
d2u = Popen(["iconv", "-f" ,"WINDOWS-1252", "-t", "UTF-8" ,"{}".format(calientecsvori),"-o","{}".format(calientecsv)], stdout=PIPE, stderr=PIPE)
s = d2u.communicate()
# if not s[1]: #no ocurrio error
d2u = Popen(["iconv", "-f" ,"WINDOWS-1252", "-t", "UTF-8" ,"{}".format(listsessionsori),"-o","{}".format(listsessions)], stdout=PIPE, stderr=PIPE)
s = d2u.communicate()
# if not s[1]: #no ocurrio error

# Luego hay que convertir a formato (de lineas) unix para obtener algo legible
# (esta operacion es idempotente, no hay copia de seguridad):
d2u = Popen(["dos2unix", "{}".format(calientecsv)], stdout=PIPE, stderr=PIPE)
s = d2u.communicate()
# if not s[1]: #no ocurrio error
d2u = Popen(["dos2unix", "{}".format(listsessions)], stdout=PIPE, stderr=PIPE)
s = d2u.communicate()
# if not s[1]: #no ocurrio error


#Utiles
def castFecha(unafecha):
    """Castear un objeto fecha para las fechas levantadas de listados"""
    if (unafecha == '-') or (unafecha == ''):
        return None
    f=unafecha.split(", ",1)[1]
    f = f.replace("Enero","01").replace("Febrero","02").replace("Marzo","03").replace("Abril","04").replace("Mayo","05").replace("Junio","06").replace("Julio","07").replace("Agosto","08").replace("Septiembre","09").replace("Setiembre","09").replace("Octubre","10").replace("Noviembre","11").replace("Diciembre","12").replace("a.m.","am").replace("p.m.","pm")
    return time.strptime(f,"%d de %m de %Y, %I:%M:%S %p")
    #se pueden imprimir con time.asctime(castFecha(unafecha))
    #y con time.strftime("formato", fecha)

def diferencia(fechaHoy, fechaAnterior):
    """Dadas 2 fechas (objetos time) devuelve la diferencia entre ambas.
    El primer parametro es el mas actual, (mas positivo y mayor) y se 
    usara casi siempre como el dia de hoy"""
    diferencia = abs(mktime(fechaHoy) - mktime (fechaAnterior))
    dias, rresto = divmod(diferencia, 86400)
    horas, resto = divmod(rresto, 3600)
    minutos, segundos = divmod(resto, 60)
    return [dias,horas,minutos,segundos]

def parseProteccion(strProteccion):
    """Dado un string con una proteccion de un elemento de cinta
    ie: "Protected for 4 weeks 4 days 3 hours."
    devuelve un numero de segundos equivalente.
    ie: 1 dia 2 horas = 26*3600
    El parseo conviene hacerlo de atras para adelante.
    """
    #print "parseando proteccion de " + strProteccion
    if "/" in strProteccion:
	   return 0 #TODO: FIX: until
    cadena = strProteccion.replace("Protected for ","").replace(".","")
    campos = cadena.split(" ")
    capturando = "valor" #semana, dia, hora
    valor = 0 #nro de segundos en esta unidad. Ie: horas(3600), dias(86400), semanas(604800)
    suma = 0
    for c in range(len(campos)):
        d = c * (-1) - 1
        #print str(c) + " -> " + str(d)
        #print campos[d]
        if capturando == "valor":
            if "week" in campos[d]:
                valor = 604800
            if "day" in campos[d]:
                valor = 86400
            if "hour" in campos[d]:
                valor = 3600
            capturando = "numero"
        else:
            #print "sumando {} por {}".format(valor, campos[d])
            #print "en el index {}, del +1 en campos[{}]".format(d,campos[d+1])
            suma = suma + valor * int(campos[d])
            capturando = "valor"
    return suma

def obtenerFechaUntil(unaCadena):
    #TODO
    return 1

def contenidoCaliente(unafecha, otrafecha):
    """Toma 2 struct de time (fechas) y, calculando la diferencia
    y aplicando criterios, devuelve Bool si es contenido caliente o no
    """
    #esta dif es la proteccion original del source en el job
    #La idea es que los jobs de backup  graban en VTL con proteccion de 10 dias.
    #La copia pone esto en 7 dias.
    # Si esta dif da 10 dias, es un contenido que nunca se bajo a cinta.
    # De haberse bajado a cinta, tendria 7 dias.
    dif = diferencia(unafecha, otrafecha)
    return dif[0] >= 10

def imprimirRegistro(unaFecha,unaProteccion):
    """Para debug, quiero saber que caracho esta haciendo realmente"""
    proteccion = parseProteccion(unaProteccion)


###############################

def abrirPuntoYComa(file):
    salida = []
    f = codecs.open(file, encoding='utf-8')
    for line in f:
        row = line.split(';')
        salida.append(row)
    return salida

def abrirTabs(file):
    salida = []
    f = codecs.open(file, encoding='utf-8')
    for line in f:
        row = line.split('\t')
        salida.append(row)
    return salida

#################################
def aux_antiguo(nombretemplate='antiguo.j2'):
    ahora=time.localtime()
    ahoraTx = time.strftime("%d/%m %H:%M:%S",ahora)
    #renglones objetos calientes
    roc = abrirPuntoYComa(calientecsv)
    sesionesCalientes = {}
    # ssa = {} #sesiones sin acumular
    for r in roc:
        if "Expired" in r[2]:
            continue
        if "(Missing" in r[2]:
            continue
    	if "until" in r[2]:
    	    #Casos como "Protected until 10/12/18 09:12:00 a.m."
            #Determinar fecha de back up y proteccion.
            #TODO
            fechaBackup = castFecha(r[1])
            proteccion = obtenerFechaUntil(r[2])
            cadenaFechaExpiracion =r[2].split("until ")[1].replace("a.m.","am").replace("p.m.","pm")
            fechaExpiracion = time.strptime(cadenaFechaExpiracion,"%d/%m/%y %I:%M:%S %p")
        else:
            #Determinar fecha de back up y proteccion.
            fechaBackup = castFecha(r[1])
            proteccion = parseProteccion(r[2])
            #si la proteccion es mayor a 864000 segundos (10 dias) informarlo como caliente
            fechaExpiracion = time.localtime(proteccion + mktime(ahora))

        if (proteccion > 864000) or (contenidoCaliente(fechaExpiracion, fechaBackup)):
            clave = r[0]
            tamanyo = int(r[3])
            cinta = r[4]

            # index=len(ssa.keys()) + 1
            # ssa[index]=[clave,tamanyo,cinta]

            #acumulador de sesiones para antiguo.hml
            if clave in sesionesCalientes:
                registroSesion = sesionesCalientes[clave]

                #registroSesion = nombreJob,nro objetos, tamanyo
                #sumo uno al contador de recursos calientes de la sesion y el tamanyo de los bytes calientes
                #TODO: Mantengo la misma cinta, para no complicarme.
                sesionesCalientes[clave] = ['s/d', registroSesion[1] + 1, registroSesion[2] + tamanyo,cinta]
            else:
                # Esta sesion no existe aun en el dic, la agrego como va
                sesionesCalientes[clave] = ['s/d',1,tamanyo,cinta]

    rListaSesiones = []
    rListaSesiones = abrirTabs(listsessions)

    servidor = rListaSesiones[1][0].replace('#Cell Manager:','')
    fecha =  rListaSesiones[2][0].replace('#Creation Date:','')
    # ssa = len(ssa)
    # print ssa

    for r in rListaSesiones[5:]:
        clave = r[-1].rstrip()
        if clave in sesionesCalientes:
            sesionesCalientes[clave][0] = r[1]

    return render_template(nombretemplate,sesiones=sesionesCalientes,servidor=servidor,fecha=fecha)
    
#archsalida = 'antiguo.html'
#f = open(archsalida, 'w')
#f.write(output.encode('utf-8'))
#f.close()
