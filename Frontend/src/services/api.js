import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

// Track 401 errors to avoid infinite loops
let is401Handling = false

// Attach access token to every request
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
    console.log('📤 Request sent with token:', token.substring(0, 10) + '...')
  } else {
    console.warn('⚠️ No access token in request for:', config.url)
  }
  return config
})

// Auto-refresh on 401 with better error handling
apiClient.interceptors.response.use(
  (res) => {
    console.log('✅ API Response successful:', res.status, res.config.url)
    return res
  },
  async (error) => {
    const original = error.config
    const status = error.response?.status
    
    console.error('❌ API Error:', {
      status,
      url: original.url,
      hasRefresh: !!original._retry,
      hasRefreshToken: !!localStorage.getItem('refresh_token'),
    })

    // Only handle 401 once per request
    if (status === 401 && !original._retry) {
      console.warn('⚠️ 401 Unauthorized - Attempting to refresh token...')
      original._retry = true
      
      const refresh = localStorage.getItem('refresh_token')
      if (refresh) {
        try {
          console.log('🔄 Refreshing token...')
          const { data } = await axios.post(`${BASE_URL}/auth/token/refresh/`, { refresh }, {
            headers: { 'Content-Type': 'application/json' }
          })
          
          // Token refresh successful
          localStorage.setItem('access_token', data.access)
          console.log('✅ Token refreshed successfully')
          
          // Retry original request with new token
          original.headers.Authorization = `Bearer ${data.access}`
          return apiClient(original)
        } catch (refreshError) {
          console.error('❌ Token refresh failed:', refreshError.message)
          
          // Only clear tokens and redirect if refresh truly failed
          console.log('🚪 Logging out due to failed token refresh...')
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user')
          
          // Delay redirect to allow error display
          setTimeout(() => {
            window.location.href = '/login'
          }, 500)
        }
      } else {
        console.warn('⚠️ No refresh token available - redirecting to login')
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        
        // Delay redirect to allow error display
        setTimeout(() => {
          window.location.href = '/login'
        }, 500)
      }
    }
    
    return Promise.reject(error)
  }
)

// ── Auth ──────────────────────────────────────────────────────────────────────
export const authService = {
  register: (username, email, password, firstName = '', lastName = '') =>
    apiClient.post('/auth/register/', { username, email, password, password_confirm: password, first_name: firstName, last_name: lastName }),
  login: (username, password) =>
    apiClient.post('/auth/login/', { username, password }),
  logout: (refresh) =>
    apiClient.post('/auth/logout/', { refresh }),
  getProfile: () =>
    apiClient.get('/auth/profile/'),
  updateProfile: (data) =>
    apiClient.patch('/auth/profile/', data),
  refreshToken: (refresh) =>
    apiClient.post('/auth/token/refresh/', { refresh }),
}

// ── Tournaments ───────────────────────────────────────────────────────────────
export const tournamentService = {
  getAll: (params) => apiClient.get('/tournaments/', { params }),
  getById: (id) => apiClient.get(`/tournaments/${id}/`),
  create: (data) => apiClient.post('/tournaments/create/', data),
  join: (id) => apiClient.post(`/tournaments/${id}/join/`, {}),
  updateStatus: (id, status) => apiClient.post(`/tournaments/${id}/update-status/`, { status }),
}

// ── Matches ───────────────────────────────────────────────────────────────────
export const matchService = {
  getTournamentMatches: (tournamentId) => apiClient.get(`/matches/tournament/${tournamentId}/`),
  getById: (id) => apiClient.get(`/matches/${id}/`),
  submitResult: (id, player1Score, player2Score, proofFile) => {
    const form = new FormData()
    form.append('player1_score', player1Score)
    form.append('player2_score', player2Score)
    if (proofFile) form.append('proof', proofFile)
    return apiClient.post(`/matches/${id}/submit-result/`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  getPlayerStats: (playerId) => apiClient.get(`/matches/player/${playerId}/stats/`),
  getPlayerMatches: (playerId, params) => apiClient.get(`/matches/player/${playerId}/matches/`, { params }),
}

// ── Auctions ──────────────────────────────────────────────────────────────────
export const auctionService = {
  getActive: () => apiClient.get('/auctions/active/'),
  getTournamentAuctions: (tournamentId, params) =>
    apiClient.get(`/auctions/tournament/${tournamentId}/`, { params }),
  getById: (id) => apiClient.get(`/auctions/${id}/`),
  start: (data) => apiClient.post('/auctions/start/', data),
  placeBid: (auctionId, bidAmount) =>
    apiClient.post(`/auctions/${auctionId}/place-bid/`, { bid_amount: bidAmount }),
  getBidHistory: (auctionId) => apiClient.get(`/auctions/${auctionId}/bid-history/`),
  getUserStats: (userId) => apiClient.get(`/auctions/user/${userId}/stats/`),
}

// ── Leaderboard ───────────────────────────────────────────────────────────────
export const leaderboardService = {
  getTournamentLeaderboard: (tournamentId) =>
    apiClient.get(`/leaderboard/tournament/${tournamentId}/`),
  getRankings: (params) => apiClient.get('/leaderboard/rankings/', { params }),
  getTopPlayers: (params) => apiClient.get('/leaderboard/top-players/', { params }),
  getPlayerStats: (playerId) => apiClient.get(`/leaderboard/player/${playerId}/stats/`),
  getMyRank: (tournamentId) => apiClient.get(`/leaderboard/my-rank/${tournamentId}/`),
}

// ── Missions ──────────────────────────────────────────────────────────────────
export const missionService = {
  getAvailable: (params) => apiClient.get('/missions/available/', { params }),
  start: (missionId) => apiClient.post('/missions/start/', { mission_id: missionId }),
  getMyMissions: (params) => apiClient.get('/missions/my-missions/', { params }),
  getById: (id) => apiClient.get(`/missions/${id}/`),
  getPendingRewards: () => apiClient.get('/missions/pending-rewards/'),
  claimReward: (userMissionId) =>
    apiClient.post(`/missions/${userMissionId}/claim-reward/`, {}),
  getStats: () => apiClient.get('/missions/stats/'),
}

// ── Clubs ─────────────────────────────────────────────────────────────────────
export const clubService = {
  getAll: (params) => apiClient.get('/clubs/', { params }),
  getById: (id) => apiClient.get(`/clubs/${id}/`),
  create: (data) => apiClient.post('/clubs/create/', data),
  update: (id, data) => apiClient.put(`/clubs/${id}/update/`, data),
  join: (id) => apiClient.post(`/clubs/${id}/join/`, {}),
  leave: (id) => apiClient.post(`/clubs/${id}/leave/`, {}),
  getUserClubs: (userId) => apiClient.get(`/clubs/user/${userId}/`),
  getStats: (id) => apiClient.get(`/clubs/${id}/stats/`),
  getMembers: (id) => apiClient.get(`/clubs/${id}/members/`),
}

// ── Reports ───────────────────────────────────────────────────────────────────
export const reportService = {
  create: (data) => apiClient.post('/reports/create/', data),
  getAll: (params) => apiClient.get('/reports/', { params }),
  getById: (id) => apiClient.get(`/reports/${id}/`),
  review: (id) => apiClient.post(`/reports/${id}/review/`, {}),
  approve: (id, data) => apiClient.post(`/reports/${id}/approve/`, data),
  reject: (id, notes) => apiClient.post(`/reports/${id}/reject/`, { resolution_notes: notes }),
  getStats: () => apiClient.get('/reports/stats/'),
}

// ── ML / Predictions ──────────────────────────────────────────────────────────
export const mlService = {
  predict: (player1Id, player2Id, useCache = true) =>
    apiClient.post('/ml/predict/', { player1_id: player1Id, player2_id: player2Id, use_cache: useCache }),
  getModelStats: () => apiClient.get('/ml/model-stats/'),
}

// ── WebSocket helpers ─────────────────────────────────────────────────────────
export const createNotificationSocket = () =>
  new WebSocket(`${WS_URL}/ws/notifications/`)

export const createMatchSocket = (matchId) =>
  new WebSocket(`${WS_URL}/ws/matches/${matchId}/`)

export const createAuctionSocket = (auctionId) =>
  new WebSocket(`${WS_URL}/ws/auctions/${auctionId}/`)

export default apiClient
