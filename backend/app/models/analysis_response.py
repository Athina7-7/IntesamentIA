# analysis_response.py: Define la respuesta completa que el backend envía al frontend
# Este modelo agrupa todos los resultados en un solo objeto JSON

from pydantic import BaseModel
from app.models.sentiment_result import SentimentResult
from app.models.emotion_result import EmotionResult


class AnalysisResponse(BaseModel):
    # Texto original tal como lo escribió el usuario
    original_text: str

    # Texto después de aplicar limpieza básica (minúsculas, sin caracteres raros)
    cleaned_text: str

    # Resultados completos del análisis de sentimiento
    sentiment: SentimentResult

    # Resultados completos del análisis de emociones
    emotion: EmotionResult

    # Explicación generada por el servicio de explicación
    explanation: str

    # Tiempo total que tardó el backend en procesar la reseña (en segundos)
    processing_time_seconds: float
