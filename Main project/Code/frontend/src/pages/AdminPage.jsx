import React, { useState, useEffect } from 'react'
import { aslDatasetAPI } from '../services/api'

/**
 * Admin Page Component
 * 
 * Admin panel for managing ASL video dataset.
 * Allows adding, viewing, and deleting ASL videos.
 */
function AdminPage() {
  const [videos, setVideos] = useState([])
  const [loading, setLoading] = useState(true)
  const [showAddForm, setShowAddForm] = useState(false)
  const [newGloss, setNewGloss] = useState('')
  const [newFile, setNewFile] = useState(null)
  const [uploading, setUploading] = useState(false)

  useEffect(() => {
    loadVideos()
  }, [])

  const loadVideos = async () => {
    try {
      const data = await aslDatasetAPI.list(0, 100)
      setVideos(data)
    } catch (error) {
      console.error('Error loading videos:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddVideo = async (e) => {
    e.preventDefault()

    if (!newGloss || !newFile) {
      alert('Please provide both gloss and video file')
      return
    }

    setUploading(true)
    try {
      await aslDatasetAPI.add(newGloss, newFile)
      setNewGloss('')
      setNewFile(null)
      setShowAddForm(false)
      loadVideos()
    } catch (error) {
      alert(`Error: ${error.message}`)
    } finally {
      setUploading(false)
    }
  }

  const handleDelete = async (videoId) => {
    if (!window.confirm('Are you sure you want to delete this ASL video?')) {
      return
    }

    try {
      await aslDatasetAPI.delete(videoId)
      loadVideos()
    } catch (error) {
      alert(`Error: ${error.message}`)
    }
  }

  return (
    <div className="min-h-screen pt-28 pb-20 bg-surface-50">
      <div className="container-main">
        <div className="flex items-center justify-between mb-8 animate-fade-in">
          <div>
            <h1 className="mb-2">Admin Panel</h1>
            <p className="text-primary-600">Manage your ASL video dataset</p>
          </div>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="btn-primary"
          >
            {showAddForm ? 'Cancel' : 'Add ASL Video'}
          </button>
        </div>

        {/* Add Form */}
        {showAddForm && (
          <div className="card mb-8 animate-slide-up bg-brand-50/50 border-brand-100 p-6 md:p-8">
            <h2 className="text-2xl font-bold mb-6 text-brand-800">Add New ASL Video</h2>
            <form onSubmit={handleAddVideo} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="label">
                    ASL Gloss (Sign Name)
                  </label>
                  <input
                    type="text"
                    value={newGloss}
                    onChange={(e) => setNewGloss(e.target.value)}
                    className="input"
                    placeholder="e.g., hello, world, thank-you"
                    required
                  />
                </div>
                <div>
                  <label className="label">
                    Video File
                  </label>
                  <input
                    type="file"
                    accept="video/*"
                    onChange={(e) => setNewFile(e.target.files[0])}
                    className="input bg-white"
                    required
                  />
                </div>
              </div>
              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={uploading}
                  className="btn-primary"
                >
                  {uploading ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                      </svg>
                      Uploading...
                    </span>
                  ) : 'Upload to Dataset'}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Video List */}
        <div className="card overflow-hidden animate-slide-up">
          <div className="p-6 border-b border-primary-100 bg-surface-50">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-primary-800">
                Dataset Library
              </h2>
              <span className="badge bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm font-medium">
                {videos.length} videos
              </span>
            </div>
          </div>

          {loading ? (
            <div className="text-center py-12">
              <div className="w-12 h-12 border-4 border-primary-100 border-t-brand-500 rounded-full animate-spin mx-auto mb-4"></div>
              <p className="text-primary-500">Loading dataset...</p>
            </div>
          ) : videos.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead className="bg-surface-50 text-primary-500 text-xs uppercase tracking-wider font-semibold">
                  <tr>
                    <th className="p-4 pl-6">Gloss</th>
                    <th className="p-4">Duration</th>
                    <th className="p-4">File Path</th>
                    <th className="p-4 text-right pr-6">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-primary-100">
                  {videos.map((video) => (
                    <tr key={video.video_id} className="hover:bg-primary-50 transition-colors">
                      <td className="p-4 pl-6 font-bold text-primary-900">{video.gloss}</td>
                      <td className="p-4 font-mono text-sm text-primary-600">{video.duration.toFixed(2)}s</td>
                      <td className="p-4 text-sm text-primary-500 font-mono truncate max-w-xs">
                        {video.file_path}
                      </td>
                      <td className="p-4 text-right pr-6">
                        <button
                          onClick={() => handleDelete(video.video_id)}
                          className="text-error hover:text-error-dark font-medium text-sm transition-colors hover:bg-error-light/10 px-3 py-1.5 rounded-lg"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-16">
              <div className="text-4xl mb-4">📂</div>
              <p className="text-xl text-primary-900 font-medium">No ASL videos found</p>
              <p className="text-primary-500 mt-2">
                Add your first sign language video to get started.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AdminPage
