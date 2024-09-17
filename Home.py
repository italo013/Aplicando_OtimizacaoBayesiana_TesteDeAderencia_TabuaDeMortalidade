import pandas as pd
import streamlit as st
from lib.text import demonstracao_agravo, chi_square_text, ks_test_text


df_tabuas = pd.read_excel('Funções Biométricas (Com Fórmulas).xlsx', sheet_name='qx')
df = pd.read_csv('modelo_csv.csv', sep=';')

st.set_page_config(page_title="Home", page_icon="📊")

def main():
    st.title('Aplicando Otimização Bayesiana para aprimorar o Teste de Aderência das Tábuas de Mortalidade')

    st.markdown(
    """
    O objetivo principal deste projeto é empregar a [**Otimização Bayesiana**](https://github.com/bayesian-optimization/BayesianOptimization) para aprimorar o teste de aderência das tábuas de mortalidade. Para isso, ajustes de agravo e suavização, bem como deslocamentos, são aplicados às tábuas de mortalidade para encontrar a configuração que oferece a melhor aderência, ou seja, que não rejeita Hipótese Nula (H₀). 

    - **Hipótese Nula (H₀):** As frequências observadas seguem a distribuição esperada. Em outras palavras, **não há diferença significativa** entre as frequências observadas e as esperadas.

    - **Hipótese Alternativa (H₁):** As frequências observadas **não seguem** a distribuição esperada. Em outras palavras, **há uma diferença significativa** entre as frequências observadas e as esperadas.
    
    O agravo aumenta as taxas de mortalidade, enquanto a suavização as diminui. O deslocamento, por outro lado, atrasa as taxas de mortalidade.

    **DEMONSTRAÇÃO DO AGRAVO/SUAVIZAÇÃO E DESLOCAMENTO:**
    """
    )

    demonstracao_agravo(df_tabuas=df_tabuas)

    st.markdown(
    """    
    Os métodos de avaliação primários utilizados para medir a aderência são o [**Teste Qui-Quadrado (Chi-Square)**](https://www.ibm.com/docs/pt-br/spss-statistics/29.0.0?topic=statistics-tests-independence-chi-square) e o [**Teste de Kolmogorov-Smirnov (KS)**](https://www.ibm.com/docs/pt-br/spss-statistics/29.0.0?topic=tests-one-sample-kolmogorov-smirnov-test).
    """
    )

    with st.expander("Teste Qui-Quadrado (Chi-Square)"):
        chi_square_text()

    with st.expander("Teste de Kolmogorov-Smirnov (KS)"):
        ks_test_text()

if __name__ == '__main__':
    main()