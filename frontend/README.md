# IntesamentIA – Frontend Angular

Interfaz web del sistema IntesamentIA. Consume la API REST del backend FastAPI.

## Comandos

```bash
npm install
ng serve
```

Disponible en: `http://localhost:4200`

## Estructura

```
src/app/
├── core/services/       → review-api.service.ts (HTTP al backend)
├── models/              → Interfaces TypeScript (tipado de la respuesta)
├── features/            → review-analyzer (componente principal)
└── shared/components/   → result-card, confidence-chart (reutilizables)
```
