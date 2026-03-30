import { motion } from 'framer-motion'

export default function Card({ 
  children, 
  className = '', 
  hover = true,
  glowing = false,
  variant = 'default',
  animate = true,
  ...props 
}) {
  const baseStyles = 'rounded-xl overflow-hidden transition-smooth'
  
  const variants = {
    default: 'glassmorphism-thick',
    dark: 'bg-dark-900/40 border border-dark-700/50 backdrop-blur-sm',
    elevated: 'bg-dark-900/60 border border-neon-blue/20 shadow-gaming backdrop-blur-lg',
    glow: 'bg-dark-900/50 border border-neon-blue/40 shadow-gaming backdrop-blur-lg neon-glow-md',
    premium: 'bg-gradient-to-br from-dark-900/80 via-dark-950/60 to-dark-900/80 border-2 border-transparent bg-clip-padding backdrop-blur-xl',
  }

  // Premium variant gets gradient border effect
  const isPremium = variant === 'premium'
  const borderStyle = isPremium ? {
    backgroundImage: 'linear-gradient(135deg, #00f0ff, #7a00ff)',
    backgroundOrigin: 'border-box',
    WebkitBackgroundClip: 'padding-box',
  } : {}

  return (
    <motion.div
      whileHover={hover && animate ? { 
        y: -6,
        boxShadow: '0 20px 60px rgba(0, 240, 255, 0.2)',
      } : {}}
      whileTap={hover && animate ? { scale: 0.98 } : {}}
      className={`${baseStyles} ${variants[variant]} ${glowing ? 'neon-glow-md' : ''} ${className}`}
      style={borderStyle}
      {...props}
    >
      {children}
    </motion.div>
  )
}
