/**
 * API Service
 * 
 * Handles all HTTP requests to the backend API.
 * Provides error handling and response formatting.
 */

import axios from 'axios'

// Prefer 127.0.0.1 over localhost to avoid IPv6/::1 resolution issues on some machines.
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'
console.log('[API] baseURL =', API_BASE_URL)

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 min — image generation can be slow
  headers: {
    'Content-Type': 'application/json',
  },
})

// Derive the storage base URL from the API base (strip /api suffix)
export const STORAGE_BASE_URL = API_BASE_URL.replace(/\/api$/, '')

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    // Only extract error details on error responses
    if (response.status >= 400) {
      const message = response.data?.detail || response.data?.message || response.message || 'An error occurred'
      console.error('API Error:', message)
      return Promise.reject(new Error(message))
    }
    
    // Return the full response on success
    return response
  },
  (error) => {
    const message = error.response?.data?.detail || error.response?.data?.message || error.message || 'An error occurred'
    console.error('API Error:', message)
    return Promise.reject(new Error(message))
  }
)

/**
 * Video API endpoints
 */
export const videoAPI = {
  upload: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/videos/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  process: (videoId) => api.post(`/videos/${videoId}/process`),
  
  getStatus: (videoId) => api.get(`/videos/${videoId}/status`),
  
  getResult: (videoId) => api.get(`/videos/${videoId}/result`),
  
  getAll: () => api.get('/videos'),
  
  getASLVideoUrl: (videoId) => `${API_BASE_URL}/videos/${videoId}/asl-video`,
  
  delete: (videoId) => api.delete(`/videos/${videoId}`)
}

// Dynamic ASL API
export const dynamicASLAPI = {
  generateVideo: (text, videoId = null) => {
    const payload = { text }
    if (videoId !== null && videoId !== undefined) {
      payload.video_id = videoId
    }
    return api.post('/generate-asl', payload)
  },
  
  getAvailableSigns: () => api.get('/available-signs'),
  
  getResult: async (videoId) => {
    const response = await api.get(`/videos/${videoId}/result`)
    return response.data
  },

  /**
   * Get ASL video URL
   */
  getASLVideoUrl: (videoId) => {
    return `${API_BASE_URL}/videos/${videoId}/asl-video`
  },

  /**
   * List all videos
   */
  list: async (skip = 0, limit = 20) => {
    const response = await api.get('/videos', { params: { skip, limit } })
    return response.data
  },
}

// Real-Time ASL API
export const realtimeASLAPI = {
  generateRealtimeASL: (userInput, userContext = null) => {
    const payload = { 
      user_input: userInput,
      user_context: userContext
    }
    return api.post('/realtime-asl', payload)
  },
  
  getRealtimeHistory: () => api.get('/realtime-history'),
  
  getRealtimeVideoUrl: (videoFile) => {
    return `${API_BASE_URL}/storage/processed/realtime/${videoFile}`
  }
}

// Generative (Avatar) ASL API
export const generativeASLAPI = {
  generateAvatarASL: (text, tokens = null) => {
    const payload = { text }
    if (tokens && Array.isArray(tokens)) payload.tokens = tokens
    return api.post('/generate-asl-avatar', payload)
  },
  getAvatarVideoUrl: (videoFile) => `${API_BASE_URL}/storage/processed/generative/${videoFile}`,
}

// AI Lesson Generation API
export const aiLessonAPI = {
  generateASLLesson: (lessonTitle, lessonText, useAI = true) => {
    const payload = {
      lesson_title: lessonTitle,
      lesson_text: lessonText,
      use_ai: useAI
    }
    return api.post('/generate-asl-lesson', payload)
  },

  previewLesson: (lessonTitle, lessonText) => {
    const payload = {
      lesson_title: lessonTitle,
      lesson_text: lessonText
    }
    return api.post('/preview-lesson', payload)
  },

  getAIStatus: () => api.get('/ai-status')
}

/**
 * ASL Dataset API endpoints
 */
export const aslDatasetAPI = {
  /**
   * Add new ASL video
   */
  add: async (gloss, file) => {
    const formData = new FormData()
    formData.append('gloss', gloss)
    formData.append('file', file)
    
    const response = await api.post('/asl-dataset/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * List ASL videos
   */
  list: async (skip = 0, limit = 100, gloss = null) => {
    const params = { skip, limit }
    if (gloss) params.gloss = gloss
    
    const response = await api.get('/asl-dataset/', { params })
    return response.data
  },

  /**
   * Get ASL video details
   */
  get: async (videoId) => {
    const response = await api.get(`/asl-dataset/${videoId}`)
    return response.data
  },

  /**
   * Delete ASL video
   */
  delete: async (videoId) => {
    const response = await api.delete(`/asl-dataset/${videoId}`)
    return response.data
  },
}

/**
 * Health check
 */
export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}

export default api

