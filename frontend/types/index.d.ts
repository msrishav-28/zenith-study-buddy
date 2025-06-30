export * from './learning'
export * from './voice'
export * from './omnidim'

export interface User {
  id: number
  username: string
  email: string
  fullName: string
  learningStyle: string
  preferredLanguage: string
  isActive: boolean
  isPremium: boolean
  isVerified: boolean
}

export interface ApiResponse<T = any> {
  data: T
  message?: string
  error?: string
}

export interface PaginationParams {
  page?: number
  limit?: number
  offset?: number
}