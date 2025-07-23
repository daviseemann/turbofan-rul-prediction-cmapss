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
