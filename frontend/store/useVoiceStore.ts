import { create } from 'zustand'

interface VoiceState {
  isRecording: boolean
  isConnected: boolean
  audioLevel: number
  currentEmotion: string
  sessionId: string | null
  setRecording: (recording: boolean) => void
  setConnected: (connected: boolean) => void
  setAudioLevel: (level: number) => void
  setEmotion: (emotion: string) => void
  setSessionId: (id: string | null) => void
}

export const useVoiceStore = create<VoiceState>((set) => ({
  isRecording: false,
  isConnected: false,
  audioLevel: 0,
  currentEmotion: 'neutral',
  sessionId: null,
  setRecording: (recording) => set({ isRecording: recording }),
  setConnected: (connected) => set({ isConnected: connected }),
  setAudioLevel: (level) => set({ audioLevel: level }),
  setEmotion: (emotion) => set({ currentEmotion: emotion }),
  setSessionId: (id) => set({ sessionId: id }),
}))