import streamlit as st
import pandas as pd
import numpy as np
from skopt.space import Integer
import plotly.express as px
from lib.otimizacao import OtimizacaoBayesiana

st.set_page_config(page_title="Otimização Bayesiana", page_icon="🤖")

def reset_variables():
    if 'resultados_otimizacao' in st.session_state:
        del st.session_state.resultados_otimizacao

def main():
    st.title('Aplicando a Otimização Bayesiana')

    df_tabuas = pd.read_excel('Funções Biométricas (Com Fórmulas).xlsx', sheet_name='qx')
    modelo_csv = pd.read_csv('modelo_csv.csv', sep=';')
    
    st.sidebar.subheader("Download do Modelo do csv")
    csv = modelo_csv.to_csv(index=False, sep=';').encode('utf-8')
    st.sidebar.download_button(
        label="Download modelo CSV",
        data=csv,
        file_name="modelo_csv.csv",
        mime="text/csv",
    )

    st.sidebar.subheader("Importar Dados")
    uploaded_file = st.sidebar.file_uploader("Caso não faça upload do seu arquivo CSV a aplicação usará o modelo padrão", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep=';')
        st.sidebar.markdown("Arquivo CSV carregado com sucesso!")
    else:
        df = modelo_csv

    ob = OtimizacaoBayesiana(f_obs=np.array(df['qtda_morte']), f_vivos=np.array(df['qtda_vivo'].values), tabuas=df_tabuas)

    st.markdown("#### Configuração das tábuas:")
    col1, col2 = st.columns(2)
    
    with col1:
        fator_agravo = st.slider("Selecione o Range do Agravo e Suavização (%)", -100.00, 100.00, (-10.0, 10.0), help="Agravo e suavização são ajustes aplicados à tábua de mortalidade. O agravo aumenta as taxas de mortalidade e é representado por valores positivos neste controle deslizante. A suavização, por outro lado, diminui as taxas de mortalidade e é representado por valores negativos. Defina o intervalo de agravo selecionando valores positivos e o intervalo de suavização selecionando valores negativos.")
    
    with col2:
        delay = st.slider("Selecione o Range do Deslocamento", -100.00, 100.00, (-5.0, 5.0), help="O deslocamento é um ajuste aplicado à tábua de mortalidade que atrasa as taxas de mortalidade. Isso é representado por valores positivos neste controle deslizante. Defina o intervalo de deslocamento selecionando valores dentro do range.")

    st.markdown("#### Configuração da Otimização Bayesiana:")
    col1, col2, col3 = st.columns(3)
 
    with col1:
        n_calls = st.slider("n_calls", 1, 200, 20, help="Número total de chamadas à função objetivo. Inclui n_random_starts e n_initial_points.")

    with col2:
        random_state = st.slider("random_state", 1, 200, 32, help="Semente aleatória para garantir a reprodutibilidade dos resultados da otimização.")

    with col3:
        n_initial_points = st.slider("n_initial_points", 1, 200, 10, help="Número de pontos iniciais que a otimização deve começar.")

    if st.button('Iniciar Otimização', type='primary', on_click=reset_variables):
        with st.spinner('Aguarde enquanto a otimização é realizada...'):
            st.markdown("### Resultado Final da Otimização Bayesiana")
            
            resultado_placeholder = st.empty()
            
            if 'resultados_otimizacao' not in st.session_state:
                st.session_state.resultados_otimizacao = []
                
            resultado_otimizacao = ob.aplicar_otimizacao(
                espaco_parametros=[Integer(0, df_tabuas.shape[1]-1), 
                                   Integer(fator_agravo[0], fator_agravo[1]), 
                                   Integer(delay[0], delay[1])],
                resultado_placeholder=resultado_placeholder,
                n_calls=n_calls,
                n_initial_points=n_initial_points,
                random_state=random_state,
            )
        
            st.markdown("##### Tábuas que NÃO rejeitam H₀")
            df_resultados = pd.DataFrame(st.session_state.resultados_otimizacao)
            st.dataframe(df_resultados[(df_resultados['Decisão Qui-Quadrado'] == 'Não rejeitar H₀') & (df_resultados['Decisão KS'] == 'Não rejeitar H₀')])

            fig = px.line(st.session_state.resultados_otimizacao, 
              x='Iteração', 
              y='Função Objetivo',
              title='Evolução da Função Objetivo',
              markers=True)

            fig.update_layout(title_font_size=18)
            st.plotly_chart(fig)

if __name__ == '__main__':
    main()