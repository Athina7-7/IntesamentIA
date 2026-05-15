# dataset_service.py: Carga el dataset de evaluación y calcula métricas del modelo
# Usa el dataset SST-2 de Hugging Face (Stanford Sentiment Treebank)

from datasets import load_dataset
from app.core.model_loader import get_sentiment_pipeline
from app.utils.metrics_helper import compute_metrics
from app.core.config import EVALUATION_SAMPLE_SIZE, MAX_TOKEN_LENGTH


def evaluate_sentiment_model() -> dict:
    """
    Evalúa el modelo de sentimiento sobre una muestra del dataset SST-2.
    
    Dataset SST-2 (Stanford Sentiment Treebank):
    - Fuente: Hugging Face Hub (glue/sst2)
    - Contiene reseñas de películas en inglés etiquetadas como positivas (1) o negativas (0)
    - Total de datos: ~67,000 ejemplos de entrenamiento + ~872 de validación
    - Se usa el split de validación para evaluar (datos no vistos durante el entrenamiento del modelo)
    
    Para este proyecto usamos una MUESTRA pequeña (EVALUATION_SAMPLE_SIZE = 100 ejemplos)
    para que el endpoint responda en segundos y no en minutos.
    """

    # Cargar el split de validación del dataset SST-2 desde Hugging Face
    # Si ya fue descargado antes, se usa la caché local
    dataset = load_dataset("glue", "sst2", split="validation")

    # Tomar solo los primeros N ejemplos para que la evaluación sea rápida
    sample = dataset.select(range(min(EVALUATION_SAMPLE_SIZE, len(dataset))))

    # Extraer los textos y etiquetas verdaderas del dataset
    texts = sample['sentence']  # Lista de oraciones (strings)
    true_labels_int = sample['label']  # Lista de enteros: 0 = negativo, 1 = positivo

    # Convertir las etiquetas numéricas del dataset al formato de texto del modelo
    # El dataset SST-2 usa 0 = negative, 1 = positive
    int_to_label = {0: "negativo", 1: "positivo"}
    true_labels = [int_to_label[l] for l in true_labels_int]

    # Obtener el pipeline de sentimiento y hacer predicciones sobre todos los textos
    sentiment_pipeline = get_sentiment_pipeline()
    
    # Procesamos texto por texto para compatibilidad; batch_size mayor podría acelerar esto
    predicted_labels = []
    for text in texts:
        result = sentiment_pipeline(text, truncation=True, max_length=MAX_TOKEN_LENGTH)[0]
        # Tomar la etiqueta con mayor score de entre las dos (POSITIVE / NEGATIVE)
        top = max(result, key=lambda x: x['score'])
        label_map = {"positive": "positivo", "negative": "negativo", "neutral": "neutral"}
        predicted_labels.append(label_map.get(top['label'].lower(), top['label'].lower()))

    # Calcular las métricas comparando etiquetas reales vs predichas
    metrics = compute_metrics(true_labels, predicted_labels)

    # Agregar información del dataset a la respuesta
    metrics["dataset"] = "SST-2 (Stanford Sentiment Treebank) via Hugging Face Datasets"
    metrics["source"] = "https://huggingface.co/datasets/glue"
    metrics["description"] = "Reseñas de películas en inglés etiquetadas como positivas o negativas."
    metrics["total_validation_examples"] = len(dataset)
    metrics["evaluated_examples"] = len(sample)
    metrics["train_split"] = "80% del total para entrenamiento del modelo original"
    metrics["test_split"] = "20% para validación y evaluación"
    metrics["note"] = "Este proyecto usa modelos preentrenados; no se realiza fine-tuning."

    return metrics
