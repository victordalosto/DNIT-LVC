
# Print the percentage of validation done in Prompt
def printPercentage(SNVsName, percentage):
    SNVsName = str(SNVsName)
    percentage = str(percentage)
    MSG = "Trecho " + SNVsName + " - " + percentage + "%"
    print(MSG)


# Check if parameter is valid
def isValid(string):
    if (string is not None) and (string != "") and (string != " "):
        return True
    else:
        return False


def isNotValid(string):
    return not (isValid(string))
