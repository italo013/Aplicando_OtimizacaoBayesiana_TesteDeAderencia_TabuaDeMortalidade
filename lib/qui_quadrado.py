import pandas as pd
import numpy as np
import scipy.stats as stats
from pydantic import BaseModel, Field
from typing import List

class QuiQuadrado(BaseModel):
    """
    Classe para calcular o teste Qui-Quadrado.

    Atributos:
        f_obs (np.array): Frequências observadas.
        f_esp (np.array): Frequências esperadas.
        qui_quadrado (float): Valor calculado do Qui-Quadrado.
        valor_critico (float): Valor crítico do Qui-Quadrado.
        alpha (float): Nível de significância. Padrão é 0.05.
        decisao_critico (str): Decisão baseada no valor crítico.
        grau_liberdade (float): Graus de liberdade para o teste.
    """

    f_obs: np.ndarray = Field(...)
    f_esp: np.ndarray = Field(...)
    f_obs_filtrado: np.ndarray = Field(default=None)
    f_esp_filtrado: np.ndarray = Field(default=None)    
    qui_quadrado: float = None
    valor_critico: float = None
    alpha: float = 0.05
    decisao_critico: str = None
    grau_liberdade: float = None

    class Config:
        arbitrary_types_allowed = True

    def calcular_qui_quadrado(self) -> dict:
        """
        Método para calcular o Qui-Quadrado.

        Args:
            grau_liberdade (int): Graus de liberdade para o teste.

        Returns:
            dict: Dicionário com o Qui-Quadrado calculado, valor crítico e decisão baseada no valor crítico.
        """
        mask = ~np.logical_and(self.f_obs == 0, self.f_esp == 0)
        mask = self.f_esp != 0
        self.f_obs_filtrado = self.f_obs[mask]
        self.f_esp_filtrado = self.f_esp[mask]
        self.grau_liberdade = len(self.f_obs_filtrado) if self.f_obs_filtrado is not None else 0

        self.qui_quadrado = np.sum((self.f_obs_filtrado -self.f_esp_filtrado) **2 / self.f_esp_filtrado)

        self.valor_critico = stats.chi2.ppf(1 - self.alpha, self.grau_liberdade - 1)
        self.decisao_critico = 'Rejeitar H₀' if self.qui_quadrado > self.valor_critico else 'Não rejeitar H₀'
        
        return {
            'Qui-Quadrado calculado': round(float(self.qui_quadrado), 4),
            'Valor crítico': round(float(self.valor_critico), 4),
            'Decisão Baseada no valor crítico': self.decisao_critico,
        }