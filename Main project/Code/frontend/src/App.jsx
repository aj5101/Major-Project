import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import VideoUploadPage from './pages/VideoUploadPage'
import VideoResultPage from './pages/VideoResultPage'
import AdminPage from './pages/AdminPage'
import Navbar from './components/Navbar'
import CreateLesson from './pages/CreateLesson'
import Vocabulary from './pages/Vocabulary'
import { ErrorBoundary } from './components/ErrorBoundary'

/**
 * Main App Component
 * 
 * Sets up routing and navigation for the application.
 * Provides accessible navigation for hearing-impaired children.
 */
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-fun-purple-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <ErrorBoundary>
          <Routes>
            <Route path="/" element={<HomePage />} />
            {/* Classroom flow */}
            <Route path="/create-lesson" element={<CreateLesson />} />
            <Route path="/vocabulary" element={<Vocabulary />} />

            {/* Backward-compatible routes (keep working functionality) */}
            <Route path="/upload" element={<VideoUploadPage />} />
            <Route path="/video/:videoId" element={<VideoResultPage />} />
            <Route path="/lesson/:videoId" element={<VideoResultPage />} />
            <Route path="/admin" element={<AdminPage />} />
          </Routes>
          </ErrorBoundary>
        </main>
      </div>
    </Router>
  )
}

export default App

