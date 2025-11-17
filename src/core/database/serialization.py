"""
Serialización y deserialización entre DataFrame y registros de base de datos.
"""

import json
import pandas as pd
from typing import List, Tuple

from src.core.utils import build_preocupaciones_texto


def dataframe_to_records(df: pd.DataFrame) -> List[Tuple]:
    """
    Convierte un DataFrame en una lista de tuplas para inserción en SQLite.
    
    Args:
        df: DataFrame con datos procesados
        
    Returns:
        Lista de tuplas con los valores para INSERT
    """
    records = []
    for _, row in df.iterrows():
        preocupaciones_json = json.dumps(row.get('preocupaciones', []), ensure_ascii=False)
        potencial_upsell_json = json.dumps(row.get('potencial_upsell', []), ensure_ascii=False)
        
        record = (
            row.get('client_name', row.get('Nombre')),
            row.get('Correo Electronico', ''),
            row.get('Numero de Telefono', ''),
            str(row.get('Fecha de la Reunion', '')),
            row.get('Vendedor asignado', ''),
            int(row.get('closed', 0)),
            row.get('transcript', row.get('Transcripcion', '')),
            row.get('sector_principal'),
            row.get('sector_secundario'),
            row.get('volumen_numerico'),
            row.get('volumen_nivel'),
            1 if row.get('es_pico_estacional') else 0,
            row.get('fuente_primaria'),
            row.get('fuente_detalle'),
            preocupaciones_json,
            row.get('urgencia_nivel'),
            potencial_upsell_json,
            1 if row.get('_categorization_success', True) else 0
        )
        records.append(record)
    
    return records


def records_to_dataframe(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma el DataFrame crudo de SQLite al formato esperado por la aplicación.
    
    Args:
        df_raw: DataFrame directamente de pd.read_sql_query
        
    Returns:
        DataFrame transformado con columnas renombradas y tipos correctos
    """
    df = df_raw.rename(columns={
        'client_name': 'Nombre',
        'correo_electronico': 'Correo Electronico',
        'numero_telefono': 'Numero de Telefono',
        'fecha_reunion': 'Fecha de la Reunion',
        'vendedor_asignado': 'Vendedor asignado',
        'transcript': 'Transcripcion'
    })
    
    df['Fecha de la Reunion'] = pd.to_datetime(df['Fecha de la Reunion'])
    df['preocupaciones'] = df['preocupaciones'].apply(json.loads)
    df['potencial_upsell'] = df['potencial_upsell'].apply(json.loads)
    df['es_pico_estacional'] = df['es_pico_estacional'].astype(bool)
    df['_categorization_success'] = df['categorization_success'].astype(bool)
    df = df.drop(columns=['categorization_success'])
    
    df['preocupaciones_texto'] = df['preocupaciones'].apply(build_preocupaciones_texto)
    
    return df
