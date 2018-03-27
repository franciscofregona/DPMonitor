#!/usr/bin/env python
version = "1.0"

###Parser para archivos de Datalist de Data Protector###
#Toma como entrada el concatenado de todos los datalist del servidor
#arroja en la salida un json de un diccionario, con una clave por
# datalist, con un array de filesystems como valor.

import codecs
from pyparsing import *
import argparse
#Cuidado: la salida de debug no va a los archivos de salida, solo a la salida de error estandar.
import logging
import sys

def pprint(item,archivosalida=''):
	"""
	Imprime un diccionario, con indentaciones para legibilidad.
	"""
	print(json.dumps(item, indent=4))

Keywords = Keyword("DATALIST") | Keyword("FILESYSTEM") | Keyword("-trees") | Keyword("-exclude")
nombre = NotAny(Keywords) + Suppress(Optional('"')) + Word(alphanums +"-"+"_"+"/"+"."+"+") +  Suppress(Optional('"'))

#DATALIST "BENCH_LAN_GWs"
nombre2 = NotAny(Keywords) + QuotedString('"', unquoteResults=True)

elemento = NotAny("-trees") + NotAny("-exclude") + nombre
Trees = Group(Literal("-trees") + OneOrMore(QuotedString('"', unquoteResults=True)))
Exclude = Group(Literal("-exclude") + OneOrMore(QuotedString('"', unquoteResults=True)))


filesystemHeader = Keyword("WINFS") | Keyword("FILESYSTEM")
descripcion= nombre2
servidor= nombre
path= nombre
vss = Suppress(Literal("-vss") + restOfLine)
contenidoFS = Trees | Exclude | vss
Host = Group(Keyword("HOST") + nombre2 + nombre + Suppress("{") + ZeroOrMore(contenidoFS) + Suppress("}"))

Filesystem = Group(filesystemHeader + descripcion + servidor + Suppress(":") + path + Suppress("{") + ZeroOrMore(contenidoFS) + Suppress("}"))

inutil = NotAny(Keyword("DATALIST")) + Suppress(Word(printables))
inutilfs = Suppress(Keyword("FILESYSTEM") + Literal("{"))
contenidoDL = Filesystem ^ Host ^ inutil ^ inutilfs

Datalist = Group(Suppress(Keyword("DATALIST")) + nombre2 + OneOrMore(contenidoDL))

Archivo = OneOrMore(Datalist)


if __name__ == "__main__":
	import json

	parser = argparse.ArgumentParser(
		description="Filtro de informacion de zoning para la SAN",
		epilog="Procesamiento distribuido. Frank@5123 Mar/18")
	parser.add_argument('-v','--version', #
		action='version',
		version='%(prog)s version ' + version,
		help='Muestra el numero de version y sale.'
		)
	parser.add_argument('-d',#debug, opcional
		type=str,
		choices=["CRITICAL","ERROR","WARNING","INFO","DEBUG","NOTSET"],
		required=False,
		help='(Opcional) Salida de depuracion o debug.',
		dest='debug',
		default='CRITICAL'
		)
	parser.add_argument('-i', #Archivo de entrada.
		nargs='?',
		type=str, #String con nombre de archivo de entrada. Antes: argparse.FileType('r'),
		dest='archivoentrada',
		required=True,
		help='Nombre del archivo de entrada, generado por los switches de SAN?',
		)
	parser.add_argument('-o', #Archivo de salida. Opcional
		nargs='?',
		type=argparse.FileType('w'),
		default=sys.stdout,
		dest='archivosalida',
		help='(Opcional) Nombre de archivo de salida. De no completarse, se usa la salida estandar.',
		)

	############Capturar parametros
	args =  parser.parse_args()
	
	debugs = {
		"CRITICAL": logging.CRITICAL,
		"ERROR": logging.ERROR,
		"WARNING": logging.WARNING,
		"INFO": logging.INFO,
		"DEBUG": logging.DEBUG,
		"NOTSET": logging.NOTSET,
	}

	logging.basicConfig(level=debugs[args.debug])


	logging.info("""Parametros recibidos:
		archivoentrada: {}
		debug: {}
		archivosalida: {}
		""".format(args.archivoentrada, args.debug, args.archivosalida))
	##################################

	with codecs.open(args.archivoentrada, 'r', encoding='utf-8') as myfile:
		data = myfile.read()

	r = Archivo.parseString(data).asList()

	diccionario = {}
	for elemento in  r:
		diccionario[elemento[0]] = elemento[1:]
		# print "agregando k:{}, v:{}".format(elemento[0], elemento[1:])
	args.archivosalida.write(json.dumps(diccionario))
	args.archivosalida.close()
	# pprint(diccionario)