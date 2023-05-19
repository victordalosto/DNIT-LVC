import src.dnit.CheckIndex as CheckIndex
import src.dnit.CheckFolders as CheckFolders
import src.dnit.CheckLogsXML as CheckLogsTrecho

def index(path_hd, listToCheck, path_logger):
    return CheckIndex.check(path_hd, listToCheck, path_logger)

def folder(path_main, listSNVs, path_logger):
    CheckFolders.check(path_main, listSNVs, path_logger)

def LogsTrecho(listSNVs, path_logger):
    CheckLogsTrecho.check(listSNVs, path_logger)