# -*- coding: utf-8 -*-
import csv

from flask import render_template
import codecs
from subprocess import Popen, PIPE, STDOUT

import locale
locale.setlocale(locale.LC_ALL,'en_US.utf8')

#Utiles
###############################33

def abrir(file):
    salida = []
    f = codecs.open(file, encoding='utf-8')
    # f = codecs.open(file)
    for line in f:
        row = line.rstrip().split(';')
        salida.append(row)
    return salida

def aux_mediosVtl():
	medios = '/var/www/flask/dpmonitor/data/contenidovtl.csv'
	filas = abrir(medios)
	return render_template('mediosvtl.j2',medios=filas)

if __name__ == "__main__":
    # execute only if run as a script
    print aux_mediosVtl()
