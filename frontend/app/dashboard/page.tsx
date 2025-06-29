'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Brain, Clock, Target, TrendingUp, Award, Calendar } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Progress } from '@/components/ui/Progress'
import { useAuthStore } from '@/store/useAuthStore'
import { learningApi } from '@/lib/api/learning'
import { formatDuration, formatDate } from '@/lib/utils'
import Link from 'next/link'

export default function DashboardPage() {
  const { user } = useAuthStore()
  const [stats, setStats] = useState<any>(null)
  const [recentSessions, setRecentSessions] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const [statsRes, sessionsRes] = await Promise.all([
        learningApi.getAnalytics('week'),
        learningApi.getRecentSessions(5),
      ])
      
      setStats(statsRes.data)
      setRecentSessions(sessionsRes.data)
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-pulse">Loading...</div>
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6 space-y-8">
      {/* Welcome Section */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Welcome back, {user?.fullName}!</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Ready to continue your learning journey?
          </p>
        </div>
        <Link href="/voice-tutor">
          <Button size="lg">
            <Brain className="mr-2 h-5 w-5" />
            Start Learning
          </Button>
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Study Streak</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.currentStreak || 0} days</div>
            <p className="text-xs text-muted-foreground">
              Keep it up! Your longest: {stats?.longestStreak || 0} days
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Study Time</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatDuration(stats?.totalStudyTime || 0)}
            </div>
            <p className="text-xs text-muted-foreground">
              This week: {formatDuration(stats?.weeklyStudyTime || 0)}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Accuracy</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round((stats?.overallAccuracy || 0) * 100)}%
            </div>
            <Progress value={(stats?.overallAccuracy || 0) * 100} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Level</CardTitle>
            <Award className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Level {stats?.level || 1}</div>
            <p className="text-xs text-muted-foreground">
              {stats?.experiencePoints || 0} XP earned
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Recent Sessions */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Sessions</CardTitle>
          <CardDescription>Your latest learning activities</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentSessions.map((session) => (
              <div
                key={session.id}
                className="flex items-center justify-between p-4 rounded-lg border"
              >
                <div className="space-y-1">
                  <p className="font-medium capitalize">
                    {session.type.replace('_', ' ')} - {session.subject}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    {formatDate(session.startedAt)} • {formatDuration(session.durationSeconds)}
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-medium">
                    {Math.round((session.comprehensionScore || 0) * 100)}%
                  </p>
                  <p className="text-sm text-muted-foreground">Score</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-3">
        <Link href="/voice-tutor">
          <Card className="cursor-pointer hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Brain className="mr-2 h-5 w-5" />
                Voice Tutor
              </CardTitle>
              <CardDescription>
                Get personalized help on any subject
              </CardDescription>
            </CardHeader>
          </Card>
        </Link>

        <Link href="/language-practice">
          <Card className="cursor-pointer hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Calendar className="mr-2 h-5 w-5" />
                Practice Schedule
              </CardTitle>
              <CardDescription>
                View your upcoming practice sessions
              </CardDescription>
            </CardHeader>
          </Card>
        </Link>

        <Link href="/exam-prep">
          <Card className="cursor-pointer hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Target className="mr-2 h-5 w-5" />
                Exam Prep
              </CardTitle>
              <CardDescription>
                Prepare for your upcoming exams
              </CardDescription>
            </CardHeader>
          </Card>
        </Link>
      </div>
    </div>
  )
}