#!/usr/bin/env python3
"""
Script para reorganizar o projeto com uma estrutura mais limpa e organizada por tiers.
"""

import os
import shutil
from pathlib import Path


def create_clean_structure(base_path):
    """Cria a nova estrutura limpa e organizada."""
    directories = [
        # Core structure
        "src/data",
        "src/models",
        "src/utils",
        "src/evaluation",
        # Notebooks por tier
        "notebooks/tier-1-exploration",
        "notebooks/tier-2-development",
        "notebooks/tier-3-production",
        "notebooks/tier-4-experiments",
        # Data organization
        "data/raw",
        "data/processed",
        "data/external",
        # Models and artifacts
        "models/checkpoints",
        "models/final",
        # Results and outputs
        "results/figures",
        "results/metrics",
        "results/reports",
        # Documentation and reports
        "docs/academic",
        "docs/academic/papers",
        "docs/academic/reports",
        "docs/academic/presentations",
        "docs/technical",
        "docs/api",
        # Development tools
        "tools/scripts",
        "tools/config",
        # Tests
        "tests/unit",
        "tests/integration",
    ]

    print("🏗️ Criando estrutura limpa...")
    for directory in directories:
        dir_path = Path(base_path) / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}/")

        # Criar __init__.py para pacotes Python src
        if directory.startswith("src/") and len(directory.split("/")) == 2:
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                init_file.touch()


def organize_notebooks_by_tier(base_path):
    """Organiza notebooks por tiers de desenvolvimento."""
    base = Path(base_path)
    notebooks_dir = base / "notebooks"

    # Tier 1: Exploração inicial e EDA
    tier1_mapping = {
        "EDA.ipynb": "tier-1-exploration/01-exploratory-data-analysis.ipynb",
        "pre-processing.ipynb": "tier-1-exploration/02-data-preprocessing.ipynb",
    }

    # Tier 2: Desenvolvimento de modelos
    tier2_mapping = {
        "MLP.ipynb": "tier-2-development/01-mlp-baseline.ipynb",
        "MLP-1.ipynb": "tier-2-development/02-mlp-v1.ipynb",
        "MLP-2.ipynb": "tier-2-development/03-mlp-v2.ipynb",
        "MLP-3-BASE.ipynb": "tier-2-development/04-mlp-v3-base.ipynb",
    }

    # Tier 3: Produção (modelo final)
    tier3_mapping = {
        "Analises finais/MLP-3-FINAL.ipynb": "tier-3-production/01-final-model.ipynb",
        "MLP-artigo.ipynb": "tier-3-production/02-paper-implementation.ipynb",
    }

    # Tier 4: Experimentos
    tier4_mapping = {
        "MLP-3-FD002.ipynb": "tier-4-experiments/01-fd002-dataset.ipynb",
        "MLP-3-lr-tunning.ipynb": "tier-4-experiments/02-hyperparameter-tuning.ipynb",
        "MLP-3-outras-janelas.ipynb": "tier-4-experiments/03-window-size-experiments.ipynb",
        "MLP-3-sem-clipping.ipynb": "tier-4-experiments/04-no-clipping-experiments.ipynb",
        "MLP_4.ipynb": "tier-4-experiments/05-mlp-v4-experiments.ipynb",
        "MLP_5.ipynb": "tier-4-experiments/06-mlp-v5-experiments.ipynb",
        "MLP-3.ipynb": "tier-4-experiments/07-mlp-v3-variants.ipynb",
    }

    all_mappings = {**tier1_mapping, **tier2_mapping, **tier3_mapping, **tier4_mapping}

    print("\n📓 Organizando notebooks por tiers...")
    for src_name, dst_name in all_mappings.items():
        src_path = notebooks_dir / src_name
        if src_path.exists():
            dst_path = notebooks_dir / dst_name
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src_path), str(dst_path))
            print(f"  ✓ {src_name} → {dst_name}")


def organize_documentation(base_path):
    """Organiza documentação e relatórios."""
    base = Path(base_path)

    # Mover documentos acadêmicos
    doc_mapping = [
        (
            "Relatório_final_Aprendizado_de_maquina_DaviSeemann (5).pdf",
            "docs/academic/reports/final-report.pdf",
        ),
        ("Trabalho final.pdf", "docs/academic/reports/trabalho-final.pdf"),
        (
            "apresentação/Trabalho final.pptx",
            "docs/academic/presentations/final-presentation.pptx",
        ),
    ]

    print("\n📚 Organizando documentação...")
    for src, dst in doc_mapping:
        src_path = base / src
        dst_path = base / dst
        if src_path.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src_path), str(dst_path))
            print(f"  ✓ {src} → {dst}")

    # Mover papers
    papers_src = base / "relatorios" / "papers"
    papers_dst = base / "docs" / "academic" / "papers"

    if papers_src.exists():
        for paper in papers_src.glob("*.pdf"):
            dst_file = papers_dst / paper.name
            shutil.copy2(str(paper), str(dst_file))
            print(f"  ✓ papers/{paper.name}")


def organize_data_files(base_path):
    """Organiza arquivos de dados."""
    base = Path(base_path)
    data_src = base / "dados"
    data_dst = base / "data" / "raw"

    print("\n💾 Organizando dados...")
    if data_src.exists():
        for data_file in data_src.glob("*"):
            if data_file.is_file():
                dst_file = data_dst / data_file.name
                shutil.copy2(str(data_file), str(dst_file))
                print(f"  ✓ {data_file.name}")


def create_tier_readme_files(base_path):
    """Cria arquivos README para cada tier explicando o propósito."""
    base = Path(base_path)

    tier_descriptions = {
        "tier-1-exploration": {
            "title": "Tier 1: Exploração e Análise",
            "description": """
Este tier contém notebooks para exploração inicial dos dados e análise exploratória.

## Conteúdo:
- **01-exploratory-data-analysis.ipynb**: Análise exploratória completa do dataset C-MAPSS
- **02-data-preprocessing.ipynb**: Técnicas de pré-processamento e preparação dos dados

## Objetivo:
Entender o dataset, identificar padrões, problemas nos dados e definir estratégias de pré-processamento.
""",
        },
        "tier-2-development": {
            "title": "Tier 2: Desenvolvimento de Modelos",
            "description": """
Este tier contém o desenvolvimento iterativo dos modelos MLP.

## Conteúdo:
- **01-mlp-baseline.ipynb**: Modelo baseline inicial
- **02-mlp-v1.ipynb**: Primeira versão melhorada
- **03-mlp-v2.ipynb**: Segunda versão com ajustes
- **04-mlp-v3-base.ipynb**: Versão base do modelo final

## Objetivo:
Desenvolvimento iterativo e incremental dos modelos, testando diferentes arquiteturas e abordagens.
""",
        },
        "tier-3-production": {
            "title": "Tier 3: Produção",
            "description": """
Este tier contém os modelos finais prontos para produção.

## Conteúdo:
- **01-final-model.ipynb**: Modelo final otimizado e validado
- **02-paper-implementation.ipynb**: Implementação baseada em papers acadêmicos

## Objetivo:
Modelos finais, otimizados, documentados e prontos para uso em produção ou submissão acadêmica.
""",
        },
        "tier-4-experiments": {
            "title": "Tier 4: Experimentos",
            "description": """
Este tier contém experimentos diversos e testes de abordagens alternativas.

## Conteúdo:
- **01-fd002-dataset.ipynb**: Testes com dataset FD002
- **02-hyperparameter-tuning.ipynb**: Otimização de hiperparâmetros
- **03-window-size-experiments.ipynb**: Experimentos com tamanhos de janela
- **04-no-clipping-experiments.ipynb**: Testes sem clipping de RUL
- **05-mlp-v4-experiments.ipynb**: Experimentos com MLP v4
- **06-mlp-v5-experiments.ipynb**: Experimentos com MLP v5
- **07-mlp-v3-variants.ipynb**: Variações do modelo v3

## Objetivo:
Explorar abordagens alternativas, testar hipóteses e validar decisões de design.
""",
        },
    }

    print("\n📝 Criando READMEs dos tiers...")
    for tier, info in tier_descriptions.items():
        readme_path = base / "notebooks" / tier / "README.md"
        content = f"# {info['title']}\n{info['description']}"

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ {tier}/README.md")


def create_docs_structure(base_path):
    """Cria estrutura de documentação."""
    base = Path(base_path)

    # README principal para docs
    docs_readme = base / "docs" / "README.md"
    docs_content = """# Documentação do Projeto

## Estrutura

### 📚 Academic
Documentação acadêmica do projeto:
- **papers/**: Papers de referência utilizados
- **reports/**: Relatórios técnicos e acadêmicos
- **presentations/**: Apresentações e slides

### 🔧 Technical
Documentação técnica:
- Arquitetura do sistema
- Guias de desenvolvimento
- Especificações técnicas

### 📖 API
Documentação da API e módulos:
- Referência das funções
- Exemplos de uso
- Guias de integração
"""

    with open(docs_readme, "w", encoding="utf-8") as f:
        f.write(docs_content)
    print("  ✓ docs/README.md")


def create_project_structure_doc(base_path):
    """Cria documentação da estrutura do projeto."""
    base = Path(base_path)

    structure_doc = base / "docs" / "technical" / "project-structure.md"
    content = """# Estrutura do Projeto

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
"""

    with open(structure_doc, "w", encoding="utf-8") as f:
        f.write(content)
    print("  ✓ docs/technical/project-structure.md")


def cleanup_old_files(base_path):
    """Remove arquivos antigos de desenvolvimento após reorganização."""
    base = Path(base_path)

    # Arquivos antigos para remover
    old_files = [
        "reorganize_project.py",  # Script antigo
        "README.txt",  # README antigo
        "turbofan-daviseemann.zip",  # Arquivo zip
        "HISTORICO_ESCOLAR_DAVI_GRUMICHE_SEEMANN.pdf.PDF",  # Arquivo pessoal
        "Relatório_final_Aprendizado_de_maquina_DaviSeemann (5).pdf",  # Movido para docs/
        "Trabalho final.pdf",  # Movido para docs/
    ]

    # Notebooks antigos que foram reorganizados
    old_notebooks = [
        "notebooks/EDA.ipynb",
        "notebooks/pre-processing.ipynb",
        "notebooks/MLP.ipynb",
        "notebooks/MLP-1.ipynb",
        "notebooks/MLP-2.ipynb",
        "notebooks/MLP-3-BASE.ipynb",
        "notebooks/MLP-artigo.ipynb",
        "notebooks/MLP-3-FD002.ipynb",
        "notebooks/MLP-3-lr-tunning.ipynb",
        "notebooks/MLP-3-outras-janelas.ipynb",
        "notebooks/MLP-3-sem-clipping.ipynb",
        "notebooks/MLP_4.ipynb",
        "notebooks/MLP_5.ipynb",
        "notebooks/MLP-3.ipynb",
    ]

    # Diretórios antigos para remover (se vazios)
    old_directories = [
        "apresentação",
        "dados",
        "relatorios",
        "notebooks/Analises finais",
    ]

    print("\n🧹 Removendo arquivos antigos...")

    # Remover arquivos
    for file_path in old_files:
        full_path = base / file_path
        if full_path.exists():
            full_path.unlink()
            print(f"  ✓ Removido: {file_path}")

    # Remover notebooks antigos
    for notebook_path in old_notebooks:
        full_path = base / notebook_path
        if full_path.exists():
            full_path.unlink()
            print(f"  ✓ Removido: {notebook_path}")

    # Remover diretórios vazios
    for dir_path in old_directories:
        full_path = base / dir_path
        if full_path.exists():
            try:
                # Remove arquivos restantes primeiro
                for item in full_path.rglob("*"):
                    if item.is_file():
                        item.unlink()

                # Remove diretórios vazios recursivamente
                for item in sorted(full_path.rglob("*"), reverse=True):
                    if item.is_dir() and not any(item.iterdir()):
                        item.rmdir()

                # Remove o diretório principal se vazio
                if not any(full_path.iterdir()):
                    full_path.rmdir()
                    print(f"  ✓ Removido diretório: {dir_path}")
                else:
                    print(f"  ⚠️ Diretório não vazio: {dir_path}")

            except Exception as e:
                print(f"  ❌ Erro ao remover {dir_path}: {e}")


def main():
    """Executa a reorganização completa."""
    base_path = Path(__file__).parent

    print("🎯 Reorganização Limpa do Projeto")
    print("=" * 50)

    response = input(
        "\n⚠️  Esta operação irá reorganizar todo o projeto. Continuar? (y/N): "
    )
    if response.lower() != "y":
        print("❌ Operação cancelada.")
        return

    try:
        create_clean_structure(base_path)
        organize_notebooks_by_tier(base_path)
        organize_documentation(base_path)
        organize_data_files(base_path)
        create_tier_readme_files(base_path)
        create_docs_structure(base_path)
        create_project_structure_doc(base_path)

        # Perguntar se deve remover arquivos antigos
        cleanup_response = input(
            "\n🧹 Remover arquivos antigos de desenvolvimento? (y/N): "
        )
        if cleanup_response.lower() == "y":
            cleanup_old_files(base_path)

        print("\n✅ Reorganização concluída!")
        print("\n📋 Estrutura criada:")
        print("  📁 notebooks/ - Organizados em 4 tiers")
        print("  📁 docs/ - Documentação centralizada")
        print("  📁 src/ - Código modular")
        print("  📁 data/ - Dados organizados")
        print("  📁 results/ - Resultados e artefatos")
        print("  📁 tools/ - Ferramentas de desenvolvimento")

        print("\n🎯 Próximos passos:")
        print("1. Revisar notebooks copiados nos tiers")
        print("2. Testar imports da estrutura src/")
        print("3. Fazer commit das mudanças")
        print("4. Atualizar .gitignore se necessário")

    except Exception as e:
        print(f"\n❌ Erro durante reorganização: {e}")


if __name__ == "__main__":
    main()
