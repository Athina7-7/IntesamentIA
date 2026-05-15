# explanation_service.py: Genera una explicación en lenguaje natural del análisis
# No usa IA generativa: simplemente construye texto con plantillas basadas en los resultados

from app.models.sentiment_result import SentimentResult
from app.models.emotion_result import EmotionResult


# Palabras clave asociadas a cada sentimiento para identificarlas en el texto del usuario
POSITIVE_KEYWORDS = ["amazing", "excellent", "great", "fantastic", "love", "wonderful", "best", "perfect", "good", "outstanding"]
NEGATIVE_KEYWORDS = ["terrible", "awful", "bad", "horrible", "worst", "poor", "disappointing", "hate", "disgusting", "mediocre"]
NEUTRAL_KEYWORDS = ["okay", "average", "normal", "fine", "decent", "acceptable", "moderate"]


def generate_explanation(text: str, sentiment: SentimentResult, emotion: EmotionResult) -> str:
    """
    Construye una explicación textual del análisis basándose en:
    - El sentimiento detectado y su confianza
    - La emoción detectada y su confianza
    - Las palabras clave encontradas en el texto del usuario
    
    Esta explicación ayuda al usuario a entender por qué el modelo tomó esa decisión.
    """
    # Convertir texto a minúsculas para buscar palabras clave sin importar mayúsculas
    text_lower = text.lower()

    # Buscar qué palabras clave del texto coinciden con las listas predefinidas
    found_positive = [w for w in POSITIVE_KEYWORDS if w in text_lower]
    found_negative = [w for w in NEGATIVE_KEYWORDS if w in text_lower]
    found_neutral = [w for w in NEUTRAL_KEYWORDS if w in text_lower]

    # Construir la primera parte: resumen del sentimiento detectado
    sentiment_label = sentiment.label
    sentiment_confidence = int(sentiment.score * 100)
    emotion_label = emotion.label
    emotion_confidence = int(emotion.score * 100)

    explanation = f"La reseña fue clasificada como '{sentiment_label}' con una confianza del {sentiment_confidence}%. "
    explanation += f"La emoción predominante detectada fue '{emotion_label}' con una confianza del {emotion_confidence}%. "

    # Agregar información sobre palabras clave encontradas si existen
    if found_positive:
        explanation += f"Se identificaron expresiones con carga positiva como: {', '.join(found_positive)}. "
    if found_negative:
        explanation += f"Se detectaron términos negativos como: {', '.join(found_negative)}. "
    if found_neutral:
        explanation += f"El texto contiene palabras de tono neutro como: {', '.join(found_neutral)}. "
    if not found_positive and not found_negative and not found_neutral:
        explanation += "El modelo no encontró palabras clave explícitas, pero el contexto general del texto influyó en la predicción. "

    # Agregar interpretación de la confianza para que el usuario sepa qué tan fiable es
    if sentiment.score >= 0.90:
        explanation += "La predicción tiene muy alta confianza, lo que indica que el texto es bastante claro en su tono."
    elif sentiment.score >= 0.70:
        explanation += "La predicción tiene confianza moderada-alta; el texto tiene señales claras pero puede contener matices."
    else:
        explanation += "La predicción tiene confianza baja o moderada, lo que sugiere que el texto es ambiguo o contiene sentimientos mixtos."

    return explanation
