#!/usr/bin/env python
"""Archivo con comandos auxiliares"""
#TODO: sanitizar texto o incluir enyes y acentos como sea.
from subprocess import Popen, PIPE

import comandos_test

testing = True

# (sesiones de backup de los ultimos 15 dias)
# omnidb -session xXXxxXXxXXx (objetos de la sesion)
# omnidb -session xXXxxXXxXXx -filesystem yYYyyYYYyyyyYYyyy (objetos del FS de la S)
def listasesiones(dias=15, tipo="backup"):
    """Obtiene una lista de sesiones, del dia y antiguedad especificados"""
    # cmd = "omnidb -session -last {} -type {}".format(dias,tipo)
    if testing:
        return comandos_test.listasesiones()
        
    comando = Popen(["omnidb", "-session", "-last", dias, "-type", tipo], stdout=PIPE, stderr=PIPE)
    salida = comando.communicate()
    if len(salida[1]): #ocurrio error
        return []
    return salida[0]


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


#Stub!
#campos de listapools: 8, 26, 18, 3, 11, 12
def listadepools():
    """Retorna un string con una lista de pools.
Ejemplo:
Status  Pool name                 Media Type        MS   # of media   Free [MB]
===============================================================================
Poor    CARTUCHOS_EN_OBSERVACION  LTO-Ultrium       No           7     1518235
Good    Captura de software       LTO-Ultrium       No           0           0"""
    #omnimm -list_pools
    comando = Popen(["omnimm", "-list_pools"], stdout=PIPE, stderr=PIPE)
    salida = comando.communicate()
    if len(salida[1]): #ocurrio error
        return ''
    return salida[0]


#STUB!
#campos: 7, 11, 22, 36, 5, 17
def cintasdelpool(unpool):
    """Retorna un string con una lista de cintas pertenecientes al pool.
Ejemplo:
Status Medium Label                  Location                               Full Protected
==========================================================================================
Good   [GPS030L5] GPS030L5              [IBM:03584L32_CPDP:   245]          Yes  Permanent
Good   [PSF032L5] PSF032L5              [IBM:03584L32_CPDP:   255]          Yes  Permanent
Good   [DDU061L4] DDU061L4             <snip>                 Yes  03/28/17 16:46:25"""
    #omnimm -list_pools
    comando = Popen(["omnimm", "-list_pool", unpool], stdout=PIPE, stderr=PIPE)
    salida = comando.communicate()
    if len(salida[1]): #ocurrio error
        return ''
    return salida[0]

#Stub v2. Ahora al azar!
def contenidodecinta(unacinta):
    """Consulta por el contenido de una cinta.

Ejemplos:
Object name: srvpcorreo9e.bkp:/var/spool/imap '/var/spool/imap'
Object type        : FileSystem
Object status      : Completed
Started            : Sabado, 31 de Diciembre de 2016, 11:43:26
Finished           : Domingo, 01 de Enero de 2017, 13:47:53
Object size        : 199838949 KB
Backup type        : Full
Protection         : Permanent
Catalog retention  : Same as data protection
Access             : Private
Number of warnings : 56
Number of errors   : 0
SessionID          : 2017/01/01-6
Device name        : IBM:ULT3580-TD5_6_CPDP
Copy ID            : 31274 (Copy)
Encrypted          : No
    """
    #omnimm -list_media <media> -detail
    comando = Popen(["omnimm", "-list_media", unacinta, "-detail"], stdout=PIPE, stderr=PIPE)
    salida = comando.communicate()
    if len(salida[1]): #ocurrio error
        return ''
    return salida[0]
