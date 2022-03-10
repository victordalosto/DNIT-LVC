
# ============================================================== #
# SCRIPT NAME : LVC check.py
# AUTHOR      : Victor Hugo Dalosto de Oliveira
# EMAIL       : victordalosto@gmail.com
# DESCRIPTION : Script to check inconsistencies in LVC data
# Check if files are apt. to be approved and codificated
# ============================================================== #

import os
from src.reportLog import CreateReportLog
from src.CheckIndex import checkIndex
from src.CheckFolders import checkFolders
from src.CheckLogsXML import checkLogsXML


def check(pathHD, SNVsToBeChecked):
    '''
    Main script that checks the files for LVC import.

    @param pathHD (String) Main directory where the files are located.
    @param SNVsToBeChecked (Array) List of SNVs names or IDs to check.
    Set SNVsToBeCheckec = ["full"] to check the entire Root.
    '''

    # List of roads SNVs [id_nameSNV][kmInitial][kmFinal][adressPath]
    listSNVs = [[], [], [], []]

    # Main functions that handles all the Data Checking
    def Main():

        # Path to the script
        pathMain = os.getcwd()

        # Change the path of the directory to be able to
        # call the ffmpeg script ffprobe.exe.
        os.chdir(os.path.join(pathMain, "lib", "ffmpeg", 'bin'))

        # Create an repot log file with all checking done on files
        pathReportLog = CreateReportLog(pathMain)

        # Check for inconsistencies in Index.xml
        checkIndex(pathHD, SNVsToBeChecked, listSNVs, pathReportLog)

        # Check the integrity and structure of files and folders
        checkFolders(listSNVs, pathReportLog)

        # Check all DATA inside the LogsTrecho.XML files
        checkLogsXML(listSNVs, pathReportLog)

        # Print in the Promp tha all validations were done
        print("Verificaçao concluida com sucesso LVC Check - 100%")
        os.chdir(pathMain)

    Main()
