import pandas as pd
import streamlit as st

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
    fator_agravo = st.sidebar.slider("Selecione o Range do Agravo e Desagravo (%)", -100.00, 100.00, (-10.0, 10.0), help="Agravo e desagravo são ajustes aplicados à tábua de mortalidade. O agravo aumenta as taxas de mortalidade e é representado por valores positivos neste controle deslizante. O desagravo, por outro lado, diminui as taxas de mortalidade e é representado por valores negativos. Defina o intervalo de agravo selecionando valores positivos e o intervalo de desagravo selecionando valores negativos.")
    st.sidebar.slider("Selecione o Range do Deslocamento", -100.00, 100.00, (-5.0, 5.0), help="O deslocamento é um ajuste aplicado à tábua de mortalidade que atrasa as taxas de mortalidade. Isso é representado por valores positivos neste controle deslizante. Defina o intervalo de deslocamento selecionando valores dentro do range.")
    st.sidebar.multiselect("Selecione as Tábuas", df_tabuas.columns.tolist(), help="Selecione as Tábuas de Mortalidade que você deseja testar.")

def main(df=None):
    st.title('Teste de Aderência de Tábuas de Mortalidade')
    st.subheader('by Italo Igor [LinkedIn](https://www.linkedin.com/in/italo013/)')

    st.markdown(
    """
    O objetivo principal deste projeto é empregar a [**Otimização Bayesiana**](https://github.com/bayesian-optimization/BayesianOptimization) para aprimorar o teste de aderência das tábuas de mortalidade. Para isso, ajustes de agravo e desagravo, bem como deslocamentos, são aplicados às tábuas de mortalidade para encontrar a configuração que oferece a melhor aderência. 
    
    O agravo aumenta as taxas de mortalidade, enquanto o desagravo as diminui. O deslocamento, por outro lado, atrasa as taxas de mortalidade. 
    
    Os métodos de avaliação primários utilizados para medir a aderência são o [**Teste Qui-Quadrado (Chi-Square)**](https://www.ibm.com/docs/pt-br/spss-statistics/29.0.0?topic=statistics-tests-independence-chi-square) e o [**Teste de Kolmogorov-Smirnov (KS)**](https://www.ibm.com/docs/pt-br/spss-statistics/29.0.0?topic=tests-one-sample-kolmogorov-smirnov-test).
    """
    )

    side_bar()

if __name__ == '__main__':
    main()