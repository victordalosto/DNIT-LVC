
import os
import traceback
import xml.etree.ElementTree as ET

from src.dnit.Utils import isNotValid, isValid
from src.dnit.Logger import update_log

UFs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
Tags = ["IdTrecho", "NomeTrecho", "DataLevantamentoTrecho", "PlacaCarro", "UnidadeFederativa", "BR", "TipoTrecho", "Pista", "Sentido", "KmInicial", "KmFinal", "CaminhoPasta"]


# Check for inconsistencies in index.xml
def checkIndex(pathHD, listToCheck, pathReportLog):

    listSNVs = [[], [], [], []]

    # Path to the index.xml used as import of HD
    pathIndex = os.path.join(pathHD, "index.xml")
    print("Caminho: "+ pathIndex)
    try:
        for xml_elem in (ET.parse(pathIndex)).iter():
            TagValues = [None] * 12
            if xml_elem.tag == "Trecho":  # (1) Validation in HDs name and Ciclo's Number
                for xml_elem_child in xml_elem:
                    for i in range(len(TagValues)):
                        if xml_elem_child.tag == Tags[i] and isValid(xml_elem_child.text):
                            TagValues[i] = xml_elem_child.text
            elif xml_elem.tag == "Etiqueta":  # (2) Validation in XML DATA
                for xml_elem_child in xml_elem:
                    if (xml_elem_child.tag) == "Lote":
                        normHD = os.path.normpath(pathHD)
                        nameHD = (os.path.basename(normHD))[1]
                        if xml_elem_child.text != nameHD:
                            MSG = "Numero no Ciclo no HD (Ciclo_Lote_NºXX) esta diferente do informado no index.xml"
                            update_log("GERAL", MSG, pathReportLog)
                continue

            # Check if Road SNV should be checked according to input
            try:
                if str(TagValues[0]) not in str(listToCheck):
                    continue
            except BaseException:
                continue

            try:
                # Defines a name for the current Road SNV
                nameSNV = TagValues[0] + "_" + TagValues[1]
                currentSNV = TagValues[1]
                kmInitial = float(TagValues[9])
                kmFinal = float(TagValues[10])
                # Defines the SNV path
                path = (TagValues[11]) if TagValues[11] is not None else "None"
                pathSNV = os.path.join(pathHD, path)

                # Create an header line for the Road SNV in ReportLog
                update_log(pathSNV, "", pathReportLog)

                # Check for Null Values in index.xml
                for i in range(len(TagValues)):
                    if isNotValid(TagValues[i]):
                        MSG = "Encontrado valor nulo para o tipo: " + str(Tags[i]) + " no index.xml"
                        update_log(pathSNV, MSG, pathReportLog)

                # Check if UF in names is equals to the one in index.xml
                if TagValues[4] != currentSNV[3:5] or str(TagValues[4]).upper() not in UFs:
                    MSG = "Formato errado no tipo 'UF' no SNV de nome: " + str(currentSNV) + ". UF no index.xml: " + str(TagValues[4])
                    update_log(pathSNV, MSG, pathReportLog)

                # Check if BRs Number in the SNV name is equals to index
                try:
                    BRNames = float(currentSNV[0:3])
                    if abs(float(TagValues[5]) - BRNames) > 0.1:
                        raise ValueError()
                except BaseException:
                    MSG = "Formato errado do tipo 'BR' no SNV de nome: " + str(currentSNV) + ". BR no index.xml: " + str(TagValues[5])
                    update_log(pathSNV, MSG, pathReportLog)

                # Check if 'TipoTrecho' in index.xml is according to Edital
                if str(TagValues[6]).upper() not in ["B", "A", "N", "V", "C", "U"]:
                    MSG = "Valor Tipo Trecho errado. Deveria ser:  B, A, N, V, C, U. Valor no index.xml: " + str(TagValues[6])
                    update_log(pathSNV, MSG, pathReportLog)

                # Check if 'Pista' in index.xml is according to Edital
                if str(TagValues[7]).upper() not in ["S", "D"]:
                    MSG = "Valor de PISTA errado. Deveria ser: S para simples ou D para Duplicada. Valor no index.xml: " + str(TagValues[7])
                    update_log(pathSNV, MSG, pathReportLog)

                # Check if 'Sentido' in index.xml is according to Edital
                if str(TagValues[8]).upper() not in ["C", "D"]:
                    MSG = "Valor de SENTIDO errado. Deveria ser: 'C' para crescente ou 'D' para decrescente. Valor no index.xml: " + str(TagValues[8])
                    update_log(pathSNV, MSG, pathReportLog)
                else:
                    sentido = "D" if (kmInitial > kmFinal) else "C"
                    if sentido != str(TagValues[8]).upper():
                        MSG = "Sentido equivocado. Deveria ser: " + sentido + ", mas foi encontrado no index.xml o valor: " + str(TagValues[8])
                        update_log(pathSNV, MSG, pathReportLog)

                # Append Roads Informantions in listSNVs
                listSNVs[0].append(nameSNV)
                listSNVs[1].append(kmInitial)
                listSNVs[2].append(kmFinal)
                listSNVs[3].append(pathSNV)

            except BaseException:  # (TypeError, ValueError, IndexError):
                MSG = "Erro de formatacao no arquivo index.xml"
                update_log(TagValues[1], MSG, pathReportLog)

    except BaseException:  # (FileNotFoundError):
        MSG = "Nao foi possivel encontrar o arquivo index.xml "
        update_log("GERAL", MSG, pathReportLog)
        print("\nScript finalizou " + MSG + "\n" + traceback.format_exc())
        exit()

    finally:
        return listSNVs
