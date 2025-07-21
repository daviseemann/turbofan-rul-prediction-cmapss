#!/usr/bin/env python3
"""
Script exemplo de uso da nova estrutura modular.
Demonstra como usar os módulos criados para treinar e avaliar um modelo RUL.
"""

import numpy as np
import os
import sys

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from src.data import (
    load_data,
    create_rul_labels,
    create_all_windows,
    split_windows_by_engine,
    DEFAULT_SENSORS,
)
from src.models import create_mlp_model, create_minmax_layer, RULMetrics
from src.utils import plot_learning_curves, plot_test_results_summary


def main():
    """Exemplo completo de uso dos módulos."""

    print("🚀 Exemplo de uso da estrutura modular")
    print("=" * 50)

    # 1. Carregar dados
    print("📊 1. Carregando dados...")
    try:
        df_train = load_data("../data/raw/train_FD001.txt")
        print(f"   ✓ Dados carregados: {df_train.shape}")
    except FileNotFoundError:
        print("   ❌ Arquivos de dados não encontrados!")
        print("   💡 Certifique-se de que os dados estão em ../data/raw/")
        return

    # 2. Pré-processamento
    print("\n🔧 2. Pré-processamento...")
    df_train = create_rul_labels(df_train, Re=129)

    # Selecionar sensores
    features_to_keep = ["engine_id", "cycle"] + DEFAULT_SENSORS
    df_train = df_train[features_to_keep]
    print(f"   ✓ Sensores selecionados: {len(DEFAULT_SENSORS)}")

    # 3. Criar janelas temporais
    print("\n🪟 3. Criando janelas temporais...")
    window_size = 24
    window_stride = 1

    df_all_windows = create_all_windows(
        df_train, window_size, window_stride, DEFAULT_SENSORS
    )
    print(f"   ✓ Janelas criadas: {len(df_all_windows)}")

    # 4. Split train/val
    print("\n✂️ 4. Split train/val...")
    df_train_windows, df_val_windows = split_windows_by_engine(
        df_all_windows, test_size=0.2, random_state=42
    )

    # 5. Preparar arrays
    print("\n📦 5. Preparando arrays...")
    X_train = np.array(list(df_train_windows["data_vector"]))
    y_train = df_train_windows["RUL"].values
    X_val = np.array(list(df_val_windows["data_vector"]))
    y_val = df_val_windows["RUL"].values

    print(f"   ✓ X_train: {X_train.shape}")
    print(f"   ✓ y_train: {y_train.shape}")
    print(f"   ✓ X_val: {X_val.shape}")
    print(f"   ✓ y_val: {y_val.shape}")

    # 6. Criar e treinar modelo
    print("\n🧠 6. Criando e treinando modelo...")

    # Criar camada de normalização
    minmax_layer = create_minmax_layer(X_train)

    # Criar modelo
    input_dim = X_train.shape[1]
    model = create_mlp_model(
        input_dim=input_dim, minmax_layer=minmax_layer, lr=0.001, l1=0.1, l2=0.2
    )

    print(f"   ✓ Modelo criado com {input_dim} features de entrada")

    # Treinar (apenas algumas épocas para exemplo)
    print("   🏃 Treinando modelo...")
    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=10,  # Poucas épocas para exemplo
        batch_size=128,
        verbose=1,
    )

    # 7. Avaliar modelo
    print("\n📈 7. Avaliando modelo...")

    # Predições
    y_pred_val = model.predict(X_val).flatten()

    # Calcular métricas
    metrics = RULMetrics.calculate_all_metrics(y_val, y_pred_val)

    print("   📊 Métricas de validação:")
    for metric, value in metrics.items():
        print(f"      {metric}: {value:.2f}")

    # 8. Visualizações
    print("\n📊 8. Gerando visualizações...")

    try:
        # Curvas de aprendizagem
        plot_learning_curves(history)
        print("   ✓ Curvas de aprendizagem plotadas")

        # Preparar DataFrame de resultados
        import pandas as pd

        df_results = pd.DataFrame(
            {
                "engine_id": df_val_windows["engine_id"].values,
                "RUL_Actual": y_val,
                "RUL_Predicted": y_pred_val,
            }
        )

        # Resultados do teste
        plot_test_results_summary(df_results)
        print("   ✓ Resumo de resultados plotado")

    except Exception as e:
        print(f"   ⚠️ Erro nas visualizações: {e}")

    print("\n✅ Exemplo concluído com sucesso!")
    print("💡 Agora você pode usar os módulos em seus próprios notebooks!")


if __name__ == "__main__":
    main()
