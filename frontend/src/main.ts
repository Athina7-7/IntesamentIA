// main.ts: Punto de entrada de la aplicación Angular
// bootstrapApplication inicia la aplicación con el componente raíz y la configuración

import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

// Iniciar la aplicación Angular; si hay error, mostrarlo en consola
bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
