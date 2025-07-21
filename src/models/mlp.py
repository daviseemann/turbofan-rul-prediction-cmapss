"""
Módulo com arquiteturas de modelos para predição RUL.
"""

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input, Layer
from tensorflow.keras.regularizers import l1_l2
from tensorflow.keras.metrics import MeanSquaredError, RootMeanSquaredError


class MinMaxScalerLayer(Layer):
    """
    Camada customizada para normalização Min-Max para [-1, 1].
    """

    def __init__(self, mins, denom, **kwargs):
        super().__init__(**kwargs)
        # Convert numpy arrays to TensorFlow tensors for saving
        self.mins = tf.constant(mins, dtype=tf.float32)
        self.denom = tf.constant(denom, dtype=tf.float32)

    def call(self, inputs):
        return 2.0 * (inputs - self.mins) / self.denom - 1.0

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                # Convert tensors back to numpy arrays for serialization
                "mins": self.mins.numpy().tolist(),
                "denom": self.denom.numpy().tolist(),
            }
        )
        return config


def create_mlp_model(
    input_dim,
    minmax_layer,
    lr=0.001,
    l1=0.1,
    l2=0.2,
    hidden_units=20,
    n_hidden_layers=2,
):
    """
    Cria modelo MLP para predição RUL.

    Args:
        input_dim: Dimensão de entrada
        minmax_layer: Camada de normalização
        lr: Learning rate
        l1: Regularização L1
        l2: Regularização L2
        hidden_units: Unidades por camada oculta
        n_hidden_layers: Número de camadas ocultas

    Returns:
        Modelo compilado
    """
    from .metrics import root_mean_squared_error, rul_health_score

    reg = l1_l2(l1=l1, l2=l2)

    layers = [
        Input(shape=(input_dim,)),
        minmax_layer,
    ]

    # Adicionar camadas ocultas
    for _ in range(n_hidden_layers):
        layers.append(
            Dense(
                hidden_units,
                activation="relu",
                kernel_regularizer=reg,
                bias_regularizer=reg,
            )
        )

    # Camada de saída
    layers.append(
        Dense(1, activation="linear", kernel_regularizer=reg, bias_regularizer=reg)
    )

    model = Sequential(layers, name="MLP_RUL_Predictor")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
        loss="mse",
        metrics=[
            MeanSquaredError(name="mse"),
            RootMeanSquaredError(name="rmse"),
            rul_health_score,
        ],
    )
    return model


def create_deep_mlp_model(input_dim, minmax_layer, lr=0.001):
    """
    Cria modelo MLP mais profundo baseado no artigo.
    """
    from .metrics import rul_health_score

    reg = l1_l2(l1=0.1, l2=0.2)

    model = Sequential(
        [
            Input(shape=(input_dim,)),
            minmax_layer,
            Dense(128, activation="relu", kernel_regularizer=reg),
            Dense(64, activation="relu", kernel_regularizer=reg),
            Dense(32, activation="relu", kernel_regularizer=reg),
            Dense(16, activation="relu", kernel_regularizer=reg),
            Dense(1, activation="linear", kernel_regularizer=reg),
        ],
        name="Deep_MLP_RUL_Predictor",
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
        loss="mse",
        metrics=[
            MeanSquaredError(name="mse"),
            RootMeanSquaredError(name="rmse"),
            rul_health_score,
        ],
    )
    return model


def create_minmax_layer(X_train):
    """
    Cria camada de normalização Min-Max baseada nos dados de treino.

    Args:
        X_train: Dados de treino

    Returns:
        MinMaxScalerLayer configurada
    """
    mins = X_train.min(axis=0).astype("float32")
    maxs = X_train.max(axis=0).astype("float32")
    denom = maxs - mins
    return MinMaxScalerLayer(mins, denom, name="minmax_-1_1")
