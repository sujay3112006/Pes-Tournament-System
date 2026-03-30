import { motion } from 'framer-motion'

export default function Loader({ size = 'md', message = 'Loading...', variant = 'default' }) {
  const sizes = {
    sm: 'w-6 h-6',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
    xl: 'w-24 h-24',
  }

  return (
    <div className="flex flex-col items-center justify-center gap-4">
      {variant === 'default' && (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          className={`${sizes[size]} border-4 border-dark-700 border-t-neon-blue border-r-neon-purple rounded-full shadow-glow`}
        />
      )}

      {variant === 'gamer' && (
        <div className={`${sizes[size]} relative`}>
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
            className="w-full h-full border-4 border-transparent border-t-neon-blue border-r-neon-cyan rounded-full shadow-glow-lg"
          />
          <motion.div
            animate={{ rotate: -360 }}
            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
            className="absolute inset-0 border-4 border-transparent border-b-neon-purple border-l-neon-pink rounded-full"
          />
        </div>
      )}

      {variant === 'pulse' && (
        <motion.div
          animate={{
            scale: [1, 1.1, 1],
            boxShadow: [
              '0 0 0 0 rgba(0, 240, 255, 0.7)',
              '0 0 0 15px rgba(0, 240, 255, 0)',
            ],
          }}
          transition={{ duration: 1.5, repeat: Infinity }}
          className={`${sizes[size]} rounded-full bg-neon-blue/20 border-2 border-neon-blue`}
        />
      )}

      {message && (
        <motion.p 
          className="text-neon-blue text-sm font-semibold drop-shadow-lg glow-text"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {message}
        </motion.p>
      )}
    </div>
  )
}
