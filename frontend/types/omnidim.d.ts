export interface OmnidimSession {
  sessionId: string
  userId: string
  mode: string
  status: 'active' | 'paused' | 'completed'
  createdAt: string
  config: OmnidimSessionConfig
}

export interface OmnidimSessionConfig {
  mode: string
  userId: string
  context: Record<string, any>
  features: string[]
  voiceId: string
  language: string
}

export interface OmnidimVoiceModel {
  id: string
  name: string
  language: string
  accent?: string
  gender?: string
  ageRange?: string
  personality?: Record<string, any>
  supportedFeatures: string[]
}

export interface OmnidimAnalysisResult {
  transcript?: string
  pronunciation?: {
    phonemes: Array<{
      phoneme: string
      accuracy: number
      confidence: number
      detected: string
      expected: string
    }>
  }
  emotion?: {
    primary: string
    confidence: number
    allEmotions: Record<string, number>
    arousal: number
    valence: number
  }
  metrics?: {
    wpm: number
    pauseRatio: number
    clarity: number
    confidence: number
  }
  overallScore?: number
}