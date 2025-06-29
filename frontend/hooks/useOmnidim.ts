import { useState, useCallback, useRef, useEffect } from 'react'
import { toast } from 'react-hot-toast'

interface OmnidimConfig {
  sessionId: string
  mode: 'tutor' | 'language_practice' | 'exam_prep'
  onTranscript?: (text: string, speaker: 'user' | 'ai') => void
  onEmotion?: (emotion: string, confidence: number) => void
  onPronunciation?: (score: number, feedback: string) => void
  onInsight?: (category: string, content: any) => void
  onError?: (error: Error) => void
}

export function useOmnidim(config: OmnidimConfig) {
  const [isConnected, setIsConnected] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [audioLevel, setAudioLevel] = useState(0)
  
  const wsRef = useRef<WebSocket | null>(null)
  const mediaStreamRef = useRef<MediaStream | null>(null)
  const audioContextRef = useRef<AudioContext | null>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioQueueRef = useRef<Blob[]>([])
  
  // Connect to Omnidim WebSocket
  const connect = useCallback(async () => {
    try {
      // Get microphone permission
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          sampleRate: 48000
        }
      })
      mediaStreamRef.current = stream
      
      // Setup audio context for level monitoring
      audioContextRef.current = new AudioContext()
      const source = audioContextRef.current.createMediaStreamSource(stream)
      const analyser = audioContextRef.current.createAnalyser()
      analyser.fftSize = 256
      source.connect(analyser)
      
      // Monitor audio levels
      const dataArray = new Uint8Array(analyser.frequencyBinCount)
      const checkAudioLevel = () => {
        if (!audioContextRef.current) return
        
        analyser.getByteFrequencyData(dataArray)
        const average = dataArray.reduce((a, b) => a + b) / dataArray.length
        setAudioLevel(average / 255)
        
        requestAnimationFrame(checkAudioLevel)
      }
      checkAudioLevel()
      
      // Setup WebSocket connection
      const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL}/api/voice/ws/${config.sessionId}`
      const ws = new WebSocket(wsUrl)
      wsRef.current = ws
      
      ws.binaryType = 'arraybuffer'
      
      ws.onopen = () => {
        setIsConnected(true)
        setupMediaRecorder(stream)
        toast.success('Voice session connected')
      }
      
      ws.onmessage = async (event) => {
        if (event.data instanceof ArrayBuffer) {
          // Handle audio response
          await playAudioResponse(event.data)
        } else {
          // Handle JSON messages
          const data = JSON.parse(event.data)
          handleMessage(data)
        }
      }
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        config.onError?.(new Error('Connection failed'))
      }
      
      ws.onclose = () => {
        setIsConnected(false)
        setIsRecording(false)
        cleanup()
      }
      
    } catch (error) {
      console.error('Failed to connect:', error)
      config.onError?.(error as Error)
      toast.error('Failed to start voice session')
    }
  }, [config])
  
  // Setup media recorder for streaming audio
  const setupMediaRecorder = (stream: MediaStream) => {
    const recorder = new MediaRecorder(stream, {
      mimeType: 'audio/webm;codecs=opus',
      audioBitsPerSecond: 128000
    })
    
    recorder.ondataavailable = (event) => {
      if (event.data.size > 0 && wsRef.current?.readyState === WebSocket.OPEN) {
        // Send audio data to server
        wsRef.current.send(event.data)
      }
    }
    
    mediaRecorderRef.current = recorder
  }
  
  // Start recording
  const startRecording = useCallback(() => {
    if (mediaRecorderRef.current && !isRecording) {
      mediaRecorderRef.current.start(100) // Send chunks every 100ms
      setIsRecording(true)
    }
  }, [isRecording])
  
  // Stop recording
  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }, [isRecording])
  
  // Handle incoming messages
  const handleMessage = (data: any) => {
    switch (data.type) {
      case 'transcript':
        config.onTranscript?.(data.text, data.speaker)
        break
        
      case 'emotion':
        config.onEmotion?.(data.emotion, data.confidence)
        break
        
      case 'pronunciation':
        config.onPronunciation?.(data.score, data.feedback)
        break
        
      case 'insight':
        config.onInsight?.(data.category, data.content)
        break
        
      case 'error':
        config.onError?.(new Error(data.message))
        toast.error(data.message)
        break
    }
  }
  
  // Play audio response
  const playAudioResponse = async (audioData: ArrayBuffer) => {
    try {
      const audioBlob = new Blob([audioData], { type: 'audio/webm' })
      const audioUrl = URL.createObjectURL(audioBlob)
      const audio = new Audio(audioUrl)
      
      // Pause recording while AI is speaking
      stopRecording()
      
      audio.onended = () => {
        URL.revokeObjectURL(audioUrl)
        // Resume recording after AI finishes speaking
        startRecording()
      }
      
      await audio.play()
    } catch (error) {
      console.error('Failed to play audio:', error)
    }
  }
  
  // Send text message
  const sendMessage = useCallback((text: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'text',
        content: text
      }))
    }
  }, [])
  
  // Cleanup
  const cleanup = () => {
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach(track => track.stop())
      mediaStreamRef.current = null
    }
    
    if (audioContextRef.current) {
      audioContextRef.current.close()
      audioContextRef.current = null
    }
    
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
  }
  
  // Disconnect
  const disconnect = useCallback(() => {
    cleanup()
    toast.success('Voice session ended')
  }, [])
  
  // Auto-cleanup on unmount
  useEffect(() => {
    return () => {
      cleanup()
    }
  }, [])
  
  return {
    isConnected,
    isRecording,
    audioLevel,
    connect,
    disconnect,
    startRecording,
    stopRecording,
    sendMessage
  }
}