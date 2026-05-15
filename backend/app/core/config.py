# Configuración central de la aplicación IntesamentIA
# Aquí se definen constantes reutilizables en todo el backend

# Nombre del modelo preentrenado de Hugging Face para análisis de sentimiento
# distilbert es una versión más pequeña y rápida de BERT, afinada para SST-2 (Stanford Sentiment Treebank)
SENTIMENT_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"

# Nombre del modelo preentrenado de Hugging Face para detección de emociones
# j-hartmann/emotion-english-distilroberta-base clasifica en 7 emociones: anger, disgust, fear, joy, neutral, sadness, surprise
EMOTION_MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

# Número máximo de tokens (palabras/subpalabras) que el modelo acepta como entrada
# Los transformers tienen un límite de contexto; 512 es el estándar para BERT y variantes
MAX_TOKEN_LENGTH = 512

# Origen permitido para las peticiones CORS (Cross-Origin Resource Sharing)
# Esto permite que el frontend Angular en localhost:4200 pueda llamar al backend en localhost:8000
ALLOWED_ORIGIN = "http://localhost:4200"

# Número de ejemplos del dataset que se evalúan al llamar el endpoint /evaluation
# Se usa una muestra pequeña para que la evaluación sea rápida en tiempo real
EVALUATION_SAMPLE_SIZE = 100
