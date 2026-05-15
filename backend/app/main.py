# main.py: Punto de entrada de la aplicación FastAPI
# Aquí se configura la app, CORS, eventos de inicio y se incluyen las rutas

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import ALLOWED_ORIGIN
from app.core.model_loader import load_models
from app.routes.review_routes import router as review_router

# Crear la instancia principal de la aplicación FastAPI
# title y description aparecen en la documentación automática /docs
app = FastAPI(
    title="EmoReview API",
    description="Analizador inteligente de emociones y sentimiento en reseñas",
    version="1.0.0"
)

# Configurar CORS (Cross-Origin Resource Sharing)
# Sin esto, el navegador bloquearía las peticiones del frontend Angular (puerto 4200)
# al backend FastAPI (puerto 8000) por ser orígenes distintos
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],  # Solo permite peticiones desde localhost:4200
    allow_credentials=True,
    allow_methods=["*"],   # Permite todos los métodos HTTP: GET, POST, etc.
    allow_headers=["*"],   # Permite todos los headers
)

# Evento de startup: se ejecuta UNA VEZ cuando FastAPI arranca
# Cargamos los modelos aquí para que estén listos antes de recibir peticiones
@app.on_event("startup")
def startup_event():
    """Carga los modelos de Hugging Face en memoria al iniciar el servidor."""
    print("Cargando modelos de Hugging Face... (puede tardar la primera vez)")
    load_models()
    print("Modelos cargados correctamente. EmoReview API lista.")


# Incluir el router de reseñas con todas sus rutas (/api/reviews/analyze, etc.)
app.include_router(review_router)


# Ruta raíz para verificar que el servidor está corriendo
@app.get("/")
def root():
    return {"message": "EmoReview API funcionando correctamente"}
