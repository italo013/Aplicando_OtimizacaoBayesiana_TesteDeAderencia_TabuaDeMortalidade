import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from lib.qui_quadrado import QuiQuadrado
from lib.teste_ks import KolmogorovSmirnov
from lib.text import aplicar_fator_desloc

st.set_page_config(page_title="Teste Manual", page_icon="🔍")

def main():
    st.header('Testando a Aderência Manualmente')

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

    select_tb_mortabilidade_play = st.selectbox(
        "Tábua de Mortalidade",
        df_tabuas.columns.tolist(),
        help="Selecione a Tábua de Mortalidade que você deseja testar.",
    )
    col1, col2 = st.columns(2)
    
    with col1:
        fator_agravo_play = st.slider(
            "Agravo ou Suavização",
            -100.00,
            100.00,
            0.0,
            help="Agravo e suavização são ajustes aplicados à tábua de mortalidade. O agravo aumenta as taxas de mortalidade e é representado por valores positivos neste controle deslizante. A suavização, por outro lado, diminui as taxas de mortalidade e é representado por valores negativos. Defina o intervalo de agravo selecionando valores positivos e o intervalo de suavização selecionando valores negativos.",
        )
    
    with col2:
        desloc_play = st.slider(
            "Deslocamento",
            -100.00,
            100.00,
            0.0,
            help="O deslocamento é um ajuste aplicado à tábua de mortalidade que atrasa as taxas de mortalidade. Isso é representado por valores positivos neste controle deslizante. Defina o intervalo de deslocamento selecionando valores dentro do range.",
        )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Qui-Quadrado (Chi-Square)")
        tabua_selecionada = aplicar_fator_desloc(
                df_tabuas[select_tb_mortabilidade_play], fator_agravo_play, desloc_play
            )
        qq = QuiQuadrado(f_obs=np.array(df['qtda_morte']), f_esp=np.array(df['qtda_vivo'].values * tabua_selecionada))
        qq_result = qq.calcular_qui_quadrado()
        for key, value in qq_result.items():
            st.markdown(f"**{key}**: {value}")

    with col2:
        st.markdown("#### Kolmogorov-Smirnov (KS)")
        tabua_selecionada = aplicar_fator_desloc(
                df_tabuas[select_tb_mortabilidade_play], fator_agravo_play, desloc_play
            )
        ks = KolmogorovSmirnov(f_obs=np.array(df['qtda_morte']), f_esp=np.array(df['qtda_vivo'].values * tabua_selecionada))
        ks_result = ks.calcular_ks()
        for key, value in ks_result.items():
            st.markdown(f"**{key}**: {value}")

    fig = px.line(
        x=list(range(0, 127)),
        y=[df['qtda_morte'], df['qtda_vivo'] * tabua_selecionada],
        labels={"index": "Idade", "value": "qx"},
    )
    st.plotly_chart(fig)

if __name__ == '__main__':
    main()