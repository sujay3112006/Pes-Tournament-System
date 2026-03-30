# PES Esports Tournament - Frontend Development Guide

## 📋 Table of Contents
1. Architecture Overview
2. Component Hierarchy
3. State Management
4. Routing Structure
5. Styling Approach
6. API Integration
7. Best Practices
8. Performance Tips

## 🏗️ Architecture Overview

### Technology Stack
- **Framework**: React 18.2
- **Build Tool**: Vite 5.0
- **Styling**: Tailwind CSS 3.3
- **Routing**: React Router DOM 6.20
- **HTTP Client**: Axios 1.6
- **Animations**: Framer Motion 10.16

### Project Structure Philosophy
- **Separation of Concerns**: UI, business logic, and data are separate
- **Reusability**: Components are composed and reused throughout
- **Modularity**: Each page and component is self-contained
- **Scalability**: Easy to add new pages, components, and services

## 🧩 Component Hierarchy

### Base Components (No Dependencies)
- `Button` - All button interactions
- `Input` - Form inputs
- `Badge` - Status badges and labels
- `Loader` - Loading indicators
- `ProgressBar` - Progress visualization

### Composite Components
- `Card` - Container for content
- `Modal` - Popups and dialogs
- `Tabs` - Tab navigation
- `PlayerCard` - eFootball-style player display
- `TournamentCard` - Tournament preview

### Page Components
- Each page is a self-contained component
- Pages import and compose components
- Pages manage their own state
- Pages handle navigation

### Layout Components
- `MainLayout` - App-wide layout with navigation
- Wraps all authenticated pages
- Manages sidebar and top navigation

## 📊 State Management

### Local State (useState)
- Used for component-level state
- Form inputs, UI toggles, modals
- No prop drilling needed

### Custom Hooks (useApi)
- Centralized API call handling
- Automatic loading/error states
- Used in pages for data fetching

### Context API (Optional Future)
- For app-wide state (user, auth)
- Can be added without refactoring

### LocalStorage
- Token and user data persistence
- Auth state across page refreshes

## 🗺️ Routing Structure

```
/
├── /login              [Public]
├── /register           [Public]
├── /                   [Protected] Dashboard
├── /tournaments        [Protected] Tournament List
├── /tournaments/create [Protected] Create Tournament
├── /tournaments/:id    [Protected] Tournament Details
├── /match/:id          [Protected] Match View
├── /match/:id/live     [Protected] Live Tracker
├── /auction            [Protected] Auction
├── /leaderboard        [Protected] Leaderboard
├── /missions           [Protected] Missions
├── /clubs              [Protected] Clubs
├── /profile/:id        [Protected] User Profile
└── /*                  [Protected] 404 Page
```

## 🎨 Styling Approach

### Tailwind Utility Classes
```jsx
<div className="flex items-center justify-center gap-4 p-6 rounded-lg bg-dark-800">
  Content
</div>
```

### Custom Extensions
- Dark color palette: `dark-50` to `dark-900`
- Neon colors: `neon-blue`, `neon-purple`, `neon-pink`, `neon-green`
- Shadow effects: `shadow-glow`, `shadow-glow-lg`, `shadow-glow-purple`
- Animations: `animate-glow`, `glow-text`

### Component Variants
Each component supports multiple variants:
```jsx
<Button variant="primary" />    // Primary action
<Button variant="secondary" />  // Alternative action
<Button variant="accent" />     // Featured action
<Button variant="ghost" />      // Subtle action
<Button variant="success" />    // Positive action
<Button variant="danger" />     // Destructive action
```

## 🔌 API Integration

### Service Pattern
```javascript
// src/services/api.js
export const tournamentService = {
  getAll: (filters) => apiClient.get('/tournaments', { params: filters }),
  getById: (id) => apiClient.get(`/tournaments/${id}`),
  create: (data) => apiClient.post('/tournaments', data),
  // ...
}
```

### Usage in Components
```jsx
import { useApi } from '../hooks/useApi'
import { tournamentService } from '../services/api'

export function MyComponent() {
  const { data, loading, error, execute } = useApi(tournamentService.getAll)
  
  useEffect(() => {
    execute({ status: 'upcoming' })
  }, [])
  
  if (loading) return <Loader />
  if (error) return <ErrorMessage>{error}</ErrorMessage>
  
  return <TournamentList tournaments={data} />
}
```

### Axios Interceptors
- Automatically adds authentication token
- Handles 401 errors with redirect to login
- Request/response transformation

## ✅ Best Practices

### Component Guidelines
- ✓ Keep components small and focused
- ✓ Use descriptive component names
- ✓ Pass props for reusability
- ✓ Destructure props in function signature
- ✓ Use PropTypes or TypeScript (optional)

### State Management Rules
- ✓ Keep state as local as possible
- ✓ Lift state only when needed
- ✓ Use useCallback for function stability
- ✓ Minimize re-renders with useMemo

### Performance Tips
- ✓ Use React.memo for expensive components
- ✓ Lazy load pages with React.lazy()
- ✓ Debounce input handlers
- ✓ Use Framer Motion sparingly

### Code Organization
```jsx
// Component structure
import ... // imports
import ... // relative imports

// Constants
const CONSTANTS = ...

// Component
export default function MyComponent() {
  // State
  const [state, setState] = useState()
  
  // Effects
  useEffect(() => { ... }, [])
  
  // Handlers
  const handleClick = () => { ... }
  
  // Render
  return (
    <div>
      {/* JSX */}
    </div>
  )
}
```

### Naming Conventions
- Components: PascalCase (e.g., `MyComponent`)
- Variables/Functions: camelCase (e.g., `myVariable`)
- CSS Classes: kebab-case (Tailwind default)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_PLAYERS`)
- Boolean props: prefix with `is` or `has` (e.g., `isLoading`)

## 🚀 Performance Tips

### Code Splitting
Pages are automatically code-split by React Router:
```jsx
<Route path="/tournaments" element={<TournamentListPage />} />
// Automatically lazy-loaded
```

### Image Optimization
- Use placeholder images in demo
- Implement actual image optimization in production
- Use WebP format with fallbacks

### Bundle Analysis
```bash
npm install --save-dev vite-plugin-visualizer
# Add to vite.config.js
```

### Monitoring Performance
```jsx
// Use React DevTools Profiler
// Run performance tests in build mode
npm run build
npm run preview
```

## 🔒 Security Best Practices

- ✓ Token stored in localStorage (production: httpOnly cookies)
- ✓ CORS configured on backend
- ✓ Input validation on frontend and backend
- ✓ Secure API endpoints with authentication
- ✓ XSS protection with React's built-in escaping
- ✓ CSRF tokens for state-changing operations

## 📱 Responsive Design

### Breakpoints (Tailwind)
- `sm`: 640px - Tablets
- `md`: 768px - Small laptops
- `lg`: 1024px - Desktops
- `xl`: 1280px - Large screens

### Current Implementation
- Mobile-first approach
- Hidden sidebar on mobile (`hidden lg:flex`)
- Responsive grid layouts
- Touch-friendly button sizes

## 🐛 Debugging Tools

### Browser DevTools
- React DevTools extension
- Framer Motion DevTools
- Network tab for API calls
- Console for errors

### Local Development
```bash
# Run with source maps
npm run dev

# Build and preview
npm run build && npm run preview
```

## 📚 Additional Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [Framer Motion Documentation](https://www.framer.com/motion)
- [React Router Documentation](https://reactrouter.com)
- [Axios Documentation](https://axios-http.com)

## 📞 Common Issues & Solutions

### Styles not applying
1. Check Tailwind content paths
2. Verify class names are correct
3. Clear browser cache
4. Rebuild CSS: `npm run dev`

### API calls failing
1. Check backend is running
2. Verify VITE_API_URL in .env
3. Check browser console for CORS errors
4. Verify request payload in Network tab

### Components not rendering
1. Check import paths (relative vs absolute)
2. Verify component name exports
3. Check React DevTools for errors
4. Look for console errors

### Performance issues
1. Profile with React DevTools
2. Check for unnecessary re-renders
3. Optimize images
4. Reduce animation complexity

---

**Created for PES Esports Tournament Platform**
