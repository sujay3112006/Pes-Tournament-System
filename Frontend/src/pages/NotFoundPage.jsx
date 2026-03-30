import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'

export default function NotFoundPage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen flex items-center justify-center bg-dark-900">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <Card variant="glow" className="max-w-md">
          <div className="p-8">
            <div className="text-6xl mb-4">🏚️</div>
            <h1 className="text-4xl font-bold text-white mb-2">404 - Not Found</h1>
            <p className="text-gray-400 mb-8">The page you're looking for doesn't exist.</p>
            <div className="flex gap-4">
              <Button
                variant="primary"
                size="lg"
                className="flex-1"
                onClick={() => navigate('/')}
              >
                Home
              </Button>
              <Button
                variant="secondary"
                size="lg"
                className="flex-1"
                onClick={() => navigate(-1)}
              >
                Back
              </Button>
            </div>
          </div>
        </Card>
      </motion.div>
    </div>
  )
}
