# ============================================================== #
# SCRIPT NAME : LVC check.py
# AUTHOR      : Victor Hugo Dalosto de Oliveira
# EMAIL       : victordalosto@gmail.com
# DESCRIPTION : Script to check inconsistencies in LVC data
# Check if files are apt. to be approved and codificated
# ============================================================== #

import src.LVCcheck as LVC

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' Parameters used in the check.                                           '
'                                                                         '
' @param pathHD (String) - Provides the path in the folder to be checked. '
'                                                                         '
' @param SNVsToBeChecked (array) - Informs which sections will be checked.'  
'        Entered with ["full"] when you want to check the entire section. '
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

''''''
SNVsToBeChecked = ["full"]

# pathHD = "D:\\correcoes\\3312"
pathHD = "\\\\10.100.10.219\\Videos$\\Recebidos\\2022\\Lote3\\3314"
LVC.check(pathHD, SNVsToBeChecked)
