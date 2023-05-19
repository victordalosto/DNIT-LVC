
# Print the percentage of validation done in Prompt
def print_percentage(SNVsName, percentage):
    SNVsName = str(SNVsName)
    percentage = str(percentage)
    MSG = "Trecho " + SNVsName + " - " + percentage + "%"
    print(MSG)


# Check if parameter is valid
def is_valid(string):
    if (string is not None) and (string != "") and (string != " "):
        return True
    return False


def is_not_valid(string):
    return not (is_valid(string))


def get_UFs():
    return ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
