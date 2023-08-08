import src.dnit.LVCcheck as LVC

######################################################################
# Checker para verificar correcoes de um HD
#  @hd = Caminho raiz do HD
#  @trechos = Array com os trechos a serem verificados
#
# Exemplo:
#   hd = "E:\\Videos\\Recebidos\\2023\\Lote1\\4101"
#   hd = "\\\\10.100.10.219\\Videos$\\Recebidos\\2023\\Lote3\\4302"
#   trechos = [155, 156, 157, 158, 108, 109, 110]
#   trechos = []
#
# Atenção: Barras devem ser escapadas, ou seja \ -> \\
# Se quiser verificar todo o hd, coloque trechos = []
# Pra rodar aperta F5
######################################################################


hd = "F:\\Videos\\Recebidos\\2023\\Lote2\\4202"
trechos = []


LVC.check(hd, trechos)