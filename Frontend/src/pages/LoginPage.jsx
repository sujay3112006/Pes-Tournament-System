import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Input from '../components/Input'
import { validateEmail, validatePassword } from '../utils/helpers'
import { authService } from '../services/api'

export default function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const validateForm = () => {
    const newErrors = {}
    if (!email) newErrors.email = 'Email is required'
    else if (!validateEmail(email)) newErrors.email = 'Invalid email format'
    if (!password) newErrors.password = 'Password is required'
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
      const response = await authService.login(email, password)
      onLogin(response.data.token, response.data.user)
      navigate('/')
    } catch (error) {
      setErrors({ submit: error.response?.data?.message || 'Login failed' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-dark-900 flex items-center justify-center p-4 overflow-hidden relative">
      {/* Animated Background with Stadium Lights */}
      <div className="absolute inset-0 stadium-lights opacity-30" />
      
      {/* Floating Neon Orbs */}
      <motion.div
        className="absolute top-20 left-10 w-32 h-32 bg-neon-blue/20 rounded-full blur-3xl"
        animate={{ y: [0, 30, 0], x: [0, 20, 0] }}
        transition={{ duration: 8, repeat: Infinity }}
      />
      <motion.div
        className="absolute bottom-20 right-10 w-40 h-40 bg-neon-purple/20 rounded-full blur-3xl"
        animate={{ y: [0, -30, 0], x: [0, -20, 0] }}
        transition={{ duration: 10, repeat: Infinity }}
      />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-md z-10"
      >
        <div className="glassmorphism-thick rounded-2xl p-8 border-2 border-neon-blue/40 shadow-glow-lg relative overflow-hidden">
          {/* Animated gradient border */}
          <motion.div
            className="absolute inset-0 bg-gradient-to-br from-neon-blue/20 via-transparent to-neon-purple/20 rounded-2xl pointer-events-none"
            animate={{ opacity: [0.3, 0.6, 0.3] }}
            transition={{ duration: 3, repeat: Infinity }}
          />

          <div className="relative z-10">
            {/* Header with Glow */}
            <div className="text-center mb-8">
              <motion.h1 
                className="text-5xl font-black bg-gradient-to-r from-neon-blue via-neon-cyan to-neon-purple bg-clip-text text-transparent mb-2 drop-shadow-xl"
                animate={{ scale: [0.98, 1, 0.98] }}
                transition={{ duration: 3, repeat: Infinity }}
              >
                PES ESPORTS
              </motion.h1>
              <motion.div
                className="h-1 w-20 bg-gradient-to-r from-neon-blue to-neon-purple mx-auto mb-3 shadow-glow-md"
                animate={{ scaleX: [0.8, 1, 0.8] }}
                transition={{ duration: 2, repeat: Infinity }}
              />
              <p className="text-gray-300 font-semibold">🎮 Enter the Arena</p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-5">
              {errors.submit && (
                <motion.div 
                  className="p-4 bg-neon-pink/15 border border-neon-pink/50 rounded-lg text-neon-pink text-sm font-semibold flex items-start gap-2"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <span className="text-lg mt-0.5">⚠️</span>
                  <span>{errors.submit}</span>
                </motion.div>
              )}

              <Input
                label="📧 Email"
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value)
                  if (errors.email) setErrors({ ...errors, email: '' })
                }}
                error={errors.email}
                required
              />

              <Input
                label="🔐 Password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value)
                  if (errors.password) setErrors({ ...errors, password: '' })
                }}
                error={errors.password}
                required
              />

              <Button
                variant="primary"
                size="lg"
                className="w-full mt-8 font-black text-lg"
                isLoading={loading}
                type="submit"
              >
                ⚽ ENTER ARENA
              </Button>
            </form>

            {/* Divider */}
            <div className="my-6 flex items-center">
              <div className="flex-1 h-px bg-neon-blue/20" />
              <span className="px-3 text-gray-400 text-xs font-bold uppercase">OR</span>
              <div className="flex-1 h-px bg-neon-blue/20" />
            </div>

            {/* Social Login */}
            <div className="grid grid-cols-2 gap-4">
              <Button variant="secondary" className="w-full font-bold">
                🔵 Google
              </Button>
              <Button variant="secondary" className="w-full font-bold">
                💜 Discord
              </Button>
            </div>

            {/* Footer */}
            <p className="text-center text-gray-400 text-sm mt-8 font-semibold">
              New Player?{' '}
              <motion.a
                href="/register"
                className="text-neon-blue hover:text-neon-cyan transition-smooth font-bold"
                whileHover={{ scale: 1.05 }}
              >
                Start Game
              </motion.a>
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
