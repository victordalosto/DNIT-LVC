# ============================================================== #
# SCRIPT NAME : LVC check.py
# AUTHOR      : Victor Hugo Dalosto de Oliveira
# EMAIL       : victordalosto@gmail.com
# DESCRIPTION : Script to check inconsistencies in LVC data
# Check if files are apt. to be approved and codificated
# ============================================================== #

import src.dnit.LVCcheck as LVC

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' Parameters used in the LVC.check() function                              '
'                                                                          '
' @param list_snvs (array) - Informs the sections which will be checked.   '  
'        Specify ["full"] when you want to check the entire folder         '
'                                                                          '
' @param hd (String) - Provides the path in the folder to be checked.      '
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


hd = "\\\\10.100.10.219\\Videos\\Recebidos\\2022\\Lote3\\3310"
list_snvs = [7, 10]

LVC.check(hd, list_snvs)