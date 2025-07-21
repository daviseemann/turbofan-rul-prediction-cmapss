# Estrutura do Projeto

## Visão Geral

Este projeto segue uma estrutura organizada por funcionalidade e nível de maturidade do código.

## Estrutura de Diretórios

```
turbofan-rul-prediction-cmapss/
├── 📁 src/                          # Código fonte modular
│   ├── data/                        # Processamento de dados
│   ├── models/                      # Arquiteturas e métricas
│   ├── utils/                       # Utilitários gerais
│   └── evaluation/                  # Funções de avaliação
│
├── 📁 notebooks/                    # Notebooks organizados por tier
│   ├── tier-1-exploration/          # EDA e exploração inicial
│   ├── tier-2-development/          # Desenvolvimento iterativo
│   ├── tier-3-production/           # Modelos finais
│   └── tier-4-experiments/          # Experimentos diversos
│
├── 📁 data/                         # Dados do projeto
│   ├── raw/                         # Dados originais
│   ├── processed/                   # Dados processados
│   └── external/                    # Dados externos
│
├── 📁 models/                       # Modelos salvos
│   ├── checkpoints/                 # Checkpoints de treinamento
│   └── final/                       # Modelos finais
│
├── 📁 results/                      # Resultados e artefatos
│   ├── figures/                     # Gráficos e visualizações
│   ├── metrics/                     # Métricas de avaliação
│   └── reports/                     # Relatórios automatizados
│
├── 📁 docs/                         # Documentação
│   ├── academic/                    # Materiais acadêmicos
│   ├── technical/                   # Documentação técnica
│   └── api/                         # Documentação da API
│
├── 📁 tools/                        # Ferramentas de desenvolvimento
│   ├── scripts/                     # Scripts utilitários
│   └── config/                      # Configurações
│
└── 📁 tests/                        # Testes
    ├── unit/                        # Testes unitários
    └── integration/                 # Testes de integração
```

## Filosofia da Organização

### Separação por Responsabilidade
- **src/**: Código reutilizável e modular
- **notebooks/**: Análises e experimentação
- **docs/**: Toda documentação centralizada
- **data/**: Dados organizados por tipo

### Tiers de Notebooks
- **Tier 1**: Exploração e entendimento
- **Tier 2**: Desenvolvimento iterativo  
- **Tier 3**: Produção e finalização
- **Tier 4**: Experimentos e testes

Esta estrutura facilita:
- Navegação intuitiva
- Manutenção do código
- Colaboração em equipe
- Reprodutibilidade dos resultados
