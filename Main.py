import src.dnit.LVCcheck as LVC

# Checker para verificar correcoes de um HD
# @hd = Caminho raiz do HD
# @trechos = Array com os trechos a serem verificados
# Lembrar que o caminho das pastas deve conter barras escapadas \ -> \\
# Exemplo:
#   hd = "E:\\Videos\\Recebidos\\2023\\Lote1\\4101"
#   trechos = [155, 156, 157, 158, 108, 109, 110]

hd = "E:\\Videos\\Recebidos\\2023\\Lote1\\4101"
trechos = [155, 156, 157, 158, 108, 109, 110]


LVC.check(hd, trechos)