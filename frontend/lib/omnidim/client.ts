import axios from 'axios'

const OMNIDIM_API_URL = process.env.NEXT_PUBLIC_OMNIDIM_API_URL || 'https://api.omnidim.io/v1'

class OmnidimClient {
  private apiKey: string
  
  constructor(apiKey: string) {
    this.apiKey = apiKey
  }
  
  async createSession(config: {
    mode: 'tutor' | 'language_practice' | 'exam_prep'
    userId: string
    context: any
  }) {
    const response = await axios.post(
      `${OMNIDIM_API_URL}/sessions/create`,
      config,
      {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        }
      }
    )
    return response.data
  }
  
  async getVoiceModels(language?: string) {
    const params = language ? { language } : {}
    const response = await axios.get(
      `${OMNIDIM_API_URL}/voices`,
      {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`
        },
        params
      }
    )
    return response.data.voices
  }
  
  async analyzeSpeech(audioBlob: Blob, analysisType: string = 'full') {
    const formData = new FormData()
    formData.append('audio', audioBlob, 'audio.webm')
    formData.append('analysis_type', analysisType)
    
    const response = await axios.post(
      `${OMNIDIM_API_URL}/analyze/speech`,
      formData,
      {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`
        }
      }
    )
    return response.data
  }
}

export default OmnidimClient