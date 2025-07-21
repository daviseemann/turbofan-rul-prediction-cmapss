#!/usr/bin/env python3
"""
Script para remover arquivos antigos de desenvolvimento e manter apenas a estrutura limpa.
"""

import shutil
from pathlib import Path


def remove_old_development_files(base_path):
    """Remove todos os arquivos antigos de desenvolvimento."""
    base = Path(base_path)

    print("🧹 Removendo arquivos antigos de desenvolvimento...")
    print("=" * 60)

    # 1. Arquivos antigos na raiz
    old_root_files = [
        "reorganize_project.py",
        "README.txt",
        "turbofan-daviseemann.zip",
        "HISTORICO_ESCOLAR_DAVI_GRUMICHE_SEEMANN.pdf.PDF",
        "Relatório_final_Aprendizado_de_maquina_DaviSeemann (5).pdf",
        "Trabalho final.pdf",
    ]

    print("\n📄 Removendo arquivos da raiz...")
    for file_name in old_root_files:
        file_path = base / file_name
        if file_path.exists():
            file_path.unlink()
            print(f"  ✓ {file_name}")
        else:
            print(f"  ⚪ {file_name} (não encontrado)")

    # 2. Notebooks antigos dispersos
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

    print("\n📓 Removendo notebooks antigos...")
    for notebook in old_notebooks:
        notebook_path = base / notebook
        if notebook_path.exists():
            notebook_path.unlink()
            print(f"  ✓ {notebook}")
        else:
            print(f"  ⚪ {notebook} (não encontrado)")

    # 3. Diretórios antigos completos
    old_directories = [
        "apresentação",
        "dados",
        "relatorios",
        "notebooks/Analises finais",
    ]

    print("\n📁 Removendo diretórios antigos...")
    for dir_name in old_directories:
        dir_path = base / dir_name
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"  ✓ {dir_name}/ (completo)")
            except Exception as e:
                print(f"  ❌ Erro ao remover {dir_name}: {e}")
        else:
            print(f"  ⚪ {dir_name}/ (não encontrado)")

    print("\n✅ Limpeza concluída!")


def show_current_structure(base_path):
    """Mostra a estrutura atual do projeto."""
    base = Path(base_path)

    print("\n📁 Estrutura atual do projeto:")
    print("=" * 40)

    # Mostrar apenas diretórios principais e alguns arquivos importantes
    important_items = [
        "src/",
        "notebooks/",
        "docs/",
        "data/",
        "models/",
        "results/",
        "tools/",
        "tests/",
        "README.md",
        "requirements.txt",
        "LICENSE",
        ".gitignore",
    ]

    for item in important_items:
        item_path = base / item
        if item_path.exists():
            if item.endswith("/"):
                # É um diretório
                sub_items = list(item_path.iterdir())
                print(f"  📁 {item} ({len(sub_items)} items)")
            else:
                # É um arquivo
                print(f"  📄 {item}")
        else:
            print(f"  ⚪ {item} (não encontrado)")


def main():
    """Executa a limpeza dos arquivos antigos."""
    base_path = Path(__file__).parent

    print("🎯 Limpeza de Arquivos Antigos")
    print("=" * 40)

    # Mostrar estrutura atual
    show_current_structure(base_path)

    # Confirmar limpeza
    print("\n⚠️  Esta operação irá REMOVER permanentemente arquivos antigos!")
    print("   Certifique-se de que já executou o script de reorganização.")
    response = input("\nContinuar com a limpeza? (y/N): ")

    if response.lower() != "y":
        print("❌ Limpeza cancelada.")
        return

    # Executar limpeza
    try:
        remove_old_development_files(base_path)

        # Mostrar estrutura final
        print("\n" + "=" * 60)
        show_current_structure(base_path)

        print("\n🎉 Projeto limpo e organizado!")
        print("\n💡 Próximos passos recomendados:")
        print("   1. Revisar a estrutura final")
        print("   2. Testar os imports dos módulos src/")
        print("   3. Fazer commit das mudanças")
        print("   4. Atualizar .gitignore se necessário")

    except Exception as e:
        print(f"\n❌ Erro durante limpeza: {e}")
        print("   Reverta as mudanças se necessário.")


if __name__ == "__main__":
    main()
