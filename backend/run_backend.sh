#!/bin/bash
# Script para levantar el backend de EmoReview

# Activar el entorno virtual (Linux/Mac)
source venv/bin/activate

# Iniciar el servidor FastAPI con recarga automática en modo desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
