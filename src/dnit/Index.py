# ============================================================== #
# SCRIPT NAME : LVC check.py
# AUTHOR      : Victor Hugo Dalosto de Oliveira
# EMAIL       : victordalosto@gmail.com
# DESCRIPTION : Script to check inconsistencies in LVC data
# Check if files are apt. to be approved and codificated
# ============================================================== #

import os
import xml.etree.ElementTree as ET

from src.dnit.Utils import isValid
from src.dnit.Logger import update_log


# Check for inconsistencies in index.xml
def get_ids(path_hd, path_logger, snvs_to_be_checked):
    index = os.path.join(path_hd, "index.xml")
    try:
        list_to_check = []
        text_excluded_trechos = ""
        for xml_element in (ET.parse(index)).iter():
            # Tags That contains <Trecho> are verified here
            if xml_element.tag == "Trecho":
                for node in xml_element:
                    if (node.tag == "IdTrecho"):
                        print(node.text)
                        if ((str(snvs_to_be_checked[0]).lower() == "full") or \
                           (node.text in snvs_to_be_checked)):
                            list_to_check.append(node.text)
                        else:
                            text_excluded_trechos += node.text + "; "
        # Update ReportLog with Roads SNVs that hasn't been checked
        if text_excluded_trechos != "":
            update_log("GERAL", "Ids excluidos da verificacao: " + text_excluded_trechos, path_logger)

    except BaseException:
        update_log("GERAL", "Nao foi possivel encontrar o arquivo index.xml ", path_logger)
        exit()

    finally:
        return list_to_check
