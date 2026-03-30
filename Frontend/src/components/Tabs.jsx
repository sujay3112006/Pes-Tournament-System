import { motion } from 'framer-motion'

export default function Tabs({ tabs, activeTab, onTabChange }) {
  return (
    <div className="flex gap-2 mb-6 border-b border-neon-blue/20 pb-0 overflow-x-auto backdrop-blur-sm">
      {tabs.map((tab, index) => (
        <motion.button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={`
            px-4 py-3 font-semibold whitespace-nowrap transition-smooth relative
            ${activeTab === tab.id
              ? 'text-neon-blue drop-shadow-lg'
              : 'text-gray-400 hover:text-gray-200'
            }
          `}
          whileHover={{ y: -2 }}
          whileTap={{ scale: 0.98 }}
        >
          {tab.label}
          {activeTab === tab.id && (
            <motion.div 
              layoutId="activeTab"
              initial={{ opacity: 0, scaleX: 0 }}
              animate={{ opacity: 1, scaleX: 1 }}
              exit={{ opacity: 0, scaleX: 0 }}
              transition={{ type: 'spring', damping: 20, stiffness: 300 }}
              className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-neon-blue to-neon-cyan shadow-glow-md" 
            />
          )}
        </motion.button>
      ))}
    </div>
  )
}
