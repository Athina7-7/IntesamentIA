// sentiment-result.model.ts: Estructura del resultado de sentimiento recibido del backend
import { ScoreItem } from './score-item.model';

export interface SentimentResult {
  label: string;
  score: number;
  all_scores: ScoreItem[];
}
