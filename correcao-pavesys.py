import os
import shutil

caminho_hd = "E:\\4202 R01"
caminho_rede = "\\\\10.100.10.219\\Videos$\\Recebidos\\2023\\Lote2"

dirs_dias = os.listdir(caminho_hd)

for dia in dirs_dias:
    caminho_dia = os.path.join(caminho_hd, dia)
    for trecho in os.listdir(caminho_dia):
        caminho_trecho = os.path.join(caminho_dia, trecho)
        for correcao in os.listdir(os.path.join(caminho_trecho, "videos")):
            caminho_correcao = os.path.join(caminho_rede, '4202', dia, trecho, "videos", correcao)
            if os.path.exists(caminho_correcao):
                print(caminho_correcao)
                shutil.rmtree(caminho_correcao)
