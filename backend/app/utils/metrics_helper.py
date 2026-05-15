# metrics_helper.py: Funciones para calcular métricas de evaluación del modelo
# Estas métricas ayudan a entender qué tan bien funciona el modelo en datos reales

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from typing import List


def compute_metrics(true_labels: List[str], predicted_labels: List[str]) -> dict:
    """
    Calcula las métricas estándar de clasificación.
    
    - Accuracy: porcentaje de predicciones correctas sobre el total
    - Precision: de todas las predicciones positivas, cuántas fueron correctas
    - Recall: de todos los casos positivos reales, cuántos detectó el modelo
    - F1-score: media armónica entre precision y recall (equilibrio entre los dos)
    
    Se usa average='weighted' porque puede haber clases desbalanceadas
    """

    # accuracy_score compara directamente las listas de etiquetas
    accuracy = accuracy_score(true_labels, predicted_labels)

    # zero_division=0 evita errores cuando una clase no aparece en las predicciones
    precision = precision_score(true_labels, predicted_labels, average='weighted', zero_division=0)

    recall = recall_score(true_labels, predicted_labels, average='weighted', zero_division=0)

    f1 = f1_score(true_labels, predicted_labels, average='weighted', zero_division=0)

    # Retornar como diccionario con valores redondeados a 4 decimales para legibilidad
    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4)
    }
