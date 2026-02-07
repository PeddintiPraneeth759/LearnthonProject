import { motion } from 'framer-motion'

function SourcesList({ sources }) {
  if (!sources || sources.length === 0) return null

  return (
    <motion.div 
      className="sources-section"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.5 }}
    >
      <h3 className="result-section-title">Trusted Sources</h3>
      <div className="sources-grid">
        {sources.map((source, index) => (
          <motion.a
            key={index}
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="source-card"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 + index * 0.1 }}
            whileHover={{ scale: 1.01 }}
          >
            <div className="source-icon">📰</div>
            <div className="source-info">
              <div className="source-title">{source.title}</div>
              <div className="source-publisher">{source.publisher}</div>
            </div>
            <span className="source-arrow">→</span>
          </motion.a>
        ))}
      </div>
    </motion.div>
  )
}

export default SourcesList
