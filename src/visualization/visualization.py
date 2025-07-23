import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plots(history, xlim=None, ylim=None):
    if hasattr(history, "history"):
        history = history.history
    plt.figure(figsize=(14, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history["loss"], ".-", label="Train loss")
    if "val_loss" in history.keys():
        plt.plot(history["val_loss"], ".-", label="Val loss")
    plt.xlabel("Epochs")
    plt.legend()
    plt.yscale("log")
    plt.grid(which="both")
    plt.subplot(1, 2, 2)
    plt.plot(history["rmse"], ".-", label="Train rmse")
    plt.xlabel("Epochs")
    if "val_rmse" in history.keys():  # Check for val_rmse explicitly
        plt.plot(history["val_rmse"], ".-", label="Val rmse")
        # Correct title to show actual RMSE values and best (minimum) val_rmse
        plt.title(
            f"Val rmse: {np.min(history['val_rmse']):.2f} (best) | {history['val_rmse'][-1]:.2f} (last)"
        )
    # if 'val_rul_health_score' in history.keys(): # Check for val_rmse explicitly
    #   plt.plot(history['val_rul_health_score'], '.-', label='val rhs')
    #   # Correct title to show actual RMSE values and best (minimum) val_rmse
    #   plt.title(f"Val rhs: {np.min(history['val_rul_health_score']):.2f} (best) | {history['val_rul_health_score'][-1]:.2f} (last)");
    plt.legend()
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.grid()


def plot_rul_by_engine(df, engines_to_plot=5):
    """Plota o RUL ao longo do tempo para algumas engines"""
    # Selecionar engines para visualizar
    engine_ids = df["engine_id"].unique()[:engines_to_plot]

    plt.figure(figsize=(8, 6))

    for engine_id in engine_ids:
        engine_data = df[df["engine_id"] == engine_id]
        plt.plot(engine_data["cycle"], engine_data["RUL"], label=f"Engine {engine_id}")

    plt.xlabel("Cycle")
    plt.ylabel("RUL")
    plt.title("RUL por Engine ID")
    plt.legend()
    plt.grid(True)
    plt.show()