"""
Validación de estructura de datos para archivos cargados.
"""

import pandas as pd
from typing import Dict, List, Optional, Tuple


REQUIRED_COLUMNS = {
    "Nombre": "string",
    "Correo Electronico": "string",
    "Numero de Telefono": "string", 
    "Fecha de la Reunion": "datetime",
    "Vendedor asignado": "string",
    "closed": "boolean",
    "Transcripcion": "string"
}


def validate_dataframe_schema(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Valida que el DataFrame tenga la estructura correcta.
    
    Args:
        df: DataFrame a validar
        
    Returns:
        Tuple con (es_válido, lista_de_errores)
    """
    errors = []
    
    missing_columns = set(REQUIRED_COLUMNS.keys()) - set(df.columns)
    if missing_columns:
        errors.append(f"❌ Faltan columnas requeridas: {', '.join(missing_columns)}")
    
    extra_columns = set(df.columns) - set(REQUIRED_COLUMNS.keys())
    if extra_columns:
        errors.append(f"⚠️ Columnas adicionales (se ignorarán): {', '.join(extra_columns)}")
    
    if len(df) == 0:
        errors.append("❌ El archivo está vacío")
        return False, errors
    
    for col, expected_type in REQUIRED_COLUMNS.items():
        if col not in df.columns:
            continue
            
        if expected_type == "datetime":
            try:
                pd.to_datetime(df[col])
            except Exception as e:
                errors.append(f"❌ Columna '{col}' debe ser fecha válida (formato: YYYY-MM-DD)")
        
        elif expected_type == "boolean":
            valid_values = {0, 1, "0", "1", True, False, "True", "False", "true", "false"}
            invalid = df[col].apply(lambda x: x not in valid_values if pd.notna(x) else False)
            if invalid.any():
                errors.append(f"❌ Columna '{col}' debe contener valores booleanos (0/1 o True/False)")
        
        elif expected_type == "string":
            if df[col].isna().all():
                errors.append(f"⚠️ Columna '{col}' está completamente vacía")
    
    if "Transcripcion" in df.columns:
        empty_transcripts = df["Transcripcion"].isna() | (df["Transcripcion"].str.strip() == "")
        if empty_transcripts.any():
            count = empty_transcripts.sum()
            errors.append(f"❌ {count} filas tienen transcripciones vacías (requeridas para categorización)")
    
    is_valid = len([e for e in errors if e.startswith("❌")]) == 0
    
    return is_valid, errors


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza el DataFrame al formato esperado.
    
    Args:
        df: DataFrame a normalizar
        
    Returns:
        DataFrame normalizado
    """
    df_normalized = df.copy()
    
    df_normalized = df_normalized[list(REQUIRED_COLUMNS.keys())]
    
    df_normalized["Fecha de la Reunion"] = pd.to_datetime(df_normalized["Fecha de la Reunion"])
    
    df_normalized["closed"] = df_normalized["closed"].apply(
        lambda x: bool(int(x)) if pd.notna(x) else False
    )
    
    for col in ["Nombre", "Correo Electronico", "Numero de Telefono", "Vendedor asignado", "Transcripcion"]:
        df_normalized[col] = df_normalized[col].fillna("").astype(str).str.strip()
    
    return df_normalized


def get_validation_summary(df: pd.DataFrame) -> Dict[str, any]:
    """
    Genera un resumen de validación del DataFrame.
    
    Args:
        df: DataFrame validado
        
    Returns:
        Diccionario con estadísticas de validación
    """
    closed_count = int(df["closed"].sum())
    total_rows = len(df)
    
    return {
        "total_rows": total_rows,
        "valid_transcripts": int((~df["Transcripcion"].isna() & (df["Transcripcion"].str.strip() != "")).sum()),
        "closed_count": closed_count,
        "open_count": total_rows - closed_count,
        "unique_sellers": int(df["Vendedor asignado"].nunique()),
        "sellers": sorted(df["Vendedor asignado"].unique().tolist()),
        "date_range": {
            "min": df["Fecha de la Reunion"].min().strftime("%Y-%m-%d"),
            "max": df["Fecha de la Reunion"].max().strftime("%Y-%m-%d")
        }
    }
