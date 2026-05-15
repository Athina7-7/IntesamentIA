// app.config.ts: Configuración de la aplicación Angular (modo standalone)
// Aquí se registran los providers globales como HttpClient

import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';

// provideHttpClient() habilita HttpClient en toda la aplicación
// Esto es necesario para que ReviewApiService pueda hacer peticiones HTTP al backend
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter([]),        // Router vacío: esta app es de una sola página
    provideHttpClient()       // Habilita HttpClient para peticiones HTTP
  ]
};
