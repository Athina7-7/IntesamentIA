# sentiment_result.py: Define la estructura de los resultados de análisis de sentimiento

from pydantic import BaseModel
from typing import List


class ScoreItem(BaseModel):
    # Representa una etiqueta con su puntuación de confianza
    # Ejemplo: {"label": "POSITIVE", "score": 0.98}
    label: str
    score: float


class SentimentResult(BaseModel):
    # La etiqueta ganadora: la clase con mayor puntuación (ej: "POSITIVE")
    label: str

    # La confianza del modelo en esa etiqueta, valor entre 0 y 1
    score: float

    # Lista con las puntuaciones de todas las clases posibles
    # Útil para mostrar gráficos de barras en el frontend
    all_scores: List[ScoreItem]
