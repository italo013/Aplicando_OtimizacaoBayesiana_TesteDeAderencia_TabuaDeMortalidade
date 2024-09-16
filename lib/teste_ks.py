import pandas as pd
import numpy as np
import scipy.stats as stats
from pydantic import BaseModel, Field
from typing import List

class KolmogorovSmirnov(BaseModel):
    """
    Classe para calcular o teste de Kolmogorov-Smirnov.

    Atributos:
        f_obs (np.array): Frequências observadas.
        f_esp (np.array): Frequências esperadas.
        ks (float): Valor calculado do teste KS.
        valor_critico (float): Valor crítico do teste KS.
        alpha (float): Nível de significância. Padrão é 0.05.
        decisao_critico (str): Decisão baseada no valor crítico.
        grau_liberdade (float): Graus de liberdade para o teste.
    """

    f_obs: np.ndarray = Field(...)
    f_esp: np.ndarray = Field(...)
    f_obs_filtrado: np.ndarray = Field(default=None)
    f_esp_filtrado: np.ndarray = Field(default=None)
    ks: float = None
    valor_critico: float = None
    alpha: float = 0.05
    decisao_critico: str = None
    grau_liberdade: float = None

    class Config:
        arbitrary_types_allowed = True

    def calcular_ks(self) -> dict:
        """
        Método para calcular o teste de Kolmogorov-Smirnov.

        Args:
            grau_liberdade (int): Graus de liberdade para o teste.

        Returns:
            dict: Dicionário com o KS calculado, valor crítico e decisão baseada no valor crítico.
        """
        mask = ~np.logical_and(self.f_obs == 0, self.f_esp == 0)
        self.f_obs_filtrado = self.f_obs[mask]
        self.f_esp_filtrado = self.f_esp[mask]
        self.grau_liberdade = len(self.f_obs_filtrado) if self.f_obs_filtrado is not None else 0

        self.ks = np.max(np.abs((np.cumsum(self.f_obs) / np.sum(self.f_obs)) - (np.cumsum(self.f_esp) / np.sum(self.f_esp))))

        self.valor_critico = stats.ksone.ppf(1 - self.alpha, self.grau_liberdade - 1)
        self.decisao_critico = 'Rejeitar H₀' if self.ks > self.valor_critico else 'Não rejeitar H₀'
        
        return {
            'KS calculado': round(float(self.ks), 4),
            'Valor crítico': round(float(self.valor_critico), 4),
            'Decisão Baseada no valor crítico': self.decisao_critico
        }
