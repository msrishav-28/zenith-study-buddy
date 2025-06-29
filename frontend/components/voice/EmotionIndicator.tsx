'use client'

import { motion } from 'framer-motion'
import { Smile, Meh, Frown, AlertCircle, HelpCircle, Zap } from 'lucide-react'

interface EmotionIndicatorProps {
  emotion: string
  confidence?: number
}

const emotionConfig = {
  happy: { icon: Smile, color: 'text-green-500', label: 'Happy' },
  neutral: { icon: Meh, color: 'text-gray-500', label: 'Neutral' },
  confused: { icon: HelpCircle, color: 'text-yellow-500', label: 'Confused' },
  frustrated: { icon: Frown, color: 'text-red-500', label: 'Frustrated' },
  excited: { icon: Zap, color: 'text-purple-500', label: 'Excited' },
  concerned: { icon: AlertCircle, color: 'text-orange-500', label: 'Concerned' },
}

export function EmotionIndicator({ emotion, confidence = 1 }: EmotionIndicatorProps) {
  const config = emotionConfig[emotion as keyof typeof emotionConfig] || emotionConfig.neutral
  const Icon = config.icon

  return (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      transition={{ type: 'spring', stiffness: 500, damping: 30 }}
      className="flex items-center space-x-2"
    >
      <div className={`relative ${config.color}`}>
        <Icon className="w-8 h-8" />
        {confidence < 0.7 && (
          <div className="absolute -top-1 -right-1 w-3 h-3 bg-yellow-400 rounded-full" />
        )}
      </div>
      <div>
        <p className="text-sm font-medium">{config.label}</p>
        {confidence && (
          <p className="text-xs text-gray-500">
            {Math.round(confidence * 100)}% confident
          </p>
        )}
      </div>
    </motion.div>
  )
}