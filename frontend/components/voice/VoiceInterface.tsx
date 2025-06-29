'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Mic, MicOff, Volume2, Brain, Loader2, Settings } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { VoiceVisualizer } from './VoiceVisualizer'
import { TranscriptDisplay } from './TranscriptDisplay'
import { EmotionIndicator } from './EmotionIndicator'
import { useOmnidim } from '@/hooks/useOmnidim'

interface VoiceInterfaceProps {
  sessionId: string
  mode: 'tutor' | 'language_practice' | 'exam_prep'
  subject?: string
  onSessionEnd?: () => void
}

export function VoiceInterface({
  sessionId,
  mode,
  subject,
  onSessionEnd
}: VoiceInterfaceProps) {
  const [transcript, setTranscript] = useState<Array<{
    text: string
    speaker: 'user' | 'ai'
    timestamp: Date
  }>>([])
  const [currentEmotion, setCurrentEmotion] = useState<string>('neutral')
  const [isAISpeaking, setIsAISpeaking] = useState(false)
  
  const {
    isConnected,
    isRecording,
    audioLevel,
    connect,
    disconnect,
    startRecording,
    stopRecording
  } = useOmnidim({
    sessionId,
    mode,
    onTranscript: (text, speaker) => {
      setTranscript(prev => [...prev, {
        text,
        speaker,
        timestamp: new Date()
      }])
      setIsAISpeaking(speaker === 'ai')
    },
    onEmotion: (emotion, confidence) => {
      if (confidence > 0.7) {
        setCurrentEmotion(emotion)
      }
    },
    onError: (error) => {
      console.error('Voice error:', error)
    }
  })
  
  useEffect(() => {
    connect()
    return () => {
      disconnect()
    }
  }, [connect, disconnect])
  
  const toggleRecording = () => {
    if (isRecording) {
      stopRecording()
    } else {
      startRecording()
    }
  }
  
  const endSession = () => {
    disconnect()
    onSessionEnd?.()
  }
  
  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      {/* AI Avatar and Visualizer */}
      <Card className="p-8 bg-gradient-to-br from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20">
        <div className="flex flex-col items-center space-y-6">
          {/* AI Avatar */}
          <motion.div
            animate={{
              scale: isAISpeaking ? [1, 1.05, 1] : 1,
            }}
            transition={{
              duration: 2,
              repeat: isAISpeaking ? Infinity : 0,
              ease: "easeInOut"
            }}
            className="relative"
          >
            <div className="w-32 h-32 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
              <Brain className="w-16 h-16 text-white" />
            </div>
            
            {/* Connection Status */}
            <motion.div
              className="absolute -bottom-2 -right-2"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
            >
              <div className={`w-6 h-6 rounded-full ${
                isConnected ? 'bg-green-500' : 'bg-red-500'
              } border-4 border-white dark:border-gray-800`} />
            </motion.div>
          </motion.div>
          
          {/* Status Text */}
          <div className="text-center">
            <h3 className="text-xl font-semibold">
              {mode === 'tutor' && 'AI Tutor'}
              {mode === 'language_practice' && 'Language Coach'}
              {mode === 'exam_prep' && 'Exam Companion'}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              {isConnected ? (
                isAISpeaking ? "Speaking..." : "Listening..."
              ) : (
                "Connecting..."
              )}
            </p>
          </div>
          
          {/* Emotion Indicator */}
          <EmotionIndicator emotion={currentEmotion} />
          
          {/* Voice Visualizer */}
          <VoiceVisualizer 
            audioLevel={audioLevel}
            isActive={isRecording || isAISpeaking}
            mode={isAISpeaking ? 'ai' : 'user'}
          />
        </div>
      </Card>
      
      {/* Transcript Display */}
      <Card className="p-6">
        <div className="flex justify-between items-center mb-4">
          <h4 className="text-lg font-semibold">Conversation</h4>
          <Button variant="ghost" size="sm">
            <Settings className="w-4 h-4" />
          </Button>
        </div>
        <TranscriptDisplay messages={transcript} />
      </Card>
      
      {/* Controls */}
      <div className="flex justify-center gap-4">
        {!isConnected ? (
          <Button size="lg" disabled>
            <Loader2 className="mr-2 h-5 w-5 animate-spin" />
            Connecting...
          </Button>
        ) : (
          <>
            <Button
              size="lg"
              variant={isRecording ? "destructive" : "default"}
              onClick={toggleRecording}
              disabled={isAISpeaking}
            >
              {isRecording ? (
                <>
                  <MicOff className="mr-2 h-5 w-5" />
                  Stop Speaking
                </>
              ) : (
                <>
                  <Mic className="mr-2 h-5 w-5" />
                  Start Speaking
                </>
              )}
            </Button>
            
            <Button
              size="lg"
              variant="outline"
              onClick={endSession}
            >
              End Session
            </Button>
          </>
        )}
      </div>
      
      {/* Quick Phrases */}
      {mode === 'tutor' && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
          <Button variant="outline" size="sm" onClick={() => {}}>
            "Explain again"
          </Button>
          <Button variant="outline" size="sm" onClick={() => {}}>
            "Give example"
          </Button>
          <Button variant="outline" size="sm" onClick={() => {}}>
            "Test me"
          </Button>
          <Button variant="outline" size="sm" onClick={() => {}}>
            "Slower please"
          </Button>
        </div>
      )}
    </div>
  )
}