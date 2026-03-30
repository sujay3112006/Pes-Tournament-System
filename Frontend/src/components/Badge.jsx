import { motion } from 'framer-motion'

export default function Badge({ children, variant = 'default', size = 'md', animated = true }) {
  const variants = {
    default: 'bg-dark-800/60 text-gray-300 border border-dark-700/50',
    primary: 'bg-neon-blue/15 text-neon-blue border border-neon-blue/50 shadow-glow',
    success: 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/50 shadow-glow',
    warning: 'bg-yellow-500/15 text-yellow-400 border border-yellow-500/50 shadow-glow',
    danger: 'bg-neon-pink/15 text-neon-pink border border-neon-pink/50 shadow-glow-pink',
    purple: 'bg-neon-purple/15 text-neon-purple border border-neon-purple/50 shadow-glow-purple',
    status: 'bg-gradient-to-r from-neon-blue/20 to-neon-purple/20 text-neon-blue border border-neon-blue/30 shadow-glow',
  }

  const sizes = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1.5 text-sm',
    lg: 'px-4 py-2 text-base',
  }

  return (
    <motion.span
      whileHover={animated ? { scale: 1.08 } : {}}
      className={`inline-block rounded-full font-semibold transition-smooth ${variants[variant]} ${sizes[size]}`}
    >
      {children}
    </motion.span>
  )
}
