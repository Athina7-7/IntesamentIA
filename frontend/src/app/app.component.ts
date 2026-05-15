// app.component.ts: Componente raíz de la aplicación Angular
// Es el punto de entrada del árbol de componentes

import { Component } from '@angular/core';
import { ReviewAnalyzerComponent } from './features/review-analyzer/review-analyzer.component';

@Component({
  selector: 'app-root',
  standalone: true,
  // Importar el componente principal de análisis de reseñas
  imports: [ReviewAnalyzerComponent],
  template: `<app-review-analyzer></app-review-analyzer>`,
  styles: [`
    :host { display: block; }
  `]
})
export class AppComponent {
  title = 'EmoReview';
}
