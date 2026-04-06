import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Input from '../components/Input'
import Card from '../components/Card'
import { tournamentService } from '../services/api'

export default function CreateTournamentPage() {
  const navigate = useNavigate()
  
  // Initialize with future dates (1 and 2 hours from now)
  const getDefaultDates = () => {
    const now = new Date()
    
    const start = new Date(now.getTime() + 60 * 60 * 1000) // 1 hour from now
    const end = new Date(now.getTime() + 120 * 60 * 1000) // 2 hours from now
    
    // Convert to local datetime-local format (YYYY-MM-DDTHH:mm)
    const toLocalDateTimeString = (date) => {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      return `${year}-${month}-${day}T${hours}:${minutes}`
    }
    
    return {
      start_date: toLocalDateTimeString(start),
      end_date: toLocalDateTimeString(end),
    }
  }
  
  const { start_date: defaultStart, end_date: defaultEnd } = getDefaultDates()
  
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    format: 'Knockout',
    max_players: 32,
    prize_pool: 1000,
    rules: '',
    location: 'Virtual',
    is_public: true,
    start_date: defaultStart,
    end_date: defaultEnd,
  })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData({ ...formData, [name]: type === 'checkbox' ? checked : value })
    if (errors[name]) setErrors({ ...errors, [name]: '' })
  }

  const validate = () => {
    const e = {}
    if (!formData.name) e.name = 'Tournament name is required'
    if (!formData.start_date) e.start_date = 'Start date is required'
    if (!formData.end_date) e.end_date = 'End date is required'
    if (parseInt(formData.max_players) < 2) e.max_players = 'Minimum 2 players'
    return e
  }

  const handleSubmit = async (ev) => {
    ev.preventDefault()
    const newErrors = validate()
    if (Object.keys(newErrors).length > 0) { setErrors(newErrors); return }

    try {
      setLoading(true)
      
      // Convert datetime-local strings to ISO format correctly
      // datetime-local returns local time, so we need to convert it properly
      const convertToISOString = (localDateTimeString) => {
        // Parse the datetime-local string (format: "2026-04-04T14:04")
        const [datePart, timePart] = localDateTimeString.split('T')
        const [year, month, day] = datePart.split('-')
        const [hours, minutes] = timePart.split(':')
        
        // Create date in local timezone and convert to ISO
        const date = new Date(year, parseInt(month) - 1, day, hours, minutes, 0)
        return date.toISOString()
      }
      
      const payload = {
        ...formData,
        max_players: parseInt(formData.max_players),
        prize_pool: parseInt(formData.prize_pool),
        start_date: convertToISOString(formData.start_date),
        end_date: convertToISOString(formData.end_date),
      }
      
      console.log('📝 Tournament create payload:', payload)
      console.log('📅 Start date ISO:', payload.start_date)
      console.log('📅 End date ISO:', payload.end_date)
      console.log('📅 Now:', new Date().toISOString())
      
      const { data } = await tournamentService.create(payload)
      navigate(`/tournaments/${data.tournament_id}`)
    } catch (err) {
      console.error('❌ Tournament create error:', err.response?.data || err.message)
      console.error('Error status:', err.response?.status)
      console.error('Full error:', err)
      
      // Parse error response
      let errorMessage = 'Failed to create tournament'
      let fieldErrors = {}
      
      if (err.response?.data) {
        const data = err.response.data
        
        // Handle different error response formats
        if (data.message) {
          errorMessage = data.message
        } else if (data.detail) {
          errorMessage = data.detail
        } else if (data.error) {
          errorMessage = data.error
        }
        
        // Extract field-specific errors
        if (data.errors) {
          if (typeof data.errors === 'object') {
            fieldErrors = data.errors
          }
        }
      }
      
      // Set errors
      const allErrors = { submit: errorMessage }
      
      // Add field-specific errors if any
      if (Object.keys(fieldErrors).length > 0) {
        Object.entries(fieldErrors).forEach(([field, error]) => {
          if (Array.isArray(error)) {
            allErrors[field] = error[0] // Get first error message
          } else if (typeof error === 'string') {
            allErrors[field] = error
          }
        })
      }
      
      setErrors(allErrors)
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">🏆 Create Tournament</h1>
          <p className="text-gray-400">Set up your own esports tournament</p>
        </div>

        <Card variant="glow">
          <div className="p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              {errors.submit && (
                <div className="p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-400">{errors.submit}</div>
              )}

              <Input label="Tournament Name" type="text" placeholder="e.g., Spring Championship 2026"
                name="name" value={formData.name} onChange={handleChange} error={errors.name} required />

              <Input label="Description" type="text" placeholder="Describe your tournament"
                name="description" value={formData.description} onChange={handleChange} />

              <div>
                <label className="block text-sm font-semibold text-gray-300 mb-2">Format <span className="text-red-500">*</span></label>
                <select name="format" value={formData.format} onChange={handleChange}
                  className="w-full px-4 py-2.5 rounded-lg bg-dark-800 border border-dark-700 focus:border-neon-blue text-white focus:outline-none">
                  <option value="Knockout">Knockout (Single Elimination)</option>
                  <option value="League">League (Round Robin)</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <Input label="Start Date" type="datetime-local" name="start_date"
                  value={formData.start_date} onChange={handleChange} error={errors.start_date} required />
                <Input label="End Date" type="datetime-local" name="end_date"
                  value={formData.end_date} onChange={handleChange} error={errors.end_date} required />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <Input label="Max Players" type="number" min="2" max="256" name="max_players"
                  value={formData.max_players} onChange={handleChange} error={errors.max_players} required />
                <Input label="Prize Pool (coins)" type="number" min="0" name="prize_pool"
                  value={formData.prize_pool} onChange={handleChange} />
              </div>

              <Input label="Location" type="text" placeholder="Virtual" name="location"
                value={formData.location} onChange={handleChange} />

              <Input label="Rules" type="text" placeholder="Tournament rules (optional)"
                name="rules" value={formData.rules} onChange={handleChange} />

              <div className="flex gap-4 pt-4">
                <Button variant="primary" size="lg" className="flex-1" type="submit" isLoading={loading}>
                  Create Tournament
                </Button>
                <Button variant="secondary" size="lg" className="flex-1" onClick={() => navigate('/tournaments')}>
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
