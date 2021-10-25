import numpy as np
import pandas as pd
import scipy.stats as stats

'''ary = np.array([[6,1], [1.409100,1.523520]])
chi2_contingency(ary)

print(chi2_contingency(ary))

#15,137217'''

qui_quadrado_tabu = stats.chi2.ppf(q = 0.95, df = 80)
#p_valor = 1-stats.chi2.cdf(x=18.194805, df=4)
p_valor = 1-stats.chi2.cdf(x=38.123016, df=53)

print('Critical Value')
print(qui_quadrado_tabu)
print(p_valor)


