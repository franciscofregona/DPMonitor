#!/usr/bin/env python
from subprocess import Popen, PIPE
import string
import time

def digitos(unstring):
    """dado un string, deja solo los digitos en orden"""
    all=string.maketrans('','')
    nodigs=all.translate(all, string.digits)
    return int(unstring.translate(all, nodigs))

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

def castFecha(unafecha):
    """Castear un objeto fecha para las fechas levantadas de listados"""
    if (unafecha == '-') or (unafecha == ''):
        return None
    otrafecha=unafecha.replace("a.m.","am").replace("p.m.","pm")
    return time.strptime(otrafecha,"%d/%m/%Y %I:%M:%S %p")

class cinta():
    """Cinta, con datos del listado de cintas y del contenido de la cinta."""
    def __init__(self,pLabel,status="Indefinido",medium="Indefinido",location="Indefinido",
        full="Indefinido",protected="Indefinido"):
        #Id primario de la cinta: label!
        self.Label = pLabel
        self.objetosdecinta = obtenerobjetosdecinta(self.Label)
        #TODO: si objetos no es un array, levantar excepcion.
        #self.tamanos = self.calculartamanos()
        #self.mixta = self.chequearcintamixta()
        self.size = "Indefinido"
        self.Status = status
        self.Medium = medium
        self.Location = location
        self.Full = full
        self.Protected = protected

    def __str__(self):
        # p = "Expirada"
        # if self.Protected:
        #     p = "Protegida"
        # m = "Homogenea"
        # if self.mixta:
        #     m = "Mixta"
#        return "Cinta ID:{} con {} objetos. {}. {}. Tamano Perm: {}, Tamano Prot: {}, Tamano Exp: {}.".format(self.Label,len(self.objetosdecinta),m,p,self.tamanos[0], self.tamanos[1], self.tamanos[2])
        return "{}".format(self.Label)
    def longprint(self):
        # print self.__str__()
        # print ("\n")
        for i  in self.objetosdecinta:
            print i
    
    def chequearcintamixta(self):
        """chequea una cinta en busca de contenido mixto. Esto es, tiene
        contenido de proteccion permanente junto a contenido expirado.
        Retorna Booleano."""
        if len(self.objetosdecinta) < 2:
            # self.mixta = False
            return False
        if (self.tamanos[0] == 0) or (self.tamanos[1] == 0):
            # self.mixta = False
            return False
        # self.mixta = True
        return True

    def calculartamanos(self):
        """devuelve la lista [tamanopermanente,longprint tamanoprotegido, tamanoexpirado]"""
        tamanopermanente = 0
        tamanoprotegido = 0
        tamanoexpirado = 0
        for i in self.objetosdecinta:
            proteccion = i.calcularproteccion()
            if  proteccion == "Permanent":
                tamanopermanente = tamanopermanente + i.tamano()
            elif proteccion == "Expired":
                tamanoexpirado = tamanoexpirado + i.tamano()
            else:
                tamanoprotegido = tamanoprotegido + i.tamano()
        return [tamanopermanente, tamanoprotegido, tamanoexpirado]

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

class objetodecinta:
    def __init__(self, pObject_name='', pObject_type='', pObject_status='',\
        pStarted='', pFinished='', pObject_size='', pBackup_type='', pProtection='',\
        pCatalog_retention='', pAccess='', pNumber_of_warnings='', pNumber_of_errors='',\
        pSessionID='', pDevice_name='', pCopy_ID='', pEncrypted='',pCinta=''):
        self.Object_name = pObject_name
        self.Object_type = pObject_type
        self.Object_status = pObject_status
        self.Started = pStarted
        self.Finished = pFinished
        self.Object_size = pObject_size
        self.Backup_type = pBackup_type
        self.Protection = pProtection
        self.Catalog_retention = pCatalog_retention
        self.Access = pAccess
        self.Number_of_warnings = pNumber_of_warnings
        self.Number_of_errors = pNumber_of_errors
        self.SessionID = pSessionID
        self.Device_name = pDevice_name
        self.Copy_ID = pCopy_ID
        self.Encrypted = pEncrypted
        self.Cinta = pCinta

    def  __str__(self):
        """print method"""
        return "{};{};{};{};{}".format(self.SessionID,self.Finished,self.Protection, self.Object_size, self.Cinta)
    def tamano(self):
        """Tamano del objeto"""
        return self.Object_size
    def calcularproteccion(self):
        """Determinar si se trata de un contenido permanente, expirado o protegido."""
        if "Permanent" in self.Protection:
            self.Protection = "Permanent"
            return "Permanent"
        elif "Expired" in self.Protection:
            #Si se trata de un contenido expirado
            self.Protection = "Expired"
            return "Expired"
        else: #No quedan mas opciones, se trata de un contenido protegido
            self.Protection = "Protected"
            return "Protected"
    def calcularCaliente():
        """Retorna true si es un objeto caliente
        se puede usar time.strftime('%y/%m/%d %H:%M (%a)',castFecha(algo) """
        return False
    
        
 
def obtenerobjetosdecinta(unacinta):
    """dado un nombre de una cinta, retorna un array de objetodecinta."""
    contenidosucio = contenidodecinta(unacinta)
    contenidolimpio = contenidosucio.lstrip() #viene un enter adicional al comienzo
    salida = []
    lista = contenidolimpio.split('\r\n  \r\n')
    for i in lista:
        items = i.splitlines()
        obj = objetodecinta()
        for j in items:
            # item.append(j.partition(':')[0].lstrip().rstrip())
            # item.append(j.partition(':')[2].lstrip().rstrip())
            campo = j.partition(':')[0].lstrip().rstrip().replace(" ", "_")
            valor = j.partition(':')[2].lstrip().rstrip()
            if campo == 'Object_size':
                valor = digitos(valor)
            setattr(obj, campo, valor)
            obj.Cinta = unacinta
        salida.append(obj)
    return salida



def obtenercintas(unpool):
    """Toma una lista de cintas, salida del comando de dp, y crea la lista de objetos cinta."""
    contenidos = cintasdelpool(unpool)
    salida = []
    renglones = contenidos.splitlines() #Ahora tengo una lista de renglones (y no un string solo)
    for renglon in renglones[3:]:  #de los renglones, no todos. Del 2do en adelante!
        #Detectar renglones vacios aqui.
        if renglon.strip() == "":
            continue
        rcampos = campos(renglon, 7, 11, 22, 36, 5, 17)
        tmpcinta = cinta(rcampos[2], rcampos[0], rcampos[1], rcampos[3], rcampos[4], rcampos[5])
        salida.append(tmpcinta)
    return salida

if __name__ == "__main__":
    mipool = "GFS_VTL_backup"
    cs = obtenercintas(mipool)
    for c in cs:
        c.longprint()
