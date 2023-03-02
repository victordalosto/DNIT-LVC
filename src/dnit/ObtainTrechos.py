
import os
import xml.etree.ElementTree as ET

from src.dnit.Utils import isValid
from src.dnit.Report import updateLog

Tags = ["IdTrecho", "NomeTrecho", "UnidadeFederativa", "BR"]


# Check for inconsistencies in index.xml
def ObtainTrechos(pathHD, pathReportLog, SNVsToBeChecked):

    # Path to the index.xml used as import of HD
    pathIndex = os.path.join(pathHD, "index.xml")
    listToCheck = []
    try:
        # String with all SNVs to be excluded from verification
        ExcludedSNV = ""
        # Loop to get all Roads SNVs inside PathHD
        for xml_Element in (ET.parse(pathIndex)).iter():
            # Tags That contains <Trecho> are verified here
            if xml_Element.tag == "Trecho":
                Values = [None] * 4
                for xml_Element_child in xml_Element:
                    for i in range(len(Values)):
                        if xml_Element_child.tag == Tags[i] and isValid(xml_Element_child.text):
                            Values[i] = xml_Element_child.text

                # Check if the file is in the list to be verified
                if (str(SNVsToBeChecked[0]).lower() == "full") or \
                        (str(Values[0]) in str(SNVsToBeChecked)) or \
                        (str(Values[1]) in str(SNVsToBeChecked)) or \
                        (str(Values[2]) in str(SNVsToBeChecked)) or \
                        (str(Values[3]) in str(SNVsToBeChecked)):
                    listToCheck.append(Values[0])
                else:
                    nameSNV = Values[0] + "_" + Values[1]
                    ExcludedSNV += nameSNV + "; "
        # Update ReportLog with Roads SNVs that hasn't been checked
        if ExcludedSNV != "":
            updateLog("GERAL", "Trechos excluidos da verificacao: " + ExcludedSNV, pathReportLog)

    except BaseException:
        updateLog("GERAL", "Nao foi possivel encontrar o arquivo index.xml ", pathReportLog)
        exit()

    finally:
        return listToCheck
