import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import MainLayout from './layouts/MainLayout'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import TournamentListPage from './pages/TournamentListPage'
import CreateTournamentPage from './pages/CreateTournamentPage'
import TournamentDetailsPage from './pages/TournamentDetailsPage'
import MatchViewPage from './pages/MatchViewPage'
import LiveMatchTrackerPage from './pages/LiveMatchTrackerPage'
import AuctionPage from './pages/AuctionPage'
import LeaderboardPage from './pages/LeaderboardPage'
import MissionsPage from './pages/MissionsPage'
import ClubPage from './pages/ClubPage'
import ProfilePage from './pages/ProfilePage'
import NotFoundPage from './pages/NotFoundPage'
import { authService } from './services/api'

function ProtectedRoute({ children, isAuthenticated, isLoading }) {
  // Check localStorage directly - this is the SOURCE OF TRUTH
  const access = localStorage.getItem('access_token')
  const token = localStorage.getItem('token')
  const hasToken = access || token
  
  console.log('🛡️ ProtectedRoute rendering:', {
    isAuthenticated,
    isLoading,
    access_token: access ? access.substring(0, 10) + '...' : null,
    token: token ? token.substring(0, 10) + '...' : null,
    hasToken: !!hasToken,
    willAllow: isAuthenticated || !!hasToken,
  })
  
  if (isLoading) {
    console.log('🛡️ Still loading, showing loading screen')
    return <div className="flex items-center justify-center h-screen bg-dark-900"><p className="text-white">Loading...</p></div>
  }
  
  const isAuth = isAuthenticated || !!hasToken
  
  if (!isAuth) {
    console.warn('❌ ProtectedRoute: Not authenticated, redirecting to /login')
    return <Navigate to="/login" replace />
  }
  
  console.log('✅ ProtectedRoute: Allowing access')
  return children
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [user, setUser] = useState(null)

  useEffect(() => {
    console.log('� APP INITIAL MOUNT - Checking auth...')
    // Check for 'access_token' first, then fallback to 'token' (for compatibility)
    const access = localStorage.getItem('access_token') || localStorage.getItem('token')
    console.log('🔍 Access token found:', !!access)
    
    if (access) {
      const storedUser = localStorage.getItem('user')
      console.log('🔍 Stored user found:', !!storedUser)
      
      if (storedUser) {
        try {
          const userData = JSON.parse(storedUser)
          console.log('✅ User data parsed:', userData)
          setUser(userData)
          setIsAuthenticated(true)
        } catch (e) {
          console.error('❌ Error parsing user data:', e)
          localStorage.removeItem('access_token')
          localStorage.removeItem('token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user')
          setIsAuthenticated(false)
        }
      } else {
        console.log('⚠️ Token exists but no user, still count as authenticated')
        setIsAuthenticated(true)
      }
    } else {
      console.log('❌ No token found')
      setIsAuthenticated(false)
    }
    console.log('✅ Initial auth check complete, setting isLoading=false')
    setIsLoading(false)
  }, [])

  // Watch for state changes
  useEffect(() => {
    console.log('📊 App state updated:', { 
      isAuthenticated, 
      isLoading, 
      hasUser: !!user,
      tokenInStorage: !!localStorage.getItem('access_token')
    })
  }, [isAuthenticated, isLoading, user])

  const handleLogin = (userData, accessToken, refreshToken) => {
    console.log('💾 handleLogin called')
    console.log('💾 Saving tokens...')
    console.log('💾 accessToken:', accessToken)
    console.log('💾 refreshToken:', refreshToken)
    
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)
    localStorage.setItem('user', JSON.stringify(userData))
    
    console.log('💾 Tokens saved. Verifying...')
    console.log('💾 access_token in localStorage:', localStorage.getItem('access_token'))
    console.log('💾 refresh_token in localStorage:', localStorage.getItem('refresh_token'))
    
    console.log('💾 Setting isAuthenticated=true, isLoading=false')
    setIsAuthenticated(true)
    setIsLoading(false)
    setUser(userData)
    
    console.log('✅ Login handler complete. New state:', {
      isAuthenticated: true,
      isLoading: false,
      user: userData
    })
  }

  const handleLogout = async () => {
    const refresh = localStorage.getItem('refresh_token')
    try { await authService.logout(refresh) } catch { /* ignore */ }
    localStorage.removeItem('access_token')
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    setIsAuthenticated(false)
    setUser(null)
  }

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
        <Route path="/register" element={<RegisterPage onLogin={handleLogin} />} />
        <Route
          path="/*"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated} isLoading={isLoading}>
              <MainLayout user={user} onLogout={handleLogout}>
                <Routes>
                  <Route path="/" element={<DashboardPage user={user} />} />
                  <Route path="/tournaments" element={<TournamentListPage />} />
                  <Route path="/tournaments/create" element={<CreateTournamentPage />} />
                  <Route path="/tournaments/:id" element={<TournamentDetailsPage user={user} />} />
                  <Route path="/match/:id" element={<MatchViewPage user={user} />} />
                  <Route path="/match/:id/live" element={<LiveMatchTrackerPage />} />
                  <Route path="/auction" element={<AuctionPage user={user} />} />
                  <Route path="/leaderboard" element={<LeaderboardPage user={user} />} />
                  <Route path="/missions" element={<MissionsPage user={user} />} />
                  <Route path="/clubs" element={<ClubPage user={user} />} />
                  <Route path="/profile/:id" element={<ProfilePage user={user} />} />
                  <Route path="*" element={<NotFoundPage />} />
                </Routes>
              </MainLayout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  )
}

export default App
