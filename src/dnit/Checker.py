import src.dnit.CheckIndex as CheckIndex
import src.dnit.CheckFolders as CheckFolders
import src.dnit.CheckLogsXML as CheckLogsTrecho

def index(root_hd, snvs, logger):
    print("Checking index: ", root_hd)
    return CheckIndex.check(root_hd, snvs, logger)

def folder(path_main, array_snv_infos, logger):
    print("Checking folders: ", path_main)
    CheckFolders.check(path_main, array_snv_infos, logger)

def logsTrecho(array_snv_infos, logger):
    print("Checking logsTrecho")
    CheckLogsTrecho.check(array_snv_infos, logger)