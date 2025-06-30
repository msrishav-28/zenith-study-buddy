'use client'

import { motion } from 'framer-motion'
import { Brain, Mic, Globe, Target, Sparkles, ArrowRight } from 'lucide-react'
import Link from 'next/link'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'

export default function HomePage() {
  return (
    <div className="relative">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-purple-950 dark:via-gray-900 dark:to-blue-950">
        <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
        
        <div className="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 sm:py-32 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl">
                Learn Through{' '}
                <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                  Natural Conversation
                </span>
              </h1>
              <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-gray-600 dark:text-gray-300">
                Experience personalized AI tutoring that adapts to your voice, emotions, and learning style. 
                Powered by Omnidim's advanced voice AI technology.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="mt-10 flex items-center justify-center gap-x-6"
            >
              <Link href="/register">
                <Button size="lg" className="group">
                  Start Learning Free
                  <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                </Button>
              </Link>
              <Link href="/demo">
                <Button size="lg" variant="outline">
                  <Mic className="mr-2 h-4 w-4" />
                  Try Voice Demo
                </Button>
              </Link>
            </motion.div>
          </div>

          {/* Feature Cards */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="mt-20 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4"
          >
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.5 + index * 0.1 }}
              >
                <Card className="relative h-full p-6 hover:shadow-lg transition-shadow">
                  <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-to-br from-purple-500 to-blue-500">
                    <feature.icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold">{feature.title}</h3>
                  <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                    {feature.description}
                  </p>
                </Card>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Demo Section */}
      <section className="py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              See It In Action
            </h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
              Watch how our AI tutors adapt to different learning scenarios
            </p>
          </div>

          <div className="mt-16 grid grid-cols-1 gap-8 lg:grid-cols-3">
            {demos.map((demo) => (
              <Card key={demo.title} className="overflow-hidden">
                <div className="aspect-video bg-gradient-to-br from-purple-100 to-blue-100 dark:from-purple-900 dark:to-blue-900"></div>
                <div className="p-6">
                  <h3 className="text-lg font-semibold">{demo.title}</h3>
                  <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                    {demo.description}
                  </p>
                  <Button className="mt-4" variant="outline" size="sm">
                    Watch Demo
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

const features = [
  {
    title: 'AI Voice Tutor',
    description: 'Natural conversations with subject-expert AI tutors that adapt to your learning style.',
    icon: Brain,
  },
  {
    title: 'Language Practice',
    description: 'Practice any language with native-speaking AI partners and real-time pronunciation feedback.',
    icon: Globe,
  },
  {
    title: 'Exam Preparation',
    description: 'Voice-based quizzing and explanations to help you ace your exams.',
    icon: Target,
  },
  {
    title: 'Emotion-Aware',
    description: 'AI that detects and responds to your emotions for optimal learning.',
    icon: Sparkles,
  },
]

const demos = [
  {
    title: 'Math Tutoring Session',
    description: 'See how our AI explains complex calculus concepts through conversation.',
  },
  {
    title: 'Spanish Conversation',
    description: 'Watch a real-time language practice session with pronunciation feedback.',
  },
  {
    title: 'SAT Prep Quiz',
    description: 'Experience adaptive questioning that adjusts to your knowledge level.',
  },
]