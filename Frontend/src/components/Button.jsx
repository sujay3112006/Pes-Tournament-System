import { motion } from 'framer-motion'

export default function Button({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  onClick = () => {}, 
  className = '',
  disabled = false,
  isLoading = false,
  glow = true,
  ...props 
}) {
  const baseStyles = 'font-semibold font-display rounded-xl transition-smooth focus:outline-none focus:ring-2 relative overflow-hidden'
  
  const variants = {
    primary: `
      bg-gradient-to-r from-neon-blue via-cyan-400 to-neon-purple
      hover:shadow-glow-lg hover:shadow-cyan-500/50
      text-dark-900 font-bold border border-neon-blue/50
      ${glow ? 'btn-glow' : ''}
    `,
    secondary: `
      bg-transparent border-2 border-neon-blue text-neon-blue
      hover:bg-neon-blue/10 hover:shadow-glow
      ${glow ? 'btn-glow' : ''}
    `,
    accent: `
      bg-gradient-to-r from-neon-purple to-pink-500
      hover:shadow-glow-pink text-white border border-neon-purple/50
      ${glow ? 'btn-glow' : ''}
    `,
    ghost: `
      text-neon-blue hover:bg-neon-blue/10 border border-neon-blue/30
      hover:border-neon-blue/60 hover:shadow-glow
    `,
    success: `
      bg-gradient-to-r from-emerald-600 to-emerald-500
      hover:shadow-emerald-500/50 text-white border border-emerald-400/50
      ${glow ? 'btn-glow' : ''}
    `,
    danger: `
      bg-gradient-to-r from-red-600 to-red-500
      hover:shadow-red-500/50 text-white border border-red-400/50
      ${glow ? 'btn-glow' : ''}
    `,
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-5 py-2.5 text-base',
    lg: 'px-7 py-3.5 text-lg',
    xl: 'px-10 py-4 text-xl',
  }

  return (
    <motion.button
      whileHover={{ scale: disabled ? 1 : 1.05 }}
      whileTap={{ scale: disabled ? 1 : 0.95 }}
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'} ${className}`}
      onClick={onClick}
      disabled={disabled || isLoading}
      {...props}
    >
      {/* Shimmer effect */}
      <motion.div
        className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
        animate={{
          x: ['100%', '-100%'],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          repeatDelay: 1,
        }}
        style={{ pointerEvents: 'none' }}
      />
      
      {isLoading ? (
        <span className="flex items-center justify-center">
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Loading...
        </span>
      ) : (
        <span className="relative z-10 flex items-center justify-center">{children}</span>
      )}
    </motion.button>
  )
}
