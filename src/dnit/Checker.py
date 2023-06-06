import src.dnit.CheckIndex as CheckIndex
import src.dnit.CheckFolders as CheckFolders
import src.dnit.CheckLogsXML as CheckLogsTrecho

def index(root_hd, snvs, logger):
    return CheckIndex.check(root_hd, snvs, logger)

def folder(path_main, array_snv_infos, logger):
    CheckFolders.check(path_main, array_snv_infos, logger)

def logsTrecho(array_snv_infos, logger):
    CheckLogsTrecho.check(array_snv_infos, logger)