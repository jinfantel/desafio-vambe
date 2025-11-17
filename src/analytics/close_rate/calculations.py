"""
Funciones de cálculo para métricas de tasa de cierre.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple

from src.core.utils import get_month_name_es


def calculate_monthly_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula estadísticas mensuales de cierre.
    
    Args:
        df: DataFrame con datos
        
    Returns:
        DataFrame con estadísticas por mes
    """
    df_monthly = df.copy()
    df_monthly["Fecha de la Reunion"] = pd.to_datetime(df_monthly["Fecha de la Reunion"])
    df_monthly["year_month"] = df_monthly["Fecha de la Reunion"].dt.to_period("M")
    
    monthly_stats = df_monthly.groupby("year_month").agg({
        "closed": ["sum", "count"]
    }).reset_index()
    
    monthly_stats.columns = ["year_month", "closed_sum", "total"]
    monthly_stats["close_rate"] = monthly_stats["closed_sum"] / monthly_stats["total"]
    monthly_stats["month_name"] = monthly_stats["year_month"].apply(
        lambda x: f"{get_month_name_es(x.month)} {x.year}"
    )
    
    return monthly_stats


def generate_future_months(last_period: pd.Period, n_months: int = 6) -> List[str]:
    """
    Genera lista de nombres de meses futuros.
    
    Args:
        last_period: Último periodo de datos
        n_months: Cantidad de meses a proyectar
        
    Returns:
        Lista con nombres de meses futuros
    """
    future_months_names = []
    current_month = last_period.month
    current_year = last_period.year
    
    for i in range(n_months):
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
        
        future_months_names.append(f"{get_month_name_es(current_month)} {current_year}")
    
    return future_months_names


def calculate_forecast(monthly_stats: pd.DataFrame, n_months: int = 6) -> Tuple[np.ndarray, List[str], float]:
    """
    Calcula proyección de cierre para los próximos meses.
    
    Args:
        monthly_stats: DataFrame con estadísticas mensuales
        n_months: Cantidad de meses a proyectar
        
    Returns:
        Tuple con (valores proyectados, nombres de meses, promedio proyectado)
    """
    x_numeric = np.arange(len(monthly_stats))
    y = monthly_stats["close_rate"].values
    
    coeffs = np.polyfit(x_numeric, y, 1)
    
    last_period = monthly_stats["year_month"].iloc[-1]
    future_months_names = generate_future_months(last_period, n_months)
    
    future_x = np.arange(len(monthly_stats), len(monthly_stats) + n_months)
    future_y = coeffs[0] * future_x + coeffs[1]
    
    future_y = np.clip(future_y, 0, 1)
    
    avg_forecast = float(np.mean(future_y))
    
    return future_y, future_months_names, avg_forecast


def prepare_heatmap_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
    """
    Prepara datos para el heatmap.
    
    Args:
        df: DataFrame con datos categorizados
        
    Returns:
        Tuple con (pivot de tasas, pivot de conteos, orden de columnas)
    """
    pivot = df.pivot_table(
        index="sector_principal",
        columns="volumen_nivel",
        values="closed",
        aggfunc=["mean", "count"]
    )
    
    close_rate_pivot = pivot["mean"].fillna(0)
    count_pivot = pivot["count"].fillna(0)
    
    volume_order = ["Bajo (<100)", "Medio (100-250)", "Alto (251-500)", "Muy Alto (>500)", "Desconocido"]
    existing_cols = [col for col in volume_order if col in close_rate_pivot.columns]
    
    close_rate_pivot = close_rate_pivot[existing_cols]
    count_pivot = count_pivot[existing_cols]
    
    return close_rate_pivot, count_pivot, existing_cols


def create_hover_text(close_rate_pivot: pd.DataFrame, count_pivot: pd.DataFrame) -> List[List[str]]:
    """
    Crea texto hover para el heatmap.
    
    Args:
        close_rate_pivot: DataFrame con tasas de cierre
        count_pivot: DataFrame con conteos
        
    Returns:
        Matriz de textos hover
    """
    hover_text = []
    for i in range(len(close_rate_pivot)):
        row_text = []
        for j in range(len(close_rate_pivot.columns)):
            rate = close_rate_pivot.iloc[i, j]
            count = count_pivot.iloc[i, j]
            row_text.append(
                f"Sector: {close_rate_pivot.index[i]}<br>"
                f"Volumen: {close_rate_pivot.columns[j]}<br>"
                f"Tasa: {rate:.1%}<br>"
                f"Leads: {int(count)}"
            )
        hover_text.append(row_text)
    
    return hover_text
