
import os
import glob
from src.reportLog import updateLog


# ############################################### #
#  The structure of files in folder is defined as
#   XXXX (HDs NAME)
#       - XX_XX_XXXX (DATE OF SURVEY)
#           - XXX_YYYYYYYYYY (NUM_ROADSNV)
#               - GEO (Folder)
#                       *.csv (file)
#               - LogsTrecho.xml
#               - VIDEOS (Folder)
#                   - Camera1 (Folder)
#                       *.mp4 (File)
#                   - Camera2 (Folder)
#                       *.mp4 (File)
#                   - Camera3 (Folder)
#                       *.mp4 (File)
# ############################################### #

# Function that checks the integrity of files in HD
def checkFolders(listSNVs, pathReportLog):
    for i in range(len(listSNVs[3])):
        SNV = listSNVs[3][i]

        # Check if address path exists on HD
        if os.path.exists(SNV) is False:
            MSG = "Nao foi possivel encontrar para o trecho "
            MSG += str(listSNVs[0][i]) + ", "
            MSG += "o seu caminho na pasta. "
            updateLog(SNV, MSG, pathReportLog)

        else:
            # Defines the paths of the files to be checked
            pathLog = os.path.join(SNV, "LogsTrecho.xml")
            pathVideo = os.path.join(SNV, "videos")
            pathCam1 = os.path.join(pathVideo, "camera1")
            pathCam2 = os.path.join(pathVideo, "camera2")
            pathCam3 = os.path.join(pathVideo, "camera3")

            # Check if LogsTrecho.xml exists
            if os.path.exists(pathLog) is False:
                MSG = "Nao foi possivel encontrar o arquivo LogsTrecho.xml"
                updateLog(SNV, MSG, pathReportLog)

            # Check if Videos folder exists
            if os.path.exists(pathVideo) is False:
                MSG = "Nao foi possivel encontrar a pasta videos"
                updateLog(SNV, MSG, pathReportLog)
            else:

                # Check if videos/camera3 path exists
                if (os.path.exists(pathCam3) is False):
                    MSG = "Nao foi possivel encontrar a pasta camera3"
                    updateLog(SNV, MSG, pathReportLog)

                # Check integrity of camera1 and camera2 in videos folder
                checkVideosIntegrity(pathCam1, "camera1", SNV, pathReportLog)
                checkVideosIntegrity(pathCam2, "camera2", SNV, pathReportLog)

            # Check if folder contains an CSV RAW input
            hasCSV = False
            pathGEO = os.path.join(SNV, "GEO")
            for root, dir, files in os.walk(pathGEO):
                for file in files:
                    if file.endswith(".csv"):
                        hasCSV = True
            if (hasCSV is False):
                MSG = "Trecho nao tem arquivo de dados brutos em formato .CSV"
                updateLog(SNV, MSG, pathReportLog)


# Check the integrity of videos .mp4 files
def checkVideosIntegrity(path, type, SNV, pathReportLog):
    # Changed to catch multiple mp4 files
    pathCam = path
    # Check if folder exist
    if os.path.exists(path) is False:
        MSG = "Nao foi possivel encontrar a pasta: " + type
        updateLog(SNV, MSG, pathReportLog)
    else:
        # Check if files exists and are ok
        try:
            for file in glob.glob(os.path.join(path, "*.mp4")):
                pathCam = os.path.join(path, file)
                # Check if file is corrupted
                if os.path.getsize(pathCam) == 0:
                    MSG = "Arquivo corrompido na pasta: " + type
                    updateLog(SNV, MSG, pathReportLog)
        except BaseException:
            MSG = "Problema ao verificar a pasta: " + type
            updateLog(SNV, MSG, pathReportLog)

        # If glob didn't catch any .mp4:
        if not pathCam.endswith("mp4"):
            MSG = "Nenhum arquivo 'mp4' encontrado na pasta: " + type
            updateLog(SNV, MSG, pathReportLog)
