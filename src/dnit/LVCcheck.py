import os
import src.dnit.Logger as Logger
import src.dnit.Index as Index
import src.dnit.Checker as Checker
import src.dnit.CheckIndex as CheckIndex

def check(folder, array_snvs):
    # Path to the script
    path_main = os.path.dirname(os.path.dirname(__file__))

    # Change the path of the directory to ffmpeg script ffprobe.exe
    os.chdir(os.path.join(path_main, "lib", "ffmpeg", 'bin'))

    # Create an repot log file with all checking done on files
    logger = Logger.create_report_logger(os.path.join(path_main, "logs"))

    # Obtains the List of roads SNVs to be checked
    array_ids = Index.get_ids_from_xml(folder, logger, array_snvs)

    # Check for inconsistencies in Index.xml
    array_snv_infos = Checker.index(folder, array_ids, logger)

    # Check the integrity and structure of files and folders
    Checker.folder(path_main, array_snv_infos, logger)

    # Check all DATA inside the LogsTrecho.XML files
    Checker.LogsTrecho(array_snv_infos, logger)

    print("Verificaçao concluida com sucesso LVC Check - 100%")