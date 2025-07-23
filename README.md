# turbofan-rul-prediction-cmapss

## Descrição do Projeto

Este projeto tem como objetivo prever a vida útil remanescente (RUL - Remaining Useful Life) de motores turbofan utilizando o conjunto de dados C-MAPSS da NASA. A abordagem combina técnicas de aprendizado de máquina e redes neurais para realizar prognósticos precisos.

## Estrutura do Projeto

- **notebooks/**: Contém os notebooks Jupyter utilizados para análise exploratória, pré-processamento e treinamento dos modelos.
- **data/**: Arquivos de dados utilizados no projeto.
- **src/**: Código-fonte organizado em módulos:
  - **preprocessing/**: Funções para pré-processamento dos dados.
  - **models/**: Arquiteturas e treinamento de modelos.
  - **utils/**: Funções utilitárias como métricas e visualizações.
- **artifacts/**: Modelos treinados e outros artefatos gerados durante o projeto.

## Conjunto de Dados

O conjunto de dados C-MAPSS contém informações de sensores coletadas de motores turbofan simulados. Ele é dividido em diferentes subconjuntos, cada um representando condições operacionais específicas.

## Tecnologias Utilizadas

- Python
- Pandas
- NumPy
- TensorFlow
- Scikit-learn
- Matplotlib
- Seaborn

## Como Executar

1. Clone este repositório:

   ```bash
   git clone https://github.com/daviseemann/turbofan-rul-prediction-cmapss.git
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Navegue até a pasta `notebooks/` e execute os notebooks Jupyter para reproduzir os resultados.

## Referências

- [C-MAPSS Dataset](https://data.nasa.gov/dataset/C-MAPSS-Data-Set/ff5v-kuh6)
- Relatório: "A Deep Learning Model for Remaining Useful Life Prediction of Aircraft Turbofan Engine on C-MAPSS Dataset"

## Contato

Davi Seemann  
Email: [daviseemann@example.com](mailto:daviseemann@example.com)
