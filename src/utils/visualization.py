"""
Funções de visualização para análise de dados e resultados.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


def plot_rul_by_engine(df, engines_to_plot=5, figsize=(10, 6)):
    """
    Plota o RUL ao longo do tempo para algumas engines.

    Args:
        df: DataFrame com colunas engine_id, cycle, RUL
        engines_to_plot: Número de engines para plotar
        figsize: Tamanho da figura
    """
    # Selecionar engines para visualizar
    engine_ids = df["engine_id"].unique()[:engines_to_plot]

    plt.figure(figsize=figsize)

    for engine_id in engine_ids:
        engine_data = df[df["engine_id"] == engine_id]
        plt.plot(
            engine_data["cycle"],
            engine_data["RUL"],
            label=f"Engine {engine_id}",
            marker="o",
            markersize=2,
        )

    plt.xlabel("Cycle")
    plt.ylabel("RUL")
    plt.title("RUL por Engine ID")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def plot_learning_curves(history, figsize=(15, 12)):
    """
    Plota curvas de aprendizagem do treinamento.

    Args:
        history: History object do Keras ou dict com métricas
        figsize: Tamanho da figura
    """
    if hasattr(history, "history"):
        history = history.history

    plt.figure(figsize=figsize)

    # Plot Loss (MSE)
    plt.subplot(3, 1, 1)
    plt.plot(history["loss"], label="Treino", linewidth=2)
    if "val_loss" in history:
        plt.plot(history["val_loss"], label="Validação", linewidth=2)
    plt.title("Loss (MSE)", fontsize=14)
    plt.xlabel("Epochs")
    plt.ylabel("MSE")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale("log")

    # Plot RMSE
    if "rmse" in history:
        plt.subplot(3, 1, 2)
        plt.plot(history["rmse"], label="Treino", linewidth=2)
        if "val_rmse" in history:
            plt.plot(history["val_rmse"], label="Validação", linewidth=2)
            # Show best and last val_rmse
            best_rmse = np.min(history["val_rmse"])
            last_rmse = history["val_rmse"][-1]
            plt.title(
                f"RMSE - Best: {best_rmse:.2f} | Last: {last_rmse:.2f}", fontsize=14
            )
        plt.xlabel("Epochs")
        plt.ylabel("RMSE")
        plt.legend()
        plt.grid(True, alpha=0.3)

    # Plot NASA Score
    if "rul_health_score" in history:
        plt.subplot(3, 1, 3)
        plt.plot(history["rul_health_score"], label="Treino", linewidth=2)
        if "val_rul_health_score" in history:
            plt.plot(history["val_rul_health_score"], label="Validação", linewidth=2)
            # Show best and last val_rhs
            best_rhs = np.min(history["val_rul_health_score"])
            last_rhs = history["val_rul_health_score"][-1]
            plt.title(
                f"NASA Score - Best: {best_rhs:.2f} | Last: {last_rhs:.2f}", fontsize=14
            )
        plt.xlabel("Epochs")
        plt.ylabel("NASA Score")
        plt.legend()
        plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_rul_predictions(df, start=1, stop=5, dataset_type="test", figsize=(12, 8)):
    """
    Plota comparação entre RUL real e predito por engine.

    Args:
        df: DataFrame com colunas engine_id, cycle/last_cycle, RUL, RUL_PREDICTED
        start: Engine inicial para plotar
        stop: Engine final para plotar
        dataset_type: Tipo do dataset (para título)
        figsize: Tamanho da figura
    """
    engine_ids = df["engine_id"].unique()[start - 1 : stop]

    # Determinar coluna de ciclo
    cycle_col = "last_cycle" if "last_cycle" in df.columns else "cycle"

    plt.figure(figsize=figsize)

    for engine_id in engine_ids:
        engine_data = df[df["engine_id"] == engine_id]
        plt.plot(
            engine_data[cycle_col],
            engine_data["RUL"],
            label=f"Engine {engine_id} - Real",
            linestyle="-",
            linewidth=2,
        )
        plt.plot(
            engine_data[cycle_col],
            engine_data["RUL_PREDICTED"],
            label=f"Engine {engine_id} - Predicted",
            linestyle="--",
            linewidth=2,
        )

    plt.xlabel("Cycle")
    plt.ylabel("RUL")
    plt.title(f"Comparação RUL Real vs. Predito ({dataset_type.capitalize()} Set)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def plot_prediction_errors(y_true, y_pred, figsize=(15, 5)):
    """
    Plota análise de erros de predição.

    Args:
        y_true: Valores verdadeiros
        y_pred: Valores preditos
        figsize: Tamanho da figura
    """
    errors = y_true - y_pred

    plt.figure(figsize=figsize)

    # Histograma dos erros
    plt.subplot(1, 3, 1)
    plt.hist(errors, bins=50, alpha=0.7, color="skyblue", edgecolor="black")
    plt.title("Histograma dos Erros\n(y_true - y_pred)")
    plt.xlabel("Erro")
    plt.ylabel("Frequência")
    plt.grid(True, alpha=0.3)

    # Scatter plot: Real vs Predito
    plt.subplot(1, 3, 2)
    plt.scatter(y_true, y_pred, alpha=0.6, color="red")

    # Linha de predição perfeita
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    plt.plot(
        [min_val, max_val],
        [min_val, max_val],
        "k--",
        linewidth=2,
        label="Predição Perfeita",
    )

    plt.xlabel("RUL Real")
    plt.ylabel("RUL Predito")
    plt.title("Real vs. Predito")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Residuals plot
    plt.subplot(1, 3, 3)
    plt.scatter(y_pred, errors, alpha=0.6, color="green")
    plt.axhline(y=0, color="red", linestyle="--", linewidth=2)
    plt.xlabel("RUL Predito")
    plt.ylabel("Resíduos")
    plt.title("Gráfico de Resíduos")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_test_results_summary(df_results, figsize=(15, 10)):
    """
    Plota resumo completo dos resultados no conjunto de teste.

    Args:
        df_results: DataFrame com engine_id, RUL_Actual, RUL_Predicted
        figsize: Tamanho da figura
    """
    plt.figure(figsize=figsize)

    # Plot 1: RUL vs Engine ID
    plt.subplot(2, 2, 1)
    plt.plot(
        df_results["engine_id"],
        df_results["RUL_Actual"],
        "o-",
        label="Actual RUL",
        linewidth=2,
        markersize=4,
    )
    plt.plot(
        df_results["engine_id"],
        df_results["RUL_Predicted"],
        "x--",
        label="Predicted RUL",
        linewidth=2,
        markersize=6,
    )
    plt.xlabel("Engine ID")
    plt.ylabel("RUL")
    plt.title("Actual vs. Predicted RUL")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 2: Prediction Error vs Engine ID
    errors = df_results["RUL_Actual"] - df_results["RUL_Predicted"]
    plt.subplot(2, 2, 2)
    plt.plot(df_results["engine_id"], errors, "o-", color="red", linewidth=2)
    plt.axhline(0, color="black", linestyle="--", linewidth=1)
    plt.xlabel("Engine ID")
    plt.ylabel("Erro (Actual - Predicted)")
    plt.title("Erro de Predição por Engine")
    plt.grid(True, alpha=0.3)

    # Plot 3: Histograma dos erros
    plt.subplot(2, 2, 3)
    plt.hist(errors, bins=20, alpha=0.7, color="lightblue", edgecolor="black")
    plt.xlabel("Erro")
    plt.ylabel("Frequência")
    plt.title("Distribuição dos Erros")
    plt.grid(True, alpha=0.3)

    # Plot 4: Real vs Predito scatter
    plt.subplot(2, 2, 4)
    plt.scatter(
        df_results["RUL_Actual"], df_results["RUL_Predicted"], alpha=0.7, color="purple"
    )

    min_val = min(df_results["RUL_Actual"].min(), df_results["RUL_Predicted"].min())
    max_val = max(df_results["RUL_Actual"].max(), df_results["RUL_Predicted"].max())
    plt.plot([min_val, max_val], [min_val, max_val], "k--", linewidth=2)

    plt.xlabel("RUL Actual")
    plt.ylabel("RUL Predicted")
    plt.title("Scatter: Actual vs Predicted")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_sensor_correlation_matrix(df, sensor_cols, figsize=(12, 10)):
    """
    Plota matriz de correlação dos sensores.

    Args:
        df: DataFrame com dados dos sensores
        sensor_cols: Lista de colunas de sensores
        figsize: Tamanho da figura
    """
    correlation_matrix = df[sensor_cols].corr()

    plt.figure(figsize=figsize)
    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
    )
    plt.title("Matriz de Correlação dos Sensores")
    plt.tight_layout()
    plt.show()


def plot_sensor_degradation(df, sensor_cols, engines_to_plot=3, figsize=(15, 10)):
    """
    Plota degradação dos sensores ao longo do tempo.

    Args:
        df: DataFrame com dados
        sensor_cols: Lista de sensores para plotar
        engines_to_plot: Número de engines para mostrar
        figsize: Tamanho da figura
    """
    n_sensors = len(sensor_cols)
    n_cols = 3
    n_rows = (n_sensors + n_cols - 1) // n_cols

    plt.figure(figsize=figsize)

    for i, sensor in enumerate(sensor_cols[:12]):  # Limitar a 12 sensores
        plt.subplot(n_rows, n_cols, i + 1)

        for engine_id in df["engine_id"].unique()[:engines_to_plot]:
            engine_data = df[df["engine_id"] == engine_id]
            plt.plot(
                engine_data["cycle"],
                engine_data[sensor],
                label=f"Engine {engine_id}",
                alpha=0.7,
            )

        plt.xlabel("Cycle")
        plt.ylabel(sensor)
        plt.title(f"Sensor {sensor}")
        plt.grid(True, alpha=0.3)
        if i == 0:
            plt.legend()

    plt.tight_layout()
    plt.show()
