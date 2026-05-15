// review-analyzer.component.ts: Componente principal de la aplicación
// Orquesta el formulario, las llamadas al backend y la visualización de resultados

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ReviewApiService } from '../../core/services/review-api.service';
import { AnalysisResponse } from '../../models/analysis-response.model';
import { ResultCardComponent } from '../../shared/components/result-card/result-card.component';
import { ConfidenceChartComponent } from '../../shared/components/confidence-chart/confidence-chart.component';

@Component({
  selector: 'app-review-analyzer',
  standalone: true,
  // Importar módulos necesarios: CommonModule para *ngIf/*ngFor, FormsModule para [(ngModel)]
  imports: [CommonModule, FormsModule, ResultCardComponent, ConfidenceChartComponent],
  templateUrl: './review-analyzer.component.html',
  styleUrls: ['./review-analyzer.component.scss']
})
export class ReviewAnalyzerComponent {

  // Texto de la reseña escrito por el usuario en el textarea
  reviewText: string = '';

  // Almacena la respuesta completa del backend cuando llega
  analysisResult: AnalysisResponse | null = null;

  // Controla si se muestra el indicador de carga (spinner)
  isLoading: boolean = false;

  // Almacena mensajes de error si la petición falla
  errorMessage: string = '';

  // Inyectar el servicio de API para comunicarse con el backend
  constructor(private reviewApiService: ReviewApiService) {}

  /**
   * Método que se llama cuando el usuario hace clic en "Analizar reseña".
   * Envía el texto al backend y maneja la respuesta o error.
   */
  analyzeReview(): void {
    // Validar que el usuario escribió algo antes de enviar
    if (!this.reviewText.trim()) {
      this.errorMessage = 'Por favor escribe una reseña antes de analizar.';
      return;
    }

    // Limpiar estado anterior: quitar errores, ocultar resultados, mostrar spinner
    this.errorMessage = '';
    this.analysisResult = null;
    this.isLoading = true;

    // Llamar al servicio para hacer la petición POST al backend
    this.reviewApiService.analyzeReview({ text: this.reviewText }).subscribe({
      // Callback de éxito: se llama cuando el backend responde correctamente
      next: (response: AnalysisResponse) => {
        this.analysisResult = response;
        this.isLoading = false;
      },
      // Callback de error: se llama si la petición falla (backend caído, error de red, etc.)
      error: (err) => {
        this.errorMessage = 'Error al conectar con el backend. Asegúrate de que el servidor esté corriendo en http://localhost:8000';
        this.isLoading = false;
        console.error('Error de API:', err);
      }
    });
  }

  /**
   * Determina la clase CSS de color según el sentimiento detectado.
   * Esto cambia el color de la tarjeta de sentimiento visualmente.
   */
  getSentimentColorClass(): string {
    if (!this.analysisResult) return '';
    const label = this.analysisResult.sentiment.label.toLowerCase();
    if (label.includes('positivo')) return 'positive';
    if (label.includes('negativo')) return 'negative';
    return 'neutral';
  }

  /**
   * Limpia los resultados y el textarea para empezar de nuevo.
   */
  clearForm(): void {
    this.reviewText = '';
    this.analysisResult = null;
    this.errorMessage = '';
  }
}
