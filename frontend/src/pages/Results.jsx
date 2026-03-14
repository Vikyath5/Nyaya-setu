import { useTheme } from '../context/ThemeContext.jsx'
import { useNavigate, useLocation } from 'react-router-dom'
import { useEffect } from 'react'
import { getChecklistDownloadUrl } from '../services/api.js'
import './Results.css'

/* ─── SVG Icons ─────────────────────────────────────────── */
function SunIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="5" />
      <line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" />
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
      <line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" />
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
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

function ScaleIcon() {
  return (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 3v18" /><path d="M5 7l7-4 7 4" />
      <path d="M2 14l3-7 3 7a4.2 4.2 0 0 1-6 0z" />
      <path d="M16 14l3-7 3 7a4.2 4.2 0 0 1-6 0z" />
    </svg>
  )
}

function DownloadIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="7 10 12 15 17 10" />
      <line x1="12" y1="15" x2="12" y2="3" />
    </svg>
  )
}

function CheckIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  )
}

function AlertIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  )
}

function BackIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="19" y1="12" x2="5" y2="12" /><polyline points="12 19 5 12 12 5" />
    </svg>
  )
}

/* ─── Half-Donut Chart ──────────────────────────────────── */
function HalfDonut({ percentage = 50 }) {
  const radius = 70
  const circumference = Math.PI * radius
  const offset = circumference - (percentage / 100) * circumference

  return (
    <div className="donut-wrap">
      <svg viewBox="0 0 180 100" className="donut-svg">
        <path
          d="M 10 90 A 70 70 0 0 1 170 90"
          fill="none"
          stroke="var(--donut-track)"
          strokeWidth="14"
          strokeLinecap="round"
        />
        <path
          d="M 10 90 A 70 70 0 0 1 170 90"
          fill="none"
          stroke="var(--accent-primary)"
          strokeWidth="14"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="donut-value"
        />
      </svg>
      <div className="donut-label">
        <span className="donut-pct">{percentage}%</span>
        <span className="donut-sub">Viability</span>
      </div>
    </div>
  )
}

/* ─── Timeline ──────────────────────────────────────────── */
function Timeline({ nodes = [] }) {
  const fadedNodes = [
    { label: 'Evidence', time: 'Timeline unpredictable' },
    { label: 'Arguments', time: 'Timeline unpredictable' },
    { label: 'Verdict', time: 'Timeline unpredictable' },
  ];

  return (
    <div className="timeline">
      <div className="timeline-track">
        {nodes.map((node, i) => (
          <div key={i} className={`timeline-node ${node.active ? 'timeline-node--active' : ''} ${node.done ? 'timeline-node--done' : ''}`}>
            <span className="timeline-time">{node.time}</span>
            <div className="timeline-dot" />
            <span className="timeline-label">{node.label}</span>
          </div>
        ))}
        
        <div className="timeline-divider">
          <span className="timeline-divider-text">
            Further proceedings depend on court schedules, evidence submission, and legal arguments. The duration of later stages cannot be predicted.
          </span>
        </div>

        {fadedNodes.map((node, i) => (
          <div key={`faded-${i}`} className="timeline-node timeline-node--faded" title="Timeline unpredictable">
            <span className="timeline-time">{node.time}</span>
            <div className="timeline-dot" />
            <span className="timeline-label">{node.label}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

/* ─── Progress Bar ──────────────────────────────────────── */
function ProgressBar({ label, value, color }) {
  return (
    <div className="progress-item">
      <div className="progress-header">
        <span className="progress-label">{label}</span>
        <span className="progress-value">{value}%</span>
      </div>
      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${value}%`, background: color }} />
      </div>
    </div>
  )
}

/* ─── Checklist Item ────────────────────────────────────── */
function ChecklistItem({ label, required }) {
  return (
    <div className={`checklist-item ${required ? 'checklist-item--required' : ''}`}>
      <div className={`checklist-icon ${required ? 'checklist-icon--missing' : 'checklist-icon--done'}`}>
        {required ? <AlertIcon /> : <CheckIcon />}
      </div>
      <span className="checklist-label">{label}</span>
      <span className={`checklist-tag ${required ? '' : 'checklist-tag--done'}`}>
        {required ? 'Required' : 'Recommended'}
      </span>
    </div>
  )
}

/* ─── Case Card ─────────────────────────────────────────── */
function CaseCard({ title, citation, match, delay }) {
  return (
    <div className="case-card stagger-in" style={{ animationDelay: `${delay}ms` }}>
      <div className="case-card-top">
        <h4 className="case-card-title">{title}</h4>
        <span className="match-badge">{match}% Match</span>
      </div>
      <p className="case-card-citation">{citation}</p>
      <span className="bns-badge">✓ Updated to BNS Guidelines</span>
    </div>
  )
}

/* ═══════════════════════════════════════════════════════════
   Main Results Page
   ═══════════════════════════════════════════════════════════ */
export default function Results() {
  const { theme, toggleTheme } = useTheme()
  const navigate = useNavigate()
  const location = useLocation()

  // Get results from navigation state
  const { results, query } = location.state || {}

  // Redirect to home if no results
  useEffect(() => {
    if (!results) {
      navigate('/')
    }
  }, [results, navigate])

  if (!results) return null

  // Destructure API response
  const {
    case_strength,
    predicted_outcome,
    estimated_timeline,
    similar_cases,
    legal_explanation,
    required_documents,
    checklist_pdf,
  } = results

  const handleDownloadPdf = () => {
    if (checklist_pdf) {
      window.open(getChecklistDownloadUrl(checklist_pdf), '_blank')
    }
  }

  return (
    <div className="results-page">
      {/* ─── Top Action Bar ─────────────────────────────── */}
      <nav className="nav-bar">
        <div className="nav-left">
          <button className="nav-back" onClick={() => navigate('/')} aria-label="Back to home" id="back-btn">
            <BackIcon />
          </button>
          <a href="/" className="nav-logo">
            <span className="nav-logo-icon"><ScaleIcon /></span>
            <span className="nav-logo-text">Nyaya<span>Setu</span></span>
          </a>
        </div>
        <div className="nav-actions">
          <button className="theme-toggle" onClick={toggleTheme} aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`} id="theme-toggle-results">
            <span className="theme-toggle-knob">
              {theme === 'light' ? <SunIcon /> : <MoonIcon />}
            </span>
          </button>
          <button className="btn btn-primary" id="download-checklist-btn" onClick={handleDownloadPdf}>
            <DownloadIcon /> Download Checklist
          </button>
          <button className="btn btn-secondary" onClick={() => navigate('/')} id="new-analysis-btn">
            New Analysis
          </button>
        </div>
      </nav>

      {/* ─── Success Banner ──────────────────────────────── */}
      <div className="success-banner stagger-in">
        <span className="success-icon">✓</span>
        <span>Analysis complete — {case_strength?.label || 'Analyzed'} case ({case_strength?.score || 0}% viability)</span>
      </div>

      {/* ─── Bento Grid ─────────────────────────────────── */}
      <main className="bento-grid">

        {/* Bento 1 — Legal Translation */}
        <section className="bento bento-1 glass-card stagger-in" id="bento-legal-translation">
          <div className="bento-header">
            <h2>Legal Translation</h2>
            <span className="status-tag status-tag--info">Detected: {legal_explanation?.detected_type || 'Legal Matter'}</span>
          </div>
          <div className="bento-body">
            <p className="legal-summary">{legal_explanation?.summary || 'Analysis complete.'}</p>
            <div className="legal-points">
              {(legal_explanation?.legal_points || []).map((point, i) => (
                <div className="legal-point" key={i}>
                  <span className="legal-point-marker" style={{ background: i === 0 ? 'var(--semantic-positive)' : 'var(--accent-primary)' }} />
                  <p><strong>{point.title}:</strong> {point.content}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Bento 2 — Case Viability */}
        <section className="bento bento-2 glass-card stagger-in" id="bento-case-viability">
          <div className="bento-header">
            <h2>Case Viability</h2>
          </div>
          <div className="bento-body bento-body--center">
            <HalfDonut percentage={case_strength?.score || 0} />
            <div className="viability-list">
              <div className="viability-group">
                <h4 className="viability-heading viability-heading--pro">Strengths</h4>
                <ul>
                  {(case_strength?.strengths || []).map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </div>
              <div className="viability-group">
                <h4 className="viability-heading viability-heading--con">Weaknesses</h4>
                <ul>
                  {(case_strength?.weaknesses || []).map((w, i) => (
                    <li key={i}>{w}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* Bento 3 — Judicial Timeline */}
        <section className="bento bento-3 glass-card stagger-in" id="bento-timeline">
          <div className="bento-header">
            <h2>Judicial Timeline</h2>
            <span className="status-tag status-tag--accent">
              Estimated Initial Timeline: {estimated_timeline?.duration || 'N/A'} (until first hearing)
            </span>
          </div>
          <div className="bento-body">
            <Timeline nodes={estimated_timeline?.nodes || []} />
          </div>
        </section>

        {/* Bento 4 — Outcome Simulation */}
        <section className="bento bento-4 glass-card stagger-in" id="bento-outcome">
          <div className="bento-header">
            <h2>Outcome Simulation</h2>
          </div>
          <div className="bento-body">
            <div className="outcome-bars">
              {(predicted_outcome?.outcomes || []).map((outcome, i) => (
                <ProgressBar
                  key={i}
                  label={outcome.label}
                  value={outcome.percentage}
                  color={outcome.color}
                />
              ))}
            </div>
            <div className="outcome-callout glass-card">
              <div className="callout-indicator" />
              <div>
                <p className="callout-title">Recommendation</p>
                <p className="callout-text">{predicted_outcome?.recommendation || 'Consult a qualified advocate for personalized advice.'}</p>
              </div>
            </div>
          </div>
        </section>

        {/* Bento 5 — Precedent Engine */}
        <section className="bento bento-5 glass-card stagger-in" id="bento-precedent">
          <div className="bento-header">
            <h2>Precedent Engine</h2>
          </div>
          <div className="bento-body">
            <div className="case-list">
              {(similar_cases || []).map((sc, i) => (
                <CaseCard
                  key={i}
                  title={sc.title}
                  citation={sc.citation}
                  match={sc.match}
                  delay={i * 100 + 100}
                />
              ))}
            </div>
          </div>
        </section>

        {/* Bento 6 — Filing Checklist */}
        <section className="bento bento-6 glass-card stagger-in" id="bento-checklist">
          <div className="bento-header">
            <h2>Filing Checklist</h2>
            <button className="btn btn-primary btn-sm" onClick={handleDownloadPdf} id="download-pdf-btn">
              <DownloadIcon /> Download PDF
            </button>
          </div>
          <div className="bento-body">
            <div className="checklist">
              {(required_documents || []).map((doc, i) => (
                <ChecklistItem
                  key={i}
                  label={doc.name}
                  required={doc.required}
                />
              ))}
            </div>
          </div>
        </section>

      </main>
    </div>
  )
}
