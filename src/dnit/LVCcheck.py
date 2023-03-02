# ============================================================== #
# SCRIPT NAME : LVC check.py
# AUTHOR      : Victor Hugo Dalosto de Oliveira
# EMAIL       : victordalosto@gmail.com
# DESCRIPTION : Script to check inconsistencies in LVC data
# Check if files are apt. to be approved and codificated
# ============================================================== #

import os
import src.dnit.Logger as Logger
import src.dnit.Index as Index
from src.dnit.CheckIndex import checkIndex
from src.dnit.CheckFolders import checkFolders
from src.dnit.CheckLogsXML import checkLogsXML

def check(path_hd, snvs_to_be_checked):
    # Path to the script
    path_main = os.path.dirname(os.path.dirname(__file__))

    # Change the path of the directory to ffmpeg script ffprobe.exe
    os.chdir(os.path.join(path_main, "lib", "ffmpeg", 'bin'))

    # Create an repot log file with all checking done on files
    path_logger = Logger.create_report_log(os.path.join(path_main, "logs"))

    # Obtains the List of roads SNVs to be checked
    listToCheck = Index.get_ids(path_hd, path_logger, snvs_to_be_checked)

    # Check for inconsistencies in Index.xml
    listSNVs = checkIndex(path_hd, listToCheck, path_logger)

    # Check the integrity and structure of files and folders
    checkFolders(path_main, listSNVs, path_logger)

    # Check all DATA inside the LogsTrecho.XML files
    checkLogsXML(listSNVs, path_logger)

    print("Verificaçao concluida com sucesso LVC Check - 100%")