'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { Brain, BookOpen, Calculator, Flask, Code, History, Languages } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Select } from '@/components/ui/Select'
import { voiceApi } from '@/lib/api/voice'
import { toast } from 'react-hot-toast'

const subjects = [
  { id: 'math', name: 'Mathematics', icon: Calculator, description: 'Algebra, Calculus, Geometry' },
  { id: 'science', name: 'Science', icon: Flask, description: 'Physics, Chemistry, Biology' },
  { id: 'language', name: 'Language Arts', icon: BookOpen, description: 'Grammar, Writing, Literature' },
  { id: 'programming', name: 'Programming', icon: Code, description: 'Python, JavaScript, Algorithms' },
  { id: 'history', name: 'History', icon: History, description: 'World History, Civilizations' },
  { id: 'languages', name: 'Foreign Languages', icon: Languages, description: 'Spanish, French, German' },
]

const difficulties = [
  { value: 'beginner', label: 'Beginner - Just starting out' },
  { value: 'intermediate', label: 'Intermediate - Some experience' },
  { value: 'advanced', label: 'Advanced - Looking for challenges' },
]

export default function VoiceTutorPage() {
  const router = useRouter()
  const [selectedSubject, setSelectedSubject] = useState('')
  const [difficulty, setDifficulty] = useState('intermediate')
  const [isStarting, setIsStarting] = useState(false)

  const startSession = async () => {
    if (!selectedSubject) {
      toast.error('Please select a subject')
      return
    }

    setIsStarting(true)
    try {
      const response = await voiceApi.startTutorSession({
        subject: selectedSubject,
        difficulty,
      })
      
      router.push(`/voice-tutor/${selectedSubject}/session/${response.data.session_id}`)
    } catch (error) {
      toast.error('Failed to start session')
      setIsStarting(false)
    }
  }

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-4">AI Voice Tutor</h1>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Get personalized tutoring through natural conversation. Our AI adapts to your learning style and pace.
          </p>
        </div>

        {/* Subject Selection */}
        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Choose a subject</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {subjects.map((subject) => (
              <Card
                key={subject.id}
                className={`cursor-pointer transition-all hover:shadow-lg ${
                  selectedSubject === subject.id ? 'ring-2 ring-primary' : ''
                }`}
                onClick={() => setSelectedSubject(subject.id)}
              >
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <subject.icon className="mr-2 h-5 w-5" />
                    {subject.name}
                  </CardTitle>
                  <CardDescription>{subject.description}</CardDescription>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>

        {/* Difficulty Selection */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Select difficulty level</CardTitle>
          </CardHeader>
          <CardContent>
            <Select
              value={difficulty}
              onValueChange={(value) => setDifficulty(value)}
              className="w-full"
            >
              {difficulties.map((diff) => (
                <option key={diff.value} value={diff.value}>
                  {diff.label}
                </option>
              ))}
            </Select>
          </CardContent>
        </Card>

        {/* Start Button */}
        <div className="text-center">
          <Button
            size="lg"
            onClick={startSession}
            disabled={!selectedSubject || isStarting}
            className="min-w-[200px]"
          >
            {isStarting ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2" />
                Starting Session...
              </>
            ) : (
              <>
                <Brain className="mr-2 h-5 w-5" />
                Start Voice Session
              </>
            )}
          </Button>
        </div>
      </motion.div>
    </div>
  )
}