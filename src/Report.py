
import os
from datetime import datetime

from src.Utils import isValid


# Create a report log.txt file with all checking done on files
def CreateReportLog(pathMain):
    # Create a log file named as the current date in the Folder ../Main/lib/
    # File named as LOG_dd_mm_yyyy_hh_mm_ss
    TEXT = "LOG_" + datetime.now().strftime("%Y_%m_%d_%Hh_%Mm_%Ss") + ".txt"
    pathReportLog = os.path.join(pathMain, "Logs", TEXT)
    if os.path.isfile(pathReportLog) is False:
        # Create a LOG.txt
        Log = open(pathReportLog, "w")
    else:
        # Clean LOG.txt
        Log = open(pathReportLog, "r+")
        Log.truncate(0)
    # Add header in Log with dates time of verification (same as files name)
    MSG = "Log: " + datetime.now().strftime("%d/%m/%Y - %H:%M:%S\n\n")
    Log.writelines(MSG)
    Log.close()
    return pathReportLog


# Function that updates the Log with a new status
def updateLog(header, MSG, pathReportLog):
    # Add identation to the MSG text
    if (isValid(MSG)):
        MSG = "  * " + MSG
    # Fix the notation if file come as: //10.100.10.219\2102\videos
    header = header.replace("/", "\\")
    # Get all the text already in the Log file
    listLines = (open(pathReportLog, "r")).readlines()
    try:
        # Create a line for the road Name if it doesn't exist
        line = listLines.index(header+"\n")
        listLines.insert(line+1, MSG+"\n")
    except ValueError:
        # Road Line SNV already exists. Append new update in it
        listLines.append(header+"\n")
        listLines.append(MSG+"\n\n")
    # Append new Text to the Log.txt
    Log = open(pathReportLog, "w")
    Log.writelines(listLines)
    Log.close()
