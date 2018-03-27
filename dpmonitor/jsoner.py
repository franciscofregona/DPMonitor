import json

def escribir(nombrearchivo, data):
	with open(nombrearchivo, 'w') as outfile:
		json.dump(data, outfile)

def leer(nombrearchivo):
	fp = open(nombrearchivo)
	return json.load(fp)