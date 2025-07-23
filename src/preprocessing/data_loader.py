import pandas as pd
import numpy as np

def cmapss_loader_pandas(train_path, test_path, test_rul_path):

    # Nomes das colunas (de acordo com a documentação original do C-MAPSS)
    column_names = (
        ["engine_id", "cycle"]
        + [f"op{i}" for i in range(1, 4)]
        + [f"s{i}" for i in range(1, 22)]
    )

    train_df = pd.read_csv(train_path, sep="\s+", header=None, names=column_names)
    test_df = pd.read_csv(test_path, sep="\s+", header=None, names=column_names)
    test_rul_df = pd.read_csv(test_rul_path, sep="\s+", header=None, names=["RUL"])

    return train_df, test_df, test_rul_df
