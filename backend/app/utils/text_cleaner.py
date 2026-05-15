# text_cleaner.py: Utilidad para limpiar el texto antes de pasarlo al modelo
# La limpieza básica mejora la calidad de las predicciones

import re


def clean_text(text: str) -> str:
    """
    Aplica limpieza básica al texto de la reseña.
    No aplica stemming ni lematización porque los modelos transformer
    trabajan con texto casi natural (sus tokenizadores manejan eso internamente).
    """
    # Eliminar espacios al inicio y al final del texto
    text = text.strip()

    # Reemplazar múltiples espacios o saltos de línea consecutivos por un solo espacio
    # re.sub busca el patrón y lo reemplaza en toda la cadena
    text = re.sub(r'\s+', ' ', text)

    # Eliminar caracteres especiales que no aportan significado semántico
    # Se conservan letras, números, espacios y puntuación básica (. , ! ? ')
    text = re.sub(r'[^a-zA-Z0-9\s.,!?\'\-]', '', text)

    # Convertir todo a minúsculas para normalizar el texto
    # (distilbert-uncased ya no distingue mayúsculas, pero es buena práctica)
    text = text.lower()

    return text
