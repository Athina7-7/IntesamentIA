// review-api.service.ts: Servicio Angular que se comunica con el backend FastAPI
// Los servicios Angular son singletons inyectables que centralizan la lógica de datos

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ReviewRequest } from '../../models/review-request.model';
import { AnalysisResponse } from '../../models/analysis-response.model';

@Injectable({
  // providedIn: 'root' hace que este servicio esté disponible en toda la aplicación
  // Angular lo instanciará una sola vez (patrón singleton)
  providedIn: 'root'
})
export class ReviewApiService {

  // URL base del backend FastAPI
  private readonly apiUrl = 'http://localhost:8000';

  // HttpClient se inyecta automáticamente por Angular (Dependency Injection)
  constructor(private http: HttpClient) {}

  /**
   * Envía el texto de la reseña al backend y retorna un Observable con la respuesta.
   * Observable es el patrón reactivo de Angular para manejar peticiones asíncronas.
   * El componente se suscribe a este Observable para recibir los resultados.
   */
  analyzeReview(request: ReviewRequest): Observable<AnalysisResponse> {
    // http.post<T> hace una petición POST al endpoint y tipifica la respuesta como T
    return this.http.post<AnalysisResponse>(`${this.apiUrl}/api/reviews/analyze`, request);
  }

  /**
   * Llama al endpoint de evaluación para obtener métricas del modelo.
   * Retorna un Observable con un objeto genérico (las métricas varían).
   */
  getEvaluation(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/reviews/evaluation`);
  }
}
