import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import Input from '../components/Input'
import Modal from '../components/Modal'
import Badge from '../components/Badge'
import Loader from '../components/Loader'
import { clubService } from '../services/api'

export default function ClubPage({ user }) {
  const [clubs, setClubs] = useState([])
  const [myClubs, setMyClubs] = useState([])
  const [selectedClub, setSelectedClub] = useState(null)
  const [members, setMembers] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreate, setShowCreate] = useState(false)
  const [createForm, setCreateForm] = useState({ name: '', description: '' })
  const [creating, setCreating] = useState(false)
  const [joining, setJoining] = useState(null)
  const [error, setError] = useState('')

  const load = async () => {
    setLoading(true)
    try {
      const [allRes, myRes] = await Promise.all([
        clubService.getAll(),
        user?.user_id ? clubService.getUserClubs(user.user_id) : Promise.resolve({ data: { clubs: [] } }),
      ])
      
      // Extract clubs array from response
      // Backend returns { count: n, clubs: [...] }
      const allClubs = allRes.data?.clubs || allRes.data?.results || allRes.data || []
      const myClubsList = myRes.data?.clubs || myRes.data?.results || myRes.data || []
      
      setClubs(Array.isArray(allClubs) ? allClubs : [])
      setMyClubs(Array.isArray(myClubsList) ? myClubsList : [])
    } catch (err) {
      console.error('Clubs load error:', err)
      setClubs([])
      setMyClubs([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [user])

  const openClub = async (club) => {
    setSelectedClub(club)
    try {
      const { data } = await clubService.getMembers(club.club_id)
      setMembers(data.members || [])
    } catch { setMembers([]) }
  }

  const handleCreate = async (e) => {
    e.preventDefault()
    if (!createForm.name) return
    setCreating(true)
    setError('')
    try {
      await clubService.create(createForm)
      setShowCreate(false)
      setCreateForm({ name: '', description: '' })
      await load()
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create club')
    } finally {
      setCreating(false)
    }
  }

  const handleJoin = async (clubId) => {
    setJoining(clubId)
    try {
      await clubService.join(clubId)
      await load()
    } catch (err) {
      console.error('Join club error:', err)
    } finally {
      setJoining(null)
    }
  }

  const handleLeave = async (clubId) => {
    try {
      await clubService.leave(clubId)
      await load()
      if (selectedClub?.club_id === clubId) setSelectedClub(null)
    } catch (err) {
      console.error('Leave club error:', err)
    }
  }

  const isMember = (club) => myClubs.some(c => c.club_id === club.club_id)

  if (loading) return <div className="flex justify-center py-20"><Loader message="Loading clubs..." /></div>

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">🧑‍🤝‍🧑 Clubs</h1>
          <p className="text-gray-400">Join or create a club to compete together</p>
        </div>
        <Button variant="primary" size="lg" onClick={() => setShowCreate(true)}>Create Club</Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* My Clubs */}
        {myClubs.length > 0 && (
          <div className="lg:col-span-3">
            <h2 className="text-2xl font-bold text-white mb-4">My Clubs</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
              {myClubs.map((club) => (
                <Card key={club.club_id} variant="glow" hover>
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="text-xl font-bold text-white">{club.name}</h3>
                      {club.is_verified && <Badge variant="success" size="sm">✓ Verified</Badge>}
                    </div>
                    <p className="text-gray-400 text-sm mb-4">{club.description}</p>
                    <div className="flex justify-between items-center">
                      <span className="text-neon-blue font-semibold">{club.member_count} members</span>
                      <div className="flex gap-2">
                        <Button variant="secondary" size="sm" onClick={() => openClub(club)}>View</Button>
                        {club.owner_id !== user?.user_id && (
                          <Button variant="ghost" size="sm" onClick={() => handleLeave(club.club_id)}>Leave</Button>
                        )}
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Club Detail */}
        {selectedClub && (
          <div className="lg:col-span-2">
            <Card variant="glow">
              <div className="p-6">
                <h2 className="text-2xl font-bold text-white mb-2">{selectedClub.name}</h2>
                <p className="text-gray-400 mb-4">{selectedClub.description}</p>
                <div className="grid grid-cols-3 gap-4 mb-6 text-sm">
                  <div><p className="text-gray-400">Members</p><p className="font-bold text-neon-blue">{selectedClub.member_count}</p></div>
                  <div><p className="text-gray-400">Wins</p><p className="font-bold text-green-400">{selectedClub.stats?.wins ?? 0}</p></div>
                  <div><p className="text-gray-400">Owner</p><p className="font-bold text-white">{selectedClub.owner_username}</p></div>
                </div>
                <h3 className="text-lg font-bold text-white mb-3">Members</h3>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {members.map((m, idx) => (
                    <div key={m.user_id || idx} className="flex items-center justify-between p-3 bg-dark-800 rounded-lg">
                      <div>
                        <p className="font-semibold text-white">{m.username}</p>
                        <p className="text-xs text-gray-400 capitalize">{m.role}</p>
                      </div>
                      <Badge variant="primary" size="sm">{m.contribution_score ?? 0} pts</Badge>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          </div>
        )}

        {/* Explore Clubs */}
        <div className={selectedClub ? '' : 'lg:col-span-3'}>
          <h2 className="text-2xl font-bold text-white mb-4">🌍 Explore Clubs</h2>
          <div className={`grid gap-4 ${selectedClub ? 'grid-cols-1' : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4'}`}>
            {clubs.map((club, idx) => (
              <motion.div key={club.club_id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: idx * 0.08 }}>
                <Card variant="glow" hover>
                  <div className="p-5">
                    <h3 className="text-lg font-bold text-white mb-1">{club.name}</h3>
                    <p className="text-sm text-gray-400 mb-3">Owner: {club.owner_username}</p>
                    <div className="flex justify-between text-sm mb-4">
                      <span className="text-gray-400">Members</span>
                      <span className="font-bold text-neon-blue">{club.member_count}</span>
                    </div>
                    {isMember(club)
                      ? <Badge variant="success" className="w-full text-center">Joined</Badge>
                      : (
                        <Button variant="secondary" size="md" className="w-full"
                          isLoading={joining === club.club_id}
                          onClick={() => handleJoin(club.club_id)}>
                          Join
                        </Button>
                      )
                    }
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Create Club Modal */}
      <Modal isOpen={showCreate} onClose={() => setShowCreate(false)} title="Create New Club" size="md">
        <form onSubmit={handleCreate} className="space-y-4">
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <Input label="Club Name" placeholder="Enter club name (3-255 chars)"
            value={createForm.name} onChange={(e) => setCreateForm({ ...createForm, name: e.target.value })} required />
          <Input label="Description" placeholder="Short description (optional)"
            value={createForm.description} onChange={(e) => setCreateForm({ ...createForm, description: e.target.value })} />
          <div className="flex gap-3 pt-2">
            <Button variant="primary" className="flex-1" type="submit" isLoading={creating}>Create</Button>
            <Button variant="secondary" className="flex-1" onClick={() => setShowCreate(false)}>Cancel</Button>
          </div>
        </form>
      </Modal>
    </motion.div>
  )
}
