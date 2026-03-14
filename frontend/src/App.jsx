import { Routes, Route } from 'react-router-dom'
import './App.css'
import Home from './pages/Home.jsx'
import Results from './pages/Results.jsx'

function App() {
  return (
    <div className="app-container">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </div>
  )
}

export default App
