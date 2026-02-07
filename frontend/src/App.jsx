import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Header from './components/Header'
import NewsInput from './components/NewsInput'
import VerdictCard from './components/VerdictCard'
import LoadingSpinner from './components/LoadingSpinner'
import axios from 'axios'

// API URL - uses environment variable in production, proxy in development
const API_URL = import.meta.env.VITE_API_URL || ''

function App() {
  const [claim, setClaim] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleVerify = async () => {
    if (!claim.trim() || claim.length < 5) {
      setError('Please enter a valid claim (at least 5 characters)')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post(`${API_URL}/api/verify`, { claim })
      setResult(response.data)
    } catch (err) {
      console.error('Verification error:', err)
      setError(err.response?.data?.detail || 'Failed to verify the claim. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <Header />
      
      <main className="main-content">
        <motion.div 
          className="hero"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="hero-title">
            Verify News with <span>AI-Powered</span> Fact Checking
          </h1>
          <p className="hero-subtitle">
            Enter a news headline, claim, or statement below to check its authenticity 
            using trusted sources and AI verification.
          </p>
        </motion.div>

        <NewsInput 
          value={claim}
          onChange={setClaim}
          onSubmit={handleVerify}
          loading={loading}
        />

        <AnimatePresence mode="wait">
          {loading && (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <LoadingSpinner />
            </motion.div>
          )}

          {error && !loading && (
            <motion.div
              key="error"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="error-card"
            >
              <div className="error-icon">⚠️</div>
              <h3 className="error-title">Verification Failed</h3>
              <p className="error-message">{error}</p>
            </motion.div>
          )}

          {result && !loading && (
            <motion.div
              key="result"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <VerdictCard result={result} />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <footer className="footer">
        <p className="footer-text">
          Powered by <span>AI</span> • Always verify with multiple sources
        </p>
      </footer>
    </div>
  )
}

export default App
