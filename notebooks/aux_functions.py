
"""aux_functions.py

Utilidades para replicar rapidamente o pré‑processamento do dataset C‑MAPSS (ou
estruturas similares) no Google Colab.

Novidade 🔧
-----------
* `rul_clip` (int | None): valor máximo opcional para *capping* do RUL.  
  Se definido, todos os valores do RUL maiores que `rul_clip` são truncados
  para esse limite.

Funcionalidades
---------------
1. Monta o Google Drive (caso ainda não esteja montado);
2. Carrega automaticamente os arquivos de treino, teste e RUL de uma pasta no Drive;
3. Gera DataFrames em janelas deslizantes (sliding‑windows) para treino e teste;
4. Disponibiliza uma função "one‑liner" (`get_preprocessed_data`) para executar tudo.

Exemplo de uso em um notebook Colab
-----------------------------------
from aux_functions import get_preprocessed_data

gdrive_folder = "/content/drive/MyDrive/cmapss/FD001"
df_train_win, df_test_win, df_rul = get_preprocessed_data(
    gdrive_folder,
    window=30,
    step=1,
    rul_clip=125,        # <- novo parâmetro!
    sep="\\s+",
    header=None
)
print(df_train_win.shape, df_test_win.shape, df_rul.describe())
"""


from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Tuple, List, Optional


# --------------------------------------------------------------------------- #
# Google Drive interface                                                     #
# --------------------------------------------------------------------------- #
def mount_drive() -> None:
    """Monta o Google Drive no Colab (ignora em ambientes fora do Colab)."""
    try:
        from google.colab import drive  # type: ignore
        drive.mount('/content/drive', force_remount=False)
    except ModuleNotFoundError:
        print("[aux_functions] Ambiente não‑Colab detectado – montagem do Drive ignorada.")


# --------------------------------------------------------------------------- #
# Carregamento de dados bruto                                                #
# --------------------------------------------------------------------------- #
def _read_csv(folder: str, filename: str, **kwargs) -> pd.DataFrame:
    path = f"{folder.rstrip('/')}/{filename}"
    return pd.read_csv(path, **kwargs)


def load_raw_datasets(
    gdrive_folder: str,
    train_name: str = 'train_FD001.txt',
    test_name: str = 'test_FD001.txt',
    rul_name: str = 'RUL_FD001.txt',
    **read_csv_kwargs,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Lê *train*, *test* e *RUL* de `gdrive_folder`."""
    df_train = _read_csv(gdrive_folder, train_name, **read_csv_kwargs)
    df_test = _read_csv(gdrive_folder, test_name, **read_csv_kwargs)
    df_rul = _read_csv(gdrive_folder, rul_name, **read_csv_kwargs)
    return df_train, df_test, df_rul


# --------------------------------------------------------------------------- #
# Geração de janelas                                                         #
# --------------------------------------------------------------------------- #
def _windows_per_unit(
    df: pd.DataFrame,
    unit_col: str,
    order_col: str,
    window: int,
    step: int,
) -> List[pd.DataFrame]:
    windows: List[pd.DataFrame] = []
    for _, grp in df.groupby(unit_col):
        grp_sorted = grp.sort_values(order_col)
        for start in range(0, len(grp_sorted) - window + 1, step):
            windows.append(grp_sorted.iloc[start : start + window])
    return windows


def _flatten_windows(
    windows: List[pd.DataFrame],
    drop_cols: List[str],
) -> pd.DataFrame:
    flat_rows = []
    for w in windows:
        features = w.drop(columns=drop_cols).values.flatten(order='C')
        flat_rows.append(features)
    return pd.DataFrame(flat_rows)


def generate_windowed_datasets(
    df_train: pd.DataFrame,
    df_test: pd.DataFrame,
    window: int = 30,
    step: int = 1,
    unit_col: str = 'id',
    order_col: str = 'cycle',
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Transforma *train* e *test* em DataFrames de janelas deslizantes."""
    drop_cols = [unit_col, order_col]

    train_windows = _windows_per_unit(df_train, unit_col, order_col, window, step)
    test_windows = _windows_per_unit(df_test, unit_col, order_col, window, step)

    df_train_win = _flatten_windows(train_windows, drop_cols)
    df_test_win = _flatten_windows(test_windows, drop_cols)
    return df_train_win, df_test_win


# --------------------------------------------------------------------------- #
# Pipeline completo                                                          #
# --------------------------------------------------------------------------- #
def _clip_rul(df_rul: pd.DataFrame, rul_clip: Optional[int]) -> pd.DataFrame:
    if rul_clip is None:
        return df_rul
    return df_rul.clip(upper=rul_clip)


def get_preprocessed_data(
    gdrive_folder: str,
    window: int = 30,
    step: int = 1,
    rul_clip: Optional[int] = None,
    train_name: str = 'train_FD001.txt',
    test_name: str = 'test_FD001.txt',
    rul_name: str = 'RUL_FD001.txt',
    **read_csv_kwargs,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Pipeline end‑to‑end que devolve (*df_train_win*, *df_test_win*, *df_rul*).

    Parâmetros
    ----------
    gdrive_folder : str
        Pasta no Google Drive contendo os arquivos.
    window, step : int
        Tamanho e passo da janela deslizante.
    rul_clip : int | None
        Limite superior para o RUL (capping). Se `None`, não aplica.
    *_name : str
        Nomes dos arquivos dentro da pasta.
    **read_csv_kwargs
        Parâmetros adicionais para `pandas.read_csv`.
    """
    mount_drive()

    # 1) Lê arquivos brutos
    df_train, df_test, df_rul = load_raw_datasets(
        gdrive_folder, train_name, test_name, rul_name, **read_csv_kwargs
    )

    # 2) Aplica clipping opcional do RUL
    df_rul = _clip_rul(df_rul, rul_clip)

    # 3) Gera janelas
    df_train_win, df_test_win = generate_windowed_datasets(
        df_train, df_test, window, step
    )

    return df_train_win, df_test_win, df_rul


__all__ = [
    'mount_drive',
    'load_raw_datasets',
    'generate_windowed_datasets',
    'get_preprocessed_data',
]
