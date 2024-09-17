# Aplicando Otimização Bayesiana para aprimorar o Teste de Aderência das Tábuas de Mortalidade

## Sobre o Projeto
Este projeto foi desenvolvido para simplificar o Teste de Aderência das Tábuas de Mortalidade utilizando Otimização Bayesiana para aprimorar, otimizar e automatizar aplicando ajustes de agravo, suavização e deslocamento às tábuas de mortalidade para encontrar a configuração que oferece a melhor aderência, ou seja, que não rejeita a Hipótese Nula (H₀).


## Estrutura de Pastas
```
├── lib/                                  # Diretório contendo módulos Python
│ ├── __init__.py                         # Arquivo de inicialização do pacote
│ ├── otimizacao.py                       # Implementação da otimização Bayesiana
│ ├── qui_quadrado.py                     # Implementação do teste Qui-Quadrado
│ ├── teste_ks.py                         # Implementação do teste Kolmogorov-Smirnov
│ ├── text.py                             # Funções auxiliares para manipulação de texto
│ └── utils.py                            # Funções utilitárias gerais
├── pages/                                # Diretório contendo páginas da aplicação Streamlit
│ ├── 1_🔍Teste_Manualmente.py            # Página para teste manual de aderência
│ ├── 2_🤖Usando_Otimização_Bayesiana.py  # Página para otimização Bayesiana automática
│ └── 3_📞Contatos.py                     # Página de contatos
├── Home.py                             # Página inicial da aplicação Streamlit
├── Funções Biométricas (Com Fórmulas).xlsx  # Planilha com funções biométricas
├── modelo_csv.csv                        # Arquivo CSV modelo para importação de dados
├── README.md                             # Documentação do projeto
```

## Tecnologias Utilizadas
Este projeto utiliza uma variedade de tecnologias modernas para implementar a otimização bayesiana e fornecer uma interface amigável para o usuário. As principais tecnologias incluem:
1. **Python:** A linguagem de programação principal usada para implementar a lógica de otimização bayesiana e os testes estatísticos.
2. **Programação Orientada a Objeto (POO):** O projeto foi desenvolvido utilizando os princípios da POO, o que permite uma estrutura de código mais organizada, modular e reutilizável. Classes como OtimizacaoBayesiana, QuiQuadrado e KolmogorovSmirnov são exemplos claros dessa abordagem.
3. **Pydantic:** Uma biblioteca poderosa para validação de dados e gerenciamento de configurações em Python. O Pydantic é utilizado extensivamente neste projeto para definir modelos de dados, validar entradas e garantir a integridade dos dados em todo o processo de otimização. Pydantic é conhecido por sua velocidade, facilidade de uso e integração com outras ferramentas do ecossistema Python.
4. **Streamlit:** Uma biblioteca Python usada para criar a interface web interativa. Streamlit permite a criação rápida de aplicativos web.
5. **Pandas:** Utilizada para manipulação e análise de dados estruturados. É particularmente útil para lidar com os dados das tábuas de mortalidade e resultados dos testes.
6. **NumPy:** Biblioteca fundamental para computação científica em Python, usada para operações matemáticas eficientes em arrays e matrizes.
7. **Plotly:** Biblioteca de visualização de dados interativa, usada para criar gráficos dinâmicos e informativos dos resultados da otimização.
8. **scikit-optimize (skopt):** Uma biblioteca de otimização que fornece implementações de várias técnicas de otimização bayesiana.
9. **SciPy:** Usada para implementação de testes estatísticos, como o teste Kolmogorov-Smirnov.

## Como executar o projeto
1. Crie um novo ambiente conda:
```bash
   conda create -n streamlit_env python=3.10
```

2. Ative o ambiente recém-criado:
```bash
    conda activate streamlit_env
```

3. Instale dependências necessárias:
```bash
   pip install requirements.txt
```

4. Para executar a aplicação Streamlit, use o comando:
```bash
   streamlit run Home.py
```

## Funcionalidades
O projeto de Otimização Bayesiana para melhorar o teste de aderência de tábuas de mortalidade possui as seguintes funcionalidades principais:
1. **Página Inicial (Home.py):**
    - Visão geral do projeto
    - Explicação dos conceitos dos testes Qui-Quadrado e Kolmogorov-Smirnov
    - Demonstração dos efeitos da aplicação de ajustes (agravamento, suavização e deslocamento) nas tábuas de mortalidade

2. **Teste Manual (1_🔍Teste_Manualmente.py):**
    - Permite ao usuário testar manualmente a aderência de uma tábua de mortalidade selecionada
    - Aplicação de ajustes personalizados
    - Exibição dos resultados dos testes Qui-Quadrado e Kolmogorov-Smirnov

3. **Otimização Bayesiana (2_🤖Usando_Otimização_Bayesiana.py):**
    - Implementação do processo de Otimização Bayesiana
    - Configuração dos parâmetros de otimização pelo usuário
    - Visualização dos resultados, incluindo as tábuas de mortalidade que não rejeitam a hipótese nula

4. **Lógica de Otimização (otimizacao.py):**
    - Classe OtimizacaoBayesiana que encapsula a lógica da Otimização Bayesiana
    - Função objetivo, callback e aplicação da otimização

5. **Testes Estatísticos:**
    - Implementação do teste Qui-Quadrado (qui_quadrado.py)
    - Implementação do teste Kolmogorov-Smirnov (teste_ks.py)

6. **Ajustes nas Tábuas de Mortalidade:**
    - Aplicação de agravamento
    - Aplicação de suavização
    - Aplicação de deslocamento

7. **Visualização de Resultados:**
    - Exibição gráfica dos resultados dos testes
    - Apresentação das tábuas de mortalidade otimizadas

8. **Interface Interativa:**
    - Utilização do Streamlit para criar uma interface de usuário interativa e amigável

- Teste manual de aderência usando Qui-Quadrado e Kolmogorov-Smirnov
- Otimização Bayesiana automática para encontrar as melhores tábuas e parâmetros
- Visualização dos resultados através de gráficos interativos
- Interface web amigável construída com Streamlit

O objetivo principal do projeto é encontrar a configuração ótima de ajustes (agravamento, suavização e deslocamento) para as tábuas de mortalidade que forneça o melhor ajuste, ou seja, não rejeite a hipótese nula nos testes de aderência.

Este conjunto de funcionalidades permite aos usuários explorar, testar e otimizar tábuas de mortalidade de forma interativa e eficiente, utilizando técnicas avançadas de otimização e estatística.

## Contribuição
Contribuições são bem-vindas! Por favor, abra uma issue para discutir mudanças importantes antes de fazer um pull request.