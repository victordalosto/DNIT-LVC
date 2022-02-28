
import os
import traceback
import xml.etree.ElementTree as ET

from src.reportLog import updateLog


# Check for inconsistencies in index.xml
def checkIndex(pathHD, SNVsToBeChecked, listSNVs, pathReportLog):

    # Path to the index.xml used as import of HD
    pathIndex = os.path.join(pathHD, "index.xml")
    try:
        tree = ET.parse(pathIndex)
        # String with all SNVs to be excluded from verification
        ExcludedSNV = ""
        UFs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
               "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
               "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

        # Loop to get all Roads SNVs inside PathHD
        for elem in tree.iter():
            # (1) Validation in HDs name and Ciclo's Number
            if elem.tag == "Etiqueta":
                for child in elem:
                    if (child.tag) == "Lote":
                        normHD = os.path.normpath(pathHD)
                        nameHD = (os.path.basename(normHD))[1]
                        if child.text != nameHD:
                            MSG = "Nome no HD XXXX (Ciclo_Lote_NºXX) esta \
                                  diferente do informado no index.xml"
                            updateLog("GERAL", MSG, pathReportLog)

            # (2) Validation in XML DATA
            # Tags That contains <Trecho> are verified here
            if elem.tag == "Trecho":
                TValues = [None] * 12
                # List with all Tags to be verified according to the Edital
                Tags = ["IdTrecho", "NomeTrecho", "DataLevantamentoTrecho",
                        "PlacaCarro", "UnidadeFederativa", "BR",
                        "TipoTrecho", "Pista", "Sentido", "KmInicial",
                        "KmFinal", "CaminhoPasta"]
                for child in elem:
                    for i in range(len(TValues)):
                        if child.tag == Tags[i]:
                            TValues[i] = child.text

                # Defines a name for the current Road SNV
                nameSNV = TValues[0] + "_" + TValues[1]
                currentSNV = TValues[1]

                # Check if the file is in the list to be verified
                if str(SNVsToBeChecked[0]).lower() != "full" and \
                        (currentSNV not in SNVsToBeChecked) and \
                        (nameSNV not in SNVsToBeChecked) and \
                        (str(TValues[0]) not in str(SNVsToBeChecked)):
                    ExcludedSNV += currentSNV + "; "
                    continue  # Goes to the next Road SNV

                try:
                    path = (TValues[11]) if TValues[11] is not None else "None"
                    pathSNV = os.path.join(pathHD, path)

                    # Create an line for the Road SNV
                    updateLog(pathSNV, "", pathReportLog)

                    # Check for Null Values in index.xml
                    for i in range(len(TValues)):
                        if TValues[i] is None:
                            MSG = "Encontrado valor nulo para o tipo: "
                            MSG += str(Tags[i]) + "no index.xml"
                            updateLog(pathSNV, MSG, pathReportLog)

                    # Check if UF in names is equal to the one in index.xml
                    if TValues[4] != currentSNV[3:5] or TValues[4] not in UFs:
                        MSG = "Formato errado no tipo 'UF' no SNV de nome: "
                        MSG += str(currentSNV) + ". "
                        MSG += "UF no index.xml: " + str(TValues[4])
                        updateLog(pathSNV, MSG, pathReportLog)

                    # Check if BRs Number in thename is equal to the index.xml
                    try:
                        BRNames = float(currentSNV[0:3])
                        if abs(float(TValues[5]) - BRNames) > 0.1:
                            raise ValueError()
                    except BaseException:
                        MSG = "Formato errado do tipo 'BR' no SNV de nome: "
                        MSG += str(currentSNV) + ". "
                        MSG += "BR no index.xml: " + str(TValues[5])
                        updateLog(pathSNV, MSG, pathReportLog)

                    # Check if 'TipoTrecho' in index.xml is according to Edital
                    if TValues[6] not in ["B", "A", "N", "V", "C", "U"]:
                        MSG = "Valor Tipo Trecho errado. Deveria ser: "
                        MSG += " B, A, N, V, C, U. "
                        MSG += "Valor no index.xml: " + str(TValues[6])
                        updateLog(pathSNV, MSG, pathReportLog)

                    # Check if 'Pista' in index.xml is according to Edital
                    if TValues[7] not in ["S", "D"]:
                        MSG = "Valor de PISTA errado. Deveria ser: "
                        MSG += "S para simples ou D para Duplicada. "
                        MSG += "Valor no index.xml: " + str(TValues[7])
                        updateLog(pathSNV, MSG, pathReportLog)

                    # Check if 'Sentido' in index.xml is according to Edital
                    if TValues[8] not in ["C", "D"]:
                        MSG = "Valor de SENTIDO errado. Deveria ser: "
                        MSG += "'C' para crescente ou 'D' para decrescente. "
                        MSG += "Valor no index.xml: " + str(TValues[8])
                        updateLog(pathSNV, MSG, pathReportLog)
                    kmInitial = float(TValues[9])
                    kmFinal = float(TValues[10])

                    # Append Roads Informantions in listSNVs
                    listSNVs[0].append(nameSNV)
                    listSNVs[1].append(kmInitial)
                    listSNVs[2].append(kmFinal)
                    listSNVs[3].append(pathSNV)
                except BaseException:  # (TypeError, ValueError, IndexError):
                    MSG = "Erro devido a formatacao no arquivo no index.xml"
                    updateLog(TValues[1], MSG, pathReportLog)

        # Update ReportLog with Roads SNVs that hasn't been checked
        if ExcludedSNV != "":
            MSG = "Trechos excluidos da verificacao: "
            updateLog("GERAL", MSG + ExcludedSNV, pathReportLog)

    # FileNotFoundError:
    except BaseException:
        MSG = "Nao foi possivel encontrar o arquivo index.xml "
        updateLog("GERAL", MSG, pathReportLog)
        print("\nScript finalizou " + MSG + "\n" + traceback.format_exc())
        exit()
