# ============================================================== #
# SCRIPT NAME : LVC check.py
# AUTHOR      : Victor Hugo Dalosto de Oliveira
# EMAIL       : victordalosto@gmail.com
# DESCRIPTION : Script to check inconsistencies in LVC data
# Check if files are apt. to be approved and codificated
# ============================================================== #

import src.LVCcheck as LVC

'''
' Parameters used in the check.
'
' @param pathHD (String) - Provides the path in the folder to be checked.
'
' @param SNVsToBeChecked (array) - Informs which sections will be checked.
'         Entered with ["full"] when you want to check the entire section.
'''

pathHD = "E:/2319"
SNVsToBeChecked = ["full"]

# Calls the function that will check the files
LVC.check(pathHD, SNVsToBeChecked)
