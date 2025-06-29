import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'
import { Toaster } from 'react-hot-toast'
import { Header } from '@/components/layout/Header'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'LearnFlow AI - Voice-Powered Learning',
  description: 'AI-powered personalized learning through natural conversation',
  keywords: 'education, AI, voice learning, tutoring, language learning',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          <div className="min-h-screen bg-background">
            <Header />
            <main className="flex-1">
              {children}
                        daily_stats[day]["total_time"] += session.duration_seconds
            if session.comprehension_score:
                daily_stats[day]["scores"].append(session.comprehension_score)
        
        # Calculate averages
        result = []
        for day_data in daily_stats.values():
            if day_data["scores"]:
                day_data["avg_score"] = sum(day_data["scores"]) / len(day_data["scores"])
            del day_data["scores"]  # Remove raw scores
            result.append(day_data)
        
        return sorted(result, key=lambda x: x["date"])
    
    def _calculate_weekly_progress(self, sessions: List) -> Dict:
        """Calculate weekly progress summary"""
        if not sessions:
            return {
                "total_time": 0,
                "sessions_completed": 0,
                "average_score": 0,
                "improvement": 0
            }
        
        total_time = sum(s.duration_seconds for s in sessions)
        avg_score = sum(s.comprehension_score or 0 for s in sessions) / len(sessions)
        
        # Calculate improvement (compare first half to second half)
        mid_point = len(sessions) // 2
        if mid_point > 0:
            first_half_avg = sum(s.comprehension_score or 0 for s in sessions[:mid_point]) / mid_point
            second_half_avg = sum(s.comprehension_score or 0 for s in sessions[mid_point:]) / (len(sessions) - mid_point)
            improvement = ((second_half_avg - first_half_avg) / first_half_avg * 100) if first_half_avg > 0 else 0
        else:
            improvement = 0
        
        return {
            "total_time": total_time,
            "sessions_completed": len(sessions),
            "average_score": round(avg_score, 2),
            "improvement": round(improvement, 1)
        }
    
    def _get_recommendations(self, sessions: List, progress: Progress) -> List[str]:
        """Get focus area recommendations"""
        recommendations = []
        
        if not sessions:
            return ["Start with a beginner-friendly subject to build momentum"]
        
        # Check streak
        if progress and progress.current_streak < 3:
            recommendations.append("Build consistency - aim for a 7-day study streak")
        
        # Check session duration
        avg_duration = sum(s.duration_seconds for s in sessions) / len(sessions)
        if avg_duration < 900:  # Less than 15 minutes
            recommendations.append("Increase session duration to 15-20 minutes for better learning")
        
        # Check difficulty progression
        difficulties = [s.difficulty for s in sessions if s.difficulty]
        if difficulties and all(d == difficulties[0] for d in difficulties):
            recommendations.append("Challenge yourself with varied difficulty levels")
        
        return recommendations[:3]  # Return top 3 recommendations