import { apiClient } from './client'

export const voiceApi = {
  // Tutor
  startTutorSession: (data: {
    subject: string
    difficulty: string
  }) => {
    return apiClient.post('/voice/tutor/start', {
      type: 'tutor',
      subject: data.subject,
      difficulty: data.difficulty,
    })
  },
  
  endTutorSession: (sessionId: string) => {
    return apiClient.post(`/voice/tutor/end/${sessionId}`)
  },
  
  // Language Practice
  startLanguagePractice: (data: {
    targetLanguage: string
    scenario: string
    proficiency: string
  }) => {
    return apiClient.post('/voice/language/start', data)
  },
  
  getSupportedLanguages: () => {
    return apiClient.get('/voice/language/languages')
  },
  
  getScenarios: () => {
    return apiClient.get('/voice/language/scenarios')
  },
  
  // Exam Prep
  startExamPrep: (data: {
    examType: string
    topics: string[]
    questionCount: number
  }) => {
    return apiClient.post('/voice/exam/start', data)
  },
  
  getAvailableExams: () => {
    return apiClient.get('/voice/exam/exams')
  },
  
  getExamTopics: (examType: string) => {
    return apiClient.get(`/voice/exam/topics/${examType}`)
  },
  
  // Pronunciation
  analyzePronunciation: (audioBlob: Blob, targetText?: string, language: string = 'en-US') => {
    const formData = new FormData()
    formData.append('audio_file', audioBlob, 'audio.webm')
    if (targetText) {
      formData.append('target_text', targetText)
    }
    formData.append('language', language)
    
    return apiClient.post('/voice/pronunciation/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
}