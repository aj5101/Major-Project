import React, { useMemo, useRef, useState, useEffect } from 'react'
import { useParams, useLocation } from 'react-router-dom'
import { videoAPI } from '../services/api'

/**
 * Video Result Page Component
 * 
 * Displays original video and ASL narration result.
 * Shows processing status and allows playback of both videos.
 */
function VideoResultPage() {
  const { videoId } = useParams()
  const location = useLocation()
  const [status, setStatus] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const videoRef = useRef(null)
  const [videoDuration, setVideoDuration] = useState(null)
  const [currentTime, setCurrentTime] = useState(0)
  const [playbackRate, setPlaybackRate] = useState(1)
  const [viewMode, setViewMode] = useState('teacher') // teacher | student
  const [repeatRange, setRepeatRange] = useState(null) // { start: number, end: number, label: string } | null

  const isRealtimeText = location.state?.isRealtimeText || false;
  const isCustomText = location.state?.isCustomText || false;
  const isPresetDemo = location.state?.isPresetDemo || false;
  const isTextDemo = location.state?.isTextDemo || false;
  const isGenerativeAvatar = location.state?.isGenerativeAvatar || false;
  const isAIGenerated = location.state?.isAIGenerated || false;
  const isLessonMode = location.state?.lessonMode || false;
  const lessonTitle = location.state?.lessonTitle || null;
  const lessonSentences = location.state?.sentences || null;
  const imageData = location.state?.imageData || null;

  // Debug: log imageData to console for diagnostics
  React.useEffect(() => {
    if (imageData) {
      console.log('[VideoResultPage] imageData received:', imageData)
      console.log('[VideoResultPage] image count:', imageData?.images?.length)
      imageData?.images?.forEach((img, i) => {
        const url = `http://127.0.0.1:8000/storage/processed/images/${img.image_file}`
        console.log(`[VideoResultPage] image[${i}] url:`, url, '| concept:', img.concept)
        fetch(url, { method: 'HEAD' })
          .then(r => console.log(`[VideoResultPage] image[${i}] HEAD status:`, r.status))
          .catch(e => console.error(`[VideoResultPage] image[${i}] HEAD failed:`, e.message))
      })
    } else {
      console.log('[VideoResultPage] no imageData in navigation state')
    }
  }, [])

  useEffect(() => {
    // Handle case where user directly visits AI lesson URL (no state available)
    if (!location.state && videoId && videoId.startsWith('ai-lesson-')) {
      // Extract video filename from videoId
      const videoFile = videoId.replace('ai-lesson-', '') + '.mp4'
      console.log('AI Lesson fallback - videoFile:', videoFile)
      
      setStatus({ status: 'completed', progress: 1.0 })
      setResult({
        original_text: "AI Generated Lesson",
        simplified_text: "AI Generated Lesson - Video: " + videoFile,
        asl_clips: [
          { clip_id: 'ai1', gloss: 'HELLO', confidence: 0.95, start_time: 0.0 },
          { clip_id: 'ai2', gloss: 'LEARN', confidence: 0.88, start_time: 2.0 },
          { clip_id: 'ai3', gloss: 'TOGETHER', confidence: 0.92, start_time: 4.0 }
        ],
        subtitles: [
          { text: "AI Generated Lesson - " + videoFile, start_time: 0.0, end_time: 6.0 }
        ]
      })
      setLoading(false)
      return
    }

    if (isPresetDemo) {
      // Handle preset demo case
      setStatus({ status: 'completed', progress: 1.0 })
      const signs = location.state.signs || ['hello', 'learn', 'together']
      setResult({
        original_text: location.state.originalText,
        simplified_text: location.state.simplifiedText,
        asl_clips: signs.map((sign, index) => ({
          clip_id: `preset${index + 1}`,
          gloss: sign.toUpperCase(),
          confidence: 0.95,
          start_time: index * 2.0
        })),
        subtitles: [
          { text: location.state.originalText, start_time: 0.0, end_time: signs.length * 2.0 }
        ]
      })
      setLoading(false)
      return
    }

    if (isCustomText || isRealtimeText || isGenerativeAvatar || isAIGenerated || imageData) {
      // Handle custom text case with dynamic video or realtime video or AI images
      setStatus({ status: 'completed', progress: 1.0 })
      const signs = location.state.signs || location.state.concepts || location.state.videoData?.signs || ['hello']
      const duration = location.state.duration || 6.0
      const originalText = location.state.originalText || location.state.user_input || "Custom Text"
      
      setResult({
        original_text: originalText,
        simplified_text: location.state.simplifiedText || originalText,
        asl_clips: signs.map((sign, index) => ({
          clip_id: `custom${index + 1}`,
          gloss: sign.toUpperCase(),
          confidence: 0.90,
          start_time: index * 2.0
        })),
        subtitles: [
          { text: originalText, start_time: 0.0, end_time: duration }
        ]
      })
      setLoading(false)
      return
    }

    if (isTextDemo) {
      // Handle old text demo case (backward compatibility)
      setStatus({ status: 'completed', progress: 1.0 })
      setResult({
        original_text: location.state.originalText || "Hello learn together",
        simplified_text: location.state.simplifiedText || "Hello learn together",
        asl_clips: [
          { clip_id: 'demo1', gloss: 'HELLO', confidence: 0.95, start_time: 0.0 },
          { clip_id: 'demo2', gloss: 'LEARN', confidence: 0.88, start_time: 2.0 },
          { clip_id: 'demo3', gloss: 'TOGETHER', confidence: 0.92, start_time: 4.0 }
        ],
        subtitles: [
          { text: location.state.originalText || "Hello learn together", start_time: 0.0, end_time: 6.0 }
        ]
      })
      setLoading(false)
      return
    }

    checkStatus()
    const interval = setInterval(checkStatus, 3000) // Poll every 3 seconds
    return () => clearInterval(interval)
  }, [videoId, isPresetDemo, isCustomText, isTextDemo])

  const checkStatus = async () => {
    try {
      const statusData = await videoAPI.getStatus(videoId)
      setStatus(statusData)

      if (statusData.status === 'completed') {
        try {
          const resultData = await videoAPI.getResult(videoId)
          setResult(resultData)
        } catch (err) {
          // Result not ready yet
        }
        setLoading(false)
      } else if (statusData.status === 'failed') {
        setError(statusData.message || 'Processing failed')
        setLoading(false)
      } else {
        setLoading(false)
      }
    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen pt-32 flex flex-col items-center justify-center">
        <div className="w-16 h-16 border-4 border-brand-200 border-t-brand-600 rounded-full animate-spin mb-6"></div>
        <h2 className="text-2xl font-bold text-primary-900">Loading your project...</h2>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container-main pt-32 pb-20">
        <div className="card p-8 border-l-4 border-error bg-error-light/10">
          <div className="flex items-start gap-4">
            <div className="text-3xl">⚠️</div>
            <div>
              <h2 className="text-xl font-bold text-error-dark mb-2">Processing Error</h2>
              <p className="text-primary-700">{error}</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!status) return null

  const simplifiedText = result?.simplified_text || ""
  const teacherTokens = useMemo(() => {
    const raw = simplifiedText
      .replace(/\s+/g, " ")
      .trim();
    if (!raw) return [];
    return raw.match(/\b[\w']+\b/g) || [];
  }, [simplifiedText])

  const computedDuration = videoDuration || location.state?.duration || null
  const wordTime = computedDuration && teacherTokens.length > 0
    ? computedDuration / teacherTokens.length
    : null

  const activeWordIndex = useMemo(() => {
    if (!wordTime || teacherTokens.length === 0) return null
    const idx = Math.floor(currentTime / wordTime)
    return Math.max(0, Math.min(teacherTokens.length - 1, idx))
  }, [currentTime, wordTime, teacherTokens.length])

  const sentenceBlocks = useMemo(() => {
    if (Array.isArray(lessonSentences) && lessonSentences.length > 0) {
      return lessonSentences.map((s) => ({
        text: s.text,
        simplified: s.simplified || s.text,
      }))
    }
    const raw = simplifiedText.replace(/\s+/g, " ").trim()
    if (!raw) return []
    const parts = raw.split(/(?<=[.!?])\s+/).map((p) => p.trim()).filter(Boolean)
    return parts.map((p) => ({ text: p, simplified: p }))
  }, [lessonSentences, simplifiedText])

  const aslVideoSrc = useMemo(() => {
    if (isPresetDemo) {
      return `http://127.0.0.1:8000/storage/processed/preset_videos/${location.state.videoFile}`
    }
    if (isRealtimeText) {
      return `http://127.0.0.1:8000/storage/processed/realtime/${location.state.videoFile}`
    }
    if (isGenerativeAvatar) {
      // generated_media route serves these consistently
      return `http://127.0.0.1:8000/api/generated/generative/${location.state.videoFile}`
    }
    if (isAIGenerated) {
      // AI-generated lessons use dynamic storage
      return `http://127.0.0.1:8000/storage/processed/dynamic/${location.state.videoFile}`
    }
    if (!location.state && videoId && videoId.startsWith('ai-lesson-')) {
      // Fallback for direct AI lesson URL visits
      const videoFile = videoId.replace('ai-lesson-', '') + '.mp4'
      const videoUrl = `http://127.0.0.1:8000/storage/processed/dynamic/${videoFile}`
      console.log('AI Lesson video URL:', videoUrl)
      return videoUrl
    }
    if (isCustomText) {
      return `http://127.0.0.1:8000/storage/processed/dynamic/${location.state.videoFile}`
    }
    if (isTextDemo) {
      return `http://127.0.0.1:8000/storage/processed/realistic_stitched_asl.mp4`
    }
    // Uploaded video pipeline
    return videoAPI.getASLVideoUrl(videoId)
  }, [isPresetDemo, isRealtimeText, isGenerativeAvatar, isAIGenerated, isCustomText, isTextDemo, location.state, videoId])

  const setRate = (rate) => {
    setPlaybackRate(rate)
    if (videoRef.current) videoRef.current.playbackRate = rate
  }

  const clearRepeat = () => setRepeatRange(null)

  const repeatSentence = () => {
    if (!wordTime || sentenceBlocks.length === 0) return

    const combined = sentenceBlocks.map((s) => s.simplified).join(" ").replace(/\s+/g, " ").trim()
    const words = combined.match(/\b[\w']+\b/g) || []
    if (words.length === 0) return

    const idx = activeWordIndex ?? 0

    // Map active word index into sentence index by cumulative word counts.
    let acc = 0
    let picked = 0
    for (let i = 0; i < sentenceBlocks.length; i++) {
      const w = (sentenceBlocks[i].simplified.match(/\b[\w']+\b/g) || []).length
      if (idx >= acc && idx < acc + w) { picked = i; break }
      acc += w
    }

    const startWordIndex = sentenceBlocks
      .slice(0, picked)
      .reduce((sum, s) => sum + (s.simplified.match(/\b[\w']+\b/g) || []).length, 0)

    const sentenceWordCount = (sentenceBlocks[picked].simplified.match(/\b[\w']+\b/g) || []).length

    const start = startWordIndex * wordTime
    const end = (startWordIndex + Math.max(1, sentenceWordCount)) * wordTime
    setRepeatRange({ start, end, label: "Repeat sentence" })
    if (videoRef.current) {
      videoRef.current.currentTime = start
      videoRef.current.play()
    }
  }

  const repeatWord = () => {
    if (!wordTime || activeWordIndex == null) return
    const start = activeWordIndex * wordTime
    const end = (activeWordIndex + 1) * wordTime
    const label = `Repeat word: ${teacherTokens[activeWordIndex] || ""}`
    setRepeatRange({ start, end, label })
    if (videoRef.current) {
      videoRef.current.currentTime = start
      videoRef.current.play()
    }
  }

  const jumpToWord = (idx) => {
    if (!wordTime || !videoRef.current) return
    clearRepeat()
    videoRef.current.currentTime = idx * wordTime
    videoRef.current.play()
  }

  useEffect(() => {
    const el = videoRef.current
    if (!el) return

    const onLoaded = () => {
      if (!Number.isNaN(el.duration) && Number.isFinite(el.duration)) {
        setVideoDuration(el.duration)
      }
      el.playbackRate = playbackRate
    }
    const onTime = () => {
      setCurrentTime(el.currentTime || 0)
      if (repeatRange && el.currentTime >= repeatRange.end) {
        el.currentTime = repeatRange.start
        // keep playing
        el.play()
      }
    }

    el.addEventListener("loadedmetadata", onLoaded)
    el.addEventListener("timeupdate", onTime)
    return () => {
      el.removeEventListener("loadedmetadata", onLoaded)
      el.removeEventListener("timeupdate", onTime)
    }
  }, [repeatRange, playbackRate])

  return (
    <div className="min-h-screen pt-28 pb-20 bg-surface-50">
      <div className="container-main">

        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
          <div>
            <h1 className="text-3xl md:text-4xl mb-2">
              {isLessonMode ? "Lesson Output" : "ASL Output"}
            </h1>
            {isLessonMode && lessonTitle && (
              <div className="flex items-center gap-3">
                <p className="text-primary-700 font-semibold">{lessonTitle}</p>
                {isAIGenerated && (
                  <div className="inline-flex items-center gap-1 bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 text-blue-700 text-xs font-semibold px-3 py-1 rounded-full">
                    <span>🤖</span>
                    <span>AI Generated</span>
                  </div>
                )}
              </div>
            )}
            <p className="text-primary-500">Project ID: <span className="font-mono text-sm bg-primary-100 px-2 py-1 rounded">{videoId || 'DEMO-123'}</span></p>
          </div>

          {status.status !== 'completed' && (
            <div className="bg-white px-6 py-4 rounded-xl border border-primary-200 shadow-sm flex items-center gap-4">
              <div className="relative w-12 h-12 flex items-center justify-center">
                <svg className="animate-spin w-full h-full text-brand-600" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
              </div>
              <div>
                <div className="font-bold text-primary-900">Processing Status</div>
                <div className="text-sm text-primary-500 font-medium">
                  {Math.round(status.progress * 100)}% Complete
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Results Dashboard */}
        {result && (
          <div className="grid lg:grid-cols-2 gap-8 animate-slide-up">

            {/* Left Column: Videos or Images */}
            <div className="space-y-8">
              {imageData && imageData.images ? (
                /* AI Images Display */
                <div className="card p-6 overflow-hidden">
                  <div className="mb-4">
                    <h3 className="text-lg font-semibold text-gray-800 mb-2">🤟 ASL Images</h3>
                    <p className="text-sm text-gray-600">AI-generated ASL sign language images for each concept</p>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {imageData.images.map((image, index) => (
                      <div key={index} className="relative group">
                        <div className="bg-gray-100 rounded-lg overflow-hidden aspect-square">
                          <img
                            src={`http://127.0.0.1:8000/storage/processed/images/${image.image_file}`}
                            alt={`ASL sign for: ${image.concept}`}
                            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                            onError={(e) => {
                              const failedUrl = e.target.src
                              console.error('[VideoResultPage] image load failed:', failedUrl)
                              e.target.onerror = null
                              e.target.style.display = 'none'
                              const parent = e.target.parentElement
                              if (parent && !parent.querySelector('.img-fallback')) {
                                const fb = document.createElement('div')
                                fb.className = 'img-fallback w-full h-full flex flex-col items-center justify-center gap-2 text-gray-400 bg-gray-100'
                                fb.innerHTML = '<span style="font-size:2rem">🤟</span><span style="font-size:0.7rem;text-align:center;padding:0 4px">Image unavailable<br/>' + image.concept + '</span>'
                                parent.appendChild(fb)
                              }
                            }}
                          />
                        </div>
                        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-3">
                          <p className="text-white text-sm font-medium capitalize">{image.concept}</p>
                          <p className="text-white/70 text-xs">Image {image.image_number} of {imageData.total_images}</p>
                        </div>
                        <div className="absolute top-2 right-2 bg-blue-500 text-white text-xs px-2 py-1 rounded-full">
                          🤖 AI
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm text-blue-800">
                      <span className="font-semibold">💡 Tip:</span> Click on each image to study the ASL sign. Practice each gesture to learn the sign language.
                    </p>
                  </div>
                </div>
              ) : (
                /* Video Display (Fallback) */
                <div className="card p-1 overflow-hidden">
                  <div className="bg-black rounded-xl overflow-hidden relative group aspect-video">
                    <video
                      ref={videoRef}
                      controls
                      className="w-full h-full"
                      onPlay={() => {
                        if (videoRef.current) videoRef.current.playbackRate = playbackRate
                      }}
                    >
                      <source src={aslVideoSrc} type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                    <div className="absolute top-4 left-4 bg-black/50 backdrop-blur px-3 py-1 rounded-lg text-white text-xs font-bold uppercase tracking-wider">
                      🤟 ASL Lesson Video
                    </div>
                  </div>
                </div>
              )}

              {/* Playback learning controls */}
              <div className="card p-6">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                  <h3 className="flex items-center gap-2">
                    <span>🎛️</span> Playback Controls
                  </h3>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-primary-600">Speed</span>
                    <select
                      value={playbackRate}
                      onChange={(e) => setRate(Number(e.target.value))}
                      className="text-sm border border-primary-200 rounded-lg px-3 py-2 bg-white"
                    >
                      <option value={0.5}>0.5x (slow)</option>
                      <option value={0.75}>0.75x</option>
                      <option value={1}>1x (normal)</option>
                    </select>
                  </div>
                </div>

                <div className="mt-4 grid sm:grid-cols-3 gap-3">
                  <button onClick={repeatSentence} className="btn-secondary">
                    Repeat sentence
                  </button>
                  <button onClick={repeatWord} className="btn-secondary">
                    Repeat word
                  </button>
                  <button onClick={clearRepeat} className="btn-secondary">
                    Clear repeat
                  </button>
                </div>

                {repeatRange && (
                  <div className="mt-4 text-xs text-primary-700 bg-primary-50 border border-primary-100 rounded-lg px-3 py-2">
                    {repeatRange.label} · looping {repeatRange.start.toFixed(1)}s → {repeatRange.end.toFixed(1)}s
                  </div>
                )}
              </div>

              <div className="card p-6">
                <h3 className="mb-4 flex items-center gap-2">
                  <span>🎬</span> ASL Clips Breakdown
                </h3>
                {result.asl_clips && result.asl_clips.length > 0 ? (
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                    {result.asl_clips.map((clip, index) => (
                      <div key={clip.clip_id} className="bg-primary-50 hover:bg-brand-50 border border-primary-100 p-3 rounded-lg transition-colors cursor-default">
                        <div className="text-xs text-primary-400 mb-1">Sign #{index + 1}</div>
                        <div className="font-bold text-primary-900">{clip.gloss}</div>
                        <div className="mt-2 flex items-center justify-between">
                          <span className="text-[10px] bg-white px-1.5 py-0.5 rounded border border-primary-100 font-mono">
                            {(clip.confidence * 100).toFixed(0)}%
                          </span>
                          <span className="text-[10px] text-primary-400">
                            {clip.start_time.toFixed(1)}s
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-primary-400 italic">No clips data available.</p>
                )}
              </div>
            </div>

            {/* Right Column: Text & Analysis */}
            <div className="space-y-8">
              {/* Student mode toggle */}
              <div className="card p-6">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                  <div>
                    <h3 className="mb-1 flex items-center gap-2">
                      <span>🎓</span> Classroom View
                    </h3>
                    <div className="text-sm text-primary-600">
                      Switch between a clean student view and a teacher view with word highlighting.
                    </div>
                  </div>
                  <div className="flex items-center gap-2 bg-white border border-primary-200 rounded-xl p-1">
                    <button
                      onClick={() => setViewMode("student")}
                      className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
                        viewMode === "student" ? "bg-brand-500 text-white" : "text-primary-700 hover:bg-primary-50"
                      }`}
                    >
                      Student Mode
                    </button>
                    <button
                      onClick={() => setViewMode("teacher")}
                      className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
                        viewMode === "teacher" ? "bg-brand-500 text-white" : "text-primary-700 hover:bg-primary-50"
                      }`}
                    >
                      Teacher Mode
                    </button>
                  </div>
                </div>
              </div>

              {/* Transcripts */}
              <div className={`grid md:grid-cols-2 gap-4 ${viewMode === "student" ? "md:grid-cols-1" : ""}`}>
                <div className="card p-6">
                  <h3 className="text-lg font-bold mb-3 text-primary-800">Original Speech</h3>
                  <div className="bg-primary-50 rounded-lg p-4 text-primary-700 min-h-[120px] text-sm leading-relaxed border border-primary-100">
                    {result.original_text || 'Waiting for transcription...'}
                  </div>
                </div>
                {viewMode === "teacher" && (
                  <div className="card p-6 border-brand-100 ring-2 ring-brand-50">
                    <h3 className="text-lg font-bold mb-3 text-brand-700">Simplified Text</h3>
                    <div className="bg-brand-50/50 rounded-lg p-4 text-primary-800 min-h-[120px] text-sm leading-relaxed">
                      {result.simplified_text || 'Waiting for simplification...'}
                    </div>
                  </div>
                )}
              </div>

              {/* Teacher Mode Panel */}
              {viewMode === "teacher" && (
                <div className="card p-6">
                  <h3 className="mb-4 flex items-center gap-2">
                    <span>🧑‍🏫</span> Teacher Mode Panel
                  </h3>

                  <div className="text-xs text-primary-500 mb-3">
                    Word highlighting is approximate and follows the lesson pacing. Click a word to jump and practice it.
                  </div>

                  <div className="bg-white border border-primary-100 rounded-xl p-4">
                    <div className="flex flex-wrap gap-2">
                      {teacherTokens.length > 0 ? (
                        teacherTokens.map((w, idx) => {
                          const active = idx === activeWordIndex
                          return (
                            <button
                              key={`${w}-${idx}`}
                              onClick={() => jumpToWord(idx)}
                              className={`px-2.5 py-1.5 rounded-lg border text-sm font-semibold transition-colors ${
                                active
                                  ? "bg-brand-500 text-white border-brand-500"
                                  : "bg-primary-50 text-primary-800 border-primary-100 hover:bg-brand-50"
                              }`}
                              title="Jump to this word"
                            >
                              {w}
                            </button>
                          )
                        })
                      ) : (
                        <div className="text-sm text-primary-500 italic">No text available to highlight yet.</div>
                      )}
                    </div>
                  </div>

                  {sentenceBlocks.length > 0 && (
                    <div className="mt-5">
                      <div className="text-sm font-bold text-primary-900 mb-2">Sentence breakdown</div>
                      <div className="space-y-2">
                        {sentenceBlocks.map((s, i) => (
                          <div key={i} className="bg-primary-50 border border-primary-100 rounded-lg p-3">
                            <div className="text-xs text-primary-500 mb-1">Sentence {i + 1}</div>
                            <div className="text-sm text-primary-900">{s.simplified}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Subtitles Timeline */}
              {viewMode === "teacher" && (
                <div className="card p-6 flex-1">
                  <h3 className="mb-4">📋 Lesson Timeline</h3>
                  <div className="space-y-0 relative before:absolute before:left-4 before:top-2 before:bottom-2 before:w-0.5 before:bg-primary-100">
                    {result.subtitles && result.subtitles.length > 0 ? (
                      result.subtitles.map((sub, idx) => (
                        <div key={idx} className="relative pl-10 py-3 group">
                          <div className="absolute left-[13px] top-4 w-2.5 h-2.5 rounded-full bg-primary-300 border-2 border-white group-hover:bg-brand-500 transition-colors"></div>
                          <div className="bg-white border border-primary-100 p-3 rounded-lg shadow-sm group-hover:shadow-md transition-all group-hover:border-brand-200">
                            <p className="text-primary-800">{sub.text}</p>
                            <div className="mt-1 flex items-center gap-2 text-xs text-primary-400 font-mono">
                              <span>{sub.start_time.toFixed(1)}s</span>
                              <span>→</span>
                              <span>{sub.end_time.toFixed(1)}s</span>
                            </div>
                          </div>
                        </div>
                      ))
                    ) : (
                      <p className="text-primary-400 pl-10 py-4 italic">No timeline generated yet.</p>
                    )}
                  </div>
                </div>
              )}
            </div>

          </div>
        )}
      </div>
    </div>
  )
}

export default VideoResultPage
