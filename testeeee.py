import pandas as pd
import os
import teste_aderencia
import numpy as ny
import matplot
import scipy.stats as stats

path = os.getcwd()
print(path + '/5.SERV_FALEC_EXON.csv')

#######################################################IMPORTAÇÕES#######################################################
#Importando o csv 5.SERV_FALEC_EXON
df_full = pd.read_csv(path + '/5.SERV_FALEC_EXON.csv',
                        usecols=['NU_ANO',
                                'CO_SEXO_SERVIDOR',
                                'DT_NASC_SERVIDOR',
                                'CO_SITUACAO',
                                'DT_SITUACAO',
                                'CO_TIPO_VINCULO'], encoding='UTF-8', sep=';').assign(IDADE = '')

#Importando o csv com as tábuas
df_tabuas = pd.read_csv(path + '/df_tabuas_biometricas.csv', sep=';')


########################################################CÁLCULOS########################################################
#Calculando as IDADES dentro do df_full
for c in range(0, len(df_full)):
    df_full.loc[c, 'IDADE'] = 2020 - int(df_full.loc[c, 'DT_NASC_SERVIDOR'][-4:])

#Criando uma matriz com a quantidade de registros de cada IDADE
ary_expostos = []
for l in range(126+1):
    linha = []
    for c in range(1):
        qtda = len(df_full[df_full['IDADE'] == l])
        linha.append(qtda)
    ary_expostos.append(linha)

df_expostos = pd.DataFrame(data=ary_expostos)

#Criando uma matriz com o número de MORTES esperadas por idade e o X² calculado
ary_esperados = []
for l2 in range(126+1):
    linha2 = []
    for c2 in range(107):
        esperado = ary_expostos[l2][0] * df_tabuas.iloc[l2, c2]
        linha2.append(esperado)
    ary_esperados.append(linha2)

df_esperados = pd.DataFrame(data=ary_esperados, columns=df_tabuas.columns.values)
df_esperados.loc['Total'] = df_esperados.sum(axis=0)

#Cálculo do X²
ary_qui_quadrado = []
for l3 in range(126+1):
    linha3 = []
    for c3 in range(106+1):
        if df_esperados.iloc[l3, c3] == 0.0:
            qui_quadrado = 0
            linha3.append(qui_quadrado)
        elif df_esperados.iloc[l3, c3] != 0.0:
            qui_quadrado = (ary_expostos[l3][0] - df_esperados.iloc[l3, c3])**2/df_esperados.iloc[l3, c3]
            linha3.append(qui_quadrado)
    ary_qui_quadrado.append(linha3)

df_qui_quadrado = pd.DataFrame(data=ary_qui_quadrado, columns=df_tabuas.columns.values)
df_qui_quadrado.loc['qui_quadrado'] = df_qui_quadrado.sum(axis=0)
df_qui_quadrado.loc['p_value'] = 1-stats.chi2.cdf(x=df_qui_quadrado.loc['qui_quadrado'], df=53)

#df_qui_quadrado.sort_values(['Total'], axis=1, inplace=True)

qui_quadrado_tabu = stats.chi2.ppf(q=0.95, df=53)

print(df_qui_quadrado)
print(f'X² Tabelado: {qui_quadrado_tabu:.4f}')
'''print(type(float(ary_expostos[22][0])))
print(df_esperados.iloc[0, 86])
print(type(df_esperados.iloc[0, 0]))
#print((ary_expostos[20][0] - df_esperados.iloc[20, 0])**2/df_esperados.iloc[20, 0])
print(type((ary_expostos[22][0] - df_esperados.iloc[22, 0])**2/df_esperados.iloc[22, 0]))

#df_esperados.to_csv('Dados dos Esperados')
print(df_qui_quadrado)
print(type(df_qui_quadrado))
'''
#df_qui_quadrado.to_csv('Dados dos Qui-Quadrado.csv', encoding='UTF-8')#
#df_expostos.to_csv('Data Frame dos Expostos.csv', encoding='UTF-8')