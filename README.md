# Turbofan RUL Prediction using C-MAPSS Dataset

Este projeto implementa modelos de Machine Learning para predição de Remaining Useful Life (RUL) de motores turbofan usando o dataset C-MAPSS da NASA.

## 📋 Sobre o Projeto

O objetivo é prever o tempo de vida útil restante de motores de aeronaves com base em dados de sensores, utilizando redes neurais MLP (Multi-Layer Perceptron). O projeto segue metodologias apresentadas em papers acadêmicos sobre prognostics e health management.

## 🏗️ Estrutura do Projeto

```
turbofan-rul-prediction-cmapss/
├── 📁 src/                          # Código fonte modular
│   ├── data/                        # Processamento de dados
│   ├── models/                      # Arquiteturas e métricas
│   ├── utils/                       # Utilitários e visualização
│   └── evaluation/                  # Funções de avaliação
│
├── 📁 notebooks/                    # Notebooks organizados por tier
│   ├── tier-1-exploration/          # EDA e exploração inicial
│   ├── tier-2-development/          # Desenvolvimento iterativo
│   ├── tier-3-production/           # Modelos finais
│   └── tier-4-experiments/          # Experimentos diversos
│
├── 📁 data/                         # Dados organizados
│   ├── raw/                         # Dados originais C-MAPSS
│   ├── processed/                   # Dados processados
│   └── external/                    # Dados externos
│
├── 📁 docs/                         # Documentação centralizada
│   ├── academic/                    # Papers, relatórios, apresentações
│   ├── technical/                   # Documentação técnica
│   └── api/                         # Documentação da API
│
├── 📁 models/                       # Modelos e checkpoints
│   ├── checkpoints/                 # Checkpoints de treinamento
│   └── final/                       # Modelos finais
│
├── 📁 results/                      # Resultados e artefatos
│   ├── figures/                     # Gráficos e visualizações
│   ├── metrics/                     # Métricas de avaliação
│   └── reports/                     # Relatórios automatizados
│
└── 📁 tools/                        # Ferramentas de desenvolvimento
    ├── scripts/                     # Scripts utilitários
    └── config/                      # Configurações
```

### 📊 Organização por Tiers

**Tier 1 - Exploração**: EDA, análise inicial dos dados
**Tier 2 - Desenvolvimento**: Desenvolvimento iterativo de modelos
**Tier 3 - Produção**: Modelos finais e implementações prontas
**Tier 4 - Experimentos**: Testes, variações e experimentos diversos

## 🚀 Getting Started

### Pré-requisitos

- Python 3.8+
- TensorFlow 2.8+
- Pandas, NumPy, Scikit-learn
- Matplotlib, Seaborn

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/daviseemann/turbofan-rul-prediction-cmapss.git
cd turbofan-rul-prediction-cmapss
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Instale o pacote em modo desenvolvimento:

```bash
pip install -e .
```

### Uso da Nova Estrutura

```python
# Imports da estrutura modular
from src.data import load_data, create_rul_labels, create_all_windows, DEFAULT_SENSORS
from src.models import create_mlp_model, create_minmax_layer, RULMetrics
from src.utils import plot_learning_curves
from src.evaluation import ModelEvaluator

# Fluxo completo
df_train = load_data('data/raw/train_FD001.txt')
df_train = create_rul_labels(df_train, Re=129)

# Janelas temporais
df_windows = create_all_windows(df_train, 24, 1, DEFAULT_SENSORS)
df_train_windows, df_val_windows = split_windows_by_engine(df_windows)

# Modelo
minmax_layer = create_minmax_layer(X_train)
model = create_mlp_model(input_dim, minmax_layer)

# Avaliação
evaluator = ModelEvaluator(model, X_test, y_test)
metrics = evaluator.calculate_metrics()
```

## 📊 Dataset

O projeto utiliza o dataset C-MAPSS (Commercial Modular Aero-Propulsion System Simulation) da NASA:

- **FD001**: Condições simples de operação e falha
- **FD002**: Múltiplas condições operacionais
- **FD003**: Múltiplos modos de falha
- **FD004**: Múltiplas condições e modos de falha

### Sensores Utilizados

14 dos 21 sensores disponíveis são utilizados, conforme literatura:
`s2, s3, s4, s7, s8, s9, s11, s12, s13, s14, s15, s17, s20, s21`

## 🧠 Metodologia

### Pré-processamento

- Normalização Min-Max para [-1, 1]
- Criação de janelas temporais (window_size=24, stride=1)
- Modelo de degradação linear por partes (Re=129)

### Arquitetura

- **MLP**: 2 camadas ocultas com 20 neurônios cada
- **Ativação**: ReLU nas camadas ocultas, Linear na saída
- **Regularização**: L1/L2 (0.1/0.2)
- **Otimizador**: Adam (lr=0.001)

### Métricas

- **RMSE**: Root Mean Square Error
- **NASA Score**: Health Score assimétrico (penaliza late predictions)
- **MAPE**: Mean Absolute Percentage Error

## 📈 Resultados

| Métrica    | FD001    |
| ---------- | -------- |
| RMSE       | ~18-20   |
| NASA Score | ~250-300 |

## 📁 Notebooks por Tier

### Tier 1: Exploração e Análise

- `01-exploratory-data-analysis.ipynb`: Análise exploratória completa
- `02-data-preprocessing.ipynb`: Técnicas de pré-processamento

### Tier 2: Desenvolvimento de Modelos

- `01-mlp-baseline.ipynb`: Modelo baseline inicial
- `02-mlp-v1.ipynb`: Primeira versão melhorada
- `03-mlp-v2.ipynb`: Segunda versão com ajustes
- `04-mlp-v3-base.ipynb`: Versão base do modelo final

### Tier 3: Produção

- `01-final-model.ipynb`: Modelo final otimizado
- `02-paper-implementation.ipynb`: Implementação baseada em papers

### Tier 4: Experimentos

- `01-fd002-dataset.ipynb`: Testes com dataset FD002
- `02-hyperparameter-tuning.ipynb`: Otimização de hiperparâmetros
- `03-window-size-experiments.ipynb`: Experimentos com janelas
- `04-no-clipping-experiments.ipynb`: Testes sem clipping
- E outros experimentos diversos...

## 🔧 Scripts

- `scripts/train_model.py`: Script para treinar modelo
- `scripts/evaluate_model.py`: Script para avaliar modelo
- `scripts/create_submission.py`: Criar arquivo de submissão

## 📚 Referências

1. Saxena, A., et al. "Damage propagation modeling for aircraft engine run-to-failure simulation." (2008)
2. Zheng, S., et al. "Long Short-Term Memory Network for Remaining Useful Life estimation." (2017)
3. NASA Prognostics Center of Excellence - C-MAPSS Dataset

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 👨‍💻 Autor

**Davi Seemann**

- GitHub: [@daviseemann](https://github.com/daviseemann)

## 🏆 Reconhecimentos

- NASA Prognostics Center of Excellence
- UFSC - Universidade Federal de Santa Catarina
- Professores e colegas do curso de Aprendizado de Máquina
