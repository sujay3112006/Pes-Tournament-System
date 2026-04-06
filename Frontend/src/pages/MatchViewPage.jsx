import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import Badge from '../components/Badge'
import Loader from '../components/Loader'
import { matchService, mlService } from '../services/api'

export default function MatchViewPage({ user }) {
  const { id } = useParams()
  const navigate = useNavigate()
  const [match, setMatch] = useState(null)
  const [score, setScore] = useState({ player1: 0, player2: 0 })
  const [proof, setProof] = useState(null)
  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [prediction, setPrediction] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await matchService.getById(id)
        setMatch(data)
        if (data.player1_id && data.player2_id) {
          try {
            const { data: pred } = await mlService.predict(data.player1_id, data.player2_id)
            setPrediction(pred)
          } catch { /* prediction optional */ }
        }
      } catch (err) {
        console.error('Failed to load match:', err)
        console.error('Match error status:', err.response?.status)
        if (err.response?.status === 404) {
          setError(`Match with ID ${id} not found`)
        } else {
          setError('Failed to load match details')
        }
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [id])

  const handleSubmitScore = async () => {
    if (!proof) { setError('Please upload match proof'); return }
    setError('')
    setSubmitting(true)
    try {
      await matchService.submitResult(id, score.player1, score.player2, proof)
      setSubmitted(true)
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to submit result')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <div className="flex justify-center py-20"><Loader message="Loading match..." /></div>
  if (!match) return (
    <div className="text-center py-20">
      <p className="text-red-400 font-semibold mb-2">❌ {error || 'Match not found.'}</p>
      <p className="text-gray-400 text-sm">The match you're looking for doesn't exist or you don't have access to it.</p>
    </div>
  )

  const isPlayer = user?.user_id === match.player1_id || user?.user_id === match.player2_id
  const canSubmit = isPlayer && match.status !== 'completed' && !submitted

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div className="mb-8">
        <Button variant="ghost" size="sm" onClick={() => navigate(-1)} className="mb-4">← Back</Button>
        <h1 className="text-4xl font-bold text-white mb-2">⚔️ Match Details</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          {/* Players */}
          <Card variant="glow">
            <div className="p-8">
              <div className="grid grid-cols-3 gap-4 mb-8">
                <div className="text-center">
                  <div className="w-20 h-20 rounded-full bg-gradient-to-r from-neon-blue to-neon-purple mx-auto mb-3 flex items-center justify-center">
                    <span className="text-2xl font-bold">P1</span>
                  </div>
                  <h3 className="text-lg font-bold text-white">{match.player1_username}</h3>
                  {prediction && (
                    <p className="text-neon-blue text-sm font-bold mt-1">
                      {Math.round(prediction.player1_win_probability * 100)}% win
                    </p>
                  )}
                </div>
                <div className="flex items-center justify-center">
                  <span className="text-2xl font-bold text-neon-blue">VS</span>
                </div>
                <div className="text-center">
                  <div className="w-20 h-20 rounded-full bg-gradient-to-r from-neon-purple to-neon-pink mx-auto mb-3 flex items-center justify-center">
                    <span className="text-2xl font-bold">P2</span>
                  </div>
                  <h3 className="text-lg font-bold text-white">{match.player2_username}</h3>
                  {prediction && (
                    <p className="text-neon-pink text-sm font-bold mt-1">
                      {Math.round(prediction.player2_win_probability * 100)}% win
                    </p>
                  )}
                </div>
              </div>

              {match.status === 'completed' && match.score && (
                <div className="text-center py-4 border-t border-dark-600">
                  <p className="text-gray-400 text-sm mb-1">Final Score</p>
                  <p className="text-4xl font-black text-white">
                    {match.score.player1} — {match.score.player2}
                  </p>
                </div>
              )}

              <div className="flex justify-between items-center pt-6 border-t border-dark-600 mt-4">
                <Badge variant={match.status === 'live' ? 'success' : match.status === 'completed' ? 'primary' : 'warning'}>
                  {match.status}
                </Badge>
                {match.status === 'live' && (
                  <Button variant="secondary" size="sm" onClick={() => navigate(`/match/${id}/live`)}>
                    Watch Live
                  </Button>
                )}
              </div>
            </div>
          </Card>

          {/* Score Submission */}
          {canSubmit && (
            <Card variant="glow">
              <div className="p-6">
                <h2 className="text-2xl font-bold text-white mb-6">Submit Final Score</h2>
                {error && <p className="text-red-400 text-sm mb-4">{error}</p>}
                <div className="grid grid-cols-3 gap-4 mb-6">
                  <div>
                    <label className="block text-sm font-semibold text-gray-300 mb-2">{match.player1_username}'s Goals</label>
                    <input type="number" min="0" max="20" value={score.player1}
                      onChange={(e) => setScore({ ...score, player1: parseInt(e.target.value) || 0 })}
                      className="w-full text-center text-4xl font-bold bg-dark-800 border-2 border-neon-blue rounded-lg py-4 text-neon-blue focus:outline-none" />
                  </div>
                  <div className="flex items-end justify-center pb-2">
                    <span className="text-3xl font-bold text-gray-400">-</span>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-300 mb-2">{match.player2_username}'s Goals</label>
                    <input type="number" min="0" max="20" value={score.player2}
                      onChange={(e) => setScore({ ...score, player2: parseInt(e.target.value) || 0 })}
                      className="w-full text-center text-4xl font-bold bg-dark-800 border-2 border-neon-purple rounded-lg py-4 text-neon-purple focus:outline-none" />
                  </div>
                </div>

                <div className="mb-6">
                  <label className="block text-sm font-semibold text-gray-300 mb-2">Upload Match Proof 📸</label>
                  <input type="file" accept="image/*,video/*,.pdf"
                    onChange={(e) => setProof(e.target.files?.[0])}
                    className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg text-gray-300 file:bg-neon-blue file:text-white file:border-0 file:rounded file:px-4 file:py-2 file:cursor-pointer file:font-semibold" />
                  {proof && <p className="text-sm text-green-400 mt-2">✓ {proof.name}</p>}
                </div>

                <Button variant="primary" size="lg" className="w-full" onClick={handleSubmitScore} isLoading={submitting}>
                  Submit Score for Review
                </Button>
              </div>
            </Card>
          )}

          {submitted && (
            <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}>
              <Card variant="glow">
                <div className="p-8 text-center">
                  <div className="text-6xl mb-4">✓</div>
                  <h3 className="text-2xl font-bold text-green-400 mb-2">Score Submitted!</h3>
                  <p className="text-gray-400 mb-6">
                    Your result ({score.player1} - {score.player2}) has been submitted for verification.
                  </p>
                  <Button variant="primary" onClick={() => navigate('/')}>Return to Dashboard</Button>
                </div>
              </Card>
            </motion.div>
          )}
        </div>

        {/* Sidebar */}
        <div>
          <Card variant="glow">
            <div className="p-6 space-y-4">
              <h3 className="text-xl font-bold text-white">Match Info</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Status</span>
                  <span className="font-semibold text-white capitalize">{match.status}</span>
                </div>
                {match.match_date && (
                  <div className="flex justify-between">
                    <span className="text-gray-400">Date</span>
                    <span className="font-semibold text-white">{new Date(match.match_date).toLocaleDateString()}</span>
                  </div>
                )}
                {prediction && (
                  <div className="pt-3 border-t border-dark-700">
                    <p className="text-gray-400 text-xs mb-2">AI Prediction (confidence: {Math.round(prediction.confidence * 100)}%)</p>
                    <div className="flex justify-between">
                      <span className="text-neon-blue font-bold">{match.player1_username}: {Math.round(prediction.player1_win_probability * 100)}%</span>
                      <span className="text-neon-pink font-bold">{match.player2_username}: {Math.round(prediction.player2_win_probability * 100)}%</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </Card>
        </div>
      </div>
    </motion.div>
  )
}
