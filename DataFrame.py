import pandas as pd
import numpy as np

lstNome = np.array(['Italo', 'Igor', 'Gomes'])
lstIdade = np.array([18,30,31])

print(lstNome)
print(lstIdade)

df = pd.DataFrame(data={'Nomes':lstNome, 'Idades':lstIdade})
print(df)

lstDados = [['Italo', 21], ['Igor', 30], ['Gomes', 35]]
lstTabua = ['ALSS-72', 'IBGE 2019']
#df2 = pd.DataFrame(columns=['Nomes', 'Idade'], data=lstDados)
df2 = pd.DataFrame(columns=lstTabua, data=lstDados)
print(df2)
