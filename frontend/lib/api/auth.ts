import { apiClient } from './client'

export const authApi = {
  register: (data: {
    username: string
    email: string
    password: string
    full_name: string
    learning_style: string
  }) => {
    return apiClient.post('/auth/register', data)
  },
  
  login: (username: string, password: string) => {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    
    return apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  
  getMe: (token: string) => {
    return apiClient.get('/auth/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  },
  
  logout: () => {
    return apiClient.post('/auth/logout')
  },
}