# ============================================================== #
# SCRIPT NAME : LVC check.py
# AUTHOR      : Victor Hugo Dalosto de Oliveira
# EMAIL       : victordalosto@gmail.com
# DESCRIPTION : Script to check inconsistencies in LVC data
# Check if files are apt. to be approved and codificated
# ============================================================== #


def checkLVC(pathHD, SNVsToBeChecked):
    '''
    Main script that checks the files for LVC import.

    @param pathHD (String) Main directory where the Index.xml and files are located.
    @param SNVsToBeChecked (Array) List of SNVs names or IDs to check. Set to ["full"] to check the entire Root.
    '''
    version = "1.0"

    from datetime import datetime
    import os
    import glob
    import xml.etree.ElementTree as ET
    import traceback
    import subprocess
    import json

    # Path to the script.
    pathMain = os.getcwd()

    # Change the path of the directory to call the ffmpeg script.
    os.chdir(os.path.join(pathMain, "lib", "ffmpeg", 'bin'))

    # Path to the index.xml used as import of HD.
    pathIndex = os.path.join(pathHD, "index.xml")

    # Create output log file with current date.
    pathReportLog = os.path.join(pathMain, "lib", ("Relatorio_" + datetime.now().strftime("%d_%m_%Y_%Hh_%Mm_%Ss") + ".txt"))

    # List of roads SNVs [id_nameSNV][kmInitial][kmFinal][adressPath]
    listSNVs = [[], [], [], []]

    # List of problems found [name][MsgOfProblem][name]
    listProblems = [[], []]

    # Create an repot log file with all checking done on files
    def reportLog():
        if os.path.isfile(pathReportLog) is False:  # Create a RelatorioLVC.txt
            reportLog = open(pathReportLog, "w")
        else:
            reportLog = open(pathReportLog, "r+")  # Clean RelatorioLVC.txt
            reportLog.truncate(0)
        reportLog.writelines("Log: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S - "))
        reportLog.writelines("Version: v" + version+"\n\n")
        reportLog.close()

    # Create an array with informations about the roads to be manipulated
    # listSNVs = [id_nameSNV][kmInitial][kmFinal][adressPath]
    def checkIndex():
        try:
            tree = ET.parse(pathIndex)
            updateLog("VERIFICACOES GERAIS", "")
            TrechosExcluidos = ""
            UFs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
            for elem in tree.iter():
                # Get the 'Lote' inside Directory and compare with HDs name
                if elem.tag == "Etiqueta":
                    for child in elem:
                        if (child.tag) == "Lote":
                            nameHD = (os.path.basename(os.path.normpath(pathHD)))[1]
                            if child.text != nameHD:
                                updateLog("VERIFICACOES GERAIS", "Nome no HD XXXX (Ciclo_Lote_NºXX) esta diferente do informado no index.xml")
                # Check Trechos
                if elem.tag == "Trecho":
                    TrechosValues = [None] * 12
                    TrechosTags = ["IdTrecho", "NomeTrecho", "DataLevantamentoTrecho", "PlacaCarro", "UnidadeFederativa", "BR", "TipoTrecho", "Pista", "Sentido", "KmInicial", "KmFinal", "CaminhoPasta"]
                    for child in elem:
                        for i in range(len(TrechosValues)):
                            if child.tag == TrechosTags[i]:
                                TrechosValues[i] = child.text

                    nameSNV = TrechosValues[0] + "_" + TrechosValues[1]
                    currentSNV = TrechosValues[1]
                    if str(SNVsToBeChecked[0]).lower() != "full":
                        if (currentSNV not in SNVsToBeChecked) and (nameSNV not in SNVsToBeChecked) and (str(TrechosValues[0]) not in str(SNVsToBeChecked)):
                            TrechosExcluidos = TrechosExcluidos + currentSNV + "; "
                            continue
                    try:
                        pathSNV = os.path.join(pathHD, ((TrechosValues[11]) if TrechosValues[11] is not None else "None"))
                        updateLog(pathSNV, "")
                        # Check Null Values in Index.xml
                        for i in range(len(TrechosValues)):
                            if TrechosValues[i] is None:
                                updateLog(pathSNV, ("Encontrado valor nulo para o tipo: <" + str(TrechosTags[i]) + ">"))
                        if TrechosValues[4] != currentSNV[3:5] or TrechosValues[4] not in UFs:
                            updateLog(pathSNV, "Formato errado para o tipo 'UF' no SNV de nome: " + str(currentSNV) + ". UF no index: " + str(TrechosValues[4]))
                        try:
                            if abs(float(TrechosValues[5]) - float(currentSNV[0:3])) > 0.1 :
                                updateLog(pathSNV, "Formato errado para o tipo 'BR' no SNV de nome: " + str(currentSNV) + ". BR no index: " + str(TrechosValues[5]))
                        except:
                            updateLog(pathSNV, "Formato errado para o tipo 'BR' no SNV de nome: " + str(currentSNV) + ". BR no index: " + str(TrechosValues[5]))
                        # Check if 'TipoTrecho' in Index.xml is according to Edital
                        if TrechosValues[6] not in ["B", "A", "N", "V", "C", "U"]:
                            updateLog(pathSNV, ("Valor Tipo Trecho errado. Deveria ser B, A, N, V, C, U. Valor no index: " + str(TrechosValues[6])))
                        # Check if 'Pista' in Index.xml is according to Edital
                        if TrechosValues[7] not in ["S", "D"]:
                            updateLog(pathSNV, ("Valor de PISTA errado. Deveria ser: 'S para simples e D para Duplicada'. Valor no index: " + str(TrechosValues[7])))
                        # Check if 'Sentido' in Index.xml is according to Edital
                        if TrechosValues[8] not in ["C", "D"]:
                            updateLog(pathSNV, ("Valor de SENTIDO errado. Deveria ser: 'C para crescente e D para decrescente'. Valor no index: " + str(TrechosValues[8])))
                        kmInitial = float(TrechosValues[9])
                        kmFinal = float(TrechosValues[10])
                        listSNVs[0].append(nameSNV)
                        listSNVs[1].append(kmInitial)
                        listSNVs[2].append(kmFinal)
                        listSNVs[3].append(pathSNV)
                    except:  # (TypeError, ValueError, IndexError):
                        updateLog(TrechosValues[1], "Erro devido a formatacao no arquivo no Index.xml")
            if TrechosExcluidos != "":
                updateLog("VERIFICACOES GERAIS", "Trechos excluidos da verificacao: " + TrechosExcluidos)

        except:  # FileNotFoundError:
            updateLog("VERIFICACOES GERAIS", "Nao foi possivel encontrar o arquivo index.xml")
            print("\nScript finalizou = Nao foi possivel encontrar o arquivo index.xml")
            exit()

    # Function that check the integrity of files in HD
    def checkFolders():
        for i in range(len(listSNVs[3])):
            SNV = listSNVs[3][i]
            # Check if adress Path exists on HD
            if os.path.exists(SNV) is False:
                updateLog(SNV, ("Nao foi possivel encontrar para o trecho " + str(listSNVs[0][i]) + ", seu caminho na pasta: " + SNV))
            else:
                pathLog = os.path.join(SNV, "LogsTrecho.xml")
                pathVideo = os.path.join(SNV, "videos")
                pathCam1 = os.path.join(pathVideo, "camera1")
                pathCam2 = os.path.join(pathVideo, "camera2")
                pathCam3 = os.path.join(pathVideo, "camera3")
                # Check if LogsTrecho.xml exists
                if os.path.exists(pathLog) is False:
                    updateLog(SNV, "Nao foi possivel encontrar o arquivo LogsTrecho.xml")
                # Check if Videos folder exists
                if os.path.exists(pathVideo) is False:
                    updateLog(SNV, "Nao foi possivel encontrar a pasta videos")
                else:  # Check if videos/camera1 exists
                    if os.path.exists(pathCam1) is False:
                        updateLog(SNV, "Nao foi possivel encontrar a pasta camera1")
                    else:  # Check if there is a mp4 file inside camera folder
                        for file in glob.glob(os.path.join(pathCam1, "*.mp4")):
                            pathCam1 = os.path.join(pathCam1, file)
                            if os.path.getsize(pathCam1) == 0:
                                updateLog(SNV, "Camera1 esta corrompida.")
                            break
                        if not pathCam1.endswith("mp4"):
                            updateLog(SNV, "Nenhum arquivo de video do tipo '.mp4' na pasta Camera1")
                    # Same verification for camera 2 folder
                    if (os.path.exists(pathCam2) is False):
                        updateLog(SNV, "Nao foi possivel encontrar a pasta camera2")
                    else:
                        for file in glob.glob(os.path.join(pathCam2, "*.mp4")):
                            pathCam2 = os.path.join(pathCam2, file)
                            if os.path.getsize(pathCam2) == 0:
                                updateLog(SNV, "Camera1 esta corrompida.")
                            break
                        if not pathCam2.endswith("mp4"):
                            updateLog(SNV, "Nenhum arquivo de video do tipo '.mp4' na pasta Camera2")
                    # Check if camera3 (Photos) exists
                    if (os.path.exists(pathCam3) is False):
                        updateLog(SNV, "Nao foi possivel encontrar a pasta camera3")

    # Check informations inside LogsTrecho.xml and its integrity
    def checkLogsTrecho():
        # Check if Odometer values are correct
        def checkOdometer(odometro, odmTrecho):
            diff = 0
            for j in range(len(odometro)-1):
                if (odometro[j] < 0 or odmTrecho[j] < 0):
                    diff += 1
                step1 = abs(odometro[j] - odometro[j+1])
                step2 = abs(odmTrecho[j] - odmTrecho[j+1])
                # Check if Odometro + step == OdometroTrecho + step
                tolerance = 2  # Arbitrary value
                if abs(step1 - step2) > tolerance:
                    if j < len(odometro)-2:
                        step1a = abs(odometro[j] - odometro[j-1])
                        step2a = abs(odmTrecho[j] - odmTrecho[j-1])
                        step1d = abs(odometro[j+2] - odometro[j+1])
                        step2d = abs(odmTrecho[j+2] - odmTrecho[j+1])
                        MSG = "Trecho com salto odometro equivocado no " + " LogsTrecho.xml odometro (" + str(odometro[j]) + " -> " + str(odometro[j+1]) + ") =/= OdometroTrecho (" + str(odmTrecho[j]) + " -> " + str(odmTrecho[j+1]) + ")"
                        if abs((step1a + step1) - (step2a + step2)) > tolerance and ((step1d + step1) - (step2d + step2)) > tolerance:
                            updateLog(SNV, MSG)
                # Value defined according to Edital
                tolerance = 20  # Maximum step = 20m
                if (step1 > tolerance):
                    updateLog(SNV, ("Trecho com salto odometro > 20 metros (" + str(odometro[j]) + " -> " + str(odometro[j+1]) + ")"))
                if (step2 > tolerance):
                    updateLog(SNV, ("Trecho com salto odometroTrecho > 20 metros (" + str(odmTrecho[j]) + " -> " + str(odmTrecho[j+1]) + ")"))
            if diff > 0:
                updateLog(SNV, (str(diff) + " occorrencia no trecho de Odometro negativo"))

        # Check consistance about Km informations
        # Check if kms in Index.xml are Equal to LogsTrecho.xml
        def checkKM(initIndex, finalIndex, listOdometer):
            initLog = listOdometer[0]/1000
            finalLog = listOdometer[-1]/1000
            if abs(initLog - initIndex) >= 0.01:
                MSG = "KM Inicial no index.xml (" + str(round(initIndex, 3)) + ") " + "=/= LogsTrechos.xml (" + str(round(initLog, 3)) + ")"
                updateLog(SNV, MSG)
            if abs(finalLog - finalIndex) >= 0.01:
                MSG = "KM Final no index.xml (" + str(round(finalIndex, 3)) + ") " + "=/= LogsTrechos.xml (" + str(round(finalLog, 3)) + ")"
                updateLog(SNV, MSG)

        # Count the number of duplicates values in list
        def checkDuplicates(array, tolerance, error):
            odm = lista[0]  # Variable in Scope
            dups = 0
            usedValues = []
            amount = 0
            for n in range(len(array)-1):
                if round(array[n], 3) not in usedValues:
                    usedValues.append(round(array[n], 3))  # Avoid reptition
                    qtidade = array.count(round(array[n], 3))  # number of dups
                    amount = round(qtidade / len(array)*100, 2)
                    # Check if values are really duplicated
                    # Tolerance = 1 % of entire SNV and 150% of tolerance
                    if amount > 1 and qtidade > 1.5 * tolerance:
                        # Get index of all duplicated values in the entire array
                        indexs = [m for m, x in enumerate(array) if x == array[i]]
                        for j in range(len(indexs)):
                            dummy = 1  # Sum of incorrect values
                            inTolerance = True  # Evalute if values are incorrect
                            for k in range(j, len(indexs)-1):
                                # Check if Duplicated values are in sequence
                                if round(abs(indexs[k+1] - indexs[k]), 2) == 1:
                                    dummy += 1  # Start with 2 because K and K+1
                                    # Check if values are in the tolerance limit
                                    diff = abs(odm[indexs[k]] - odm[indexs[j]])
                                    if (tolerance) < diff:
                                        inTolerance = False
                                else:
                                    break
                            if inTolerance is False:
                                dups = (dummy if dummy > dups else dups)
                    if amount > 9 and qtidade > 4*tolerance:
                        updateLog(SNV, (str(qtidade) + " valores duplicados (" + str(amount) + "%) de " + error + " = " + str(array[n]) + " - tolerancia = " + str(tolerance)))
            return dups

        # Function that calls Check duplicates and export error if there is any
        def checkDups(array, tolerance, error):
            dup = checkDuplicates(array, tolerance, error)
            if dup > tolerance:
                amount = round(dup / len(array)*100, 2)
                if amount > 1:
                    updateLog(SNV, (str(dup) + " ocorrencias duplicadas (" + str(amount) + "%) " + "de " + error + " no LogsTrecho.xml"))

        # Function that check if values are inside determined limit
        def checkLimits(array, upper, botton, error):
            numUp = len([element for element in array if element >= upper])
            numBot = len([element for element in array if element <= botton])
            if numUp > upper or numBot < botton:
                amountUp = round(numUp / len(array)*100, 2)
                amountBot = round(numBot / len(array)*100, 2)
                if amountUp > 1 or amountBot > 1:
                    updateLog(SNV, (str(numUp) + " ocorrencias (" + str(amountUp) + "%)" + " >= " + str(upper) + " e " + str(numUp) + " ocorrencias (" + str(amountBot) + "%) <= " + str(botton) + " de " + error + " valores iguais no LogsTrecho.xml "))

        # Function that check number of values = 0
        def checkZeros(array, error):
            count = array.count(0)
            amount = round(count / len(array)*100, 2)
            if amount > 3:
                updateLog(SNV, (str(count) + " ocorrencias (" + str(amount) + "%) " + "de " + error + " valores nulos ou = 0 no LogsTrecho.xml"))

        # Check if video timings are correct
        def checkVideo(timingsFrente, timingsTras):
            def checkVideoDuration(path, final, local):
                for file in glob.glob(os.path.join(path, "*.mp4")):
                    path = os.path.join(path, file)  # path to Video of SNV
                    if (path.endswith('.mp4') is True):
                        duration = eval((json.loads(subprocess.check_output(f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{path}"', shell=True).decode())['streams'][0])['duration'])
                    else:
                        duration = 0  # Problem already trated in checkFolders()
                    if abs(final - duration) > 30:
                        MSG = "A Duracao do arquivo de video " + str(round(duration, 1)) + "s especificado no Logstrecho.xml esta diferente dos " + str(round(final, 1)) + "s do arquivo na pasta " + local
                        updateLog(SNV, MSG)
            tolerance = 10
            checkDups(timingsFrente, tolerance, "Valores iguais de TempoCamera 'Frente'")
            checkDups(timingsTras, tolerance, "Valores iguais de TempoCamera 'Tras'")
            checkVideoDuration((os.path.join(SNV, "videos", "camera1")), max(timingsFrente), "Camera 1")
            checkVideoDuration((os.path.join(SNV, "videos", "camera2")), max(timingsTras), "Camera 2")
            if timingsFrente[0] > 60 or timingsTras[0] > 0:
                updateLog(SNV, "Problema com os primeiros valores de timings muito alto para os videos")

        # Check if IRI values are correct
        def checkIRI(IRIint, IRIext):
            # "Ao final de cada 100 (cem) metros, os seguintes dados de
            # Irregularidade Longitudinal devem ser incorporados aos registros:"
            tolerance = 100
            checkDups(IRIint, tolerance, "Repetidos valores de IRIint")
            checkDups(IRIext, tolerance, "Repetidos valores de IRIext")
            supLim = 15
            infLim = 0
            checkLimits(IRIint, supLim, infLim, "IRIint")
            checkLimits(IRIext, supLim, infLim, "IRIext")
            checkZeros(IRIint, "IRIint")
            checkZeros(IRIext, "IRIext")

        # Check if flechas values are correct
        def checkFlecha(flechaInt, flechaExt):
            # "Ao final de cada 20 (vinte) metros devera ser incorporado ao
            # registo o valor do Afundamento da Trilha de Rodas (ATR)"
            tolerance = 20
            checkDups(flechaInt, tolerance, "Repetidos valores de flechaInt")
            checkDups(flechaExt, tolerance, "Repetidos valores de flechaExt")
            supLim = 40
            infLim = 0
            checkLimits(flechaInt, supLim, infLim, "flechaInt")
            checkLimits(flechaExt, supLim, infLim, "flechaExt")
            checkZeros(flechaInt, "flechaInt")
            checkZeros(flechaExt, "flechaExt")

        # Check if coordinates longtitude and latitude are correct
        def checkCoordinates(X, Y):
            checkZeros(X, "GPS X")
            checkZeros(Y, "GPS Y")
            tolerance = 20
            checkDups(X, tolerance, "Repetidos valores de GPS 'X'")
            checkDups(Y, tolerance, "Repetidos valores de GPS 'Y'")
            for j in range(len(X)):
                if (Y[j] < -34) or (Y[j] > 5.3) or (X[j] > -35) or (X[j] < -74):
                    updateLog(SNV, "Problema de coordenadas. Valores encontram-se fora do Brasil")

        # Check files in ../videos/camera3 folder
        def checkPhotos(extension):
            pathImg = os.path.join(SNV, "videos", "camera3")
            images = 0
            MSG = ""
            for file in os.listdir(pathImg):
                if os.path.isfile(os.path.join(pathImg, file)):
                    if (file.endswith(".png") or file.endswith(".jpeg") or file.endswith(".jpg")):
                        images += 1
                        if os.path.getsize(os.path.join(pathImg, file)) == 0:
                            updateLog(SNV, (file + " na pasta camera 3 esta corrompido"))
                        file, type = os.path.splitext(file)
                        try:
                            if float(file) < 0 or float(file) > (extension*1000+150):
                                MSG = MSG + str(file) + type + "; "
                        except ValueError:
                            MSG = MSG + file + type + "; "
            if MSG != "":
                MSG = "Problema com formatos de arquivos ou fora dos limites do index na pasta camera3: " + MSG
                updateLog(SNV, MSG)
            extensionPhoto = images*5/1000
            if (extensionPhoto < 0.91*extension or extensionPhoto > 1.15*extension):
                updateLog(SNV, "Problema relacionado ao numero de foto. Extensao no index (" + str(round(extension, 2)) + "km) =/= " + str(images) + " photos x 5m (" + str(round(extensionPhoto, 2)) + "km). Fotos deveriam estar espacadas de 5-5m, e nao " + str(round(extension*1000/images, 1)) + "m")

        # Check if velocity informations are correct
        def checkVelocity(vel1, vel2):
            tolerance = 30
            checkDups(vel1, tolerance, "Repetidos valores de Velocity")
            # Number of times that velocity appears >= 60km *(1 + 10%)
            supLim = 66
            infLim = 0
            checkLimits(vel1, supLim, infLim, "Velocity")
            checkZeros(vel1, "Velocity")
            '''
            diff = 0
            for j in range(len(vel1)):
                diference = abs(vel1[j] - vel2[j])
                if (diference > 0.2):
                    diff += 1
            if diff > 0:
                amount = round(diff / len(vel1)*100, 2)
                MSG = str(diff) + " divergences (" + str(amount) + "%) " + \
                    "from Velocity to GPS to GPS Velocity in LogsTrecho.xml"
                updateLog(SNV, MSG)
            '''

        def checkNull(value, type):
            if (value == "") or (value is None):
                updateLog(SNV, "Valor Null encontrado para: " + type)

        # Loop to get all Values from LogsTrecho.xml
        for i in range(len(listSNVs[0])):
            SNV = listSNVs[3][i]
            print("Trecho: " + listSNVs[0][i] + " - " + str(round(i/len(listSNVs[0])*100, 2)) + "%")
            try:
                root = ET.parse(os.path.join(SNV, "LogsTrecho.xml")).getroot()
                lista = [[], [], [], [], [], [], [], [], [], [], [], []]
                valuesList = [None] * 24
                typeList = ["Id", "Odometro", "OdometroTrecho", "Velocidade", "ExtLog", "DataHora", "TempoLog", "Frente", "Tras", "Velocidade", "Odometro", "Z", "X", "Y", "Azi", "Erro", "Sat", "GPRMC", "IRIInt", "IRIExt", "FlechaInt", "FlechaExt", "TipoReves", "PerUrb"]
                for index in range(len(root[0])):
                    try:
                        valuesList[0] = root[0][index].attrib.get('Id')
                        valuesList[1] = root[0][index].attrib.get('Odometro')
                        valuesList[2] = root[0][index].attrib.get('OdometroTrecho')
                        valuesList[3] = root[0][index].attrib.get('Velocidade')
                        valuesList[4] = root[0][index].attrib.get('ExtLog')
                        valuesList[5] = root[0][index].attrib.get('DataHora')
                        valuesList[6] = root[0][index].attrib.get('TempoLog')
                        valuesList[7] = (root[0][index][0].attrib).get('Frente')
                        valuesList[8] = (root[0][index][0].attrib).get('Tras')
                        valuesList[9] = (root[0][index][1].attrib).get('Velocidade')
                        valuesList[10] = (root[0][index][1].attrib).get('Odometro')
                        valuesList[11] = (root[0][index][1].attrib).get('Z')
                        valuesList[12] = (root[0][index][1].attrib).get('X')
                        valuesList[13] = (root[0][index][1].attrib).get('Y')
                        valuesList[14] = (root[0][index][1].attrib).get('Azi')
                        valuesList[15] = (root[0][index][1].attrib).get('Erro')
                        valuesList[16] = (root[0][index][1].attrib).get('Sat')
                        valuesList[17] = (root[0][index][1].attrib).get('GPRMC')
                        valuesList[18] = (root[0][index][2].attrib).get('IRIInt')
                        valuesList[19] = (root[0][index][2].attrib).get('IRIExt')
                        valuesList[20] = (root[0][index][2].attrib).get('FlechaInt')
                        valuesList[21] = (root[0][index][2].attrib).get('FlechaExt')
                        valuesList[22] = (root[0][index][2].attrib).get('TipoReves')
                        valuesList[23] = (root[0][index][2].attrib).get('PerUrb')
                        for count in range(len(valuesList)):
                            checkNull(valuesList[count], typeList[count] + ". Valor no id: " + str(int(valuesList[0])))
                            if valuesList[count] is not None and valuesList[count] != "" and valuesList[count] != " ":
                                if count not in [5, 17, 22, 23]:
                                    valuesList[count] = round(float(valuesList[count]), 10)
                        if valuesList[11] > 3000 or valuesList[11] < -50:
                            updateLog(SNV, ("Valor de altitude errada: " + str(valuesList[11]) + ". Valor no id: " + str(int(valuesList[0]))))
                        if valuesList[16] < 3:
                            updateLog(SNV, "Numero de Satelites < 3, Verificar com atencao as coordenadas GPS" + ". Valor no id: " + str(int(valuesList[0])))
                        if valuesList[14] < 0 or valuesList[14] > 360:
                            updateLog(SNV, "Valor errado de Azimute Azi: " + str(valuesList[14]) + ". Deveria ser 0º <= Azi <= 360. Valor no id: " + str(int(valuesList[0])))
                        if valuesList[15] > 100:
                            updateLog(SNV, "Valor de Error no LogsTrecho.xml > 20m (Odometro): " + str(valuesList[15]) + ". Valor no id: " + str(int(valuesList[0])))
                        lista[0].append(valuesList[1])
                        lista[1].append(valuesList[2])
                        lista[2].append(valuesList[7])
                        lista[3].append(valuesList[8])
                        lista[4].append(valuesList[18])
                        lista[5].append(valuesList[19])
                        lista[6].append(valuesList[20])
                        lista[7].append(valuesList[21])
                        lista[8].append(valuesList[12])
                        lista[9].append(valuesList[13])
                        lista[10].append(valuesList[3])
                        lista[11].append(valuesList[9])
                    except:
                        updateLog(SNV, ("Erro no arquivo xml - " + traceback.format_exc()))

                try: checkOdometer(lista[0], lista[1])
                except: updateLog(SNV, "Erro no arquivo xml - Nao foi possivel verificar o Odometro")

                try: checkKM(listSNVs[1][i], listSNVs[2][i], lista[1])
                except: updateLog(SNV, "Erro no arquivo xml - Nao foi possivel verificar os KMs")

                try: checkVideo(lista[2], lista[3])
                except: updateLog(SNV, "Erro no arquivo xml - Nao foi possivel verificar os Videos")

                try: checkIRI(lista[4], lista[5])
                except: updateLog(SNV, "Erro no arquivo xml - Nao foi possivel verificar os IRIs")

                try: checkFlecha(lista[6], lista[7])
                except: updateLog(SNV, "Erro no arquivo xml - Nao foi possivel verificar as Flechas")

                try: checkCoordinates(lista[8], lista[9])
                except: updateLog(SNV, "Erro no arquivo xml - Nao foi possivel verificar as Coordenadas GPS")

                try: checkPhotos(abs(listSNVs[1][i]-listSNVs[2][i]))
                except: updateLog(SNV, "Erro no arquivo xml - Nao foi possivel verificar as Fotos na pasta camera3")

                try: checkVelocity(lista[10], lista[11])
                except: updateLog(SNV, "Erro no arquivo xml - Nao foi possivel verificar a Velocidade")

                if (SNV not in listProblems[0]):
                    updateLog(SNV, "Trecho OK")
            except FileNotFoundError:
                updateLog(SNV, "Nao foi possivel validar o Trecho pois nao tem o arquivo LogsTrecho.xml no caminho: " + os.path.join(listSNVs[3][i], "LogsTrecho.xml"))
            except ET.ParseError:
                updateLog(SNV, "Invalid token in xml")

    def updateLog(nameTrecho, MSG):
        if (MSG == ""):
            listProblems[1].append(MSG)
        else:
            listProblems[0].append(nameTrecho)
            listProblems[1].append("  * " + MSG)
        nameTrecho = nameTrecho.replace("/", "\\")
        # Get all files already in repot Log
        listLines = (open(pathReportLog, "r")).readlines()
        try:
            line = listLines.index(nameTrecho+"\n")
            listLines.insert(line+1, listProblems[1][-1]+"\n")
        except ValueError:
            listLines.append(nameTrecho+"\n")
            listLines.append(listProblems[1][-1]+"\n\n")
        Log = open(pathReportLog, "w")
        Log.writelines(listLines)
        Log.close()

    def Main():
        reportLog()
        checkIndex()
        checkFolders()
        checkLogsTrecho()
        print("Verificaçao concluida com sucesso LVC Check - 100%")

    Main()