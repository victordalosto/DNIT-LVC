
# ============================================================== #
# SCRIPT NAME : LVC check.py
# AUTHOR      : Victor Hugo Dalosto de Oliveira
# EMAIL       : victordalosto@gmail.com
# DESCRIPTION : Script to check inconsistencies in LVC data
# Check if files are apt. to be approved and codificated
# ============================================================== #

import os
from src.ObtainTrechos import ObtainTrechos
from src.reportLog import CreateReportLog
from src.CheckIndex import checkIndex
from src.CheckFolders import checkFolders
from src.CheckLogsXML import checkLogsXML


def check(pathHD, SNVsToBeChecked):
    # Path to the script
    pathMain = os.getcwd()

    # Change the path of the directory to ffmpeg script ffprobe.exe
    os.chdir(os.path.join(pathMain, "lib", "ffmpeg", 'bin'))

    # Create an repot log file with all checking done on files
    pathReportLog = CreateReportLog(pathMain)

    # Obtains the List of roads SNVs to be checked
    listToCheck = ObtainTrechos(pathHD, pathReportLog, SNVsToBeChecked)

    # Check for inconsistencies in Index.xml
    listSNVs = checkIndex(pathHD, listToCheck, pathReportLog)

    # Check the integrity and structure of files and folders
    checkFolders(listSNVs, pathReportLog)

    # Check all DATA inside the LogsTrecho.XML files
    checkLogsXML(listSNVs, pathReportLog)

    # Print in the Promp tha all validations were done
    os.chdir(pathMain)
    print("Verificaçao concluida com sucesso LVC Check - 100%")
