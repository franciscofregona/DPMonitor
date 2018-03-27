#!/usr/bin/env python
"""Listador de tamanos de pooles"""
from pools import obtenerpools

poolesdeinteres = ["Free_VTL_LT05", "GFS_VTL_backup"]
for a in poolesdeinteres:
    print a

raw_input("Presione una tecla para salir")

def main():
    """Procedimiento principal"""
    pools = obtenerpools()
    for p in pools:
        if p.Pool_name in poolesdeinteres:
            p.inicializar()
            print "Pool {}".format(p.Pool_name)
            p.imprimir()


#if __name__ == "__main__":
#    # execute only if run as a script
#    main()
