import { apiClient } from './client'

export const learningApi = {
  // Sessions
  getRecentSessions: (limit: number = 10) => {
    return apiClient.get('/learning/sessions', { params: { limit } })
  },
  
  getSessionDetails: (sessionId: string) => {
    return apiClient.get(`/learning/sessions/${sessionId}`)
  },
  
  // Progress
  getUserProgress: () => {
    return apiClient.get('/learning/progress')
  },
  
  updateStreak: () => {
    return apiClient.post('/learning/progress/update-streak')
  },
  
  // Analytics
  getAnalytics: (timeframe: 'week' | 'month' | 'year' = 'week') => {
    return apiClient.get('/learning/analytics/dashboard', { params: { timeframe } })
  },
  
  getInsights: () => {
    return apiClient.get('/learning/analytics/insights')
  },
  
  getTrends: (metric: string, days: number = 30) => {
    return apiClient.get('/learning/analytics/performance-trends', {
      params: { metric, days }
    })
  },
}