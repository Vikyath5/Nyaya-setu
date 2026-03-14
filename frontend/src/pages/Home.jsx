import { useState, useRef, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTheme } from '../context/ThemeContext.jsx'
import { analyzeCase } from '../services/api.js'
import './Home.css'

const LOADING_MESSAGES = [
  'Cross-referencing BNS guidelines...',
  'Mapping applicable judicial precedents...',
  'Calculating case viability probabilities...',
  'Analyzing outcome simulations...',
]

function SunIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="5" />
      <line x1="12" y1="1" x2="12" y2="3" />
      <line x1="12" y1="21" x2="12" y2="23" />
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
      <line x1="1" y1="12" x2="3" y2="12" />
      <line x1="21" y1="12" x2="23" y2="12" />
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
    </svg>
  )
}

function MoonIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </svg>
  )
}

function MicIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
      <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
      <line x1="12" y1="19" x2="12" y2="23" />
      <line x1="8" y1="23" x2="16" y2="23" />
    </svg>
  )
}

function ScaleIcon() {
  return (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 3v18" />
      <path d="M5 7l7-4 7 4" />
      <path d="M2 14l3-7 3 7a4.2 4.2 0 0 1-6 0z" />
      <path d="M16 14l3-7 3 7a4.2 4.2 0 0 1-6 0z" />
    </svg>
  )
}

function ArrowIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>
  )
}

function UploadIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="17 8 12 3 7 8" />
      <line x1="12" y1="3" x2="12" y2="15" />
    </svg>
  )
}

function CloseIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  )
}

export default function Home() {
  const { theme, toggleTheme } = useTheme()
  const navigate = useNavigate()
  const textareaRef = useRef(null)
  const fileInputRef = useRef(null)

  const [query, setQuery] = useState('')
  const [files, setFiles] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [loadingMsgIndex, setLoadingMsgIndex] = useState(0)
  const [error, setError] = useState(null)

  // Auto-expand textarea
  const handleInput = useCallback((e) => {
    setQuery(e.target.value)
    const ta = e.target
    ta.style.height = 'auto'
    ta.style.height = Math.min(ta.scrollHeight, 240) + 'px'
  }, [])

  // File upload handler
  const handleFileChange = useCallback((e) => {
    const newFiles = Array.from(e.target.files)
    setFiles(prev => [...prev, ...newFiles])
  }, [])

  const removeFile = useCallback((index) => {
    setFiles(prev => prev.filter((_, i) => i !== index))
  }, [])

  // Loading message cycling
  useEffect(() => {
    if (!isLoading) return
    const timer = setInterval(() => {
      setLoadingMsgIndex(prev => {
        if (prev >= LOADING_MESSAGES.length - 1) return 0
        return prev + 1
      })
    }, 1400)
    return () => clearInterval(timer)
  }, [isLoading])

  const handleSubmit = async () => {
    if (!query.trim()) return
    setIsLoading(true)
    setLoadingMsgIndex(0)
    setError(null)

    try {
      const results = await analyzeCase(query, files)
      // Navigate to results with data
      navigate('/results', { state: { results, query } })
    } catch (err) {
      console.error('Analysis error:', err)
      setError(
        err.response?.data?.detail ||
        err.message === 'Network Error'
          ? 'Cannot connect to server. Please ensure the backend is running on http://localhost:8000'
          : `Analysis failed: ${err.message}`
      )
      setIsLoading(false)
    }
  }

  return (
    <div className="home-page">
      {/* Nav */}
      <nav className="nav-bar">
        <a href="/" className="nav-logo">
          <span className="nav-logo-icon">
            <ScaleIcon />
          </span>
          <span className="nav-logo-text">Nyaya<span>Setu</span></span>
        </a>
        <div className="nav-links-desktop">
          <a href="#how-it-works" className="nav-link">How It Works</a>
          <a href="#features" className="nav-link">Features</a>
          <button className="nav-link" onClick={() => { document.getElementById('legal-query-input')?.focus() }}>Analyze Case</button>
        </div>
        <div className="nav-actions">
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
            id="theme-toggle-home"
          >
            <span className="theme-toggle-knob">
              {theme === 'light' ? <SunIcon /> : <MoonIcon />}
            </span>
          </button>
          <button
            className="btn btn-primary btn-sm nav-cta"
            onClick={() => { document.getElementById('legal-query-input')?.focus() }}
            id="nav-get-started"
          >
            Get Started
          </button>
        </div>
      </nav>

      {/* Hero */}
      <section className="hero-section" id="hero">
        <div className="hero-content stagger-in">
          <h1 className="hero-title">AI-Powered Legal Guidance<br/>for Everyone</h1>
          <p className="hero-subtitle">
            Describe your legal situation in plain language. Our AI cross-references
            Indian judicial precedents, BNS guidelines, and outcome data to give you
            actionable intelligence.
          </p>
          <div className="hero-buttons">
            <button className="btn btn-primary btn-lg" onClick={() => { document.getElementById('legal-query-input')?.focus() }}>
              Analyze My Case
              <ArrowIcon />
            </button>
            <a href="#how-it-works" className="btn btn-secondary btn-lg">Learn More</a>
          </div>
        </div>
      </section>

      {/* Main content */}
      <main className="home-main" id="analyze">
        <div className={`intake-card glass-card ${isLoading ? 'intake-card--loading' : ''}`}>
          {!isLoading ? (
            <>
              {/* Header */}
              <div className="intake-header stagger-in">
                <h2 className="intake-title">Clarity Before the Courtroom.</h2>
                <p className="intake-subtitle">
                  Describe your legal situation below. Our AI will analyze your case
                  across multiple dimensions and provide comprehensive insights.
                </p>
              </div>

              {/* Error Message */}
              {error && (
                <div className="error-banner stagger-in" id="error-banner">
                  <span className="error-icon">⚠</span>
                  <span>{error}</span>
                  <button className="error-close" onClick={() => setError(null)} aria-label="Dismiss error">
                    <CloseIcon />
                  </button>
                </div>
              )}

              {/* Text Input */}
              <div className="intake-input-wrap stagger-in">
                <textarea
                  ref={textareaRef}
                  className="intake-textarea"
                  placeholder="e.g., My employer hasn't paid my salary for 3 months despite multiple written reminders..."
                  value={query}
                  onChange={handleInput}
                  rows={3}
                  id="legal-query-input"
                />
                <button
                  className="mic-btn"
                  aria-label="Speak your query"
                  title="Speak in your language (Hindi, Tamil, etc.)"
                  id="mic-button"
                >
                  <MicIcon />
                  <span className="mic-label">Speak in your language</span>
                </button>
              </div>

              {/* File Upload */}
              <div className="intake-docs stagger-in">
                <p className="intake-docs-label">Attach supporting documents (optional)</p>
                <div className="file-upload-zone" onClick={() => fileInputRef.current?.click()}>
                  <UploadIcon />
                  <span>Click to upload PDF, JPG, or PNG files</span>
                  <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
                    onChange={handleFileChange}
                    className="file-input-hidden"
                    id="file-upload-input"
                  />
                </div>
                {files.length > 0 && (
                  <div className="uploaded-files">
                    {files.map((file, index) => (
                      <div key={index} className="uploaded-file-tag">
                        <span className="file-tag-name">{file.name}</span>
                        <button
                          className="file-tag-remove"
                          onClick={(e) => { e.stopPropagation(); removeFile(index) }}
                          aria-label={`Remove ${file.name}`}
                        >
                          <CloseIcon />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* CTA */}
              <div className="intake-cta stagger-in">
                <button
                  className="btn btn-primary btn-lg intake-submit"
                  onClick={handleSubmit}
                  disabled={!query.trim()}
                  id="analyze-btn"
                >
                  Analyze Judicial Precedents
                  <ArrowIcon />
                </button>
              </div>
            </>
          ) : (
            /* Loading State */
            <div className="intake-loading">
              <div className="loading-spinner-wrap">
                <div className="loading-spinner" />
              </div>
              <p className="loading-heading">Analyzing your legal case...</p>
              <div className="loading-bars">
                <div className="loading-bar skeleton" style={{ width: '80%', height: '14px' }} />
                <div className="loading-bar skeleton" style={{ width: '60%', height: '14px', animationDelay: '200ms' }} />
                <div className="loading-bar skeleton" style={{ width: '90%', height: '14px', animationDelay: '400ms' }} />
                <div className="loading-bar skeleton" style={{ width: '45%', height: '14px', animationDelay: '600ms' }} />
              </div>
              <p className="loading-msg" key={loadingMsgIndex}>
                {LOADING_MESSAGES[loadingMsgIndex]}
              </p>
              <div className="loading-dots">
                <span /><span /><span />
              </div>
            </div>
          )}
        </div>

        {/* How It Works Section */}
        <section className="how-it-works" id="how-it-works">
          <h2 className="section-title stagger-in">How It Works</h2>
          <div className="steps-grid">
            <div className="step-card glass-card stagger-in">
              <div className="step-number">01</div>
              <h3>Describe Your Case</h3>
              <p>Write your legal situation in plain language — any language works.</p>
            </div>
            <div className="step-card glass-card stagger-in">
              <div className="step-number">02</div>
              <h3>AI Analysis</h3>
              <p>Our AI cross-references BNS guidelines, precedents, and outcome data.</p>
            </div>
            <div className="step-card glass-card stagger-in">
              <div className="step-number">03</div>
              <h3>Get Insights</h3>
              <p>Receive case strength, timeline, outcomes, and a document checklist.</p>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="features-section" id="features">
          <h2 className="section-title stagger-in">Features</h2>
          <div className="features-grid">
            <div className="feature-card glass-card stagger-in">
              <div className="feature-icon">⚖</div>
              <h3>Case Strength Analysis</h3>
              <p>AI evaluates your case viability with strengths and weaknesses.</p>
            </div>
            <div className="feature-card glass-card stagger-in">
              <div className="feature-icon">📊</div>
              <h3>Outcome Prediction</h3>
              <p>Data-driven predictions of settlement, win, or dismissal probability.</p>
            </div>
            <div className="feature-card glass-card stagger-in">
              <div className="feature-icon">📅</div>
              <h3>Timeline Estimation</h3>
              <p>Stage-by-stage judicial timeline based on case type.</p>
            </div>
            <div className="feature-card glass-card stagger-in">
              <div className="feature-icon">🔍</div>
              <h3>Precedent Engine</h3>
              <p>Find similar past cases with matching percentages.</p>
            </div>
            <div className="feature-card glass-card stagger-in">
              <div className="feature-icon">📋</div>
              <h3>Document Checklist</h3>
              <p>Auto-generated required documents list with downloadable PDF.</p>
            </div>
            <div className="feature-card glass-card stagger-in">
              <div className="feature-icon">💡</div>
              <h3>Legal Explanation</h3>
              <p>Plain-language breakdown of applicable laws and relief options.</p>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="home-footer stagger-in">
          <p>Built for the people of India. Powered by judicial data & AI.</p>
        </footer>
      </main>
    </div>
  )
}
