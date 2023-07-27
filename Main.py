import src.dnit.LVCcheck as LVC

hd = "\\\\10.100.10.219\\Videos$\\Recebidos\\2023\\Lote1\\4101"
trechos = [161, 50, 101, 100, 98, 97, 188]

LVC.check(hd, trechos)