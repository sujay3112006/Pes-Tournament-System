import { useState } from 'react'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import Badge from '../components/Badge'
import ProgressBar from '../components/ProgressBar'
import Tabs from '../components/Tabs'

export default function MissionsPage() {
  const [activeTab, setActiveTab] = useState('daily')

  const tabs = [
    { id: 'daily', label: '📅 Daily Missions' },
    { id: 'weekly', label: '📆 Weekly Missions' },
    { id: 'rewards', label: '🎁 Completed' },
  ]

  const missions = {
    daily: [
      { id: 1, name: 'Win 2 Matches', description: 'Play and win 2 matches', reward: 100, progress: 1, max: 2, completed: false },
      { id: 2, name: 'Score 5 Goals', description: 'Score 5 goals across matches', reward: 150, progress: 3, max: 5, completed: false },
      { id: 3, name: 'Join a Tournament', description: 'Join any tournament', reward: 200, progress: 1, max: 1, completed: true },
      { id: 4, name: 'Bid in Auction', description: 'Place a bid in live auction', reward: 75, progress: 0, max: 1, completed: false },
    ],
    weekly: [
      { id: 5, name: 'Win 10 Matches', description: 'Win 10 matches this week', reward: 500, progress: 7, max: 10, completed: false },
      { id: 6, name: 'Reach Top 50', description: 'Climb to top 50 leaderboard', reward: 1000, progress: 1, max: 1, completed: false },
      { id: 7, name: 'Complete 5 Tournaments', description: 'Play and finish 5 tournaments', reward: 750, progress: 2, max: 5, completed: false },
      { id: 8, name: 'Win Championship', description: 'Win a tournament championship', reward: 2000, progress: 0, max: 1, completed: false },
    ],
    rewards: [
      { id: 9, name: 'Daily Login', description: 'Login every day', reward: 50, progress: 1, max: 1, completed: true, claimedDate: '1 day ago' },
      { id: 10, name: 'First Win', description: 'Win your first match', reward: 100, progress: 1, max: 1, completed: true, claimedDate: '3 days ago' },
    ],
  }

  const handleClaim = (missionId) => {
    console.log('Claiming reward for mission:', missionId)
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">🎯 Missions & Rewards</h1>
        <p className="text-gray-400">Complete missions to earn coins and climb the ranks</p>
      </div>

      {/* Tabs */}
      <Tabs tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Missions Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {missions[activeTab].map((mission, idx) => (
          <motion.div
            key={mission.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <Card variant={mission.completed ? 'dark' : 'glow'} hover>
              <div className="p-6">
                {/* Header */}
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-white mb-1">{mission.name}</h3>
                    <p className="text-sm text-gray-400">{mission.description}</p>
                  </div>
                  {mission.completed && (
                    <Badge variant="success" size="sm">✓ Done</Badge>
                  )}
                </div>

                {/* Reward */}
                <div className="mb-4 p-3 bg-neon-blue/10 rounded-lg border border-neon-blue/20">
                  <p className="text-sm text-gray-400 mb-1">Reward</p>
                  <p className="text-lg font-bold text-neon-blue">💰 {mission.reward}</p>
                </div>

                {/* Progress */}
                {!mission.completed && (
                  <>
                    <ProgressBar
                      value={mission.progress}
                      max={mission.max}
                      label={`Progress: ${mission.progress}/${mission.max}`}
                      variant={mission.progress === mission.max ? 'success' : 'default'}
                    />
                    <Button
                      variant="primary"
                      size="md"
                      className="w-full mt-4"
                      disabled={mission.progress < mission.max}
                    >
                      {mission.progress === mission.max ? 'Claim Reward' : 'In Progress'}
                    </Button>
                  </>
                )}

                {/* Claimed */}
                {mission.completed && mission.claimedDate && (
                  <div className="text-sm text-gray-400 mt-4">
                    Claimed {mission.claimedDate}
                  </div>
                )}

                {mission.completed && !mission.claimedDate && (
                  <Button
                    variant="success"
                    size="md"
                    className="w-full mt-4"
                    onClick={() => handleClaim(mission.id)}
                  >
                    Claim Reward
                  </Button>
                )}
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Total Rewards Info */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { label: '💰 Total Coins Earned', value: '2,500', icon: '💵' },
          { label: '✨ Missions Completed', value: '12', icon: '🏆' },
          { label: '🔥 Current Streak', value: '7 Days', icon: '🔥' },
        ].map((stat, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <Card variant="glow">
              <div className="p-6 text-center">
                <p className="text-3xl mb-2">{stat.icon}</p>
                <p className="text-gray-400 text-sm mb-2">{stat.label}</p>
                <p className="text-2xl font-bold text-neon-blue">{stat.value}</p>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>
    </motion.div>
  )
}
