# model_loader.py: Carga los modelos de Hugging Face una sola vez al iniciar la aplicación
# Esto evita recargar los modelos en cada petición, lo que sería muy lento

from transformers import pipeline
from app.core.config import SENTIMENT_MODEL_NAME, EMOTION_MODEL_NAME

# Variable global que almacenará el pipeline de sentimiento
# Un pipeline de Hugging Face encapsula tokenizador + modelo + postprocesamiento
_sentiment_pipeline = None

# Variable global que almacenará el pipeline de emociones
_emotion_pipeline = None


def load_models():
    """
    Carga ambos modelos preentrenados de Hugging Face en memoria.
    Esta función se llama una vez cuando FastAPI inicia (evento 'startup').
    Los modelos quedan en memoria RAM/VRAM para respuestas rápidas.
    """
    global _sentiment_pipeline, _emotion_pipeline

    # pipeline("text-classification") descarga automáticamente el modelo desde Hugging Face Hub
    # la primera vez; en ejecuciones posteriores lo usa desde caché local
    _sentiment_pipeline = pipeline(
        "text-classification",
        model=SENTIMENT_MODEL_NAME,
        return_all_scores=True  # Retorna las puntuaciones de TODAS las clases, no solo la más alta
    )

    _emotion_pipeline = pipeline(
        "text-classification",
        model=EMOTION_MODEL_NAME,
        return_all_scores=True  # Igual: queremos ver las probabilidades de todas las emociones
    )


def get_sentiment_pipeline():
    """Retorna el pipeline de sentimiento ya cargado."""
    return _sentiment_pipeline


def get_emotion_pipeline():
    """Retorna el pipeline de emociones ya cargado."""
    return _emotion_pipeline
