# PES Esports Tournament - Frontend

A modern, production-ready React + Vite esports tournament web application with a dark theme, animations, and comprehensive tournament management features.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ installed
- npm or yarn package manager

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

The application will start at `http://localhost:3000`

### Build

```bash
npm run build
```

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Button.jsx      # Primary button component
│   ├── Card.jsx        # Card container component
│   ├── Input.jsx       # Form input component
│   ├── Modal.jsx       # Modal dialog component
│   ├── Loader.jsx      # Loading spinner
│   ├── Badge.jsx       # Badge/tag component
│   ├── ProgressBar.jsx # Progress indicator
│   ├── Tabs.jsx        # Tab navigation
│   ├── PlayerCard.jsx  # eFootball style player card
│   └── TournamentCard.jsx # Tournament display card
│
├── pages/              # Page components
│   ├── LoginPage.jsx
│   ├── RegisterPage.jsx
│   ├── DashboardPage.jsx
│   ├── TournamentListPage.jsx
│   ├── CreateTournamentPage.jsx
│   ├── TournamentDetailsPage.jsx
│   ├── MatchViewPage.jsx
│   ├── LiveMatchTrackerPage.jsx
│   ├── AuctionPage.jsx
│   ├── LeaderboardPage.jsx
│   ├── MissionsPage.jsx
│   ├── ClubPage.jsx
│   ├── ProfilePage.jsx
│   └── NotFoundPage.jsx
│
├── layouts/            # Layout components
│   └── MainLayout.jsx  # Main app layout with sidebar
│
├── services/           # API services
│   └── api.js          # Axios instance & API endpoints
│
├── hooks/              # Custom React hooks
│   └── useApi.js       # API data fetching hook
│
├── utils/              # Utility functions
│   └── helpers.js      # Helper functions (validation, formatting)
│
├── assets/             # Images, fonts, etc.
├── App.jsx             # Main app component with routing
├── index.css           # Global styles & animations
└── main.jsx            # Entry point

public/
└── index.html          # HTML template
```

## 🎨 Design System

### Colors
- **Primary**: Neon Blue (`#00d9ff`)
- **Accent**: Neon Purple (`#a855f7`)
- **Background**: Dark Navy (`#0f172a`)
- **Card**: Dark Gray (`#1e293b`)

### Tailwind Configuration
All colors and theme values are configured in `tailwind.config.js` with custom extensions for gradients, glows, and animations.

## ✨ Features

### Authentication
- Login/Register pages with validation
- Token-based authentication
- Protected routes
- Automatic redirect on auth failure

### Tournament System
- Browse tournaments (Ongoing, Upcoming, Completed)
- Create tournaments with customizable settings
- Tournament details with player lists
- Join/Leave functionality
- Bracket visualization

### Match Management
- Match details view
- Score submission with proof upload
- Live match tracker with real-time updates
- Event timeline (goals, cards, etc.)
- Head-to-head stats

### Player Auction
- Live bidding system
- Player cards with ratings
- Bid history
- Timer countdown

### Leaderboard
- Global rankings
- Player statistics (wins, points, level)
- Top 3 podium display
- Sortable table

### Missions System
- Daily/Weekly missions with rewards
- Progress tracking
- Reward claiming
- Mission categories

### Club System
- Create and join clubs
- Club management
- Member roster
- Club leaderboard
- Messages

### User Profile
- Player statistics
- Match history
- Achievement badges
- Rank and rating display

## 🔌 API Integration

### Base URL
```
http://localhost:5000/api
```

### Authentication Endpoints
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Tournament Endpoints
- `GET /tournaments` - Get all tournaments
- `GET /tournaments/:id` - Get tournament details
- `POST /tournaments` - Create tournament
- `POST /tournaments/:id/join` - Join tournament

### Match Endpoints
- `GET /matches/:id` - Get match details
- `POST /matches/:id/submit-score` - Submit match score
- `POST /matches/:id/upload-proof` - Upload match proof

### Other Endpoints
- User, Auction, Leaderboard, Missions, Club endpoints

See `src/services/api.js` for complete endpoint definitions.

## 🛠️ Configuration

### Environment Variables
Create a `.env` file:

```env
VITE_API_URL=http://localhost:5000/api
```

## 📦 Dependencies

### Core
- **React** - UI framework
- **React Router DOM** - Routing
- **Vite** - Build tool

### Styling
- **Tailwind CSS** - Utility-first CSS framework
- **PostCSS & Autoprefixer** - CSS processing

### Animation & UI
- **Framer Motion** - Animation library

### API
- **Axios** - HTTP client

## 🚀 Performance Optimization

- Component code-splitting with React Router
- Lazy loading of pages
- Optimized animations with Framer Motion
- CSS-in-JS with Tailwind
- Bundle optimization with Vite

## 🤝 Component Examples

### Using Button Component
```jsx
<Button 
  variant="primary" 
  size="lg" 
  onClick={handleClick}
  isLoading={loading}
>
  Click Me
</Button>
```

### Using Card Component
```jsx
<Card variant="glow" hover>
  <div className="p-6">
    {/* Content */}
  </div>
</Card>
```

### Using Tabs
```jsx
<Tabs 
  tabs={tabs} 
  activeTab={activeTab} 
  onTabChange={setActiveTab}
/>
```

## 📝 Styling Notes

- All colors use Tailwind's dark theme extensions
- Glassmorphism effect available with `.glassmorphism` class
- Glow effects: `.shadow-glow`, `.shadow-glow-lg`, `.glow-text`
- Animations: `animate-pulse`, `animate-glow`
- Responsive grid system: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`

## 🐛 Troubleshooting

### Port 3000 already in use
```bash
npm run dev -- --port 3001
```

### Build errors
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Tailwind styles not applying
- Ensure content paths are correct in `tailwind.config.js`
- Run `npm run build` to regenerate CSS

## 📄 License

Created for PES Esports Tournament platform.

## 👥 Support

For issues or questions, please refer to the project documentation or contact the development team.
