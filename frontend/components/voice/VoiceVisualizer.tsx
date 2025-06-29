'use client'

import { useEffect, useRef } from 'react'
import { motion } from 'framer-motion'

interface VoiceVisualizerProps {
  audioLevel: number
  isActive: boolean
  mode: 'user' | 'ai'
}

export function VoiceVisualizer({ audioLevel, isActive, mode }: VoiceVisualizerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const animationRef = useRef<number>()
  
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    
    const width = canvas.width
    const height = canvas.height
    const centerX = width / 2
    const centerY = height / 2
    
    let phase = 0
    
    const draw = () => {
      ctx.clearRect(0, 0, width, height)
      
      if (!isActive) {
        // Draw idle state
        ctx.strokeStyle = mode === 'ai' ? '#8b5cf6' : '#3b82f6'
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.arc(centerX, centerY, 40, 0, Math.PI * 2)
        ctx.stroke()
      } else {
        // Draw active waveform
        const gradient = ctx.createLinearGradient(0, 0, width, 0)
        if (mode === 'ai') {
          gradient.addColorStop(0, '#8b5cf6')
          gradient.addColorStop(0.5, '#ec4899')
          gradient.addColorStop(1, '#8b5cf6')
        } else {
          gradient.addColorStop(0, '#3b82f6')
          gradient.addColorStop(0.5, '#06b6d4')
          gradient.addColorStop(1, '#3b82f6')
        }
        
        ctx.strokeStyle = gradient
        ctx.lineWidth = 3
        
        // Draw waveform
        ctx.beginPath()
        const segments = 100
        for (let i = 0; i <= segments; i++) {
          const x = (width / segments) * i
          const baseY = centerY
          const amplitude = audioLevel * 50
          const frequency = 0.02
          const y = baseY + amplitude * Math.sin(phase + i * frequency) * Math.sin(i * 0.05)
          
          if (i === 0) {
            ctx.moveTo(x, y)
          } else {
            ctx.lineTo(x, y)
          }
        }
        ctx.stroke()
        
        // Draw particles
        if (audioLevel > 0.3) {
          for (let i = 0; i < 5; i++) {
            const particleX = Math.random() * width
            const particleY = centerY + (Math.random() - 0.5) * audioLevel * 100
            const particleSize = Math.random() * 3 + 1
            
            ctx.fillStyle = mode === 'ai' ? '#ec4899' : '#06b6d4'
            ctx.globalAlpha = audioLevel
            ctx.beginPath()
            ctx.arc(particleX, particleY, particleSize, 0, Math.PI * 2)
            ctx.fill()
          }
          ctx.globalAlpha = 1
        }
        
        phase += 0.1
      }
      
      animationRef.current = requestAnimationFrame(draw)
    }
    
    draw()
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [audioLevel, isActive, mode])
  
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      className="relative w-full max-w-2xl"
    >
      <canvas
        ref={canvasRef}
        width={800}
        height={200}
        className="w-full h-32 rounded-lg bg-gray-100 dark:bg-gray-800"
      />
      
      {/* Glow effect when active */}
      {isActive && (
        <motion.div
          className="absolute inset-0 rounded-lg"
          animate={{
            boxShadow: [
              `0 0 20px rgba(${mode === 'ai' ? '139, 92, 246' : '59, 130, 246'}, 0.3)`,
              `0 0 40px rgba(${mode === 'ai' ? '139, 92, 246' : '59, 130, 246'}, 0.5)`,
              `0 0 20px rgba(${mode === 'ai' ? '139, 92, 246' : '59, 130, 246'}, 0.3)`,
            ]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
      )}
    </motion.div>
  )
}