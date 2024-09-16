import numpy as np

def aplicar_fator_desloc(tabua, fator, desloc):
    tabua_ajustada = tabua * (1 + (fator / 100))
    tabua_ajustada = np.roll(tabua_ajustada, int(desloc))
    tabua_ajustada[tabua_ajustada > 1] = 1
    tabua_ajustada[tabua_ajustada < 0] = 0
    return tabua_ajustada