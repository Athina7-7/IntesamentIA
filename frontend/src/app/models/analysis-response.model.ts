// analysis-response.model.ts: Estructura completa de la respuesta del backend
import { SentimentResult } from './sentiment-result.model';
import { EmotionResult } from './emotion-result.model';

export interface AnalysisResponse {
  original_text: string;
  cleaned_text: string;
  sentiment: SentimentResult;
  emotion: EmotionResult;
  explanation: string;
  processing_time_seconds: number;
}
