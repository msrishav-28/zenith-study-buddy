'use client'

import { useParams, useRouter } from 'next/navigation'
import { VoiceInterface } from '@/components/voice/VoiceInterface'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { ArrowLeft } from 'lucide-react'
import { toast } from 'react-hot-toast'

export default function VoiceSessionPage() {
  const params = useParams()
  const router = useRouter()
  const { subject, sessionId } = params as { subject: string; sessionId: string }

  const handleSessionEnd = () => {
    toast.success('Session ended successfully!')
    router.push('/dashboard')
  }

  return (
    <div className="container mx-auto p-6">
      <div className="mb-6">
        <Button
          variant="ghost"
          onClick={() => router.push('/voice-tutor')}
          className="mb-4"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Subject Selection
        </Button>
        
        <h1 className="text-3xl font-bold capitalize">
          {subject.replace('_', ' ')} Tutoring Session
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Ask questions, get explanations, and practice problems through voice
        </p>
      </div>

      <VoiceInterface
        sessionId={sessionId}
        mode="tutor"
        subject={subject}
        onSessionEnd={handleSessionEnd}
      />

      {/* Tips Card */}
      <Card className="mt-6 p-6">
        <h3 className="font-semibold mb-2">Voice Commands</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm">
          <div>• "Explain this again"</div>
          <div>• "Give me an example"</div>
          <div>• "Test my knowledge"</div>
          <div>• "Slower please"</div>
          <div>• "What does that mean?"</div>
          <div>• "I don't understand"</div>
          <div>• "Next topic"</div>
          <div>• "Review summary"</div>
        </div>
      </Card>
    </div>
  )
}