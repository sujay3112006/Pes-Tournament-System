import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import Badge from '../components/Badge'
import ProgressBar from '../components/ProgressBar'
import Tabs from '../components/Tabs'
import Loader from '../components/Loader'
import { missionService } from '../services/api'

export default function MissionsPage() {
  const [activeTab, setActiveTab] = useState('daily')
  const [myMissions, setMyMissions] = useState({ active: [], completed: [] })
  const [available, setAvailable] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [claiming, setClaiming] = useState(null)

  const tabs = [
    { id: 'daily', label: '📅 Daily' },
    { id: 'weekly', label: '📆 Weekly' },
    { id: 'my', label: '🎯 My Missions' },
  ]

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      try {
        const [availRes, myRes, statsRes] = await Promise.all([
          missionService.getAvailable({ mission_type: activeTab === 'my' ? undefined : activeTab }),
          missionService.getMyMissions(),
          missionService.getStats(),
        ])
        const missions = availRes.data.missions || availRes.data.results || (Array.isArray(availRes.data) ? availRes.data : [])
        setAvailable(missions)
        setMyMissions(myRes.data || { active: [], completed: [] })
        setStats(statsRes.data)
      } catch (err) {
        console.error('Missions load error:', err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [activeTab])

  const handleStart = async (missionId) => {
    try {
      await missionService.start(missionId)
      const { data } = await missionService.getMyMissions()
      setMyMissions(data || { active: [], completed: [] })
    } catch (err) {
      console.error('Start mission error:', err)
    }
  }

  const handleClaim = async (userMissionId) => {
    setClaiming(userMissionId)
    try {
      await missionService.claimReward(userMissionId)
      const [myRes, statsRes] = await Promise.all([missionService.getMyMissions(), missionService.getStats()])
      setMyMissions(myRes.data || { active: [], completed: [] })
      setStats(statsRes.data)
    } catch (err) {
      console.error('Claim error:', err)
    } finally {
      setClaiming(null)
    }
  }

  const displayMissions = activeTab === 'my'
    ? [...(myMissions.active || []), ...(myMissions.completed || [])]
    : available

  if (loading) return <div className="flex justify-center py-20"><Loader message="Loading missions..." /></div>

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">🎯 Missions & Rewards</h1>
        <p className="text-gray-400">Complete missions to earn coins and climb the ranks</p>
      </div>

      <Tabs tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {displayMissions.length === 0 && (
          <p className="text-gray-400 col-span-2 text-center py-12">No missions found.</p>
        )}
        {displayMissions.map((mission, idx) => {
          const isUserMission = activeTab === 'my'
          const missionId = isUserMission ? mission.mission_id : mission.mission_id
          const userMissionId = mission.user_mission_id
          const progress = mission.progress ?? 0
          const conditionValue = mission.condition_value ?? mission.condition?.value ?? 1
          const completed = mission.completed ?? false
          const rewardClaimed = mission.reward_claimed ?? false
          const reward = mission.reward ?? mission.mission?.reward ?? {}

          return (
            <motion.div key={missionId || idx} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: idx * 0.08 }}>
              <Card variant={completed ? 'dark' : 'glow'} hover>
                <div className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-white mb-1">{mission.title || mission.mission_title}</h3>
                      <p className="text-sm text-gray-400">{mission.description}</p>
                      {mission.difficulty && (
                        <Badge variant="primary" size="sm" className="mt-2 capitalize">{mission.difficulty}</Badge>
                      )}
                    </div>
                    {completed && <Badge variant="success" size="sm">✓ Done</Badge>}
                  </div>

                  <div className="mb-4 p-3 bg-neon-blue/10 rounded-lg border border-neon-blue/20">
                    <p className="text-sm text-gray-400 mb-1">Reward</p>
                    <p className="text-lg font-bold text-neon-blue">
                      💰 {reward.coins ?? 0} coins {reward.points ? `• ${reward.points} pts` : ''}
                    </p>
                  </div>

                  {isUserMission && !completed && (
                    <ProgressBar value={progress} max={conditionValue} label={`${progress}/${conditionValue}`}
                      variant={progress >= conditionValue ? 'success' : 'default'} />
                  )}

                  {/* Actions */}
                  {!isUserMission && (
                    <Button variant="primary" size="md" className="w-full mt-4" onClick={() => handleStart(missionId)}>
                      Start Mission
                    </Button>
                  )}
                  {isUserMission && completed && !rewardClaimed && (
                    <Button variant="success" size="md" className="w-full mt-4"
                      isLoading={claiming === userMissionId}
                      onClick={() => handleClaim(userMissionId)}>
                      Claim Reward
                    </Button>
                  )}
                  {isUserMission && completed && rewardClaimed && (
                    <p className="text-sm text-gray-400 mt-4 text-center">✓ Reward claimed</p>
                  )}
                </div>
              </Card>
            </motion.div>
          )
        })}
      </div>

      {/* Stats */}
      {stats && (
        <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            { label: '💰 Coins Earned', value: stats.total_coins_earned?.toLocaleString() ?? 0 },
            { label: '✨ Completed', value: stats.missions_completed ?? 0 },
            { label: '🎯 Started', value: stats.missions_started ?? 0 },
            { label: '⭐ Points Earned', value: stats.total_points_earned?.toLocaleString() ?? 0 },
          ].map((s, idx) => (
            <motion.div key={idx} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: idx * 0.1 }}>
              <Card variant="glow">
                <div className="p-6 text-center">
                  <p className="text-gray-400 text-sm mb-2">{s.label}</p>
                  <p className="text-2xl font-bold text-neon-blue">{s.value}</p>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      )}
    </motion.div>
  )
}
