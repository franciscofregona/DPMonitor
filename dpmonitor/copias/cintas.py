"""archivo para cintas y sus cositas"""
from comandos import cintasdelpool, campos
from contenidos import obtenerobjetosdecinta


class cinta():
    """Cinta, con datos del listado de cintas y del contenido de la cinta."""
    def __init__(self,pLabel,status="Indefinido",medium="Indefinido",location="Indefinido",
        full="Indefinido",protected="Indefinido"):
        #Id primario de la cinta: label!
        self.Label = pLabel
        self.objetosdecinta = obtenerobjetosdecinta(self.Label)
        #TODO: si objetos no es un array, levantar excepcion.
        self.tamanos = self.calculartamanos()
        self.mixta = self.chequearcintamixta()
        self.size = "Indefinido"
        self.Status = status
        self.Medium = medium
        self.Location = location
        self.Full = full
        self.Protected = protected

    def __str__(self):
        p = "Expirada"
        if self.Protected:
            p = "Protegida"
        m = "Homogenea"
        if self.mixta:
            m = "Mixta"
#        return "Cinta ID:{} con {} objetos. {}. {}. Tamano Perm: {}, Tamano Prot: {}, Tamano Exp: {}.".format(self.Label,len(self.objetosdecinta),m,p,self.tamanos[0], self.tamanos[1], self.tamanos[2])
        return "{};{};{};{};Perm;{};Prot;{};Exp;{}".format(self.Label, len(self.objetosdecinta),\
         m, p, self.tamanos[0], self.tamanos[1], self.tamanos[2])
    def longprint(self):
        print self.__str__()
        print ("\n")
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
        """devuelve la lista [tamanopermanente, tamanoprotegido, tamanoexpirado]"""
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

