import { useState, useEffect } from 'react'
import { useLocation, useNavigate, Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import Button from '../components/Button'

export default function MainLayout({ children, user, onLogout }) {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const location = useLocation()
  const navigate = useNavigate()

  const navItems = [
    { label: 'Dashboard', path: '/', icon: '🏠' },
    { label: 'Tournaments', path: '/tournaments', icon: '🏆' },
    { label: 'Match', path: '/match/1', icon: '⚔️' },
    { label: 'Auction', path: '/auction', icon: '💰' },
    { label: 'Leaderboard', path: '/leaderboard', icon: '📊' },
    { label: 'Missions', path: '/missions', icon: '🎯' },
    { label: 'Clubs', path: '/clubs', icon: '🧑‍🤝‍🧑' },
    { label: 'Profile', path: `/profile/${user?.id || 1}`, icon: '👤' },
  ]

  const handleLogout = () => {
    onLogout()
    navigate('/login')
  }

  return (
    <div className="flex h-screen bg-dark-900 text-white">
      {/* Sidebar */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            transition={{ type: 'tween' }}
            className="w-64 bg-dark-800 border-r border-dark-700 overflow-y-auto hidden lg:flex flex-col"
          >
            {/* Logo */}
            <div className="p-6 border-b border-dark-700">
              <h1 className="text-2xl font-bold bg-gradient-to-r from-neon-blue to-neon-purple bg-clip-text text-transparent glow-text">
                PES Esports
              </h1>
            </div>

            {/* Navigation */}
            <nav className="flex-1 p-4 space-y-2">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`
                    flex items-center gap-3 px-4 py-3 rounded-lg transition-smooth
                    ${location.pathname === item.path
                      ? 'bg-gradient-to-r from-neon-blue/30 to-neon-purple/30 text-neon-blue border border-neon-blue/50'
                      : 'text-gray-400 hover:text-white hover:bg-dark-700'
                    }
                  `}
                >
                  <span className="text-xl">{item.icon}</span>
                  <span className="font-semibold">{item.label}</span>
                </Link>
              ))}
            </nav>

            {/* User Info */}
            <div className="p-4 border-t border-dark-700 space-y-3">
              {user && (
                <div className="p-3 bg-dark-700/50 rounded-lg">
                  <p className="text-sm text-gray-400">Logged in as</p>
                  <p className="font-semibold text-neon-blue">{user.username || 'Player'}</p>
                </div>
              )}
              <Button
                variant="ghost"
                size="md"
                onClick={handleLogout}
                className="w-full justify-center"
              >
                Logout
              </Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div className="flex-1 flex flex-col w-full lg:w-auto">
        {/* Top Bar */}
        <div className="h-16 bg-dark-800 border-b border-dark-700 flex items-center justify-between px-4 lg:px-6">
          {/* Menu Toggle */}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-neon-blue hover:text-neon-purple transition-smooth"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          {/* Mobile Menu */}
          <div className="lg:hidden flex gap-4 items-center">
            {user && <span className="text-sm text-gray-400">{user.username}</span>}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-neon-blue hover:text-neon-purple transition-smooth"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>

          {/* Desktop User Menu */}
          <div className="hidden lg:flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-neon-blue to-neon-purple flex items-center justify-center">
                <span className="text-sm font-bold">P</span>
              </div>
              <span className="font-semibold">{user?.username || 'Player'}</span>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="lg:hidden bg-dark-800 border-b border-dark-700 overflow-hidden"
            >
              <nav className="p-4 space-y-2">
                {navItems.map((item) => (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`
                      flex items-center gap-3 px-4 py-3 rounded-lg transition-smooth
                      ${location.pathname === item.path
                        ? 'bg-gradient-to-r from-neon-blue/30 to-neon-purple/30 text-neon-blue border border-neon-blue/50'
                        : 'text-gray-400 hover:text-white hover:bg-dark-700'
                      }
                    `}
                  >
                    <span className="text-xl">{item.icon}</span>
                    <span className="font-semibold">{item.label}</span>
                  </Link>
                ))}
              </nav>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Page Content */}
        <div className="flex-1 overflow-y-auto">
          <div className="p-4 lg:p-8">
            {children}
          </div>
        </div>
      </div>
    </div>
  )
}
