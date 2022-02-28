# DNIT-LVC

The program presented here is a DATA verification script used to validate the files received by the National Department of Infrastructure and Transport - [DNIT](https://www.gov.br/dnit/) as part of the continuous visual monitoring of the main roads in Brazil.

The script has been used to validate more than 110000 km of filmed federal roads with appropriately equipped vehicles.

‏‏‎ ‎
## DATA

The data analyzed by the program are part of the Edital RDC Nº 0311 (2020-2024), which records the mechanical properties and captures images of the federal roads, taken annually by certified vehicles that travel the Brazilian federal highways.

For each Brazilian federal road, a folder is created containing 2 continuous video films, images of the road surface recorded at an frequency of 5 meters, the vehicle tracking system, the wheel track deflection, and the index of longitudinal irregularities. All these files are combined in an XML file that allows posterior analysis of the road surface.

‏‏‎ ‎
## PROGRAM

The program works by calling the LVCcheck.py function, providing as parameters, the path of the folder containing the files, and the roads to be checked. It provides as an output, a log containing a summary of the results of all the checks performed.
The validations are divided into 3 sections: `Index`, `files`, and `Logs`.
* The `Index` validation consists in checking that all the information in the summary file that imports the files and folders is correct and corresponds to the information in the Edital. It checks the addresses, the states and road names, the kilometers, the direction, the quantity, and the type of the road.
* The `files` evaluate whether all the files to be imported are correct and arranged in the proposed structure. It verifies that each highway has video and photographic material. It ensures that the duration of the footage matches the highway and that the number of photos is correct. It also checks that the geographic positions, log information, and all raw data are present and not corrupted.
* Checks in the `Log` cofirm that the data is correct. Checks are made that the odometer, speed, and date of realization in the field are correct, and that the prepositions of the editorial have been observed. It is checked if the geographical position through which the vehicle passed corresponds to the indicated road. It is checked if the Id, road surface, number of satellites and azimuth information match. It is also checked if the wheel track deflection and longitudinal irregularity index are compatible and do not have irregular values, according to the practical values. It is also checked that the presented values are not duplicated or distorted and that all the information is consistent with the expected practical values.
