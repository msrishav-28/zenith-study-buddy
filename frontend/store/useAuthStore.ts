import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { authApi } from '@/lib/api/auth'

interface User {
  id: number
  username: string
  email: string
  fullName: string
  learningStyle: string
  isActive: boolean
  isPremium: boolean
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      
      login: async (username: string, password: string) => {
        const response = await authApi.login(username, password)
        const { access_token } = response.data
        
        // Get user data
        const userResponse = await authApi.getMe(access_token)
        
        set({
          token: access_token,
          user: userResponse.data,
          isAuthenticated: true,
        })
      },
      
      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
      },
      
      setUser: (user: User) => {
        set({ user })
      },
    }),
    {
      name: 'auth-storage',
    }
  )
)