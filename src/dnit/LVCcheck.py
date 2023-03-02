
# ============================================================== #
# SCRIPT NAME : LVC check.py
# AUTHOR      : Victor Hugo Dalosto de Oliveira
# EMAIL       : victordalosto@gmail.com
# DESCRIPTION : Script to check inconsistencies in LVC data
# Check if files are apt. to be approved and codificated
# ============================================================== #

import os
from src.dnit.ObtainTrechos import ObtainTrechos
from src.dnit.Report import CreateReportLog
from src.dnit.CheckIndex import checkIndex
from src.dnit.CheckFolders import checkFolders
from src.dnit.CheckLogsXML import checkLogsXML


def check(pathHD, SNVsToBeChecked):
    # Path to the script
    pathMain = os.path.dirname(os.path.dirname(__file__))

    # Change the path of the directory to ffmpeg script ffprobe.exe
    os.chdir(os.path.join(pathMain, "lib", "ffmpeg", 'bin'))

    # Create an repot log file with all checking done on files
    pathReportLog = CreateReportLog(pathMain)

    # Obtains the List of roads SNVs to be checked
    listToCheck = ObtainTrechos(pathHD, pathReportLog, SNVsToBeChecked)

    # Check for inconsistencies in Index.xml
    listSNVs = checkIndex(pathHD, listToCheck, pathReportLog)

    # Check the integrity and structure of files and folders
    checkFolders(pathMain, listSNVs, pathReportLog)

    # Check all DATA inside the LogsTrecho.XML files
    checkLogsXML(listSNVs, pathReportLog)

    print("Verificaçao concluida com sucesso LVC Check - 100%")