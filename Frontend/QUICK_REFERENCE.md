# 🚀 QUICK REFERENCE GUIDE

## 📂 Project Location
```
c:\Users\Sujay\Desktop\pes football tournament\Frontend
```

## ⚡ Common Commands

```bash
# Development
npm run dev          # Start dev server (localhost:3000)

# Production
npm run build        # Build for production
npm run preview      # Preview production build

# Dependencies
npm install          # Install all packages
npm update           # Update packages
npm list             # List installed packages
```

## 📁 Key Files to Know

### Configuration
- `vite.config.js` - Vite build settings
- `tailwind.config.js` - Theme colors & extensions
- `postcss.config.js` - CSS processing
- `package.json` - Dependencies & scripts
- `.env.example` - Environment template

### Core
- `src/App.jsx` - Main app + routing
- `src/main.jsx` - Entry point
- `src/index.css` - Global styles

### Folders
- `src/components/` - 10 reusable components
- `src/pages/` - 14 feature pages
- `src/services/` - API integration
- `src/hooks/` - Custom hooks
- `src/utils/` - Helper functions
- `dist/` - Production build (after `npm run build`)

## 🎨 Component Quick Reference

```jsx
// Button
<Button variant="primary" size="lg" onClick={handler}>Click</Button>

// Card
<Card variant="glow" hover>
  <div className="p-6">Content</div>
</Card>

// Input
<Input label="Email" type="email" value={val} onChange={handler} error="Error" />

// Modal
<Modal isOpen={open} onClose={close} title="Title">Content</Modal>

// Badge
<Badge variant="success">Label</Badge>

// ProgressBar
<ProgressBar value={50} max={100} label="Progress" />

// Loader
<Loader size="md" message="Loading..." />

// Tabs
<Tabs tabs={tabs} activeTab={active} onTabChange={setActive} />
```

## 🌐 Routes Reference

| Route | Component | Protected |
|-------|-----------|-----------|
| `/login` | LoginPage | No |
| `/register` | RegisterPage | No |
| `/` | DashboardPage | ✓ |
| `/tournaments` | TournamentListPage | ✓ |
| `/tournaments/create` | CreateTournamentPage | ✓ |
| `/tournaments/:id` | TournamentDetailsPage | ✓ |
| `/match/:id` | MatchViewPage | ✓ |
| `/match/:id/live` | LiveMatchTrackerPage | ✓ |
| `/auction` | AuctionPage | ✓ |
| `/leaderboard` | LeaderboardPage | ✓ |
| `/missions` | MissionsPage | ✓ |
| `/clubs` | ClubPage | ✓ |
| `/profile/:id` | ProfilePage | ✓ |
| `/*` | NotFoundPage | ✓ |

## 🎨 Tailwind Classes Cheat Sheet

```jsx
// Colors
className="text-neon-blue bg-dark-800 border-neon-purple"

// Sizing
className="w-full h-12 px-4 py-2"

// Flexbox
className="flex items-center justify-between gap-4"

// Responsive
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3"

// Hover/Active
className="hover:bg-dark-700 transition-smooth"

// Shadows/Glow
className="shadow-glow shadow-glow-lg"

// Custom
className="glassmorphism neon-glow glow-text stadium-lights"
```

## 🔗 API Service Methods

```javascript
import { 
  authService,
  userService,
  tournamentService,
  matchService,
  auctionService,
  missionsService,
  clubService
} from '../services/api'

// Auth
await authService.login(email, password)
await authService.register(email, password, username)

// Tournaments
await tournamentService.getAll(filters)
await tournamentService.getById(id)
await tournamentService.create(data)
await tournamentService.join(id)

// Matches
await matchService.getById(id)
await matchService.submitScore(id, { player1: 2, player2: 1 })
await matchService.uploadProof(id, file)

// Auctions
await auctionService.getActive()
await auctionService.placeBid(playerId, amount)

// And more...
```

## 🎯 Common Patterns

### Using useState
```jsx
const [state, setState] = useState(initialValue)
```

### Using useEffect
```jsx
useEffect(() => {
  // Fetch data
}, [dependency])
```

### Using useApi Hook
```jsx
const { data, loading, error, execute } = useApi(apiFunction)
useEffect(() => {
  execute(params)
}, [])
```

### Conditional Rendering
```jsx
{condition && <Component />}
{loading ? <Loader /> : <Content />}
```

### Framer Motion
```jsx
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  exit={{ opacity: 0 }}
  whileHover={{ y: -8 }}
>
  Content
</motion.div>
```

## 🔍 Debugging Tips

```jsx
// Console log
console.log('value:', value)

// React DevTools - Use $r to access component in console
$r.state
$r.props

// Check Props in JSX
<Component {...{...props}} />

// Error Boundary (optional future addition)
<ErrorBoundary>
  <ComponentThatMightError />
</ErrorBoundary>
```

## 📱 Responsive Breakpoints

- `sm:` 640px and up
- `md:` 768px and up
- `lg:` 1024px and up
- `xl:` 1280px and up

```jsx
<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
```

## 🎬 Animation Classes

```jsx
// Built-in Framer Motion
<motion.div
  animate={{ rotate: 360 }}
  transition={{ duration: 2 }}
/>

// Custom animations
className="animate-pulse animate-glow"

// Hover effects
whileHover={{ scale: 1.05 }}
whileTap={{ scale: 0.95 }}
```

## ✅ Pre-commit Checklist

- [ ] No console.log() left in code
- [ ] All imports are used
- [ ] Components are exported correctly
- [ ] No TypeErrors in console
- [ ] Build passes: `npm run build`
- [ ] Dev server runs: `npm run dev`

## 🔑 Environment Variables Template

```env
# Backend API
VITE_API_URL=http://localhost:5000/api

# Optional future additions
VITE_APP_NAME=PES Esports Tournament
VITE_APP_VERSION=1.0.0
```

## 📊 Build Output Locations

- Development: Served from `src/` (Vite dev server)
- Production: Built to `dist/` folder
- Entry file: `dist/index.html`
- CSS: `dist/assets/index-*.css`
- JS: `dist/assets/index-*.js`

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Port 3000 in use | `npm run dev -- --port 3001` |
| Styles not applying | Clear cache, rebuild CSS |
| API calls failing | Check VITE_API_URL in .env |
| Build fails | `npm install` then `npm run build` |
| Components not rendering | Check import paths & exports |

## 🚀 Deployment Checklist

- [ ] Set production VITE_API_URL
- [ ] Run `npm run build`
- [ ] Test with `npm run preview`
- [ ] Check `dist/` folder size
- [ ] Verify all routes work
- [ ] Test authentication flow
- [ ] Check responsive design
- [ ] Deploy `dist/` folder

## 📚 Documentation Files

- **README.md** - Quick start
- **DEVELOPMENT.md** - Dev guide
- **PROJECT_OVERVIEW.md** - Complete overview
- **This file** - Quick reference

## 🎓 Learning Path

1. Understand project structure
2. Review existing components
3. Learn routing in App.jsx
4. Study page implementations
5. Explore API service pattern
6. Practice adding new components
7. Integrate with backend

## 💬 Key Concepts

- **Components**: Reusable UI pieces
- **Pages**: Full-screen features
- **Services**: API communication
- **Hooks**: Reusable logic
- **State**: Component data
- **Props**: Component parameters
- **Routing**: URL-based navigation

---

**Quick Access**: Keep this file open for rapid reference during development!

Last Updated: March 30, 2026
