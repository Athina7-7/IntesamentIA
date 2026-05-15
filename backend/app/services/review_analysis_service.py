# review_analysis_service.py: Orquesta el análisis completo de una reseña
# PARALELISMO: Este archivo implementa el procesamiento paralelo de sentimiento y emoción
# usando concurrent.futures.ThreadPoolExecutor

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.utils.text_cleaner import clean_text
from app.services.sentiment_service import analyze_sentiment
from app.services.emotion_service import analyze_emotion
from app.services.explanation_service import generate_explanation
from app.models.review_request import ReviewRequest
from app.models.analysis_response import AnalysisResponse


def analyze_review(request: ReviewRequest) -> AnalysisResponse:
    """
    Analiza una reseña completa aplicando:
    1. Limpieza del texto
    2. Análisis paralelo de sentimiento y emoción
    3. Generación de explicación
    4. Ensamblado de la respuesta final
    """
    # Registrar el tiempo de inicio para calcular el tiempo total de procesamiento
    start_time = time.time()

    # Limpiar el texto antes de pasarlo a los modelos
    cleaned = clean_text(request.text)

    # PARALELISMO CON ThreadPoolExecutor
    # ThreadPoolExecutor crea un pool de hilos que pueden ejecutarse simultáneamente
    # Esto es útil para tareas de I/O o cómputo independiente como la inferencia de dos modelos
    # max_workers=2 significa que usamos exactamente 2 hilos: uno por cada análisis
    with ThreadPoolExecutor(max_workers=2) as executor:
        
        # executor.submit() envía una tarea al pool y retorna un Future
        # Un Future representa el resultado de una operación que aún no terminó
        # Ambas tareas se envían ANTES de esperar cualquier resultado → corren en paralelo
        future_sentiment = executor.submit(analyze_sentiment, cleaned)
        future_emotion = executor.submit(analyze_emotion, cleaned)

        # as_completed() retorna los futuros en el orden en que terminan
        # Aquí simplemente esperamos ambos resultados (el orden no importa)
        results = {}
        for future in as_completed([future_sentiment, future_emotion]):
            # Identificar cuál futuro terminó comparando con las referencias originales
            if future is future_sentiment:
                results['sentiment'] = future.result()
            elif future is future_emotion:
                results['emotion'] = future.result()

    # Generar la explicación usando los resultados de ambos modelos
    explanation = generate_explanation(cleaned, results['sentiment'], results['emotion'])

    # Calcular tiempo total transcurrido desde el inicio
    elapsed = round(time.time() - start_time, 3)

    # Construir y retornar la respuesta completa
    return AnalysisResponse(
        original_text=request.text,
        cleaned_text=cleaned,
        sentiment=results['sentiment'],
        emotion=results['emotion'],
        explanation=explanation,
        processing_time_seconds=elapsed
    )
