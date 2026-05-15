# emotion_result.py: Define la estructura de los resultados de análisis de emociones
# Sigue la misma forma que SentimentResult para mantener consistencia

from pydantic import BaseModel
from typing import List
from app.models.sentiment_result import ScoreItem


class EmotionResult(BaseModel):
    # La emoción dominante detectada (ej: "joy", "anger", "sadness")
    label: str

    # Confianza del modelo en esa emoción, entre 0 y 1
    score: float

    # Puntuaciones de todas las emociones detectadas por el modelo
    all_scores: List[ScoreItem]
