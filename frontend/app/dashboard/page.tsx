'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Brain, Clock, Target, TrendingUp, Award, Calendar, 
  Sparkles, BookOpen, Mic, ChevronRight
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Progress } from '@/components/ui/Progress'
import { useAuthStore } from '@/store/useAuthStore'
import { learningApi } from '@/lib/api/learning'
import { formatDuration, formatDate } from '@/lib/utils'
import Link from 'next/link'

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

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
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Brain className="w-16 h-16 text-primary mx-auto mb-4 animate-pulse" />
          <p className="text-lg text-muted-foreground">Loading your learning journey...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-purple-50/20 dark:from-gray-950 dark:via-gray-900 dark:to-purple-950/20">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Welcome Section */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                Welcome back, {user?.fullName?.split(' ')[0]}!
              </h1>
              <p className="text-lg text-muted-foreground mt-2">
                You're on a {stats?.currentStreak || 0} day learning streak! Keep it up! 🔥
              </p>
            </div>
            <Link href="/voice-tutor">
              <Button size="lg" variant="gradient" className="group">
                <Mic className="mr-2 h-5 w-5" />
                Start Learning
                <ChevronRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
          </div>
        </motion.div>

        {/* Stats Grid */}
        <motion.div 
          variants={container}
          initial="hidden"
          animate="show"
          className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8"
        >
          <motion.div variants={item}>
            <Card hover glass className="relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-orange-500/20 to-red-500/20 rounded-full blur-3xl" />
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Study Streak</CardTitle>
                <div className="p-2 bg-orange-100 dark:bg-orange-900/20 rounded-lg">
                  <Target className="h-5 w-5 text-orange-600 dark:text-orange-400" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{stats?.currentStreak || 0} days</div>
                <p className="text-xs text-muted-foreground mt-1">
                  Best: {stats?.longestStreak || 0} days
                </p>
                <div className="mt-3 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-orange-500 to-red-500 transition-all duration-500"
                    style={{ width: `${Math.min((stats?.currentStreak / stats?.longestStreak) * 100, 100)}%` }}
                  />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={item}>
            <Card hover glass className="relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-full blur-3xl" />
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Study Time</CardTitle>
                <div className="p-2 bg-blue-100 dark:bg-blue-900/20 rounded-lg">
                  <Clock className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">
                  {formatDuration(stats?.totalStudyTime || 0)}
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  This week: {formatDuration(stats?.weeklyStudyTime || 0)}
                </p>
                <Progress value={65} className="mt-3 h-2" />
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={item}>
            <Card hover glass className="relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-full blur-3xl" />
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Accuracy</CardTitle>
                <div className="p-2 bg-green-100 dark:bg-green-900/20 rounded-lg">
                  <TrendingUp className="h-5 w-5 text-green-600 dark:text-green-400" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">
                  {Math.round((stats?.overallAccuracy || 0) * 100)}%
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  +2.5% from last week
                </p>
                <div className="mt-3 flex items-center gap-1">
                  {[...Array(5)].map((_, i) => (
                    <div
                      key={i}
                      className={`h-2 flex-1 rounded-full ${
                        i < Math.floor((stats?.overallAccuracy || 0) * 5)
                          ? 'bg-green-500'
                          : 'bg-gray-200 dark:bg-gray-700'
                      }`}
                    />
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={item}>
            <Card hover glass className="relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-full blur-3xl" />
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Level Progress</CardTitle>
                <div className="p-2 bg-purple-100 dark:bg-purple-900/20 rounded-lg">
                  <Award className="h-5 w-5 text-purple-600 dark:text-purple-400" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">Level {stats?.level || 1}</div>
                <p className="text-xs text-muted-foreground mt-1">
                  {stats?.experiencePoints || 0} / {((stats?.level || 1) * 1000)} XP
                </p>
                <Progress 
                  value={(stats?.experiencePoints || 0) / ((stats?.level || 1) * 1000) * 100} 
                  className="mt-3 h-2"
                />
              </CardContent>
            </Card>
          </motion.div>
        </motion.div>

        <div className="grid gap-6 lg:grid-cols-7">
          {/* Recent Sessions */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="lg:col-span-4"
          >
            <Card glass>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Recent Sessions</CardTitle>
                    <CardDescription>Your latest learning activities</CardDescription>
                  </div>
                  <Link href="/sessions">
                    <Button variant="ghost" size="sm">
                      View all
                      <ChevronRight className="ml-1 h-4 w-4" />
                    </Button>
                  </Link>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {recentSessions.map((session, index) => (
                  <motion.div
                    key={session.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.5 + index * 0.1 }}
                    className="flex items-center justify-between p-4 rounded-xl bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                  >
                    <div className="flex items-center gap-4">
                      <div className={`p-3 rounded-xl ${
                        session.type === 'tutor' ? 'bg-purple-100 dark:bg-purple-900/20' :
                        session.type === 'language_practice' ? 'bg-blue-100 dark:bg-blue-900/20' :
                        'bg-green-100 dark:bg-green-900/20'
                      }`}>
                        {session.type === 'tutor' && <Brain className="h-5 w-5 text-purple-600 dark:text-purple-400" />}
                        {session.type === 'language_practice' && <Mic className="h-5 w-5 text-blue-600 dark:text-blue-400" />}
                        {session.type === 'exam_prep' && <BookOpen className="h-5 w-5 text-green-600 dark:text-green-400" />}
                      </div>
                      <div>
                        <p className="font-medium capitalize">
                          {session.type.replace('_', ' ')} - {session.subject}
                        </p>
                        <p className="text-sm text-muted-foreground">
                          {formatDate(session.startedAt)} • {formatDuration(session.durationSeconds)}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-semibold">
                        {Math.round((session.comprehensionScore || 0) * 100)}%
                      </p>
                      <div className="flex items-center gap-1 mt-1">
                        {[...Array(5)].map((_, i) => (
                          <div
                            key={i}
                            className={`h-1 w-6 rounded-full ${
                              i < Math.ceil((session.comprehensionScore || 0) * 5)
                                ? 'bg-yellow-500'
                                : 'bg-gray-300 dark:bg-gray-600'
                            }`}
                          />
                        ))}
                      </div>
                    </div>
                  </motion.div>
                ))}
              </CardContent>
            </Card>
          </motion.div>

          {/* Quick Actions & Insights */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="lg:col-span-3 space-y-6"
          >
            {/* Learning Insights */}
            <Card glass>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-yellow-500" />
                  Learning Insights
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
                  <p className="text-sm">
                    <span className="font-medium text-blue-900 dark:text-blue-100">Great progress!</span>
                    <span className="text-blue-700 dark:text-blue-300"> Your accuracy improved by 15% this week.</span>
                  </p>
                </div>
                <div className="p-3 rounded-lg bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800">
                  <p className="text-sm">
                    <span className="font-medium text-purple-900 dark:text-purple-100">Study tip:</span>
                    <span className="text-purple-700 dark:text-purple-300"> Try morning sessions for better retention.</span>
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card glass>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Link href="/voice-tutor" className="block">
                  <div className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors cursor-pointer group">
                    <div className="flex items-center gap-3">
                      <Brain className="h-5 w-5 text-purple-600" />
                      <span className="font-medium">AI Voice Tutor</span>
                    </div>
                    <ChevronRight className="h-4 w-4 text-gray-400 transition-transform group-hover:translate-x-1" />
                  </div>
                </Link>
                
                <Link href="/language-practice" className="block">
                  <div className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors cursor-pointer group">
                    <div className="flex items-center gap-3">
                      <Mic className="h-5 w-5 text-blue-600" />
                      <span className="font-medium">Language Practice</span>
                    </div>
                    <ChevronRight className="h-4 w-4 text-gray-400 transition-transform group-hover:translate-x-1" />
                  </div>
                </Link>
                
                <Link href="/exam-prep" className="block">
                  <div className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors cursor-pointer group">
                    <div className="flex items-center gap-3">
                      <Target className="h-5 w-5 text-green-600" />
                      <span className="font-medium">Exam Prep</span>
                    </div>
                    <ChevronRight className="h-4 w-4 text-gray-400 transition-transform group-hover:translate-x-1" />
                  </div>
                </Link>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  )
}