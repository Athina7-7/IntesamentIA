// result-card.component.ts: Componente reutilizable que muestra una tarjeta de resultado
// Recibe datos desde el componente padre via @Input()

import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-result-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './result-card.component.html',
  styleUrls: ['./result-card.component.scss']
})
export class ResultCardComponent {
  // @Input() permite que el componente padre pase datos a este componente
  @Input() title: string = '';         // Ej: "Sentimiento" o "Emoción"
  @Input() label: string = '';         // Ej: "positivo" o "alegría"
  @Input() score: number = 0;          // Confianza entre 0 y 1
  @Input() colorClass: string = '';    // Clase CSS para colorear según resultado

  /**
   * Convierte el score (0-1) a porcentaje legible.
   * Ej: 0.9823 → "98.2%"
   */
  get scorePercent(): string {
    return `${(this.score * 100).toFixed(1)}%`;
  }
}
