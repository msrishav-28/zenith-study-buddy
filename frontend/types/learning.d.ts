export interface LearningSession {
  id: string
  userId: number
  type: SessionType
  subject?: string
  language?: string
  difficulty?: string
  startedAt: string
  endedAt?: string
  durationSeconds: number
  status: SessionStatus
  interactionCount: number
  comprehensionScore?: number
  pronunciationScore?: number
  averageEmotionScore?: number
}

export type SessionType = 'tutor' | 'language_practice' | 'exam_prep' | 'pronunciation'
export type SessionStatus = 'active' | 'completed' | 'abandoned'

export interface Progress {
  totalStudyTime: number
  totalSessions: number
  currentStreak: number
  longestStreak: number
  level: number
  experiencePoints: number
  overallAccuracy: number
  subjectProgress: Record<string, any>
}

export interface Achievement {
  id: number
  name: string
  description: string
  icon: string
  category: string
  earnedAt: string
  progressValue: number
  progressMax: number
}

export interface AnalyticsData {
  dailyStats: DailyStat[]
  weeklyProgress: WeeklyProgress
  learningInsights: string[]
  recommendedFocusAreas: string[]
}

export interface DailyStat {
  date: string
  sessions: number
  totalTime: number
  avgScore: number
}

export interface WeeklyProgress {
  totalTime: number
  sessionsCompleted: number
  averageScore: number
  improvement: number
}