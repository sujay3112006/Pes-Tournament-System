import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import Input from '../components/Input'
import Badge from '../components/Badge'

export default function MatchViewPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [score, setScore] = useState({ player1: 0, player2: 0 })
  const [proof, setProof] = useState(null)
  const [submitted, setSubmitted] = useState(false)

  const [match] = useState({
    id,
    player1: { name: 'ProGamer', rating: 92 },
    player2: { name: 'NovaStorm', rating: 89 },
    status: 'active',
    prize: '$500',
    startTime: '2026-03-30T14:00:00',
  })

  const handleSubmitScore = () => {
    if (!proof) {
      alert('Please upload match proof')
      return
    }
    setSubmitted(true)
    // API call would go here
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      {/* Header */}
      <div className="mb-8">
        <Button variant="ghost" size="sm" onClick={() => navigate(-1)} className="mb-4">
          ← Back
        </Button>
        <h1 className="text-4xl font-bold text-white mb-2">⚔️ Match Details</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Match Area */}
        <div className="lg:col-span-2 space-y-6">
          {/* Match Header */}
          <Card variant="glow">
            <div className="p-8">
              <div className="grid grid-cols-3 gap-4 mb-8">
                {/* Player 1 */}
                <div className="text-center">
                  <div className="w-20 h-20 rounded-full bg-gradient-to-r from-neon-blue to-neon-purple mx-auto mb-3 flex items-center justify-center">
                    <span className="text-2xl font-bold">P1</span>
                  </div>
                  <h3 className="text-lg font-bold text-white">{match.player1.name}</h3>
                  <p className="text-gray-400 text-sm">Rating: {match.player1.rating}</p>
                </div>

                {/* VS */}
                <div className="flex items-center justify-center">
                  <span className="text-2xl font-bold text-neon-blue">VS</span>
                </div>

                {/* Player 2 */}
                <div className="text-center">
                  <div className="w-20 h-20 rounded-full bg-gradient-to-r from-neon-purple to-neon-pink mx-auto mb-3 flex items-center justify-center">
                    <span className="text-2xl font-bold">P2</span>
                  </div>
                  <h3 className="text-lg font-bold text-white">{match.player2.name}</h3>
                  <p className="text-gray-400 text-sm">Rating: {match.player2.rating}</p>
                </div>
              </div>

              {/* Match Info */}
              <div className="flex justify-between items-center pt-6 border-t border-dark-600">
                <div>
                  <p className="text-gray-400 text-sm">Prize Pool</p>
                  <p className="text-xl font-bold text-neon-pink">💰 {match.prize}</p>
                </div>
                <Badge variant={match.status === 'active' ? 'success' : 'warning'}>
                  {match.status}
                </Badge>
              </div>
            </div>
          </Card>

          {/* Score Submission */}
          {!submitted && (
            <Card variant="glow">
              <div className="p-6">
                <h2 className="text-2xl font-bold text-white mb-6">Submit Final Score</h2>
                <div className="grid grid-cols-3 gap-4 mb-6">
                  <div>
                    <label className="block text-sm font-semibold text-gray-300 mb-2">
                      {match.player1.name}'s Goals
                    </label>
                    <input
                      type="number"
                      min="0"
                      max="10"
                      value={score.player1}
                      onChange={(e) => setScore({ ...score, player1: parseInt(e.target.value) })}
                      className="w-full text-center text-4xl font-bold bg-dark-800 border-2 border-neon-blue rounded-lg py-4 text-neon-blue focus:outline-none focus:border-neon-purple"
                    />
                  </div>
                  <div className="flex items-end justify-center pb-2">
                    <span className="text-3xl font-bold text-gray-400">-</span>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-300 mb-2">
                      {match.player2.name}'s Goals
                    </label>
                    <input
                      type="number"
                      min="0"
                      max="10"
                      value={score.player2}
                      onChange={(e) => setScore({ ...score, player2: parseInt(e.target.value) })}
                      className="w-full text-center text-4xl font-bold bg-dark-800 border-2 border-neon-purple rounded-lg py-4 text-neon-purple focus:outline-none focus:border-neon-blue"
                    />
                  </div>
                </div>

                {/* File Upload */}
                <div className="mb-6">
                  <label className="block text-sm font-semibold text-gray-300 mb-2">
                    Upload Match Proof 📸
                  </label>
                  <input
                    type="file"
                    accept="image/*,video/*"
                    onChange={(e) => setProof(e.target.files?.[0])}
                    className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg text-gray-300 file:bg-neon-blue file:text-white file:border-0 file:rounded file:px-4 file:py-2 file:cursor-pointer file:font-semibold hover:file:bg-neon-purple transition-smooth"
                  />
                  {proof && <p className="text-sm text-green-400 mt-2">✓ {proof.name}</p>}
                </div>

                <Button
                  variant="primary"
                  size="lg"
                  className="w-full"
                  onClick={handleSubmitScore}
                >
                  Submit Score for Review
                </Button>
              </div>
            </Card>
          )}

          {/* Submission Confirmation */}
          {submitted && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <Card variant="glow">
                <div className="p-8 text-center">
                  <div className="text-6xl mb-4">✓</div>
                  <h3 className="text-2xl font-bold text-green-400 mb-2">Score Submitted!</h3>
                  <p className="text-gray-400 mb-6">
                    Your match result ({score.player1} - {score.player2}) has been submitted for verification.
                  </p>
                  <Button
                    variant="primary"
                    onClick={() => navigate('/')}
                  >
                    Return to Dashboard
                  </Button>
                </div>
              </Card>
            </motion.div>
          )}
        </div>

        {/* Sidebar - Match History */}
        <div>
          <Card variant="glow">
            <div className="p-6">
              <h3 className="text-xl font-bold text-white mb-4">Head to Head</h3>
              <div className="space-y-4">
                <div className="p-4 bg-dark-800 rounded-lg">
                  <p className="text-gray-400 text-sm">Players' Previous Matches</p>
                  <p className="text-neon-blue font-semibold mt-2">2 Previous Matches</p>
                </div>
                <div className="p-4 bg-dark-800 rounded-lg">
                  <p className="text-gray-400 text-sm">Head-to-Head Record</p>
                  <p className="text-neon-pink font-semibold mt-2">1 Win - 1 Draw</p>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </motion.div>
  )
}
