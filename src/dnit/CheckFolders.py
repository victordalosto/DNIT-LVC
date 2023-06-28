
import os
import glob

import pyunpack
from src.dnit.Logger import update_log


# ############################################### #
#  The structure of files in HD folder is defined as
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
def check(pathMain, listSNVs, pathReportLog):
    # pass
    pathBin = os.path.join(pathMain, "lib", "ffmpeg", "bin")
    pathScript = os.path.join(pathBin, "ffprobe.exe")
    
    os.chdir(pathBin)

    if (not os.path.isfile(pathScript)):
        pathRAR = os.path.join(pathBin, "ffprobe.rar")
        pyunpack.Archive(pathRAR).extractall(pathBin)
        os.remove(pathRAR)

    for i in range(len(listSNVs[3])):
        SNV = listSNVs[3][i]

        # Check if address path exists on HD
        if os.path.exists(SNV) is False:
            MSG = "Nao foi possivel encontrar para o trecho " + str(listSNVs[0][i]) + ", o seu caminho na pasta. "
            update_log(SNV, MSG, pathReportLog)

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
                update_log(SNV, MSG, pathReportLog)

            # Check if Videos folder exists
            if os.path.exists(pathVideo) is False:
                MSG = "Nao foi possivel encontrar a pasta videos"
                update_log(SNV, MSG, pathReportLog)
            else:

                # Check if videos/camera3 path exists
                if (os.path.exists(pathCam3) is False):
                    MSG = "Nao foi possivel encontrar a pasta camera3"
                    update_log(SNV, MSG, pathReportLog)

                # Check integrity of camera1 and camera2 in videos folder
                checkVideosIntegrity(pathCam1, "camera1", SNV, pathReportLog)
                checkVideosIntegrity(pathCam2, "camera2", SNV, pathReportLog)

            # Check if folder contains an CSV RAW input
            hasCSV = False
            pathGEO = os.path.join(SNV, "GEO")
            for root, dir, files in os.walk(pathGEO):
                for file in files:
                    if str(file).lower().endswith(".csv"):
                        hasCSV = True
                        break
            if (hasCSV is False):
                MSG = "Trecho nao tem arquivo de dados brutos em formato .CSV"
                update_log(SNV, MSG, pathReportLog)


# Check the integrity of videos .mp4 files
def checkVideosIntegrity(path, type, SNV, pathReportLog):
    # Changed to catch multiple mp4 files
    pathCam = path
    # Check if folder exist
    if os.path.exists(path) is False:
        MSG = "Nao foi possivel encontrar a pasta: " + type
        update_log(SNV, MSG, pathReportLog)
    else:
        # Check if files exists and are ok
        try:
            for file in glob.glob(os.path.join(path, "*.mp4")):
                pathCam = os.path.join(path, file)
                # Check if file is corrupted
                if os.path.getsize(pathCam) == 0:
                    MSG = "Arquivo corrompido na pasta: " + type
                    update_log(SNV, MSG, pathReportLog)
                break
        except BaseException:
            MSG = "Problema ao verificar a pasta: " + type
            update_log(SNV, MSG, pathReportLog)

        # If glob didn't catch any .mp4:
        if not pathCam.endswith("mp4"):
            MSG = "Nenhum arquivo 'mp4' encontrado na pasta: " + type
            update_log(SNV, MSG, pathReportLog)
