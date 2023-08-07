import os
import traceback
import xml.etree.ElementTree as ET

from src.dnit.Utils import is_not_valid, print_percentage
from src.dnit.Logger import update_log
from src.dnit.CheckLogsXMLValidation import checkOdometer, checkKM, checkTempoLog, checkVideo, checkIRI, checkFlecha, checkAzimute, checkSatelites, checkCoordinates, checkAltitude, checkErros, checkPhotos, checkVelocity

typeList = ["Id", "Odometro", "OdometroTrecho", "Velocidade", "ExtLog", "DataHora", "TempoLog", "Frente", "Tras", "Velocidade", "Odometro", "Z", "X", "Y", "Azi", "Erro", "Sat", "GPRMC", "IRIInt", "IRIExt", "FlechaInt", "FlechaExt", "TipoReves", "PerUrb"]


# Check informations inside LogsTrecho.xml and its integrity
def check(listSNVs, pathRep):

    # Loop to get all Roads SNV
    for iter in range(len(listSNVs[0])):

        # Get SNVs path to be validated
        NAME = listSNVs[0][iter]
        KM_INITIAL = listSNVs[1][iter]
        KM_FINAL = listSNVs[2][iter]
        SNV = listSNVs[3][iter]

        # Print the % concluded of the DATA validation
        print_percentage(NAME, round(iter/len(listSNVs[0])*100, 2))

        try:
            # Gets the informations inside LogsTrecho.XML
            xmlTAG = ET.parse(os.path.join(SNV, "LogsTrecho.xml")).getroot()

            # List with the 24 Validations proposed in Edital for the XML
            valList = [None] * 24
            finalList = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
            # Loop that interate inside LogsTrecho.xml File
            for i in range(len(xmlTAG[0])):
                try:
                    # The code below was purposely taken out of a loop
                    valList[0] = xmlTAG[0][i].attrib.get(typeList[0])
                    valList[1] = xmlTAG[0][i].attrib.get(typeList[1])
                    valList[2] = xmlTAG[0][i].attrib.get(typeList[2])
                    valList[3] = xmlTAG[0][i].attrib.get(typeList[3])
                    valList[4] = xmlTAG[0][i].attrib.get(typeList[4])
                    valList[5] = xmlTAG[0][i].attrib.get(typeList[5])
                    valList[6] = xmlTAG[0][i].attrib.get(typeList[6])
                    valList[7] = xmlTAG[0][i][0].attrib.get(typeList[7])
                    valList[8] = xmlTAG[0][i][0].attrib.get(typeList[8])
                    valList[9] = xmlTAG[0][i][1].attrib.get(typeList[9])
                    valList[10] = xmlTAG[0][i][1].attrib.get(typeList[10])
                    valList[11] = xmlTAG[0][i][1].attrib.get(typeList[11])
                    valList[12] = xmlTAG[0][i][1].attrib.get(typeList[12])
                    valList[13] = xmlTAG[0][i][1].attrib.get(typeList[13])
                    valList[14] = xmlTAG[0][i][1].attrib.get(typeList[14])
                    valList[15] = xmlTAG[0][i][1].attrib.get(typeList[15])
                    valList[16] = xmlTAG[0][i][1].attrib.get(typeList[16])
                    valList[17] = xmlTAG[0][i][1].attrib.get(typeList[17])
                    valList[18] = xmlTAG[0][i][2].attrib.get(typeList[18])
                    valList[19] = xmlTAG[0][i][2].attrib.get(typeList[19])
                    valList[20] = xmlTAG[0][i][2].attrib.get(typeList[20])
                    valList[21] = xmlTAG[0][i][2].attrib.get(typeList[21])
                    valList[22] = xmlTAG[0][i][2].attrib.get(typeList[22])
                    valList[23] = xmlTAG[0][i][2].attrib.get(typeList[23])

                    for attribute in range(len(valList)):
                        if is_not_valid(valList[attribute]):  # Check if null
                            update_log(SNV, "Valor Null encontrado para " + typeList[attribute] + ". Valor no id: " + str(int(valList[0])), pathRep)
                        if attribute not in [5, 17, 22, 23]:  # Shoulb be a number
                            try:
                                valList[attribute] = round(float(valList[attribute]), 10)
                            except BaseException:
                                update_log(SNV, "Not a Number encontrado para " + typeList[attribute] + ". Valor no id: " + str(valList[0]), pathRep)
                    for nn in range(len(valList)):
                        finalList[nn].append(valList[nn])
                except BaseException:
                    MSG = "Error no arquivo xml - " + traceback.format_exc()
                    update_log(SNV, MSG, pathRep)

            # Pattern in message in case of a throwable error
            Err = "Erro no arquivo LogsTrecho.XML - Nao foi possivel verificar: "
            KmsINDEX = [KM_INITIAL, KM_FINAL]

            try:
                checkOdometer(SNV, finalList, pathRep)
            except BaseException:
                update_log(SNV, Err + "Odometro", pathRep)

            try:
                checkKM(SNV, KmsINDEX, finalList, pathRep)
            except BaseException:
                update_log(SNV, Err + "KMs", pathRep)

            try:
                checkVideo(SNV, finalList, pathRep)
            except BaseException:
                print (traceback.format_exc())
                update_log(SNV, Err + "Videos", pathRep)

            try:
                checkIRI(SNV, finalList, pathRep)
            except BaseException:
                update_log(SNV, Err + "IRIs", pathRep)

            try:
                checkFlecha(SNV, finalList, pathRep)
            except BaseException:
                update_log(SNV, Err + "Flechas", pathRep)

            try:
                checkAzimute(SNV, finalList, pathRep)
            except BaseException:
                update_log(SNV, Err + "Azimute", pathRep)

            try:
                checkSatelites(SNV, finalList, pathRep)
            except BaseException:
                update_log(SNV, Err + "Satelites", pathRep)

            try:
                checkCoordinates(SNV, finalList, pathRep)
            except BaseException:
                update_log(SNV, Err + "GPS", pathRep)

            try:
                checkAltitude(SNV, finalList, pathRep)
            except BaseException:
                update_log(SNV, Err + "Altitude", pathRep)

            try:
                checkTempoLog(SNV, finalList, pathRep)
            except BaseException:
                update_log(SNV, Err + "TempoLog", pathRep)

            try:
                checkErros(SNV, finalList, pathRep)
            except BaseException:
                update_log(SNV, Err + "Erros", pathRep)

            try:
                checkPhotos(SNV, KM_INITIAL-KM_FINAL, pathRep)
            except BaseException:
                update_log(SNV, Err + "Camera3", pathRep)

            try:
                checkVelocity(SNV, finalList, pathRep)
            except Exception:
                print(traceback.format_exc())
                update_log(SNV, Err + "Velocidade", pathRep)

            # try:
            #     checkData(SNV, finalList, pathRep)
            # except BaseException:
            #     update_log(SNV, Err + "Data", pathRep)

        except FileNotFoundError:
            MSG = "Nao foi possivel validar o Trecho, pois nao tem o arquivo LogsTrecho.xml no caminho: " + os.path.join(listSNVs[3][iter])
            update_log(SNV, MSG, pathRep)

        except ET.ParseError:
            MSG = "Invalid Token in LogsTrecho.XML"
            update_log(SNV, MSG, pathRep)

        except BaseException:
            MSG = "Erro durante a verificacao dos LogsTrecho.xml" + os.path.join(listSNVs[3][iter])
            update_log(SNV, MSG, pathRep)

        # Update Log, informing that checkings were done on ROAD SNV
        update_log(SNV, "Verificacao Concluida", pathRep)
