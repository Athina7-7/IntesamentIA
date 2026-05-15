# sentiment_service.py: Lógica de análisis de sentimiento
# Usa el pipeline de Hugging Face para predecir si el texto es positivo o negativo

from app.core.model_loader import get_sentiment_pipeline
from app.models.sentiment_result import SentimentResult, ScoreItem
from app.core.config import MAX_TOKEN_LENGTH


def analyze_sentiment(text: str) -> SentimentResult:
    """
    Analiza el sentimiento del texto usando el modelo distilbert-sst2.
    
    El pipeline de Hugging Face:
    1. Tokeniza el texto (lo convierte en IDs numéricos)
    2. Lo pasa por el modelo transformer
    3. Aplica softmax a la salida para obtener probabilidades
    4. Retorna etiquetas y puntuaciones
    """
    # Obtener el pipeline cargado en memoria desde model_loader
    sentiment_pipeline = get_sentiment_pipeline()

    # Ejecutar la inferencia; truncation=True corta el texto si supera MAX_TOKEN_LENGTH
    # Esto evita errores con textos muy largos
    raw_results = sentiment_pipeline(text, truncation=True, max_length=MAX_TOKEN_LENGTH)

    # raw_results tiene forma: [[{"label": "POSITIVE", "score": 0.98}, {"label": "NEGATIVE", "score": 0.02}]]
    # Es una lista de listas porque el pipeline puede procesar múltiples textos a la vez
    scores_list = raw_results[0]

    # Ordenar los resultados de mayor a menor puntuación
    scores_list_sorted = sorted(scores_list, key=lambda x: x['score'], reverse=True)

    # La etiqueta con mayor score es la predicción ganadora
    top_result = scores_list_sorted[0]

    # Normalizar la etiqueta a minúsculas para consistencia en la respuesta JSON
    top_label = top_result['label'].lower()

    # Mapear etiquetas en inglés a español para la interfaz
    label_map = {
        "positive": "positivo",
        "negative": "negativo",
        "neutral": "neutral"
    }
    display_label = label_map.get(top_label, top_label)

    # Construir la lista de ScoreItem con todas las etiquetas y sus puntajes
    all_scores = [
        ScoreItem(label=label_map.get(item['label'].lower(), item['label'].lower()), score=round(item['score'], 4))
        for item in scores_list_sorted
    ]

    # Retornar el objeto SentimentResult completo
    return SentimentResult(
        label=display_label,
        score=round(top_result['score'], 4),
        all_scores=all_scores
    )
