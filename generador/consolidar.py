#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
#
# Script de deteccion de cintas consolidables.
# y generacion del comando de consolidacion.
#
# Las cintas consolidables son aquellas que o bien tienen contenido
# "mixto" (expirado y permanente); o bien tienen contenido permanente
# exclusivamente, y tienen espacio disponible para albergar nuevo
# contenido permanente.
#
# 1- Este script lista los pools de cintas disponibles en el servidor.
# 2- El usuario seleccionara un pool y el sistema mostrara las cintas en el.
# 3- El sistema busca las cintas de ese pool y evalua cuales pueden consolidarse.
# 4- El usuario selecciona las cintas que desea consolidar y
# 5- elige un pool de cintas libres para tomar el cartucho nuevo.
# 6- Opcionalmente, marca para reciclar y mueve las cintas de origen al pool free.


# from subprocess import Popen, PIPE
import sys
import string
import logging
from comandos import listadepools, cintasdelpool, contenidodecinta

from contenidos import obtenerobjetosdecinta
from cintas import cinta


o = obtenerobjetosdecinta(contenidodecinta())
c = cinta(o)
