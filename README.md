# DNIT-LVC

The program presented here is a DATA verification script used to validate the files received by the National Department of Infrastructure and Transport - [DNIT](https://www.gov.br/dnit/) as part of the continuous visual monitoring of the main roads in Brazil.

The script has been used to validate more than 110000 km of filmed federal roads with appropriately equipped vehicles.

‏‏‎ ‎
## DATA

The data analyzed by the program are part of the Edital RDC Nº 0311 (2020-2024), which records the mechanical properties and captures images of the federal roads, taken annually by certified vehicles that travel the Brazilian federal highways.

For each Brazilian federal road, a folder is created containing 2 continuous video films, images of the road surface recorded at an frequency of 5 meters, the vehicle tracking system, the wheel track deflection, and the index of longitudinal irregularities. All these files are combined in an XML file that allows posterior analysis of the road surface.

‏‏‎ ‎
## PROGRAM

The program works by calling the LVCcheck.py function, providing as parameters the path of the folder containing the files, and the roads to be checked. It provides as an output, a log containing a summary of the results of all the checks performed.
The files validations are divided into 3 validations sections: `index`, `files`, and `Logs`.
* The `index` validation consists of verifying all the information in the summary file, which imports the files and folders, is correct and as specified in the Edital. It checks the addresses, the states and road names, the kilometers, and the direction, quantity, and type of the road
* The `files` evaluate whether all the files to be imported are correct and arranged in the proposed structure. It is verified if each highway has the video and photography footage, verifying that the duration of the footage is in accordance with the highway and that the number of photos is correct. It also checks if the geographic positions, log information, and all raw data are present and not corrupted.
* Checks in the `Log` validate that the data is correct. It is verified if the odometer information, speed, and date of realization in the field are correct, obeying the prepositions of the Edital. It is verified if the geographic position traveled by the vehicle corresponds to the specified correct road. It is verified if the information of Id, pavement surface, number of satellites, azimuth are consistent. It is also evaluated if the wheel track deflection and the index of longitudinal irregularities are compatible and don't present irregular values, according to practical values. This check also assesses that the values presented are not duplicated or corrupted and that all information is consistent with expected practical values.
