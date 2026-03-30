import { motion } from 'framer-motion'

export default function Input({
  type = 'text',
  placeholder = '',
  label = '',
  error = '',
  value = '',
  onChange = () => {},
  className = '',
  required = false,
  icon = null,
  ...props
}) {
  return (
    <div className="w-full">
      {label && (
        <motion.label 
          className="block text-sm font-semibold text-gray-300 mb-2 drop-shadow-lg"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {label}
          {required && <span className="text-neon-pink ml-1">*</span>}
        </motion.label>
      )}
      <motion.div
        className="relative"
        whileFocus={{ scale: 1.02 }}
      >
        {icon && (
          <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-neon-blue text-lg z-10">
            {icon}
          </div>
        )}
        <input
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          className={`
            w-full px-4 py-3.5 rounded-lg
            bg-dark-900/50 backdrop-blur-sm
            border-2 border-dark-700/50 focus:border-neon-blue
            text-white placeholder-gray-500
            transition-smooth focus:outline-none focus:ring-2 focus:ring-neon-blue/30
            focus:shadow-glow hover:border-dark-600
            ${icon ? 'pl-10' : ''}
            ${error ? 'border-neon-pink focus:ring-neon-pink/30 focus:border-neon-pink' : ''}
            ${className}
          `}
          {...props}
        />
        
        {/* Neon glow effect on focus */}
        <motion.div
          className="absolute inset-0 rounded-lg pointer-events-none"
          initial={{ boxShadow: '0 0 0 rgba(0, 240, 255, 0)' }}
          whileFocus={{ 
            boxShadow: '0 0 20px rgba(0, 240, 255, 0.2), inset 0 0 10px rgba(0, 240, 255, 0.05)'
          }}
          transition={{ duration: 0.3 }}
        />
      </motion.div>
      {error && (
        <motion.p 
          className="text-neon-pink text-sm mt-2 font-semibold drop-shadow-lg"
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
        >
          ⚠ {error}
        </motion.p>
      )}
    </div>
  )
}
