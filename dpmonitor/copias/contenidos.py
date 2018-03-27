"""Archivo para contenidos de cintas y cositas"""
from comandos import contenidodecinta
import string

def digitos(unstring):
    """dado un string, deja solo los digitos en orden"""
    all=string.maketrans('','')
    nodigs=all.translate(all, string.digits)
    return int(unstring.translate(all, nodigs))

class objetodecinta:
    def __init__(self, pObject_name='', pObject_type='', pObject_status='',\
        pStarted='', pFinished='', pObject_size='', pBackup_type='', pProtection='',\
        pCatalog_retention='', pAccess='', pNumber_of_warnings='', pNumber_of_errors='',\
        pSessionID='', pDevice_name='', pCopy_ID='', pEncrypted=''):
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

    def  __str__(self):
        """print method"""
        return "Objeto de cinta de " + self.Object_name + ", sesion " + \
            self.SessionID + ", " + self.Protection
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
        salida.append(obj)
    return salida

