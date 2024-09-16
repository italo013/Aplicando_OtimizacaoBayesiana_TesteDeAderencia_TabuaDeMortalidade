import logging
from lib.qui_quadrado import QuiQuadrado
from lib.teste_ks import KolmogorovSmirnov
import pandas as pd
import numpy as np
import streamlit as st


modelo = pd.read_csv('modelo_csv.csv', sep=';')
df_tabuas = pd.read_excel('Funções Biométricas (Com Fórmulas).xlsx', sheet_name='qx')

import numpy as np
from skopt import gp_minimize
from pydantic import BaseModel, Field
from typing import List, Any
from lib.utils import aplicar_fator_desloc

logging.basicConfig(level=logging.INFO)

class OtimizacaoBayesiana(BaseModel):
    f_obs: np.array = Field(...)
    f_vivos: np.array = Field(...)
    tabuas: pd.DataFrame = Field(...) 
    index: dict = Field(default_factory=dict)
    resultado_dict: dict = Field(default_factory=dict)
    extra_data: dict = Field(default_factory=dict)  # Adicione esta linha

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.get_index_tabuas()

    def get_index_tabuas(self):
        self.index = {key: value for key, value in enumerate(self.tabuas.columns)}

    def callback(self, res):
        iteracao = len(res.x_iters)
        ultimo_resultado = self.resultado_dict[len(self.resultado_dict)]
        
        # Adicione o resultado atual à lista de resultados na sessão
        st.session_state.resultados_otimizacao.append({
            'Iteração': iteracao,
            'Tábua': ultimo_resultado['tabela'],
            'Agravo/Suavização': ultimo_resultado['agravo/suavizacao'],
            'Deslocamento': ultimo_resultado['delay'],
            'Qui-Quadrado': ultimo_resultado['qui_quadrado'],
            'Qui-Quadrado Valor Crítico': ultimo_resultado['qui_quadrado_valor_critico'],
            'Decisão Qui-Quadrado': ultimo_resultado['decisao_qui_quadrado'],
            'Penalidade Qui-Quadrado': ultimo_resultado['penalidade_qui_quadrado'],
            'KS': ultimo_resultado['ks'],
            'KS Valor Crítico': ultimo_resultado['ks_valor_critico'],
            'Decisão KS': ultimo_resultado['decisao_ks'],
            'Penalidade KS': ultimo_resultado['penalidade_ks'],
            'KS': ultimo_resultado['ks'],
            'Função Objetivo': ultimo_resultado['func_obj']
        })

        self.extra_data['resultado_placeholder'].dataframe(pd.DataFrame(st.session_state.resultados_otimizacao))

    def funcao_objetivo(self, parametros):
        tabua = parametros[0]
        fator = parametros[1] if parametros[1] != -100.00 else -99.99 
        desloc = parametros[2]

        f_esp_modificado = aplicar_fator_desloc(tabua=np.array(self.tabuas.iloc[:, tabua]), fator=fator, desloc=desloc) * self.f_vivos
        logging.info(f"parans: {self.index[tabua], fator, desloc}")

        qq = QuiQuadrado(f_obs=self.f_obs, f_esp=f_esp_modificado)
        resultado_qui_quadrado = qq.calcular_qui_quadrado()
        #logging.info(f"resultado_qui_quadrado: {resultado_qui_quadrado}")

        ks = KolmogorovSmirnov(f_obs=self.f_obs, f_esp=f_esp_modificado)
        resultado_ks = ks.calcular_ks()
        #logging.info(f"resultado_ks: {resultado_ks}")

        penalidade_qui_quadrado = 99999 if resultado_qui_quadrado['Decisão Baseada no valor crítico'] == 'Rejeitar H₀' else 0
        penalidade_ks = 99999 if resultado_ks['Decisão Baseada no valor crítico'] == 'Rejeitar H₀' else 0
        #logging.info(f"{penalidade_qui_quadrado, penalidade_ks}")

        func_obj = resultado_qui_quadrado['Qui-Quadrado calculado'] + resultado_ks['KS calculado'] + penalidade_qui_quadrado + penalidade_ks
        #logging.info(f"func_obj: {func_obj}")

        self.resultado_dict[len(self.resultado_dict)+1] = {
            'tabela': self.index[tabua],
            'agravo/suavizacao': fator,
            'delay': desloc,
            'qui_quadrado': resultado_qui_quadrado['Qui-Quadrado calculado'],
            'qui_quadrado_valor_critico': resultado_qui_quadrado['Valor crítico'],
            'decisao_qui_quadrado': resultado_qui_quadrado['Decisão Baseada no valor crítico'],
            'ks': resultado_ks['KS calculado'],
            'ks_valor_critico': resultado_ks['Valor crítico'],
            'decisao_ks': resultado_ks['Decisão Baseada no valor crítico'],
            'penalidade_qui_quadrado': penalidade_qui_quadrado,
            'penalidade_ks': penalidade_ks,
            'func_obj': func_obj
        }

        return func_obj
    
    def aplicar_otimizacao(self, espaco_parametros: List[tuple], n_calls: int = 50, random_state: int = 0, n_initial_points: int = 10, resultado_placeholder=None):
        self.extra_data['resultado_placeholder'] = resultado_placeholder
        resultado = gp_minimize(self.funcao_objetivo, espaco_parametros, n_calls=n_calls, random_state=random_state, n_initial_points=n_initial_points, callback=self.callback)
        melhores_parametros = resultado.x

        return self.resultado_dict

        #logging.info(f"Melhores parâmetros: {melhores_parametros}")
        #logging.info(self.resultado_dict)