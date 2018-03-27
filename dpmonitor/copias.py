# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT

#tengo que hacer un script nuevo de salidas
# hay que buscar las ultimas sesiones (15 dias)
# filtrar, me interesan las copias
# luego quedarme con la mas nueva de cada tipo
# luego hacer un omnidb -session esasesion -detail y
# filtrar los dispositivos. ordenar y que sean unicos.

# def obtenerSesiones(dias=15):
#     comando = Popen(["omnidb", "-session", "-last", "{}".format(dias)], stdout=PIPE, stderr=PIPE)
#     salida = comando.communicate()
#     if len(salida[1]): #ocurrio error
#         return ''
#     return salida[0]

def obtenerSesionCFD2D2T(dias=10):
    """Obtiene el codigo de sesion de la ultima corrida de la copia
    CPY_FULL-D2D2T
    """
    comando = Popen(["omnidb", "-session", "-datalist", "CPY_FULL-D2D2T", "-last", "{}".format(dias)], stdout=PIPE, stderr=PIPE)
    salida = comando.communicate()
    if len(salida[1]): #ocurrio error
        return ''
    contenidos = salida[0]
    renglones = contenidos.splitlines() #Ahora tengo una lista de renglones (y no un string solo)
    renglonesExitosos = []
    for r in renglones[2:]:
        if "Fail" in r:
            continue
        renglonesExitosos.append(r)
    return campos(renglonesExitosos[-1], 17)[0].rstrip()


def obtenerSesionCID2D2TDia(dias=10):
    """Obtiene el codigo de sesion de la ultima corrida de la copia
    CPY_INCR-D2D2T_dia
    """
    comando = Popen(["omnidb", "-session", "-datalist", "CPY_INCR-D2D2T_dia", "-last", "{}".format(dias)], stdout=PIPE, stderr=PIPE)
    salida = comando.communicate()
    if len(salida[1]): #ocurrio error
        return ''
    contenidos = salida[0]
    renglones = contenidos.splitlines() #Ahora tengo una lista de renglones (y no un string solo)
    renglonesExitosos = []
    for r in renglones[2:]:
        if "Fail" in r:
            continue
        renglonesExitosos.append(r)
    return campos(renglonesExitosos[-1], 17)[0].rstrip()



def obtenerSesionCID2D2TNoche(dias=10):
    """Obtiene el codigo de sesion de la ultima corrida de la copia
    CPY_INCR-D2D2T_noche
    """
    comando = Popen(["omnidb", "-session", "-datalist", "CPY_INCR-D2D2T_noche", "-last", "{}".format(dias)], stdout=PIPE, stderr=PIPE)
    salida = comando.communicate()
    if len(salida[1]): #ocurrio error
        return ''
    contenidos = salida[0]
    renglones = contenidos.splitlines() #Ahora tengo una lista de renglones (y no un string solo)
    renglonesExitosos = []
    for r in renglones[2:]:
        if "Fail" in r:
            continue
        renglonesExitosos.append(r)
    return campos(renglonesExitosos[-1], 17)[0].rstrip()

    

def campos(unstring, *args):
    """Trasnforma una cadena en una lista de cadenas. Los parametros siguientes son
enteros con los tamanos de los cortes.

campos("hola mundo", 4, 1, 5)
['hola', '', 'mundo']"""
    posicion = 0
    salida = []
    for iterador in args:
        campo = unstring[posicion:posicion+iterador].rstrip().lstrip()
        salida.append(campo)
        posicion += iterador
    return salida

def obtenerDispositivos(sesion):
    """Toma una sesion,  hace un omnidb y restorna una lista de los dispositivos que alli aparecen.
    """
    comando = Popen(["omnidb", "-session", sesion, "-detail"], stdout=PIPE, stderr=PIPE)
    salida = comando.communicate()
    if len(salida[1]): #ocurrio error
        return ''
    contenidos = salida[0]
    
    salida = set()
    renglones = contenidos.splitlines() #Ahora tengo una lista de renglones (y no un string solo)
    for renglon in renglones[2:]:  #de los renglones, no todos. Del 2do en adelante!
        #Detectar renglones vacios aqui.
        if "Device name" not in renglon.strip():
            continue
        salida.add(renglon.split(":",1)[1].strip())
    
    arreglo = []
    for i in salida:
        arreglo.append(i)
    return arreglo


if __name__ == "__main__":
    # execute only if run as a script
    print "Full: {}".format(obtenerDispositivos(obtenerSesionCFD2D2T(15)))
    print "Noche: {}".format(obtenerDispositivos(obtenerSesionCID2D2TDia(7)))
    print "Dia: {}".format(obtenerDispositivos(obtenerSesionCID2D2TNoche(7)))