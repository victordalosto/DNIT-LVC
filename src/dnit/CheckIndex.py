import os
import traceback
import xml.etree.ElementTree as ET

from src.dnit.Utils import is_not_valid, is_valid, get_UFs
from src.dnit.Logger import update_log

valid_tags = ["IdTrecho", "NomeTrecho", "DataLevantamentoTrecho", "PlacaCarro", "UnidadeFederativa", "BR", "TipoTrecho", "Pista", "Sentido", "KmInicial", "KmFinal", "CaminhoPasta"]

def check(pathHD, listToCheck, pathReportLog):

    listSNVs = [[], [], [], []]

    # Path to the index.xml used as import of HD
    pathIndex = os.path.join(pathHD, "index.xml")
    print("Caminho: "+ pathIndex)
    try:
        for xml_element in (ET.parse(pathIndex)).iter():
            tags = [None] * 12
            if xml_element.tag == "Trecho":
                for node in xml_element:
                    for i in tags:
                        if node.tag == valid_tags[i]:
                            tags[i] = node.text
            elif xml_element.tag == "Etiqueta":
                for node in xml_element:
                    if (node.tag) == "Lote":
                        normHD = os.path.normpath(pathHD)
                        nameHD = (os.path.basename(normHD))[1]
                        if node.text != nameHD:
                            MSG = "Numero no Ciclo no HD (Ciclo_Lote_NºXX) esta diferente do informado no index.xml"
                            update_log("GERAL", MSG, pathReportLog)
                continue

            # Check if Road SNV should be checked according to input
            try:
                if str(tags[0]) not in str(listToCheck):
                    continue
            except BaseException:
                continue

            try:
                # Defines a name for the current Road SNV
                nameSNV = tags[0] + "_" + tags[1]
                currentSNV = tags[1]
                kmInitial = float(tags[9])
                kmFinal = float(tags[10])
                # Defines the SNV path
                path = (tags[11]) if tags[11] is not None else "None"
                pathSNV = os.path.join(pathHD, path)

                # Create an header line for the Road SNV in ReportLog
                update_log(pathSNV, "", pathReportLog)

                # Check for Null Values in index.xml
                for i in range(len(tags)):
                    if is_not_valid(tags[i]):
                        MSG = "Encontrado valor nulo para o tipo: " + str(valid_tags[i]) + " no index.xml"
                        update_log(pathSNV, MSG, pathReportLog)

                # Check if UF in names is equals to the one in index.xml
                if tags[4] != currentSNV[3:5] or str(tags[4]).upper() not in get_UFs():
                    MSG = "Formato errado no tipo 'UF' no SNV de nome: " + str(currentSNV) + ". UF no index.xml: " + str(tags[4])
                    update_log(pathSNV, MSG, pathReportLog)

                # Check if BRs Number in the SNV name is equals to index
                try:
                    BRNames = float(currentSNV[0:3])
                    if abs(float(tags[5]) - BRNames) > 0.1:
                        raise ValueError()
                except BaseException:
                    MSG = "Formato errado do tipo 'BR' no SNV de nome: " + str(currentSNV) + ". BR no index.xml: " + str(tags[5])
                    update_log(pathSNV, MSG, pathReportLog)

                # Check if 'TipoTrecho' in index.xml is according to Edital
                if str(tags[6]).upper() not in ["B", "A", "N", "V", "C", "U"]:
                    MSG = "Valor Tipo Trecho errado. Deveria ser:  B, A, N, V, C, U. Valor no index.xml: " + str(tags[6])
                    update_log(pathSNV, MSG, pathReportLog)

                # Check if 'Pista' in index.xml is according to Edital
                if str(tags[7]).upper() not in ["S", "D"]:
                    MSG = "Valor de PISTA errado. Deveria ser: S para simples ou D para Duplicada. Valor no index.xml: " + str(tags[7])
                    update_log(pathSNV, MSG, pathReportLog)

                # Check if 'Sentido' in index.xml is according to Edital
                if str(tags[8]).upper() not in ["C", "D"]:
                    MSG = "Valor de SENTIDO errado. Deveria ser: 'C' para crescente ou 'D' para decrescente. Valor no index.xml: " + str(tags[8])
                    update_log(pathSNV, MSG, pathReportLog)
                else:
                    sentido = "D" if (kmInitial > kmFinal) else "C"
                    if sentido != str(tags[8]).upper():
                        MSG = "Sentido equivocado. Deveria ser: " + sentido + ", mas foi encontrado no index.xml o valor: " + str(tags[8])
                        update_log(pathSNV, MSG, pathReportLog)

                # Append Roads Informantions in listSNVs
                listSNVs[0].append(nameSNV)
                listSNVs[1].append(kmInitial)
                listSNVs[2].append(kmFinal)
                listSNVs[3].append(pathSNV)

            except BaseException:  # (TypeError, ValueError, IndexError):
                MSG = "Erro de formatacao no arquivo index.xml"
                update_log(tags[1], MSG, pathReportLog)

    except BaseException:  # (FileNotFoundError):
        MSG = "Nao foi possivel encontrar o arquivo index.xml "
        update_log("GERAL", MSG, pathReportLog)
        print("\nScript finalizou " + MSG + "\n" + traceback.format_exc())
        exit()

    finally:
        return listSNVs
