# review_request.py: Define el esquema de la petición que llega al backend
# Pydantic valida automáticamente que el JSON tenga los campos correctos y los tipos esperados

from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    # 'text' es el campo requerido: la reseña escrita por el usuario
    # Field(min_length=1) garantiza que el texto no llegue vacío
    text: str = Field(..., min_length=1, description="Texto de la reseña a analizar")
