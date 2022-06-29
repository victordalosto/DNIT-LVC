
import os
import glob
import json
import subprocess
import collections

from src.reportLog import updateLog

skipCheckingDups = False


# Update the Report Log with the informations about erros
def updateReportLoop(SNV, array, MSG, pathReportLog):
    if len(array) > 0:
        ERRORMSG = "Inconsistencia de " + MSG + " no LogsTrecho.XML. Valores dos Ids com error: "
        for iterIDs in range(len(array)-1):
            ERRORMSG += str(int(array[iterIDs])) + ", "
        ERRORMSG += str(int(array[len(array)-1])) + "."
        updateLog(SNV, ERRORMSG, pathReportLog)


# Count the number of duplicates values in a array
def checkDups(SNV, inputArray, tolerance, errorType, pathReportLog):
    if (skipCheckingDups):
        return
    array = collections.Counter(inputArray)
    hashSet = set(inputArray)
    # Loop in array to check if values in array are duplicated
    for value in hashSet:
        amount = array.get(value)  # number of dups
        amountPercentage = round(amount / len(inputArray)*100, 2)
        # Update Log if the Sum of the duplicated values is High
        if amountPercentage > 9 and amount > 4*tolerance:
            MSG = "Foram encontradas: " + str(amount) + " ocorrencias de valores duplicados = " + str(value) + " do tipo: " + errorType + ". Corresponde a " + str(amountPercentage) + " % do trecho."
            updateLog(SNV, MSG, pathReportLog)


# Function that check if values are inside determined specified limit
def checkLimits(SNV, IDS, array, limitUp, limitBot, errorType, pathReportLog):
    # Gets the amount of elements that are outside limits
    indexesUp = [i for i, element in enumerate(array) if element >= limitUp]
    indexesBot = [i for i, element in enumerate(array) if element <= limitBot]
    amountUp = len(indexesUp)
    amountBot = len(indexesBot)
    if amountUp > 0:
        newArray = []
        # Convert the indexes to the IDS in the LogsTrecho.XML file
        for value in indexesUp:
            newArray.append(int(IDS[value]))
        percentUp = str(round(amountUp / len(array)*100, 2))
        MSG = "valores incomuns de " + errorType + ". " + str(amountUp) + " ocorrencias (" + percentUp + "%) >= " + str(limitUp)
        updateReportLoop(SNV, newArray, MSG, pathReportLog)
    if amountBot > 0:
        newArray = []
        # Convert the indexes to the IDS in the LogsTrecho.XML file
        for value in indexesBot:
            newArray.append(int(IDS[value]))
        percentBot = str(round(amountBot / len(array)*100, 2))
        MSG = "valores incomuns de " + errorType + ". " + str(amountBot) + " ocorrencias (" + percentBot + "%) <= " + str(limitBot)
        updateReportLoop(SNV, newArray, MSG, pathReportLog)


# Check if Odometer values are correct and according to Edital
def checkOdometer(SNV, valList, pathReportLog):
    # Handled values in checking
    IDS = valList[0]
    odometro = valList[1]
    odmTrecho = valList[2]
    ERROS = [[], [], [], []]  # Inconsistencys stored in an Array: ERROS[[], ..[]]
    MSGS = ["odometros repetidos",
            "odometros com espacamento > 20m",
            "odometros negativos",
            "espacamento do odometro =/= espacamento do odometroTrecho"]
    # Loop inside odometer values
    for j in range(len(odometro)-1):
        step1 = abs(odometro[j] - odometro[j+1])
        step2 = abs(odmTrecho[j] - odmTrecho[j+1])
        # Check if step in Odometer is greather than 0
        if (step1 == 0 or step2 == 0):
            ERROS[0].append(IDS[j])
        # Check if spacing is correct according to Edital
        tolerance = 20  # Maximum step = 20m
        if (step1 > tolerance) or (step2 > tolerance):
            ERROS[1].append(IDS[j])
        # Check if values are positive
        if (odometro[j] < 0 or odmTrecho[j] < 0):
            ERROS[2].append(IDS[j])
        # Check if Odometro + step == OdometroTrecho + step
        tolerance = 2  # Arbitrary value
        if abs(step1 - step2) > tolerance:
            # Check if passing is compensed inside 3 STEPs
            if j < len(odometro)-2:
                step1a = abs(odometro[j] - odometro[j-1])
                step1d = abs(odometro[j+2] - odometro[j+1])
                step2a = abs(odmTrecho[j] - odmTrecho[j-1])
                step2d = abs(odmTrecho[j+2] - odmTrecho[j+1])
                if abs((step1a + step1) - (step2a + step2)) > tolerance and \
                   ((step1d + step1) - (step2d + step2)) > tolerance:
                    ERROS[3].append(IDS[j])
        # Send All Errors to function updateReportLoops
    for j in range(len(ERROS)):
        updateReportLoop(SNV, ERROS[j], MSGS[j], pathReportLog)


# Check if kms in Index.xml are Equal to LogsTrecho.xml
def checkKM(SNV, KMsIndex, valList, pathReportLog):
    initIndex = KMsIndex[0]
    finalIndex = KMsIndex[1]
    listOdometer = valList[2]
    initLog = listOdometer[0]/1000
    finalLog = listOdometer[-1]/1000
    if abs(initLog - initIndex) >= 0.01:
        MSG = "KM Inicial no index.xml (" + str(round(initIndex, 3)) + ") =/= LogsTrechos.xml (" + str(round(initLog, 3)) + ")"
        updateLog(SNV, MSG, pathReportLog)
    if abs(finalLog - finalIndex) >= 0.01:
        MSG = "KM Final no index.xml (" + str(round(finalIndex, 3)) + ") =/= LogsTrechos.xml (" + str(round(finalLog, 3)) + ")"
        updateLog(SNV, MSG, pathReportLog)


# Check if video timings are correct
def checkVideo(SNV, valList, pathReportLog):
    # Get the ID, and the front and back videos timings from the XML file
    frontT = valList[7]
    backT = valList[8]
    pathFront = os.path.join(SNV, "videos", "camera1")
    pathBack = os.path.join(SNV, "videos", "camera2")

    # Compares if the video duration in XML are according to .mp4 extension
    def checkDuration(SNV, pathInput, final, local, pathReportLog):
        for file in glob.glob(os.path.join(pathInput, "*.mp4")):
            # path to Video of ROAD SNV
            pathVid = os.path.join(pathInput, file)
            # Get the duration of the .mp4 file
            if (pathVid.endswith('.mp4') is True):
                duration = eval((json.loads(subprocess.check_output(f'ffprobe -v quiet -show_streams -select_streams v:0 -of json {pathVid}', shell=True).decode())['streams'][0])['duration'])
            else:
                duration = 0  # Problem already trated in checkFolders.py
            # Check if duration of video is different than the informed in XML
            if abs(final - duration) >= 30:
                MSG = "A duracao do video: " + str(round(final, 1)) + "segundos apresentado no Logstrecho.xml esta diferente dos " + str(round(duration, 1)) + "segundos do video na pasta: " + local
                updateLog(SNV, MSG, pathReportLog)
    tolerance = 5
    checkDups(SNV, frontT, tolerance, "Valores iguais de tempo Camera 'Frente'", pathReportLog)
    checkDups(SNV, backT, tolerance, "Valores iguais de tempo Camera 'Traseira'", pathReportLog)
    checkDuration(SNV, pathFront, max(frontT), "Camera 1", pathReportLog)
    checkDuration(SNV, pathBack, max(backT), "Camera 2", pathReportLog)
    if frontT[0] > 60 or backT[0] > 60:
        MSG = "Solicita verificacao nos primeiros valores timings de video."
        MSG += "Valores parecem estar acima do comum. "
        updateLog(SNV, MSG, pathReportLog)


# Check if IRI values are correct
def checkIRI(SNV, valList, pathReportLog):
    IDS = valList[0]
    IRIint = valList[18]
    IRIext = valList[19]
    tolerance = 100
    checkDups(SNV, IRIint, tolerance, "Repetidos valores de IRIint", pathReportLog)
    checkDups(SNV, IRIext, tolerance, "Repetidos valores de IRIext", pathReportLog)
    supLim = 15
    infLim = 0
    checkLimits(SNV, IDS, IRIint, supLim, infLim, "IRIint", pathReportLog)
    checkLimits(SNV, IDS, IRIext, supLim, infLim, "IRIext", pathReportLog)


# Check if flechas values are correct
def checkFlecha(SNV, valList, pathReportLog):
    IDS = valList[0]
    fInt = valList[20]
    fExt = valList[21]
    # "Ao final de cada 20 (vinte) metros devera ser incorporado ao
    # registo o valor do Afundamento da Trilha de Rodas (ATR)"
    tolerance = 20
    checkDups(SNV, fInt, tolerance, "Repetidos valores de flechaInt", pathReportLog)
    checkDups(SNV, fExt, tolerance, "Repetidos valores de flechaExt", pathReportLog)
    supLim = 40
    infLim = 0
    checkLimits(SNV, IDS, fInt, supLim, infLim, "flechaInt", pathReportLog)
    checkLimits(SNV, IDS, fExt, supLim, infLim, "flechaExt", pathReportLog)


# Check if coordinates longtitude and latitude are correct
def checkCoordinates(SNV, valList, pathReportLog):
    IDS = valList[0]
    X = valList[12]
    Y = valList[13]
    tolerance = 20
    checkDups(SNV, X, tolerance, "Repetidos valores de GPS 'X'", pathReportLog)
    checkDups(SNV, Y, tolerance, "Repetidos valores de GPS 'Y'", pathReportLog)
    checkLimits(SNV, IDS, X, -35, -74, "X - Coordenadas GPS Fora do Brasil", pathReportLog)
    checkLimits(SNV, IDS, Y, 5.3, -34, "Y - Coordenadas GPS Fora do Brasil", pathReportLog)


# Check files in ../videos/camera3 folder
# Check if the amount of photos is in accordance with the extension of Road
def checkPhotos(SNV, extension, pathReportLog):
    extension = abs(extension)
    pathImg = os.path.join(SNV, "videos", "camera3")
    images = 0
    MSG = ""
    for file in os.listdir(pathImg):
        pathI = os.path.join(pathImg, file)
        if os.path.isfile(pathI):
            if file.endswith(".png") or file.endswith(".jpeg") or file.endswith(".jpg"):
                images += 1
                # Check if image is corrupted
                if os.path.getsize(pathI) == 0:
                    updateLog(SNV, file + " na pasta camera3 esta corrompida", pathReportLog)
                file, type = os.path.splitext(file)
                try:
                    if float(file) < 0 or float(file) > (extension*1000+150):
                        MSG = MSG + str(file) + type + "; "
                except ValueError:
                    MSG = MSG + file + type + "; "
    # Print messages that are outside the Road SNV limit
    if MSG != "":
        newMSG = "Problema com formato de arquivos ou fora dos limites index na pasta camera3: " + MSG
        updateLog(SNV, newMSG, pathReportLog)
    extensionPhoto = images*5/1000
    # Print error if folder has number of photos different than the Road SNV
    if (extensionPhoto < 0.95*extension or extensionPhoto > 1.15*extension):
        MSG = "Problema relacionado ao numero de foto. Extensao no index (" + str(round(extension, 2)) + "km) =/= " + str(images) + "  x 5m (" + str(round(extensionPhoto, 2)) + "km). Fotos deveriam estar espacadas de 5-5m, e nao " + str(round(extension*1000/images, 1)) + "m"
        updateLog(SNV, MSG, pathReportLog)


# Check if velocity informations are correct
def checkVelocity(SNV, valList, pathReportLog):
    IDS = valList[0]
    vel1 = valList[3]
    vel2 = valList[9]
    tolerance = 30
    checkDups(SNV, vel1, tolerance, "Velocidade", pathReportLog)
    # Number of times that velocity appears >= 60km *(1 + 10%)
    supLim = 66
    infLim = -0.1
    checkLimits(SNV, IDS, vel1, supLim, infLim, "Velocidade", pathReportLog)
    checkLimits(SNV, IDS, vel2, supLim, infLim, "Velocidade", pathReportLog)


# Check if coordinates Altitude are correct
def checkAltitude(SNV, valList, pathReportLog):
    IDS = valList[0]
    Altitude = valList[11]
    tolerance = 100
    checkDups(SNV, Altitude, tolerance, "Altitude", pathReportLog)
    MSG = "Valor errado para altitude"
    supLim = 3000
    infLim = -50
    checkLimits(SNV, IDS, Altitude, supLim, infLim, MSG, pathReportLog)


# Check if the amount of Satalites used to collect the coordinates is OK
def checkSatelites(SNV, valList, pathReportLog):
    IDS = valList[0]
    numSatelites = valList[16]
    newArray = []
    for ii in range(len(numSatelites)):
        if numSatelites[ii] < 3:
            newArray.append(IDS[ii])
    MSG = "Numero de satelies menor < 3, verificar com atencao o GPS"
    updateReportLoop(SNV, newArray, MSG, pathReportLog)


# Check if the values of Azimute are correct
def checkAzimute(SNV, valList, pathReportLog):
    IDS = valList[0]
    Azis = valList[14]
    supLim = 360.01
    infLim = -0.1
    MSG = "Azimute"
    checkLimits(SNV, IDS, Azis, supLim, infLim, MSG, pathReportLog)


# Check the Erros Tag in XML file
def checkErros(SNV, valList, pathReportLog):
    IDS = valList[0]
    errosList = valList[15]
    supLim = 100
    infLim = -0.1
    MSG = "Tag <Erro>"
    checkLimits(SNV, IDS, errosList, supLim, infLim, MSG, pathReportLog)
