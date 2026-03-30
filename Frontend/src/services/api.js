import axios from 'axios'

// Create base API instance
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

// Handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth Service
export const authService = {
  login: (email, password) => apiClient.post('/auth/login', { email, password }),
  register: (email, password, username) => apiClient.post('/auth/register', { email, password, username }),
  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },
}

// User Service
export const userService = {
  getProfile: (userId) => apiClient.get(`/users/${userId}`),
  updateProfile: (userId, data) => apiClient.put(`/users/${userId}`, data),
  getLeaderboard: () => apiClient.get('/users/leaderboard'),
}

// Tournament Service
export const tournamentService = {
  getAll: (filters) => apiClient.get('/tournaments', { params: filters }),
  getById: (id) => apiClient.get(`/tournaments/${id}`),
  create: (data) => apiClient.post('/tournaments', data),
  join: (id) => apiClient.post(`/tournaments/${id}/join`),
  leave: (id) => apiClient.post(`/tournaments/${id}/leave`),
}

// Match Service
export const matchService = {
  getById: (id) => apiClient.get(`/matches/${id}`),
  submitScore: (id, data) => apiClient.post(`/matches/${id}/submit-score`, data),
  uploadProof: (id, file) => {
    const formData = new FormData()
    formData.append('proof', file)
    return apiClient.post(`/matches/${id}/upload-proof`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

// Auction Service
export const auctionService = {
  getActive: () => apiClient.get('/auctions/active'),
  getPlayers: () => apiClient.get('/auctions/players'),
  placeBid: (playerId, amount) => apiClient.post(`/auctions/${playerId}/bid`, { amount }),
}

// Missions Service
export const missionsService = {
  getAll: () => apiClient.get('/missions'),
  claimReward: (missionId) => apiClient.post(`/missions/${missionId}/claim`),
}

// Club Service
export const clubService = {
  getAll: (filters) => apiClient.get('/clubs', { params: filters }),
  getById: (id) => apiClient.get(`/clubs/${id}`),
  create: (data) => apiClient.post('/clubs', data),
  join: (id) => apiClient.post(`/clubs/${id}/join`),
  leave: (id) => apiClient.post(`/clubs/${id}/leave`),
}

export default apiClient
