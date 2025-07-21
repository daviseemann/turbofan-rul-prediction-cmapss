"""
Módulo de pré-processamento de dados para predição RUL de motores turbofan.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def load_data(file_path, column_names=None):
    """
    Carrega dados do dataset C-MAPSS.

    Args:
        file_path: Caminho para o arquivo de dados
        column_names: Nomes das colunas (padrão: colunas do C-MAPSS)

    Returns:
        DataFrame com os dados carregados
    """
    if column_names is None:
        # Default column names based on the C-MAPSS dataset documentation
        column_names = (
            ["engine_id", "cycle"]
            + [f"op{i}" for i in range(1, 4)]
            + [f"s{i}" for i in range(1, 22)]
        )
    # Fix: Use engine='python' to avoid ParserWarning with regex separators
    return pd.read_csv(
        file_path, sep=r"\s+", engine="python", header=None, names=column_names
    )


def create_rul_labels(df, Re, clip_at_zero=True):
    """
    Cria os rótulos RUL usando o modelo de degradação linear por partes.

    Args:
        df: DataFrame com dados dos engines
        Re: Valor máximo de RUL (early life constant)
        clip_at_zero: Se deve clipar valores negativos em 0

    Returns:
        DataFrame com coluna RUL adicionada
    """
    grouped = df.groupby("engine_id")["cycle"].max().reset_index()
    grouped.columns = ["engine_id", "max_cycle"]

    df = df.merge(grouped, on="engine_id", how="left")
    df["RUL"] = df["max_cycle"] - df["cycle"]

    # Aplica o modelo de degradação linear por partes
    df["RUL"] = np.where(df["RUL"] > Re, Re, df["RUL"])

    if clip_at_zero:
        df["RUL"] = np.where(df["RUL"] < 0, 0, df["RUL"])

    return df.drop(columns=["max_cycle"])


def create_rul_test(df_test, df_rul, Re=129):
    """
    Cria os rótulos RUL para dados de teste usando RUL verdadeiro do último ciclo.

    Args:
        df_test: DataFrame com dados de teste (engine_id, cycle, sensores)
        df_rul: DataFrame com RUL verdadeiro do último ciclo por engine
        Re: Valor máximo de RUL (early life constant)

    Returns:
        DataFrame com coluna RUL adicionada
    """
    df_result = df_test.copy()

    # Para cada engine, calcular RUL baseado no RUL verdadeiro do último ciclo
    for engine_id in df_test["engine_id"].unique():
        # Dados desta engine
        engine_data = df_test[df_test["engine_id"] == engine_id].copy()

        # RUL verdadeiro do último ciclo
        true_final_rul = df_rul[df_rul["engine_id"] == engine_id]["RUL"].iloc[0]

        # Último ciclo desta engine
        max_cycle = engine_data["cycle"].max()

        # Calcular RUL para cada ciclo: RUL = true_final_rul + (max_cycle - current_cycle)
        engine_mask = df_result["engine_id"] == engine_id
        df_result.loc[engine_mask, "RUL"] = true_final_rul + (
            max_cycle - df_result.loc[engine_mask, "cycle"]
        )

    # Aplicar o modelo de degradação linear por partes (clipar em Re)
    df_result["RUL"] = np.where(df_result["RUL"] > Re, Re, df_result["RUL"])

    return df_result


def create_time_windows(df, window_size, window_stride, sensor_cols):
    """
    Cria janelas temporais dos dados dos sensores e retorna um DataFrame com info da janela.

    Args:
        df: DataFrame com dados dos engines
        window_size: Tamanho da janela temporal
        window_stride: Passo entre janelas
        sensor_cols: Colunas dos sensores

    Returns:
        DataFrame com janelas temporais
    """
    sequences = []
    labels = []
    engine_ids = []
    last_cycles = []

    for engine_id in df["engine_id"].unique():
        engine_data = df[df["engine_id"] == engine_id]
        sensor_data = engine_data[sensor_cols].values
        rul_data = engine_data["RUL"].values

        # Cria janelas deslizantes
        for i in range(0, len(engine_data) - window_size + 1, window_stride):
            window = sensor_data[i : i + window_size]
            label = rul_data[i + window_size - 1]
            sequences.append(window)
            labels.append(label)
            engine_ids.append(engine_id)
            last_cycles.append(engine_data["cycle"].iloc[i + window_size - 1])

    # Flatten sequences for MLP input
    n_samples = len(sequences)
    n_timesteps = window_size
    n_features = len(sensor_cols)
    flattened_sequences = np.array(sequences).reshape(
        (n_samples, n_timesteps * n_features)
    )

    df_windows = pd.DataFrame(
        {
            "engine_id": engine_ids,
            "last_cycle": last_cycles,
            "data_vector": list(flattened_sequences),
            "RUL": labels,
        }
    )

    return df_windows


def create_all_windows(df, window_size, window_stride, sensor_cols):
    """
    Cria janelas temporais em todo o dataset.

    Args:
        df: DataFrame com dados dos engines
        window_size: Tamanho da janela temporal
        window_stride: Passo entre janelas
        sensor_cols: Colunas dos sensores

    Returns:
        DataFrame com todas as janelas temporais
    """
    return create_time_windows(df, window_size, window_stride, sensor_cols)


def split_windows_by_engine(df_windows, test_size=0.2, random_state=42):
    """
    Faz split das janelas por engine_id (garante que janelas do mesmo engine ficam juntas).

    Args:
        df_windows: DataFrame com janelas temporais
        test_size: Proporção para validação/teste
        random_state: Seed para reprodutibilidade

    Returns:
        df_train_windows, df_val_windows: DataFrames separados
    """
    # Split baseado em engine_id
    unique_engines = df_windows["engine_id"].unique()
    train_engines, val_engines = train_test_split(
        unique_engines, test_size=test_size, random_state=random_state, shuffle=True
    )

    # Separar janelas por engine
    df_train_windows = df_windows[df_windows["engine_id"].isin(train_engines)].copy()
    df_val_windows = df_windows[df_windows["engine_id"].isin(val_engines)].copy()

    print(
        f"Engines treino: {len(train_engines)} | Engines validação: {len(val_engines)}"
    )
    print(
        f"Janelas treino: {len(df_train_windows)} | Janelas validação: {len(df_val_windows)}"
    )

    return df_train_windows, df_val_windows


def train_val_split(df, test_size=0.2, shuffle=True, random_state=None):
    """
    Divide dados por engine_id para treino e validação.

    Args:
        df: DataFrame com dados
        test_size: Proporção para validação
        shuffle: Se deve embaralhar
        random_state: Seed para reprodutibilidade

    Returns:
        df_train, df_val: DataFrames de treino e validação
    """
    unique_engines = np.unique(df["engine_id"])
    train_engines, val_engines = train_test_split(
        unique_engines, test_size=test_size, shuffle=shuffle, random_state=random_state
    )

    df_train = df[df["engine_id"].isin(train_engines)]
    df_val = df[df["engine_id"].isin(val_engines)]
    return df_train, df_val


def select_sensors(df, sensor_list):
    """
    Seleciona apenas os sensores especificados.

    Args:
        df: DataFrame com todos os sensores
        sensor_list: Lista de sensores a manter

    Returns:
        DataFrame filtrado
    """
    features_to_keep = ["engine_id", "cycle"] + sensor_list
    return df[features_to_keep].copy()


# Lista padrão de sensores do artigo
DEFAULT_SENSORS = [
    "s2",
    "s3",
    "s4",
    "s7",
    "s8",
    "s9",
    "s11",
    "s12",
    "s13",
    "s14",
    "s15",
    "s17",
    "s20",
    "s21",
]
