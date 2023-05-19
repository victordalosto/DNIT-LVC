import os
from datetime import datetime
from src.dnit.Utils import is_valid

# Create a report log.txt file with all checking done on files
def create_report_log(path_logs):
    log_file = "LOG-" + datetime.now().strftime("%Y_%m_%d___%Hh_%Mm") + ".txt"
    path_report_log = os.path.join(path_logs, log_file)
    if os.path.isfile(path_report_log) is False:
        Log = open(path_report_log, "w")
    else:
        Log = open(path_report_log, "r+")
        Log.truncate(0)
    header = "Log: " + datetime.now().strftime("%d/%m/%Y - %H:%M:%S\n\n")
    Log.writelines(header)
    Log.close()
    return path_report_log

# Function that updates the Log with a new status
def update_log(header, message, path_logger):
    if (is_valid(message)):
        message = "  * " + message
        header = header.replace("/", "\\") # Fix the notation to windows path
        list_lines = (open(path_logger, "r")).readlines()
        try:
            line = list_lines.index(header+"\n")
            list_lines.insert(line+1, message+"\n")
        except ValueError:
            list_lines.append(header+"\n")
            list_lines.append(message+"\n\n")
        Log = open(path_logger, "w")
        Log.writelines(list_lines)
        Log.close()