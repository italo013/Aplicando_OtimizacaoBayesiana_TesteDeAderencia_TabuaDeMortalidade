import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from lib.utils import aplicar_fator_desloc

def demonstracao_agravo(df_tabuas):
    select_tb_mortabilidade_test = st.multiselect(
        "Selecione uma Tábua de Mortalidade",
        df_tabuas.columns.tolist(),
        help="Selecione as Tábuas de Mortalidade que você deseja testar.",
    )
    fator_agravo_test = st.slider(
        "Selecione o Agravo ou Suavização",
        -100.00,
        100.00,
        0.0,
        help="Agravo e suavização são ajustes aplicados à tábua de mortalidade. O agravo aumenta as taxas de mortalidade e é representado por valores positivos neste controle deslizante. A suavização, por outro lado, diminui as taxas de mortalidade e é representado por valores negativos. Defina o intervalo de agravo selecionando valores positivos e o intervalo de suavização selecionando valores negativos.",
    )
    desloc_test = st.slider(
        "Selecione o Deslocamento",
        -100.00,
        100.00,
        0.0,
        help="O deslocamento é um ajuste aplicado à tábua de mortalidade que atrasa as taxas de mortalidade. Isso é representado por valores positivos neste controle deslizante. Defina o intervalo de deslocamento selecionando valores dentro do range.",
    )

    for tabua in select_tb_mortabilidade_test:
        df_tabuas[tabua + "_ajustada"] = aplicar_fator_desloc(
            df_tabuas[tabua], fator_agravo_test, desloc_test
        )

    fig = px.line(
        df_tabuas,
        x=df_tabuas.index,
        y=select_tb_mortabilidade_test
        + [tabua + "_ajustada" for tabua in select_tb_mortabilidade_test],
        labels={"index": "Idade", "value": "qx"},
    )
    st.plotly_chart(fig)


def chi_square_text():
    st.subheader("Teste Qui-Quadrado (Chi-Square)")

    st.markdown(
        """
        #### **O que é** 
        O Qui-Quadrado (**χ²**) é uma métrica estatística usada para comparar frequências observadas com frequências esperadas em categorias, ajudando a testar hipóteses sobre distribuições e independência entre variáveis categóricas.

        #### **Por que utilizar** 
        Utiliza-se o Qui-Quadrado para verificar se existe uma diferença significativa entre o que foi observado e o que era esperado sob uma determinada hipótese, ou para testar se duas variáveis categóricas são independentes.

        #### **Formulação**
    
    """
    )

    st.latex(
        r"""
    \chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}
    """
    )

    st.markdown("""
        A fórmula acima representa o cálculo do teste Qui-Quadrado (Chi-Square). As variáveis na fórmula são:

        - **χ²**: É o valor do Qui-Quadrado. É uma medida estatística que nos diz o quão bem nossas observações se encaixam com os resultados esperados.
        - **Oi**: São as observações ou valores reais que temos em nossa amostra.
        - **Ei**: São os valores esperados ou teóricos que esperamos obter.

        #### **Como interpretar os resultados**
        - **Valor de (**χ²**) baixo:** Pequena diferença entre observado e esperado, indicando um bom ajuste ou independência.
        - **Valor de (**χ²**) alto:** Grande diferença entre observado e esperado, sugerindo mau ajuste ou associação entre variáveis.

        #### **Hipóteses**
        - **H₀ (Hipótese Nula):** As frequências observadas seguem as frequências esperadas (no teste de aderência) ou as variáveis são independentes (no teste de independência).
        - **H₁ (Hipótese Alternativa):** As frequências observadas não seguem as esperadas ou as variáveis não são independentes.

        #### **Comparação com o valor crítico e p-value**
        - **Valor crítico:** Se (**χ²**) calculado > valor crítico, rejeitamos H₀; caso contrário, não rejeitamos H₀.
        - **p-value:** Se p-value < (**α**) (nível de significância, geralmente 0,05), rejeitamos H₀; se p-value ≥ (**α**), não rejeitamos H₀.

        O Qui-Quadrado é uma ferramenta simples e poderosa para testar associações e a adequação de distribuições em dados categóricos.
    """
    )


def ks_test_text():
    st.subheader("Teste de Kolmogorov-Smirnov (KS)")

    st.markdown(
        """
        #### **O que é** 
        O teste de Kolmogorov-Smirnov (**KS**) é uma métrica estatística utilizada para comparar a distribuição de uma amostra com uma distribuição de referência ou para comparar as distribuições de duas amostras. Ele verifica se existe uma diferença significativa entre a distribuição observada e a distribuição teórica.

        #### **Por que utilizar** 
        Utiliza-se o teste KS para verificar se uma amostra segue uma distribuição teórica específica (por exemplo, normal, uniforme) ou para comparar duas amostras para avaliar se elas vêm da mesma distribuição. É especialmente útil para dados contínuos.

        #### **Formulação**
    
    """
    )

    st.latex(
        r"""
    D = \sup |F_n(x) - F(x)|
    """
    )

    st.markdown("""
        A fórmula acima representa o cálculo do teste de Kolmogorov-Smirnov (KS). As variáveis na fórmula são:

        - **D**: É a estatística do teste KS. Representa a maior diferença absoluta entre as funções de distribuição cumulativa (CDF) da amostra e da distribuição teórica (ou entre as CDFs de duas amostras).
        - **F_n(x)**: É a função de distribuição cumulativa empírica da amostra.
        - **F(x)**: É a função de distribuição cumulativa teórica (ou a CDF da segunda amostra no caso de comparação entre duas amostras).

        #### **Como interpretar os resultados**
        - **Valor de D baixo:** Pequena diferença entre as distribuições comparadas, sugerindo que a amostra segue a distribuição teórica (ou que as duas amostras têm distribuições similares).
        - **Valor de D alto:** Grande diferença entre as distribuições, indicando que a amostra não segue a distribuição teórica (ou que as duas amostras têm distribuições diferentes).

        #### **Hipóteses**
        - **H₀ (Hipótese Nula):** A amostra segue a distribuição teórica especificada (ou as duas amostras seguem a mesma distribuição).
        - **H₁ (Hipótese Alternativa):** A amostra não segue a distribuição teórica especificada (ou as duas amostras seguem distribuições diferentes).

        #### **Comparação com o valor crítico e p-value**
        - **Valor crítico:** Se **D** calculado > valor crítico, rejeitamos H₀; caso contrário, não rejeitamos H₀.
        - **p-value:** Se p-value < **α** (nível de significância, geralmente 0,05), rejeitamos H₀; se p-value ≥ **α**, não rejeitamos H₀.

        O teste de Kolmogorov-Smirnov é uma ferramenta robusta para avaliar a aderência de uma amostra a uma distribuição teórica ou para comparar distribuições de duas amostras.
    """
    )


def download_import():
    st.sidebar.subheader("Download do Modelo do csv")
    with open('modelo_csv.csv', 'r') as file:
        file_data = file.read()
    st.sidebar.download_button('Download CSV', file_data, 'modelo_csv.csv', 'text/csv')

    st.sidebar.subheader("Importar Dados")
    uploaded_file = st.sidebar.file_uploader("Selecione um arquivo CSV. Se nenhum arquivo for importado, a aplicação usará o dado padrão.", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.markdown("Arquivo CSV carregado com sucesso!")
