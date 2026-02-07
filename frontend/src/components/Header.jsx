import { motion } from 'framer-motion'

function Header() {
  return (
    <motion.header 
      className="header"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <div className="header-content">
        <div className="logo">
          <div className="logo-icon">✓</div>
          <span className="logo-text">FactCheck AI</span>
        </div>
        <div className="header-badge">Beta Version</div>
      </div>
    </motion.header>
  )
}

export default Header
