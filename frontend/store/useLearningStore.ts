import { create } from 'zustand'

interface LearningState {
  currentSession: any | null
  sessions: any[]
  setCurrentSession: (session: any) => void
  addSession: (session: any) => void
}

export const useLearningStore = create<LearningState>((set) => ({
  currentSession: null,
  sessions: [],
  setCurrentSession: (session) => set({ currentSession: session }),
  addSession: (session) => set((state) => ({ sessions: [...state.sessions, session] })),
}))