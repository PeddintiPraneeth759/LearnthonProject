import { motion } from 'framer-motion'

function NewsInput({ value, onChange, onSubmit, loading }) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      onSubmit()
    }
  }

  return (
    <motion.div 
      className="input-section"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      <div className="input-card">
        <label className="input-label" htmlFor="claim-input">
          Enter News Claim to Verify
        </label>
        <textarea
          id="claim-input"
          className="input-textarea"
          placeholder="Paste a news headline, paragraph, or claim here...

Example: 'Scientists discover water on Mars' or 'New study claims coffee cures all diseases'"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <div className="input-footer">
          <span className="char-count">
            {value.length} characters • Press Ctrl+Enter to verify
          </span>
          <motion.button
            className="btn-primary"
            onClick={onSubmit}
            disabled={loading || value.length < 5}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
  
            {loading ? 'Verifying...' : 'Verify Claim'}
          </motion.button>
        </div>
      </div>
    </motion.div>
  )
}

export default NewsInput
