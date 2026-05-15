# review_routes.py: Define los endpoints HTTP de la API de IntesamentIA
# FastAPI usa decoradores (@router.get, @router.post) para asociar funciones a rutas

from fastapi import APIRouter, HTTPException
from app.models.review_request import ReviewRequest
from app.models.analysis_response import AnalysisResponse
from app.services.review_analysis_service import analyze_review
from app.services.dataset_service import evaluate_sentiment_model

# APIRouter permite organizar rutas en módulos separados
# El prefijo /api/reviews se agrega a todas las rutas de este archivo
router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.post("/analyze", response_model=AnalysisResponse)
def analyze_review_endpoint(request: ReviewRequest):
    """
    Endpoint principal: recibe una reseña y retorna el análisis completo.
    
    - Valida automáticamente el cuerpo JSON gracias a Pydantic (ReviewRequest)
    - Ejecuta sentiment y emotion en paralelo (ver review_analysis_service.py)
    - Retorna un JSON con todos los resultados (AnalysisResponse)
    
    Ejemplo de entrada:
    {"text": "The food was absolutely amazing!"}
    """
    try:
        # Delegar toda la lógica al servicio; este endpoint solo actúa como controlador
        result = analyze_review(request)
        return result
    except Exception as e:
        # Si algo falla (modelo no cargado, texto inválido), retornar error HTTP 500
        raise HTTPException(status_code=500, detail=f"Error al analizar la reseña: {str(e)}")


@router.get("/evaluation")
def evaluation_endpoint():
    """
    Endpoint de evaluación: carga una muestra del dataset SST-2 y calcula métricas.
    Tarda unos segundos porque ejecuta el modelo sobre 100 ejemplos reales.
    
    Retorna accuracy, precision, recall y F1-score del modelo en datos de validación.
    """
    try:
        metrics = evaluate_sentiment_model()
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al evaluar el modelo: {str(e)}")
