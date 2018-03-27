"""Archivo para pool y sus cositas"""
from comandos import cintasdelpool, listadepools, campos
from cintas import cinta

class pool:
    def __init__(self, pStatus='Indefinido', pPool_name='Indefinido', pMedia_Type='Indefinido',\
     pMS='Indefinido', pn_of_media='Indefinido', pFreeMB='Indefinido', pinicializado=False):
        self.Status = pStatus
        self.Pool_name = pPool_name
        self.Media_Type = pMedia_Type
        self.MS = pMS
        self.n_of_media = pn_of_media
        self.FreeMB = pFreeMB
        self.inicializado = False
        if pinicializado:
            self.inicializado = True
            self.cintas = obtenercintas(self.Pool_name)
        else:
            self.cintas = []
    def __str__(self):
        return "Pool " + self.Pool_name + ", " + self.n_of_media + \
            " cintas de tipo " + self.Media_Type
    def imprimir(self):
        """Imprime informacion basica de un pool"""
        print "Pool " + self.Pool_name + ", " + self.n_of_media + \
            " cintas de tipo " + self.Media_Type
        print "----------------------------------------------------------"
        if self.cintas:
            for i in self.cintas:
                print i
        else:
            print "Pool no inicializado."
    def inicializar(self):
        """Inicializar la clase es ir efectivamente a buscar el contenido de las cintas
        para cargar el pool."""
        if self.inicializado == False:
            self.cintas = obtenercintas(self.Pool_name)
            self.inicializado = True

def obtenerpools():
    """toma una lista de pools salida del comando de DP
    y la transforma en una lista de objetos pool."""
    pools = listadepools()
    salida = []
    if not pools:
        return
    pools = pools.splitlines() #ahora tengo una lista de renglones
    for renglon in pools[3:]:		#No me interesa ni la cabecera ni los iguales
        rcampos = campos(renglon, 8, 26, 18, 3, 11, 12)
        tmppool = pool(rcampos[0], rcampos[1], rcampos[2], rcampos[3], rcampos[4], rcampos[5])
        salida.append(tmppool)
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


#Stub!
def entendertipopool():
    """itera entre las cintas halladas en un pool y busca la cadena
    que identifica la unidad de cinta.
    De alli intenta identificar si se trata de un tipo LTO4, 5 o 6.
    Retorna (int)4, (int)5, (int)6... o (char)? si cambia entre cintas
    o no lo entiende."""
    pass
