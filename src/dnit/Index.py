# ============================================================== #
# SCRIPT NAME : LVC check.py
# AUTHOR      : Victor Hugo Dalosto de Oliveira
# EMAIL       : victordalosto@gmail.com
# DESCRIPTION : Script to check inconsistencies in LVC data
# Check if files are apt. to be approved and codificated
# ============================================================== #

import os
import xml.etree.ElementTree as ET

from src.dnit.Utils import is_valid
from src.dnit.Logger import update_log


# Check for inconsistencies in index.xml
def get_ids_from_xml(path_root_hd, logger, array_snvs):
    index = os.path.join(path_root_hd, "index.xml")
    try:
        ids_to_check = []
        text_excluded_trechos = ""
        for xml_element in (ET.parse(index)).iter():
            getID(array_snvs, ids_to_check, text_excluded_trechos, xml_element)
        log_snvs_not_included(logger, text_excluded_trechos)
    except BaseException:
        update_log("GERAL", "Nao foi possivel encontrar o arquivo index.xml ", logger)
        exit()
    finally:
        return ids_to_check


def getID(array_snvs, ids, text_excluded_trechos, xml_element):
    if xml_element.tag == "Trecho":
        for node in xml_element:
            if (node.tag == "IdTrecho"):
                if (isAValidId(array_snvs, node)):
                    ids.append(node.text)
                else:
                    text_excluded_trechos += node.text + "; "


def isAValidId(array_snvs, node):
    if (array_snvs == "full"):
        return True
    for snv in array_snvs:
        if (str(node.text) == str(snv)):
            return True
    return False


def log_snvs_not_included(logger, text_excluded_trechos):
    if text_excluded_trechos != "":
        update_log("GERAL", "Ids excluidos da verificacao pois não foi encontrado: " + text_excluded_trechos, logger)
