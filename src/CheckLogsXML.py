
import os
import traceback
import xml.etree.ElementTree as ET
from src.reportLog import updateLog
from src.CheckLogsXMLValidation import checkOdometer, checkKM, checkVideo,\
    checkIRI, checkFlecha, checkAzimute, checkSatelites, checkCoordinates, \
    checkAltitude, checkErros, checkPhotos, checkVelocity


# Check informations inside LogsTrecho.xml and its integrity
def checkLogsXML(listSNVs, pathRep):

    # Loop to get all Roads SNV
    for i in range(len(listSNVs[0])):

        # Get SNVs path to be validated
        SNV = listSNVs[3][i]

        # Print the % concluded of the DATA validation
        printPercentage(listSNVs[0][i], round(i/len(listSNVs[0])*100, 2))

        try:
            # Gets the informations inside LogsTrecho.XML
            LogsTrechoXML = os.path.join(SNV, "LogsTrecho.xml")
            root = ET.parse(LogsTrechoXML).getroot()

            # List with the 24 Validations proposed in Edital for the XML
            valList = [None] * 24
            finalList = [[], [], [], [], [], [], [], [], [], [], [], [],
                         [], [], [], [], [], [], [], [], [], [], [], []]
            typeList = ["Id", "Odometro", "OdometroTrecho", "Velocidade",
                        "ExtLog", "DataHora", "TempoLog", "Frente", "Tras",
                        "Velocidade", "Odometro", "Z", "X", "Y", "Azi",
                        "Erro", "Sat", "GPRMC", "IRIInt", "IRIExt",
                        "FlechaInt", "FlechaExt", "TipoReves", "PerUrb"]

            # Loop that interate inside LogsTrecho.xml File
            for index in range(len(root[0])):
                try:
                    # The code below was purposely taken out of a loop
                    valList[0] = root[0][index].attrib.get('Id')
                    valList[1] = root[0][index].attrib.get('Odometro')
                    valList[2] = root[0][index].attrib.get('OdometroTrecho')
                    valList[3] = root[0][index].attrib.get('Velocidade')
                    valList[4] = root[0][index].attrib.get('ExtLog')
                    valList[5] = root[0][index].attrib.get('DataHora')
                    valList[6] = root[0][index].attrib.get('TempoLog')
                    valList[7] = (root[0][index][0].attrib).get('Frente')
                    valList[8] = (root[0][index][0].attrib).get('Tras')
                    valList[9] = (root[0][index][1].attrib).get('Velocidade')
                    valList[10] = (root[0][index][1].attrib).get('Odometro')
                    valList[11] = (root[0][index][1].attrib).get('Z')
                    valList[12] = (root[0][index][1].attrib).get('X')
                    valList[13] = (root[0][index][1].attrib).get('Y')
                    valList[14] = (root[0][index][1].attrib).get('Azi')
                    valList[15] = (root[0][index][1].attrib).get('Erro')
                    valList[16] = (root[0][index][1].attrib).get('Sat')
                    valList[17] = (root[0][index][1].attrib).get('GPRMC')
                    valList[18] = (root[0][index][2].attrib).get('IRIInt')
                    valList[19] = (root[0][index][2].attrib).get('IRIExt')
                    valList[20] = (root[0][index][2].attrib).get('FlechaInt')
                    valList[21] = (root[0][index][2].attrib).get('FlechaExt')
                    valList[22] = (root[0][index][2].attrib).get('TipoReves')
                    valList[23] = (root[0][index][2].attrib).get('PerUrb')

                    # Validations done in XML File
                    for count in range(len(valList)):
                        # Check if value is obtainable
                        if valList[count] == "" or valList is None:
                            val = typeList[count]
                            MSG = "Valor Null encontrado para " + val
                            MSG += ". Valor no id: " + str(int(valList[0]))
                            updateLog(SNV, MSG, pathRep)
                        # Check if value is convertable to Number
                        if valList[count] is not None and \
                           valList[count] != "" and \
                           valList[count] != " ":
                            if count not in [5, 17, 22, 23]:
                                try:
                                    value = float(valList[count])
                                    valList[count] = round(value, 10)
                                except BaseException:
                                    MSG = "Not a Number encontrado para "
                                    MSG += typeList[count]
                                    MSG += ". Valor no id: " + str(valList[0])
                                    updateLog(SNV, MSG, pathRep)
                    for nn in range(len(valList)):
                        finalList[nn].append(valList[nn])
                except BaseException:
                    MSG = "Error no arquivo xml - " + traceback.format_exc()
                    updateLog(SNV, MSG, pathRep)

            # Pattern in message in case of a throwable error
            Err = "Erro no arquivo LogsTrecho.XML - "
            Err += "Nao foi possivel verificar: "
            KmsINDEX = [listSNVs[1][i], listSNVs[2][i]]

            try:
                checkOdometer(SNV, finalList, pathRep)
            except BaseException:
                updateLog(SNV, Err + "Odometro", pathRep)

            try:
                checkKM(SNV, KmsINDEX, finalList, pathRep)
            except BaseException:
                updateLog(SNV, Err + "KMs", pathRep)

            try:
                checkVideo(SNV, finalList, pathRep)
            except BaseException:
                updateLog(SNV, Err + "Videos", pathRep)

            try:
                checkIRI(SNV, finalList, pathRep)
            except BaseException:
                updateLog(SNV, Err + "IRIs", pathRep)

            try:
                checkFlecha(SNV, finalList, pathRep)
            except BaseException:
                updateLog(SNV, Err + "Flechas", pathRep)

            try:
                checkAzimute(SNV, finalList, pathRep)
            except BaseException:
                updateLog(SNV, Err + "Azimute", pathRep)

            try:
                checkSatelites(SNV, finalList, pathRep)
            except BaseException:
                updateLog(SNV, Err + "Satelites", pathRep)

            try:
                checkCoordinates(SNV, finalList, pathRep)
            except BaseException:
                updateLog(SNV, Err + "GPS", pathRep)

            try:
                checkAltitude(SNV, finalList, pathRep)
            except BaseException:
                updateLog(SNV, Err + "Altitude", pathRep)

            try:
                checkErros(SNV, finalList, pathRep)
            except BaseException:
                updateLog(SNV, Err + "Erros", pathRep)

            try:
                checkPhotos(SNV, listSNVs[1][i]-listSNVs[2][i], pathRep)
            except BaseException:
                updateLog(SNV, Err + "Camera3", pathRep)

            try:
                checkVelocity(SNV, finalList, pathRep)
            except BaseException:
                updateLog(SNV, Err + "Velocidade", pathRep)

        except FileNotFoundError:
            MSG = "Nao foi possivel validar o Trecho, " + \
                   "pois nao tem o arquivo LogsTrecho.xml no caminho: " + \
                   os.path.join(listSNVs[3][i])
            updateLog(SNV, MSG, pathRep)

        except ET.ParseError:
            MSG = "Invalid Token in LogsTrecho.XML"
            updateLog(SNV, MSG, pathRep)

        except BaseException:
            MSG = "Erro durante a verificacao dos LogsTrecho.xml"
            MSG += os.path.join(listSNVs[3][i])
            updateLog(SNV, MSG, pathRep)

        # Update Log, informing that checkings were done on ROAD SNV
        updateLog(SNV, "Verificacao Concluida", pathRep)


# Print the percentage of validation done in Prompt
def printPercentage(SNVsName, percentage):
    SNVsName = str(SNVsName)
    percentage = str(percentage)
    MSG = "Trecho " + SNVsName + " - " + percentage + "%"
    print(MSG)
