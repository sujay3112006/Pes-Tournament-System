import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Input from '../components/Input'
import Card from '../components/Card'

export default function CreateTournamentPage() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    name: '',
    format: 'knockout',
    maxPlayers: 32,
    entryFee: 0,
    prizePool: 1000,
  })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: name === 'format' ? value : (name === 'name' ? value : parseInt(value)),
    })
    if (errors[name]) setErrors({ ...errors, [name]: '' })
  }

  const validateForm = () => {
    const newErrors = {}
    if (!formData.name) newErrors.name = 'Tournament name is required'
    if (formData.maxPlayers < 2) newErrors.maxPlayers = 'Minimum 2 players required'
    if (formData.prizePool < 0) newErrors.prizePool = 'Prize pool cannot be negative'
    return newErrors
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const newErrors = validateForm()
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    try {
      setLoading(true)
      // API call would go here
      console.log('Creating tournament:', formData)
      // Simulating API delay
      await new Promise(resolve => setTimeout(resolve, 1000))
      navigate('/tournaments')
    } catch (error) {
      setErrors({ submit: 'Failed to create tournament' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">🏆 Create Tournament</h1>
          <p className="text-gray-400">Set up your own esports tournament</p>
        </div>

        {/* Form Card */}
        <Card variant="glow">
          <div className="p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              {errors.submit && (
                <div className="p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-400">
                  {errors.submit}
                </div>
              )}

              {/* Tournament Name */}
              <Input
                label="Tournament Name"
                type="text"
                placeholder="e.g., Spring Championship 2026"
                name="name"
                value={formData.name}
                onChange={handleChange}
                error={errors.name}
                required
              />

              {/* Format */}
              <div className="w-full">
                <label className="block text-sm font-semibold text-gray-300 mb-2">
                  Format <span className="text-red-500">*</span>
                </label>
                <select
                  name="format"
                  value={formData.format}
                  onChange={handleChange}
                  className="w-full px-4 py-2.5 rounded-lg bg-dark-800 border border-dark-700 focus:border-neon-blue text-white transition-smooth focus:outline-none"
                >
                  <option value="knockout">Knockout (Single Elimination)</option>
                  <option value="league">League (Round Robin)</option>
                  <option value="group">Group Stage + Knockout</option>
                </select>
              </div>

              {/* Max Players */}
              <Input
                label="Maximum Players"
                type="number"
                min="2"
                max="1024"
                name="maxPlayers"
                value={formData.maxPlayers}
                onChange={handleChange}
                error={errors.maxPlayers}
                required
              />

              {/* Entry Fee */}
              <Input
                label="Entry Fee (USD)"
                type="number"
                min="0"
                name="entryFee"
                value={formData.entryFee}
                onChange={handleChange}
              />

              {/* Prize Pool */}
              <Input
                label="Prize Pool (USD)"
                type="number"
                min="1"
                name="prizePool"
                value={formData.prizePool}
                onChange={handleChange}
                error={errors.prizePool}
                required
              />

              {/* Info */}
              <div className="p-4 bg-neon-blue/10 border border-neon-blue/30 rounded-lg">
                <p className="text-sm text-gray-300">
                  <strong>Tournament Details:</strong>
                </p>
                <ul className="mt-2 text-sm text-gray-400 space-y-1">
                  <li>• Format: <span className="text-white capitalize">{formData.format}</span></li>
                  <li>• Max Players: <span className="text-white">{formData.maxPlayers}</span></li>
                  <li>• Entry Fee: <span className="text-white">${formData.entryFee}</span></li>
                  <li>• Prize Pool: <span className="text-white">${formData.prizePool}</span></li>
                </ul>
              </div>

              {/* Buttons */}
              <div className="flex gap-4 pt-4">
                <Button
                  variant="primary"
                  size="lg"
                  className="flex-1"
                  type="submit"
                  isLoading={loading}
                >
                  Create Tournament
                </Button>
                <Button
                  variant="secondary"
                  size="lg"
                  className="flex-1"
                  onClick={() => navigate('/tournaments')}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </div>
        </Card>
      </div>
    </motion.div>
  )
}
