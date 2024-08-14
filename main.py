import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import scipy.stats as stats

df_tabuas = pd.read_excel('Funções Biométricas (Com Fórmulas).xlsx', sheet_name='qx')

def side_bar():
    st.sidebar.markdown('# Escolha os Parâmetros')
    st.sidebar.markdown("## Download do Modelo de csv")
    if st.sidebar.button('Download'):
        resultados.to_csv('resultados.csv')
        st.sidebar.markdown("Resultados exportados com sucesso!")

    st.sidebar.markdown("## Importar Frequência de Expostos")
    uploaded_file = st.sidebar.file_uploader("Escolha um arquivo CSV", type="csv", help="O arquivo csv deverá ter apenas 1 coluna")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.sidebar.markdown("Arquivo CSV carregado com sucesso!")

    st.sidebar.markdown("## Configuração dos Parâmetros")
    fator_agravo = st.sidebar.slider("Selecione o Range do Agravo e Suavização (%)", -100.00, 100.00, (-10.0, 10.0), help="Agravo e suavização são ajustes aplicados à tábua de mortalidade. O agravo aumenta as taxas de mortalidade e é representado por valores positivos neste controle deslizante. A suavização, por outro lado, diminui as taxas de mortalidade e é representado por valores negativos. Defina o intervalo de agravo selecionando valores positivos e o intervalo de suavização selecionando valores negativos.")
    st.sidebar.slider("Selecione o Range do Deslocamento", -100.00, 100.00, (-5.0, 5.0), help="O deslocamento é um ajuste aplicado à tábua de mortalidade que atrasa as taxas de mortalidade. Isso é representado por valores positivos neste controle deslizante. Defina o intervalo de deslocamento selecionando valores dentro do range.")
    st.sidebar.multiselect("Selecione as Tábuas", df_tabuas.columns.tolist(), help="Selecione as Tábuas de Mortalidade que você deseja testar.")
    chi_square_value = st.sidebar.slider("Selecione o valor do Qui-Quadrado", 0.00, 100.00, (0.0, 10.0), help="O valor do Qui-Quadrado é usado para testar a aderência das tábuas de mortalidade. Ajuste o valor usando este controle deslizante.")

def main(df=None):
    st.title('Teste de Aderência de Tábuas das Mortalidade')
    st.subheader('by Italo Igor [LinkedIn](https://www.linkedin.com/in/italo013/)')

    st.markdown(
    """
    O objetivo principal deste projeto é empregar a [**Otimização Bayesiana**](https://github.com/bayesian-optimization/BayesianOptimization) para aprimorar o teste de aderência das tábuas de mortalidade. Para isso, ajustes de agravo e suavização, bem como deslocamentos, são aplicados às tábuas de mortalidade para encontrar a configuração que oferece a melhor aderência. 

    O agravo aumenta as taxas de mortalidade, enquanto a suavização as diminui. O deslocamento, por outro lado, atrasa as taxas de mortalidade.

    **DEMONSTRAÇÃO:**
    """
    )

    def aplicar_fator_desloc(tabua, fator, desloc):
        tabua_ajustada = tabua * (1+(fator/100))
        tabua_ajustada = np.roll(tabua_ajustada, int(desloc))
        return tabua_ajustada

    select_tb_mortabilidade_test = st.multiselect("Selecione uma Tábua de Mortalidade", df_tabuas.columns.tolist(), help="Selecione as Tábuas de Mortalidade que você deseja testar.")
    fator_agravo_test = st.slider("Selecione o Agravo ou Suavização", -100.00, 100.00, 0.0, help="Agravo e suavização são ajustes aplicados à tábua de mortalidade. O agravo aumenta as taxas de mortalidade e é representado por valores positivos neste controle deslizante. A suavização, por outro lado, diminui as taxas de mortalidade e é representado por valores negativos. Defina o intervalo de agravo selecionando valores positivos e o intervalo de suavização selecionando valores negativos.")
    desloc_test = st.slider("Selecione o Deslocame", -100.00, 100.00, 0.0, help="O deslocamento é um ajuste aplicado à tábua de mortalidade que atrasa as taxas de mortalidade. Isso é representado por valores positivos neste controle deslizante. Defina o intervalo de deslocamento selecionando valores dentro do range.")    

    for tabua in select_tb_mortabilidade_test:
        df_tabuas[tabua + '_ajustada'] = aplicar_fator_desloc(df_tabuas[tabua], fator_agravo_test, desloc_test)

    fig = px.line(df_tabuas, 
                  x=df_tabuas.index, 
                  y=select_tb_mortabilidade_test + [tabua + '_ajustada' for tabua in select_tb_mortabilidade_test],
                  labels={'index': 'Idade', 'value': 'qx'},
                  )
    st.plotly_chart(fig)

    st.markdown(
    """    
    Os métodos de avaliação primários utilizados para medir a aderência são o [**Teste Qui-Quadrado (Chi-Square)**](https://www.ibm.com/docs/pt-br/spss-statistics/29.0.0?topic=statistics-tests-independence-chi-square) e o [**Teste de Kolmogorov-Smirnov (KS)**](https://www.ibm.com/docs/pt-br/spss-statistics/29.0.0?topic=tests-one-sample-kolmogorov-smirnov-test).
    """
    )

    side_bar()

    st.subheader('Teste Qui-Quadrado (Chi-Square)')

    st.latex(r'''
    \chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}
    ''')

    st.markdown("""
    A fórmula acima representa o cálculo do teste Qui-Quadrado (Chi-Square). As variáveis na fórmula são:

    - **χ²**: É o valor do Qui-Quadrado. É uma medida estatística que nos diz o quão bem nossas observações se encaixam com os resultados esperados.
    - **Oi**: São as observações ou valores reais que temos em nossa amostra.
    - **Ei**: São os valores esperados ou teóricos que esperamos obter.

    A fórmula calcula a soma das diferenças quadradas entre as observações (Oi) e os valores esperados (Ei), dividida pelo valor esperado (Ei), para todas as observações em nossa amostra.
    """)

    st.subheader('Teste de Kolmogorov-Smirnov (KS)')

    st.latex(r'''
    D_n = \sup_x |F_n(x) - F(x)|
    ''')

    st.markdown("""
    A fórmula acima representa o cálculo do teste de Kolmogorov-Smirnov (KS). As variáveis na fórmula são:

    - **Dn**: É o valor do teste KS. É uma medida estatística que nos diz o quão bem nossas observações se encaixam com os resultados esperados.
    - **Fn(x)**: É a função de distribuição empírica (FDE) que é calculada a partir dos dados da amostra.
    - **F(x)**: É a função de distribuição acumulada (FDA) da população.

    A fórmula calcula o supremo (maior valor) da diferença absoluta entre a FDE e a FDA para todas as observações em nossa amostra.
    """)

    st.subheader('Playground')
    
    # Criação da expressão LaTeX com parâmetros dinâmicos
    Oi = st.sidebar.slider("Selecione o valor de Oi", 0, 100, 5)
    Ei = st.sidebar.slider("Selecione o valor de Ei", 1, 100, 10)
    latex_expression_chi2 = f"\\chi^2 = \\sum \\frac{{({Oi} - {Ei})^2}}{{{Ei}}}"

    # Renderização da expressão LaTeX
    st.latex(latex_expression_chi2)
    


if __name__ == '__main__':
    main()