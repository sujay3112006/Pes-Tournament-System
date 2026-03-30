import { useState } from 'react'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import Input from '../components/Input'
import Modal from '../components/Modal'
import Badge from '../components/Badge'

export default function ClubPage() {
  const [showCreateClub, setShowCreateClub] = useState(false)
  const [showJoinClub, setShowJoinClub] = useState(false)
  const [myClub] = useState({
    id: 1,
    name: 'Elite Warriors',
    leader: 'ProGamer',
    members: 45,
    maxMembers: 100,
    level: 12,
    founded: '2024-01-15',
    description: 'Top competitive club',
  })

  const [clubs] = useState([
    { id: 1, name: 'Elite Warriors', leader: 'ProGamer', members: 45, level: 12, badge: '⭐' },
    { id: 2, name: 'Dynasty Esports', leader: 'NovaStorm', members: 78, level: 15, badge: '👑' },
    { id: 3, name: 'Phoenix Rising', leader: 'SkyKing', members: 32, level: 9, badge: '🔥' },
    { id: 4, name: 'Vortex Gaming', leader: 'LunaAce', members: 56, level: 11, badge: '🌀' },
  ])

  const [clubMembers] = useState([
    { id: 1, name: 'ProGamer', rank: 1, role: 'Leader', joinDate: '2024-01-15' },
    { id: 2, name: 'NovaStorm', rank: 2, role: 'Officer', joinDate: '2024-02-01' },
    { id: 3, name: 'SkyKing', rank: 3, role: 'Member', joinDate: '2024-02-15' },
    { id: 4, name: 'LunaAce', rank: 4, role: 'Member', joinDate: '2024-03-01' },
  ])

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      {/* Header */}
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">🧑‍🤝‍🧑 Clubs</h1>
          <p className="text-gray-400">Join or create a club to compete together</p>
        </div>
        <div className="flex gap-3">
          <Button
            variant="primary"
            size="lg"
            onClick={() => setShowCreateClub(true)}
          >
            Create Club
          </Button>
          <Button
            variant="secondary"
            size="lg"
            onClick={() => setShowJoinClub(true)}
          >
            Join Club
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* My Club */}
        <div className="lg:col-span-3">
          <Card variant="glow">
            <div className="p-8 bg-gradient-to-r from-neon-blue/10 to-neon-purple/10">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-3xl font-bold text-white mb-2">⭐ {myClub.name}</h2>
                  <p className="text-gray-400">Led by {myClub.leader}</p>
                </div>
                <Badge variant="primary" size="md">Level {myClub.level}</Badge>
              </div>

              <p className="text-gray-300 mb-6">{myClub.description}</p>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <p className="text-gray-400 text-sm mb-1">Members</p>
                  <p className="text-2xl font-bold text-neon-blue">{myClub.members}/{myClub.maxMembers}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm mb-1">Founded</p>
                  <p className="text-2xl font-bold text-neon-purple">{myClub.founded}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm mb-1">Club Rank</p>
                  <p className="text-2xl font-bold text-neon-pink">#247</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm mb-1">Total Points</p>
                  <p className="text-2xl font-bold text-green-400">45,280</p>
                </div>
              </div>

              <div className="mt-6 flex gap-3">
                <Button variant="secondary" size="md">Edit Club</Button>
                <Button variant="secondary" size="md">Invite Members</Button>
                <Button variant="ghost" size="md">Club Chat</Button>
              </div>
            </div>
          </Card>
        </div>

        {/* Club Members */}
        <div className="lg:col-span-2">
          <Card variant="elevated">
            <div className="p-6">
              <h3 className="text-2xl font-bold text-white mb-6">👥 Members</h3>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {clubMembers.map((member, idx) => (
                  <motion.div
                    key={member.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    className="flex items-center justify-between p-4 bg-dark-800/50 rounded-lg hover:bg-dark-700 transition-smooth"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-r from-neon-blue to-neon-purple flex items-center justify-center font-bold">
                        {member.rank}
                      </div>
                      <div>
                        <p className="font-semibold text-white">{member.name}</p>
                        <p className="text-xs text-gray-400">{member.role}</p>
                      </div>
                    </div>
                    <Badge variant="primary" size="sm">{member.joinDate}</Badge>
                  </motion.div>
                ))}
              </div>
            </div>
          </Card>
        </div>

        {/* Club Stats */}
        <div>
          <Card variant="glow">
            <div className="p-6 space-y-4">
              <h3 className="text-xl font-bold text-white">📊 Stats</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between p-3 bg-dark-800 rounded-lg">
                  <span className="text-gray-400">Avg Rating</span>
                  <span className="font-bold text-neon-blue">88.5</span>
                </div>
                <div className="flex justify-between p-3 bg-dark-800 rounded-lg">
                  <span className="text-gray-400">Total Wins</span>
                  <span className="font-bold text-neon-purple">324</span>
                </div>
                <div className="flex justify-between p-3 bg-dark-800 rounded-lg">
                  <span className="text-gray-400">Win Rate</span>
                  <span className="font-bold text-green-400">68%</span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Other Clubs */}
      <h2 className="text-2xl font-bold text-white my-8">🌍 Explore Clubs</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {clubs.map((club, idx) => (
          <motion.div
            key={club.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <Card variant="glow" hover>
              <div className="p-6">
                <div className="text-3xl mb-3">{club.badge}</div>
                <h3 className="text-lg font-bold text-white mb-2">{club.name}</h3>
                <p className="text-sm text-gray-400 mb-4">Leader: {club.leader}</p>
                <div className="space-y-2 mb-4 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Level</span>
                    <span className="font-bold text-neon-blue">{club.level}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Members</span>
                    <span className="font-bold">{club.members}</span>
                  </div>
                </div>
                <Button variant="secondary" size="md" className="w-full">
                  Join
                </Button>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Create Club Modal */}
      <Modal
        isOpen={showCreateClub}
        onClose={() => setShowCreateClub(false)}
        title="Create New Club"
        size="lg"
      >
        <form className="space-y-4">
          <Input label="Club Name" placeholder="Enter club name" required />
          <Input label="Club Tagline" placeholder="Short description" required />
          <div>
            <label className="block text-sm font-semibold text-gray-300 mb-2">Club Icon</label>
            <select className="w-full px-4 py-2.5 bg-dark-800 border border-dark-700 focus:border-neon-blue rounded-lg text-white">
              <option>⭐ Star</option>
              <option>👑 Crown</option>
              <option>🔥 Fire</option>
              <option>🌀 Vortex</option>
            </select>
          </div>
          <div className="flex gap-3 pt-4">
            <Button variant="primary" className="flex-1">Create</Button>
            <Button variant="secondary" className="flex-1" onClick={() => setShowCreateClub(false)}>Cancel</Button>
          </div>
        </form>
      </Modal>

      {/* Join Club Modal */}
      <Modal
        isOpen={showJoinClub}
        onClose={() => setShowJoinClub(false)}
        title="Join a Club"
        size="md"
      >
        <Input label="Club Code" placeholder="Enter club code" required />
        <div className="flex gap-3 mt-6">
          <Button variant="primary" className="flex-1">Join</Button>
          <Button variant="secondary" className="flex-1" onClick={() => setShowJoinClub(false)}>Cancel</Button>
        </div>
      </Modal>
    </motion.div>
  )
}
