import { motion } from 'framer-motion'
import SourcesList from './SourcesList'

function VerdictCard({ result }) {
  const getVerdictClass = (verdict) => {
    switch (verdict?.toUpperCase()) {
      case 'REAL':
        return 'real'
      case 'FAKE':
        return 'fake'
      case 'PARTIALLY TRUE':
        return 'partial'
      default:
        return 'unverified'
    }
  }

  const getVerdictIcon = (verdict) => {
    switch (verdict?.toUpperCase()) {
      case 'REAL':
        return '✅'
      case 'FAKE':
        return '❌'
      case 'PARTIALLY TRUE':
        return '⚠️'
      default:
        return '❓'
    }
  }

  const verdictClass = getVerdictClass(result.verdict)
  const confidencePercent = Math.round((result.confidence_score || 0) * 100)

  return (
    <motion.div 
      className="result-section"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="result-card">
        {/* Verdict Header */}
        <div className="verdict-header">
          <motion.div 
            className={`verdict-badge ${verdictClass}`}
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <span className="verdict-icon">{getVerdictIcon(result.verdict)}</span>
            {result.verdict}
          </motion.div>
          
          <div className="confidence-section">
            <span className="confidence-label">Confidence Score</span>
            <div className="confidence-bar-wrapper">
              <div className="confidence-bar">
                <motion.div 
                  className="confidence-fill"
                  initial={{ width: 0 }}
                  animate={{ width: `${confidencePercent}%` }}
                  transition={{ duration: 0.8, delay: 0.3 }}
                />
              </div>
              <span className="confidence-value">{confidencePercent}%</span>
            </div>
          </div>
        </div>

        {/* Result Body */}
        <div className="result-body">
          {/* Summary */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h3 className="result-section-title">Summary</h3>
            <p className="summary-text">{result.summary}</p>
          </motion.div>

          {/* Facts Grid */}
          <motion.div 
            className="facts-section"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <div className="facts-grid">
              {/* Verified Facts */}
              {result.verified_facts && result.verified_facts.length > 0 && (
                <div className="facts-card">
                  <h4 className="facts-card-title verified">
                    <span>✓</span> Verified Facts
                  </h4>
                  <ul className="facts-list">
                    {result.verified_facts.map((fact, index) => (
                      <li key={index}>{fact}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Misleading Parts */}
              {result.incorrect_or_misleading_parts && result.incorrect_or_misleading_parts.length > 0 && (
                <div className="facts-card">
                  <h4 className="facts-card-title misleading">
                    <span>✗</span> Incorrect or Misleading
                  </h4>
                  <ul className="facts-list">
                    {result.incorrect_or_misleading_parts.map((part, index) => (
                      <li key={index}>{part}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </motion.div>

          {/* Verification Date */}
          <motion.p 
            className="result-section-title"
            style={{ marginTop: '1rem', textAlign: 'right' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            Verified: {result.last_verified_date}
          </motion.p>
        </div>

        {/* Sources Section */}
        {result.trusted_sources && result.trusted_sources.length > 0 && (
          <SourcesList sources={result.trusted_sources} />
        )}
      </div>
    </motion.div>
  )
}

export default VerdictCard
