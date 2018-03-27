# -*- coding: utf-8 -*-

import csv
import re
from jinja2 import Template
from flask import render_template
import codecs
import time
from subprocess import Popen, PIPE, STDOUT

import locale
locale.setlocale(locale.LC_ALL,'en_US.utf8')

#Obtencion de dichos archivos:
#La info esta partida: los trabajos tienen servidores y rutas que se obtienen con el reporte
# dl_tree de data protector.
# Las fechas de ejecucion estan en los archivos en el directorio
#      c:\archivos de programa\omniback\config\server\schedules
# pero esta dificil de procesar, asi que en su lugar, pido la proxima ejecucion con el reporte dl_sched.
# Las cintas que usa cada trabajo estan en los archivos en
#      c:\archivos de programa\omniback\config\server\datalist\<nombredejob>
# que se procesan todos juntos con el binario parseadorDevices (generado con flex)
#####################################################
# Mas comandos de DP CLI:
# Todas las sesiones de los ultimos 3 meses
#     omnirpt -report list_sessions -timeframe (AA/MM/DD HH:MM x2) -tab > reporte.csv (p273)


#Utiles
def castFecha(unafecha):
    """Castear un objeto fecha para las fechas levantadas de listados"""
    if (unafecha == '-') or (unafecha == ''):
        return None
    otrafecha=unafecha.replace("a.m.","am").replace("p.m.","pm")
    return time.strptime(otrafecha,"%d/%m/%Y %I:%M:%S %p")
    #se pueden imprimir con time.asctime(castFecha(unafecha))
    #y con time.strftime("formato", fecha)

def seleccionarCampo(st1, st2 = '', st3 = ''):
    """El listado de trees tiene 3 campos de info: servidor, ruta y descripcion.
    Como fueron definidos a mano, probablemente por el Ale Sager, no estan super parejos.
    Y dados los 3, los elegimos siempre en el mismo orden, que es como me parece
    describen mejor la data."""
    if (st1 != '') or (st1 != '[host backup]'):
        return st1
    else:
        if  (st2 != '') or (st2 != '[host backup]'):
            return st2
        else:
            return st3

class Recurso():
    """Objeto del que se hace back up"""
    def __init__(self,specification, objectType, client, mountpoint, description, tree):
        self.specification = specification
        self.objectType = objectType
        self.client = client
        self.mountpoint = mountpoint
        self.description = description
        self.tree = tree
        self.desc = seleccionarCampo(tree, description, mountpoint)
        self.id = self.client + " " + self.desc
    
class Job():
    """Trabajo de backup, con nombre y fecha de programacion.
    Mas tarde cargara tambien con sources y unidades asignadas"""
    def __init__(self, type, sessiontype, specification, group, nextExec, mode, ultExecStart='', ultExecEnd='', ultDur=''):
        self.type = type
        self.sessiontype = sessiontype
        self.specification = specification.encode('UTF-8',errors='ignore')
        self.group = group
        self.nextExec = castFecha(nextExec)
        if self.nextExec:
            self.tiempo = time.strftime('%a %H:%M',self.nextExec)
        self.ultExecStart = ultExecStart
        self.ultExecEnd = ultExecEnd
        self.ultDur = ultDur
        self.mode = mode
        self.sources = []
        self.devices = []
    def __str__(self):
        salida = "Job de backup {}. Nro de recursos: {}".format(self.specification, len(self.sources))
        return salida
    def listaSources(self):
        salida = ""
        for s in self.sources:
            salida = salida + " " + s.id
        return salida

###############################33

def abrir(file):
    salida = []
    f = codecs.open(file, encoding='utf-8')
    # f = codecs.open(file)
    for line in f:
        row = line.split('\t')
        salida.append(row)
    return salida

def aux_trabajos(template = 'trabajos.j2'):
	#################################
	#Archivos de salidas de DP (originales)
	jobsytreesori = '/var/www/flask/dpmonitor/data/dl_trees'
	jobsyschedori = '/var/www/flask/dpmonitor/data/dl_sched'
	jobsytapesori = '/var/www/flask/dpmonitor/data/datalists'
	listsessionsori = '/var/www/flask/dpmonitor/data/list_sessions'

	#Archivos modificados para poder trabajarlos (saltos de linea DOS a Ux)
	jobsytrees = jobsytreesori + '_ux'
	jobsysched = jobsyschedori + '_ux'
	jobsytapes = jobsytapesori + '_ux'
	listsessions = listsessionsori + '_ux'

	#Primero hay que convertir la codificacion de los archivos de entrada
	d2u = Popen(["iconv", "-f" ,"WINDOWS-1252", "-t", "UTF-8" ,"{}".format(jobsytreesori),"-o","{}".format(jobsytrees)], stdout=PIPE, stderr=PIPE)
	s = d2u.communicate()
	# if not s[1]: #no ocurrio error
	d2u = Popen(["iconv", "-f" ,"WINDOWS-1252", "-t", "UTF-8" ,"{}".format(jobsyschedori),"-o","{}".format(jobsysched)], stdout=PIPE, stderr=PIPE)
	s = d2u.communicate()
	# if not s[1]: #no ocurrio error
	d2u = Popen(["iconv", "-f" ,"WINDOWS-1252", "-t", "UTF-8" ,"{}".format(listsessionsori),"-o","{}".format(listsessions)], stdout=PIPE, stderr=PIPE)
	s = d2u.communicate()
	# if not s[1]: #no ocurrio error
	d2u = Popen(["iconv", "-f" ,"UTF-16", "-t", "UTF-8" ,"{}".format(jobsytapesori),"-o","{}".format(jobsytapes)], stdout=PIPE, stderr=PIPE)
	s = d2u.communicate()
	# if not s[1]: #no ocurrio error

	# Luego hay que convertir a formato (de lineas) unix para obtener algo legible
	# (esta operacion es idempotente, no hay copia de seguridad):
	d2u = Popen(["dos2unix", "{}".format(jobsytrees)], stdout=PIPE, stderr=PIPE)
	s = d2u.communicate()
	# if not s[1]: #no ocurrio error
	d2u = Popen(["dos2unix", "{}".format(jobsysched)], stdout=PIPE, stderr=PIPE)
	s = d2u.communicate()
	# if not s[1]: #no ocurrio error
	d2u = Popen(["dos2unix", "{}".format(jobsytapes)], stdout=PIPE, stderr=PIPE)
	s = d2u.communicate()
	# if not s[1]: #no ocurrio error
	d2u = Popen(["dos2unix", "{}".format(listsessionsori)], stdout=PIPE, stderr=PIPE)
	s = d2u.communicate()
	# if not s[1]: #no ocurrio error


	renglonesjys = []
	#Hay un dict reader, pero mi archivo original tiene filas adicionales al inicio. =(
	#Me tomo la pequenia licencia de abrir el archivo y leerlo a pata
	#no va a perder demasiado tiempo.
	renglonesjys = abrir(jobsysched)

	#Capturamos info del listado. Para la cabecera del reporte.
	servidor = renglonesjys[1][0].replace('#Cell Manager:','')
	fecha =  renglonesjys[2][0].replace('#Creation Date:','')

	#Diccionario vacio para los jobs
	jobs = {}
	#Poblamos el diccionario con los jobs encontrados en jobsytrees
	for r in renglonesjys[5:]:
	    j = Job(r[0],r[1],r[2],r[3],r[4],r[6].rstrip())
	    jobs[j.specification] = j
	#Cleanup
	# del renglonesjys

	#A continuacion poblamos el dicc de jobs con la info de los directorios bkupeados por DP
	renglonesjyt = []
	renglonesjyt = abrir(jobsytrees)

	#Creo una lista de los recursos leidos y la lleno con el contenido del reporte de DP
	sourcesleidos = []
	for r in renglonesjyt[5:]:
	    j = Recurso(r[0],r[1],r[2],r[3],r[4],r[5].rstrip())
	    sourcesleidos.append(j)

	#poblar los jobs con los recursos
	for r in sourcesleidos:
	    jobs[r.specification].sources.append(r)

	#Cleanup
	del renglonesjyt
	del sourcesleidos

	# Y para finalizar, hay que procesar los tapes de cada job en jobsytapes
	# Hay escribir ese archivo en la salida estandar
	cat = Popen(["cat","{}".format(jobsytapes)],stdout=PIPE,stderr=PIPE)
	# e invocar al parser sobre esa salida (mediante el PIPE).
	pd = Popen(['/var/www/flask/dpmonitor/parseadorDevices'],stdin=cat.stdout,stdout=PIPE,stderr=PIPE)
	s = pd.communicate()

	# if not s[1]: #no ocurrio error
	#s[0] tiene la salida estandar

	registros = s[0].split('\nDATALIST')
	#El primer registro tiene un "DATALIST" extra que hay que limpiar.
	registros[0] = registros[0].replace('DATALIST','')

	renglonesjobsytapes = []

	# Estos registros estan sucios, hay que limpiarlos luego con .rstrip().lstrip()[1:-1]
	for reg in registros:
	    r = reg.split('DEVICE')
	    for compo in range(len(r)):
	        r[compo] = r[compo].rstrip().lstrip()[1:-1].replace('IBM:ULT3580-','').replace('_CPDP','').replace('_cpdp','')
	    renglonesjobsytapes.append(r)

	# del registros

	#poblar los jobs con los recursos
	for r in renglonesjobsytapes:
	    #print unicode(r[0], encoding='utf-8',errors='ignore') + " y " + jobs[unicode(r[0], encoding='utf-8',errors='ignore')].specification
	    kekey = unicode(r[0], encoding='utf-8',errors='ignore')
	    if kekey in jobs:
	    	jobs[kekey].devices = r[1:]
	#Cleanup
	# del renglonesjobsytapes

	# Abrir archivo de ultimas sesiones para calculo estadistico
	renglonesestadisticas = []
	renglonesestadisticas = abrir(listsessions)


	#Solo me interesan:
	#  nombre del job,
	#  fecha de inicio,
	#  fecha de fin,
	#  duracion,
	#  tamanyo
	#  y owner (si no es backup es disparado manualmente y no lo quiero)
	#Que encontramos (respectivamente) en los indices: [r[1],r[4],r[6],r[9],r[10],r[20],r[21]]
	for r in renglonesestadisticas[5:]:
	    if r[21] == 'SRVBACKUP\\BACKUP@srvbackup' and r[1] in jobs:
	        if castFecha(r[4]):
	            jobs[r[1]].ultExecStart = time.strftime('%y/%m/%d %H:%M (%a)',castFecha(r[4]))
	        if castFecha(r[6]):
	            jobs[r[1]].ultExecEnd = time.strftime('%y/%m/%d %H:%M (%a)',castFecha(r[6]))
	        jobs[r[1]].ultDur = r[9]


	# Separar los jobs segun programacion
	jobsprogramados = {}
	jobsnoprogramados = {}
	for j in jobs:
	    if jobs[j].nextExec:
	        jobsprogramados[j] = jobs[j]
	    else:
	        jobsnoprogramados[j]  = jobs[j]

	if __name__ != "__main__":
		return render_template('trabajos.j2',trabajosp=jobsprogramados,trabajosn=jobsnoprogramados, servidor=servidor, fecha=fecha)
	#De aqui para abajo es para debug
	else:
		import jinja2
		loader = jinja2.FileSystemLoader(searchpath='./templates')
		templateEnv = jinja2.Environment(loader=loader)
		TEMPLATE_FILE = "test.j2"
		template = templateEnv.get_template( TEMPLATE_FILE )
		outputText = template.render(trabajosp=jobsprogramados,trabajosn=jobsnoprogramados, servidor=servidor, fecha=fecha) # this is where to put args to the template renderer

		return outputText
		# return jobs

if __name__ == "__main__":
    # execute only if run as a script
    print aux_trabajos()
