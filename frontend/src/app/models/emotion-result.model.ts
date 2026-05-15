// emotion-result.model.ts: Estructura del resultado de emoción recibido del backend
import { ScoreItem } from './score-item.model';

export interface EmotionResult {
  label: string;
  score: number;
  all_scores: ScoreItem[];
}
