#!/usr/bin/env python
"""Listador de tamanos de pooles"""
from pools import obtenerpools

poolesdeinteres = [
# "Cartuchos_poor",
# "Default DDS",
# "Default File",
# "Default LTO-Ultrium",
# "Default LTO5-Ultrium",
# "Default T3480/T4890/T9490",
# "Default VTL LTO5",
# "EDUC-historicos_copia",
# "EDUC-historicos_trabajo",
# "Elecciones-2015-VMs",
# "Elecciones2013",
# "Elecciones2013-COPIA",
# "Elecciones2015",
# "Elecciones2015-COPIA",
# "Elecciones2017",
# "Elecciones2017-COPIA",
# "FILELIBRARY_SRVTSM_cpds_M",
# "FL:SRVPGWSAN1I_CPDP_Media",
# "FL:SRVPGWSAN2I_CPDP_Media",
# "Free_VTL_LTO5",
# "GFS-JUBI_backup",
# "GFS-JUBI_copia",
# "GFS-RAC_backup",
# "GFS-RAC_backup_20151102",
# "GFS-RAC_copia_20151102",
# "GFS-SCIT_backup",
# "GFS-free_LTO4",
# "GFS-free_LTO5",
# "GFS_RegistroGral_FULL",
"GFS_VTL_backup",
# "GFS_backup_20151102",
# "GFS_copia_20151102",
# "GFS_permanente_LTO5",
# "HISTORICOS",
# "IDB",
# "ISO",
# "JUBI-backup",
# "JUBI-copia",
# "Senal Santa Fe",#este no va a andar por la enye.
# "VMWARE_asr",
]


def main():
    """Procedimiento principal"""
    pools = obtenerpools()
    for p in pools:
        if p.Pool_name in poolesdeinteres:
            print "Inicializando pool {}...".format(p.Pool_name)
            p.inicializar()
            p.imprimir()
    raw_input("Presione una tecla para salir")


if __name__ == "__main__":
    # execute only if run as a script
    main()
