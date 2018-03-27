# -*- coding: utf-8 -*-

import json as jj
from flask import render_template
from subprocess import Popen, PIPE, STDOUT

# locale.setlocale(locale.LC_ALL,'en_US.utf8')
jobsysched = '/var/www/flask/dpmonitor/data/dl_sched_ux'
servidor = ''
fecha =  ''

def abrir(file):
    salida = []
    f = open(file, 'r')
    # f = codecs.open(file, encoding='utf-8')
    for line in f:
        row = line.split('\t')
        salida.append(row)
    return salida

def obtenerJobsProgramados():
	renglonesjys = abrir(jobsysched)

	#Capturamos info del listado. Para la cabecera del reporte.
	global servidor
	global fecha
	servidor = renglonesjys[1][0].replace('#Cell Manager:','')
	fecha =  renglonesjys[2][0].replace('#Creation Date:','')

	#Diccionario vacio para los jobs
	jobs = {}
	#Poblamos el diccionario con los jobs encontrados que tienen proxima ejecucion
	for r in renglonesjys[5:]:
		if r[4] != '-':
			jobs[r[2]] = r[4]
	return jobs
	

def listaSources():
	d2u = Popen(["/var/www/flask/dpmonitor/parserDatalistFile.py", "-i", "/var/www/flask/dpmonitor/data/datalists_ux", "-o", "/var/www/flask/dpmonitor/data/datalist.json"], stdout=PIPE, stderr=PIPE)
	s = d2u.communicate()

	datalist = {}
	datalistPath = "/var/www/flask/dpmonitor/data/datalist.json"
	with open(datalistPath,'r') as datalistFile:
		datalist = jj.load(datalistFile)

	programados = obtenerJobsProgramados()

	aVisualizar = {}
	for d in datalist:
		if d in programados.keys():
			aVisualizar[d] = datalist[d]
	return render_template('listasources.j2', servidor=servidor, fecha=fecha,datalist=aVisualizar)
	 #servidor="Hola Mundo", fecha="chaumundo"