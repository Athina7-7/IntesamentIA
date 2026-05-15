# emotion_service.py: Lógica de análisis de emociones
# Usa el modelo j-hartmann/emotion-english-distilroberta-base
# que clasifica en 7 emociones: anger, disgust, fear, joy, neutral, sadness, surprise

from app.core.model_loader import get_emotion_pipeline
from app.models.emotion_result import EmotionResult
from app.models.sentiment_result import ScoreItem
from app.core.config import MAX_TOKEN_LENGTH


def analyze_emotion(text: str) -> EmotionResult:
    """
    Analiza la emoción dominante en el texto.
    El proceso es el mismo que el de sentimiento, pero con un modelo diferente
    que fue entrenado específicamente para clasificar emociones humanas.
    """
    # Obtener el pipeline de emociones cargado al inicio de la app
    emotion_pipeline = get_emotion_pipeline()

    # Ejecutar inferencia con truncación para textos largos
    raw_results = emotion_pipeline(text, truncation=True, max_length=MAX_TOKEN_LENGTH)

    # Desempacar la lista de resultados del primer (único) texto procesado
    scores_list = raw_results[0]

    # Ordenar emociones de mayor a menor confianza
    scores_list_sorted = sorted(scores_list, key=lambda x: x['score'], reverse=True)

    # La emoción con mayor puntuación es la dominante
    top_result = scores_list_sorted[0]

    # Normalizar la etiqueta a minúsculas
    top_label = top_result['label'].lower()

    # Mapa de traducción de emociones al español para mostrar en la interfaz
    emotion_map = {
        "joy": "alegría",
        "anger": "enojo",
        "sadness": "tristeza",
        "fear": "miedo",
        "surprise": "sorpresa",
        "disgust": "asco",
        "neutral": "neutral"
    }
    display_label = emotion_map.get(top_label, top_label)

    # Construir la lista con todas las emociones y sus puntuaciones (para los gráficos)
    all_scores = [
        ScoreItem(label=emotion_map.get(item['label'].lower(), item['label'].lower()), score=round(item['score'], 4))
        for item in scores_list_sorted
    ]

    return EmotionResult(
        label=display_label,
        score=round(top_result['score'], 4),
        all_scores=all_scores
    )
