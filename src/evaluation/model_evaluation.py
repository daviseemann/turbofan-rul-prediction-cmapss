"""
Módulo de avaliação de modelos RUL.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
import matplotlib.pyplot as plt
import seaborn as sns

from ..models.metrics import RULMetrics, rul_health_score_numpy


class ModelEvaluator:
    """
    Classe para avaliação completa de modelos RUL.
    """

    def __init__(self, model, X_test, y_test, engine_ids=None):
        """
        Inicializa o avaliador.

        Args:
            model: Modelo treinado
            X_test: Features de teste
            y_test: Targets de teste
            engine_ids: IDs dos engines (opcional)
        """
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self.engine_ids = engine_ids
        self.predictions = None
        self.metrics = None

    def predict(self) -> np.ndarray:
        """Gera predições do modelo."""
        if self.predictions is None:
            self.predictions = self.model.predict(self.X_test).flatten()
        return self.predictions

    def calculate_metrics(self) -> Dict[str, float]:
        """Calcula todas as métricas de avaliação."""
        if self.metrics is None:
            y_pred = self.predict()
            self.metrics = RULMetrics.calculate_all_metrics(self.y_test, y_pred)
        return self.metrics

    def get_results_dataframe(self) -> pd.DataFrame:
        """Retorna DataFrame com resultados detalhados."""
        y_pred = self.predict()

        df_results = pd.DataFrame(
            {
                "RUL_Actual": self.y_test,
                "RUL_Predicted": y_pred,
                "Error": self.y_test - y_pred,
                "Abs_Error": np.abs(self.y_test - y_pred),
            }
        )

        if self.engine_ids is not None:
            df_results["Engine_ID"] = self.engine_ids

        # Adicionar categorização de erros
        df_results["Error_Category"] = pd.cut(
            df_results["Error"],
            bins=[-np.inf, -20, -10, 10, 20, np.inf],
            labels=["Large_Under", "Small_Under", "Good", "Small_Over", "Large_Over"],
        )

        return df_results

    def evaluate_by_engine(self) -> pd.DataFrame:
        """Avalia performance por engine individualmente."""
        if self.engine_ids is None:
            raise ValueError("engine_ids necessário para avaliação por engine")

        df_results = self.get_results_dataframe()

        engine_metrics = []
        for engine_id in np.unique(self.engine_ids):
            engine_mask = df_results["Engine_ID"] == engine_id
            engine_actual = df_results.loc[engine_mask, "RUL_Actual"].values
            engine_pred = df_results.loc[engine_mask, "RUL_Predicted"].values

            metrics = RULMetrics.calculate_all_metrics(engine_actual, engine_pred)
            metrics["Engine_ID"] = engine_id
            metrics["N_Samples"] = len(engine_actual)

            engine_metrics.append(metrics)

        return pd.DataFrame(engine_metrics)

    def prognostic_horizon_analysis(
        self, thresholds: List[int] = None
    ) -> Dict[int, float]:
        """
        Analisa horizonte prognóstico para diferentes thresholds.

        Args:
            thresholds: Lista de thresholds para análise

        Returns:
            Dict com % de predições dentro de cada threshold
        """
        if thresholds is None:
            thresholds = [10, 20, 30, 50]

        y_pred = self.predict()
        errors = np.abs(self.y_test - y_pred)

        ph_results = {}
        for threshold in thresholds:
            ph_results[threshold] = np.mean(errors <= threshold) * 100

        return ph_results

    def generate_comprehensive_report(self) -> str:
        """Gera relatório completo de avaliação."""
        metrics = self.calculate_metrics()
        ph_results = self.prognostic_horizon_analysis()

        report = f"""
# Relatório de Avaliação do Modelo RUL

## Métricas Gerais
- **RMSE**: {metrics['RMSE']:.2f}
- **MAE**: {metrics['MAE']:.2f}
- **NASA Health Score**: {metrics['RHS']:.2f}
- **MAPE**: {metrics['MAPE']:.2f}%

## Horizonte Prognóstico
"""
        for threshold, percentage in ph_results.items():
            report += f"- **PH-{threshold}**: {percentage:.1f}% das predições\n"

        if self.engine_ids is not None:
            df_engine = self.evaluate_by_engine()
            report += f"""
## Performance por Engine
- **Melhor RMSE**: {df_engine['RMSE'].min():.2f} (Engine {df_engine.loc[df_engine['RMSE'].idxmin(), 'Engine_ID']})
- **Pior RMSE**: {df_engine['RMSE'].max():.2f} (Engine {df_engine.loc[df_engine['RMSE'].idxmax(), 'Engine_ID']})
- **Desvio Padrão RMSE**: {df_engine['RMSE'].std():.2f}
"""

        return report


def compare_models(
    models_dict: Dict[str, Any], X_test: np.ndarray, y_test: np.ndarray
) -> pd.DataFrame:
    """
    Compara múltiplos modelos nas mesmas métricas.

    Args:
        models_dict: Dict com nome_modelo: modelo_treinado
        X_test: Features de teste
        y_test: Targets de teste

    Returns:
        DataFrame com métricas comparativas
    """
    comparison_results = []

    for model_name, model in models_dict.items():
        evaluator = ModelEvaluator(model, X_test, y_test)
        metrics = evaluator.calculate_metrics()
        metrics["Model"] = model_name
        comparison_results.append(metrics)

    df_comparison = pd.DataFrame(comparison_results)
    df_comparison.set_index("Model", inplace=True)

    return df_comparison


def create_evaluation_plots(evaluator: ModelEvaluator, figsize=(15, 12)):
    """
    Cria conjunto completo de plots de avaliação.

    Args:
        evaluator: ModelEvaluator configurado
        figsize: Tamanho da figura
    """
    df_results = evaluator.get_results_dataframe()

    fig, axes = plt.subplots(2, 3, figsize=figsize)

    # 1. Actual vs Predicted
    axes[0, 0].scatter(df_results["RUL_Actual"], df_results["RUL_Predicted"], alpha=0.6)
    min_val = min(df_results["RUL_Actual"].min(), df_results["RUL_Predicted"].min())
    max_val = max(df_results["RUL_Actual"].max(), df_results["RUL_Predicted"].max())
    axes[0, 0].plot([min_val, max_val], [min_val, max_val], "r--", linewidth=2)
    axes[0, 0].set_xlabel("RUL Actual")
    axes[0, 0].set_ylabel("RUL Predicted")
    axes[0, 0].set_title("Actual vs Predicted")
    axes[0, 0].grid(True, alpha=0.3)

    # 2. Error Distribution
    axes[0, 1].hist(
        df_results["Error"], bins=30, alpha=0.7, color="skyblue", edgecolor="black"
    )
    axes[0, 1].axvline(0, color="red", linestyle="--", linewidth=2)
    axes[0, 1].set_xlabel("Error (Actual - Predicted)")
    axes[0, 1].set_ylabel("Frequency")
    axes[0, 1].set_title("Error Distribution")
    axes[0, 1].grid(True, alpha=0.3)

    # 3. Residuals Plot
    axes[0, 2].scatter(df_results["RUL_Predicted"], df_results["Error"], alpha=0.6)
    axes[0, 2].axhline(0, color="red", linestyle="--", linewidth=2)
    axes[0, 2].set_xlabel("RUL Predicted")
    axes[0, 2].set_ylabel("Residuals")
    axes[0, 2].set_title("Residuals Plot")
    axes[0, 2].grid(True, alpha=0.3)

    # 4. Absolute Error Distribution
    axes[1, 0].hist(
        df_results["Abs_Error"], bins=30, alpha=0.7, color="orange", edgecolor="black"
    )
    axes[1, 0].set_xlabel("Absolute Error")
    axes[1, 0].set_ylabel("Frequency")
    axes[1, 0].set_title("Absolute Error Distribution")
    axes[1, 0].grid(True, alpha=0.3)

    # 5. Error Categories
    error_counts = df_results["Error_Category"].value_counts()
    axes[1, 1].pie(error_counts.values, labels=error_counts.index, autopct="%1.1f%%")
    axes[1, 1].set_title("Error Categories")

    # 6. Performance by Engine (if available)
    if evaluator.engine_ids is not None:
        try:
            df_engine = evaluator.evaluate_by_engine()
            axes[1, 2].bar(range(len(df_engine)), df_engine["RMSE"])
            axes[1, 2].set_xlabel("Engine ID")
            axes[1, 2].set_ylabel("RMSE")
            axes[1, 2].set_title("RMSE by Engine")
            axes[1, 2].tick_params(axis="x", rotation=45)
        except:
            axes[1, 2].text(
                0.5,
                0.5,
                "Engine analysis\nnot available",
                ha="center",
                va="center",
                transform=axes[1, 2].transAxes,
            )
    else:
        axes[1, 2].text(
            0.5,
            0.5,
            "Engine IDs\nnot provided",
            ha="center",
            va="center",
            transform=axes[1, 2].transAxes,
        )

    plt.tight_layout()
    plt.show()


def export_evaluation_report(evaluator: ModelEvaluator, output_path: str):
    """
    Exporta relatório completo de avaliação.

    Args:
        evaluator: ModelEvaluator configurado
        output_path: Caminho para salvar o relatório
    """
    report = evaluator.generate_comprehensive_report()
    df_results = evaluator.get_results_dataframe()

    # Salvar relatório texto
    with open(f"{output_path}_report.md", "w", encoding="utf-8") as f:
        f.write(report)

    # Salvar resultados detalhados
    df_results.to_csv(f"{output_path}_detailed_results.csv", index=False)

    # Salvar métricas por engine (se disponível)
    if evaluator.engine_ids is not None:
        try:
            df_engine = evaluator.evaluate_by_engine()
            df_engine.to_csv(f"{output_path}_engine_metrics.csv", index=False)
        except:
            pass

    print(f"Relatório exportado para: {output_path}_*")
