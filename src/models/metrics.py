"""
Métricas customizadas para avaliação de modelos RUL.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K


def root_mean_squared_error(y_true, y_pred):
    """
    Calcula RMSE entre valores reais e preditos.

    Args:
        y_true: Valores verdadeiros
        y_pred: Valores preditos

    Returns:
        RMSE como tensor TensorFlow
    """
    # Converte os inputs para float32 explicitamente
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)

    squared_diff = tf.square(y_pred - y_true)
    mean_squared = tf.reduce_mean(squared_diff)
    rmse = tf.sqrt(mean_squared)
    return rmse


def rul_health_score(y_true, y_pred):
    """
    Calcula o NASA Health Score (RHS) para predições RUL.
    Penaliza mais predições tarde (late predictions) do que cedo (early predictions).

    Args:
        y_true: Valores verdadeiros de RUL
        y_pred: Valores preditos de RUL

    Returns:
        Health Score médio como tensor TensorFlow
    """
    # Garante vetores 1D float32
    y_true = tf.cast(tf.reshape(y_true, [-1]), tf.float32)
    y_pred = tf.cast(tf.reshape(y_pred, [-1]), tf.float32)

    d = y_pred - y_true

    # Penalização assimétrica:
    # - Late predictions (d > 0): mais penalizado (exp(d/10) - 1)
    # - Early predictions (d < 0): menos penalizado (exp(-d/13) - 1)
    score = tf.where(d < 0.0, tf.exp(-d / 13.0) - 1.0, tf.exp(d / 10.0) - 1.0)

    return tf.reduce_mean(score)


def rul_health_score_numpy(y_true, y_pred):
    """
    Versão NumPy do NASA Health Score para avaliação manual.

    Args:
        y_true: Array NumPy com valores verdadeiros
        y_pred: Array NumPy com valores preditos

    Returns:
        Health Score médio
    """
    # Ensure inputs are numpy arrays and of float type
    y_true = np.asarray(y_true, dtype=np.float32)
    y_pred = np.asarray(y_pred, dtype=np.float32)

    diffs = y_pred - y_true
    scores = np.where(
        diffs < 0, np.exp(-diffs / 13.0) - 1.0, np.exp(diffs / 10.0) - 1.0
    )
    return np.mean(scores)


def mean_absolute_percentage_error(y_true, y_pred):
    """
    Calcula MAPE (Mean Absolute Percentage Error).

    Args:
        y_true: Valores verdadeiros
        y_pred: Valores preditos

    Returns:
        MAPE como tensor TensorFlow
    """
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)

    # Evita divisão por zero
    y_true = tf.where(tf.equal(y_true, 0), tf.ones_like(y_true) * 1e-8, y_true)

    return tf.reduce_mean(tf.abs((y_true - y_pred) / y_true)) * 100.0


def prognostic_horizon_error(y_true, y_pred, threshold=30):
    """
    Calcula erro no horizonte prognóstico.
    Mede quantas predições estão dentro do threshold acceptable.

    Args:
        y_true: Valores verdadeiros
        y_pred: Valores preditos
        threshold: Threshold de erro aceitável

    Returns:
        Proporção de predições dentro do threshold
    """
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)

    errors = tf.abs(y_true - y_pred)
    within_threshold = tf.cast(errors <= threshold, tf.float32)

    return tf.reduce_mean(within_threshold)


class RULMetrics:
    """
    Classe para calcular múltiplas métricas RUL de uma vez.
    """

    @staticmethod
    def calculate_all_metrics(y_true, y_pred, return_dict=True):
        """
        Calcula todas as métricas relevantes para RUL.

        Args:
            y_true: Valores verdadeiros
            y_pred: Valores preditos
            return_dict: Se deve retornar dicionário ou tupla

        Returns:
            Dicionário ou tupla com métricas
        """
        y_true = np.asarray(y_true, dtype=np.float32)
        y_pred = np.asarray(y_pred, dtype=np.float32)

        # Métricas básicas
        mse = np.mean((y_true - y_pred) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y_true - y_pred))

        # Métricas específicas para RUL
        rhs = rul_health_score_numpy(y_true, y_pred)

        # MAPE (evitando divisão por zero)
        y_true_safe = np.where(y_true == 0, 1e-8, y_true)
        mape = np.mean(np.abs((y_true - y_pred) / y_true_safe)) * 100

        # Prognostic horizon (% dentro de 30 ciclos)
        ph_30 = np.mean(np.abs(y_true - y_pred) <= 30) * 100

        if return_dict:
            return {
                "MSE": mse,
                "RMSE": rmse,
                "MAE": mae,
                "RHS": rhs,
                "MAPE": mape,
                "PH_30": ph_30,
            }
        else:
            return mse, rmse, mae, rhs, mape, ph_30
