export interface VoiceSessionConfig {
  mode: 'tutor' | 'language_practice' | 'exam_prep'
  userId: string
  subject?: string
  language?: string
  difficulty?: string
  scenario?: string
  proficiency?: string
}

export interface VoiceMessage {
  type: 'transcript' | 'emotion' | 'pronunciation' | 'audio' | 'error'
  text?: string
  speaker?: 'user' | 'ai'
  emotion?: string
  confidence?: number
  score?: number
  feedback?: string
  data?: ArrayBuffer
}

export interface PronunciationAnalysis {
  overallScore: number
  phonemeScores: PhonemeScore[]
  fluencyScore: number
  suggestions: string[]
  audioFeedbackUrl?: string
}

export interface PhonemeScore {
  phoneme: string
  accuracy: number
  confidence: number
  detected: string
  expected: string
}

export interface EmotionData {
  primaryEmotion: string
  confidence: number
  secondaryEmotions?: Array<{ emotion: string; confidence: number }>
  teachingAdaptation: Record<string, any>
}