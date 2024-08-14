from bayes_opt import BayesianOptimization
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
from sklearn.metrics import r2_score
from pydantic import BaseModel, Field
from typing import List, Tuple

df_tabuas = pd.read_excel('Funções Biométricas (Com Fórmulas).xlsx', sheet_name='qx')

class NDArray(np.ndarray):
    def to_list(self):
        return self.tolist()

class OtimizacaoBayesiana(BaseModel):
    expostos: NDArray = Field(default_factory=lambda: np.random.randint(1, 500, size=127))
    tabuas_base: List[NDArray] = Field(default_factory=lambda: [np.array(tabua) for tabua in df_tabuas.values.T.tolist()])
    fator_agravamento: Tuple[float, float] = (0.8, 1.2)
    delay_anos: Tuple[float, float] = (-5.0, 5.0)

    class Config:
        arbitrary_types_allowed = True
    
    @property
    def pbounds(self):
        return {
            'tabua_index': (0, len(self.tabuas_base) - 1),
            'fator_agravamento': self.fator_agravamento,
            'delay_anos': self.delay_anos
        }
    
    def aplicar_agravamento(self, tabua: np.ndarray, fator: float) -> np.ndarray:
        return tabua * fator

    def aplicar_delay(self, tabua: np.ndarray, delay_anos: int) -> np.ndarray:
        return np.roll(tabua, delay_anos) if delay_anos != 0 else tabua

    def calcular_aderencia(self, expostos: np.ndarray, tabua: np.ndarray) -> Tuple[float, float]:
        esperados = expostos * tabua
        r2 = r2_score(expostos, esperados)
        ks_stat = ks_2samp(expostos, esperados).statistic
        return r2, ks_stat

    def funcao_objetivo(self, tabua_index: float, fator_agravamento: float, delay_anos: float) -> float:
        tabua_base = self.tabuas_base[int(tabua_index)]
        tabua_var = self.aplicar_agravamento(tabua_base, fator_agravamento)
        tabua_var = self.aplicar_delay(tabua_var, int(delay_anos))
        r2, ks_stat = self.calcular_aderencia(self.expostos, tabua_var)
        return r2 - ks_stat

    def executar_otimizacao(self, random_state: int) -> dict:
        otimizador = BayesianOptimization(
            f=self.funcao_objetivo,
            pbounds=self.pbounds,
            random_state=random_state,
        )
        otimizador.maximize(init_points=20, n_iter=100)
        return otimizador.max

    def otimizar(self, n_repeticoes: int = 10) -> None:
        resultados = [self.executar_otimizacao(random_state=i) for i in range(n_repeticoes)]
        melhores_targets = [r['target'] for r in resultados]
        melhores_tabuas = [int(r['params']['tabua_index']) for r in resultados]
        melhores_fatores = [r['params']['fator_agravamento'] for r in resultados]
        melhores_delays = [r['params']['delay_anos'] for r in resultados]

        media_target = np.mean(melhores_targets)
        media_tabua = int(np.round(np.mean(melhores_tabuas)))
        media_fator = np.mean(melhores_fatores)
        media_delay = np.mean(melhores_delays)

        print("Média dos melhores targets:", media_target)
        print("Índice da tábua média mais aderente:", media_tabua)
        print("Média dos melhores fatores de agravamento:", media_fator)
        print("Média dos melhores delays:", media_delay)
