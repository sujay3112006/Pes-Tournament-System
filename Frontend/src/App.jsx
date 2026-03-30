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

// Protected Route Component
function ProtectedRoute({ children, isAuthenticated, isLoading }) {
  if (isLoading) return <div className="flex items-center justify-center h-screen bg-dark-900"><p>Loading...</p></div>
  return isAuthenticated ? children : <Navigate to="/login" replace />
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [user, setUser] = useState(null)

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    if (token && userData) {
      setIsAuthenticated(true)
      setUser(JSON.parse(userData))
    }
    setIsLoading(false)
  }, [])

  const handleLogin = (token, userData) => {
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(userData))
    setIsAuthenticated(true)
    setUser(userData)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setIsAuthenticated(false)
    setUser(null)
  }

  return (
    <Router>
      <Routes>
        {/* Auth Routes */}
        <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
        <Route path="/register" element={<RegisterPage onLogin={handleLogin} />} />

        {/* Protected Routes with Layout */}
        <Route
          path="/*"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated} isLoading={isLoading}>
              <MainLayout user={user} onLogout={handleLogout}>
                <Routes>
                  <Route path="/" element={<DashboardPage />} />
                  <Route path="/tournaments" element={<TournamentListPage />} />
                  <Route path="/tournaments/create" element={<CreateTournamentPage />} />
                  <Route path="/tournaments/:id" element={<TournamentDetailsPage />} />
                  <Route path="/match/:id" element={<MatchViewPage />} />
                  <Route path="/match/:id/live" element={<LiveMatchTrackerPage />} />
                  <Route path="/auction" element={<AuctionPage />} />
                  <Route path="/leaderboard" element={<LeaderboardPage />} />
                  <Route path="/missions" element={<MissionsPage />} />
                  <Route path="/clubs" element={<ClubPage />} />
                  <Route path="/profile/:id" element={<ProfilePage />} />
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
