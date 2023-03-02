# ============================================================== #
# SCRIPT NAME : LVC check.py
# AUTHOR      : Victor Hugo Dalosto de Oliveira
# EMAIL       : victordalosto@gmail.com
# DESCRIPTION : Script to check inconsistencies in LVC data
# Check if files are apt. to be approved and codificated
# ============================================================== #

import src.dnit.LVCcheck as LVC

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' Parameters used in the check.                                           '
'                                                                         '
' @param path_hd (String) - Provides the path in the folder to be checked.'
'                                                                         '
' @param snvs_to_be_checked (array) - Informs  sections will be checked.  '  
'        Entered with ["full"] when you want to check the entire section. '
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

snvs_to_be_checked = ["full"]

path_hd = "\\\\10.100.10.219\\Videos\\Recebidos\\2022\\Lote3\\3310"
LVC.check(path_hd, snvs_to_be_checked)