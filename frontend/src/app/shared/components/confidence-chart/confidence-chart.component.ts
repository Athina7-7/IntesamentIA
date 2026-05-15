// confidence-chart.component.ts: Componente que muestra un gráfico de barras con Chart.js
// Recibe los datos del componente padre y renderiza el gráfico

import { Component, Input, OnChanges, SimpleChanges, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScoreItem } from '../../../models/score-item.model';
import { Chart, registerables } from 'chart.js';

// Registrar todos los componentes de Chart.js (ejes, escalas, tooltips, etc.)
Chart.register(...registerables);

@Component({
  selector: 'app-confidence-chart',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './confidence-chart.component.html',
  styleUrls: ['./confidence-chart.component.scss']
})
export class ConfidenceChartComponent implements AfterViewInit, OnChanges {

  // Datos a graficar: lista de etiquetas con sus puntuaciones
  @Input() scores: ScoreItem[] = [];

  // Título del gráfico (ej: "Distribución de Sentimientos")
  @Input() chartTitle: string = '';

  // Color de las barras (hexadecimal)
  @Input() barColor: string = '#6366f1';

  // Referencia al elemento canvas HTML donde se dibuja el gráfico
  @ViewChild('chartCanvas') chartCanvas!: ElementRef<HTMLCanvasElement>;

  // Instancia del gráfico de Chart.js
  private chart: Chart | null = null;

  // ngAfterViewInit: se ejecuta cuando el DOM ya está disponible (el canvas existe)
  ngAfterViewInit(): void {
    this.renderChart();
  }

  // ngOnChanges: se ejecuta cuando los @Input() cambian (nuevos datos llegaron)
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['scores'] && this.chartCanvas) {
      // Destruir el gráfico anterior si existe, antes de crear uno nuevo
      if (this.chart) {
        this.chart.destroy();
      }
      this.renderChart();
    }
  }

  /**
   * Crea el gráfico de barras con Chart.js usando los datos de scores.
   */
  private renderChart(): void {
    if (!this.chartCanvas || this.scores.length === 0) return;

    const ctx = this.chartCanvas.nativeElement.getContext('2d');
    if (!ctx) return;

    // Extraer etiquetas y valores de la lista de ScoreItem
    const labels = this.scores.map(s => s.label);
    const data = this.scores.map(s => parseFloat((s.score * 100).toFixed(1)));

    this.chart = new Chart(ctx, {
      type: 'bar',  // Tipo de gráfico: barras verticales
      data: {
        labels,
        datasets: [{
          label: 'Confianza (%)',
          data,
          backgroundColor: this.barColor + 'cc',  // Color con transparencia
          borderColor: this.barColor,
          borderWidth: 1,
          borderRadius: 6,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },  // Ocultar leyenda para mantener limpieza visual
          title: {
            display: true,
            text: this.chartTitle,
            color: '#e2e8f0',
            font: { size: 14, weight: 'bold' }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,  // El eje Y va de 0 a 100 (porcentaje)
            ticks: { color: '#94a3b8', callback: (v) => `${v}%` },
            grid: { color: 'rgba(255,255,255,0.05)' }
          },
          x: {
            ticks: { color: '#94a3b8' },
            grid: { display: false }
          }
        }
      }
    });
  }
}
