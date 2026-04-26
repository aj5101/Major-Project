import { useState, useRef } from "react";
import { videoAPI, dynamicASLAPI, realtimeASLAPI, generativeASLAPI } from "../services/api";
import { useNavigate } from "react-router-dom";

export default function VideoUploadPage() {
  const [video, setVideo] = useState(null);
  const [text, setText] = useState("");
  const [status, setStatus] = useState("");
  const [isDragOver, setIsDragOver] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [inputMode, setInputMode] = useState("video"); // "video", "text", or "preset"
  const [useAvatar, setUseAvatar] = useState(true);
  const [selectedPreset, setSelectedPreset] = useState("");
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  // Preset educational phrases
  const presetPhrases = [
    "Hello students welcome to class",
    "Let's learn science and math together", 
    "Teacher asks question student answers",
    "Books help us gain knowledge",
    "School is where we learn together",
    "Hello teacher I want to learn",
    "Science helps us understand the world",
    "Math teaches us to solve problems",
    "Knowledge comes from asking questions",
    "Students and teachers learn together"
  ];

  // Helper function to extract signs from text
  const getSignsForText = (text) => {
    const wordToSign = {
      // Greetings
      'hello': 'hello', 'hi': 'hello', 'hey': 'hello',
      'good': 'hello', 'morning': 'hello', 'welcome': 'hello',
      
      // Learning verbs
      'learn': 'learn', 'learning': 'learn', 'study': 'learn', 'studying': 'learn',
      'teach': 'teacher', 'teaching': 'teacher', 'education': 'learn',
      
      // Social concepts
      'together': 'together', 'group': 'together', 'team': 'together',
      'class': 'school', 'classroom': 'school',
      
      // Educational nouns
      'book': 'book', 'books': 'book', 'reading': 'book',
      'school': 'school', 'schools': 'school',
      'teacher': 'teacher', 'teachers': 'teacher', 'instructor': 'teacher',
      'student': 'student', 'students': 'student', 'pupil': 'student',
      
      // Question/Answer
      'question': 'question', 'questions': 'question', 'ask': 'question',
      'answer': 'answer', 'answers': 'answer', 'respond': 'answer',
      
      // Knowledge concepts
      'knowledge': 'knowledge', 'know': 'knowledge', 'understand': 'knowledge',
      'understanding': 'knowledge', 'smart': 'knowledge', 'intelligent': 'knowledge',
      
      // Subjects
      'science': 'science', 'scientific': 'science',
      'math': 'math', 'mathematics': 'math', 'calculate': 'math',
      
      // Achievement words  
      'great': 'hello', 'excellent': 'hello',
      'performance': 'hello', 'grade': 'student', 'grades': 'student',  
      'cgpa': 'math', 'gpa': 'math', 'score': 'math',
      
      // Common school terms
      'mr': 'teacher', 'mister': 'teacher', 'sir': 'teacher',
      'jain': 'student', 'name': 'student', 'friend': 'student'
    }
    
    const words = text.toLowerCase().match(/\b\w+\b/g) || []
    const signs = []
    
    for (const word of words) {
      if (wordToSign[word] && !signs.includes(wordToSign[word])) {
        signs.push(wordToSign[word])
      }
    }
    
    return signs.length > 0 ? signs : ['hello', 'learn', 'together'] // Default fallback
  };

  const handleFileSelect = (file) => {
    if (file && file.type.startsWith('video/')) {
      setVideo(file);
      setStatus("");
    } else {
      alert("Please upload a valid video file.");
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleUpload = async () => {
    if (inputMode === "video" && !video) return;
    if (inputMode === "text" && !text.trim()) return;
    if (inputMode === "preset" && !selectedPreset) return;
    
    setIsUploading(true);
    setStatus(inputMode === "video" ? "Uploading video..." : 
              inputMode === "preset" ? "Loading preset ASL video..." : "Processing text...");
    
    try {
      if (inputMode === "video") {
        // Upload video to backend
        const uploadResponse = await videoAPI.upload(video);
        const { video_id } = uploadResponse;
        
        setStatus("Processing video... Converting speech to text and generating ASL narration.");
        
        // Start processing
        await videoAPI.process(video_id);
        
        // Poll for completion
        const checkStatus = async () => {
          const statusResponse = await videoAPI.getStatus(video_id);
          
          if (statusResponse.status === 'completed') {
            setStatus("Processing complete! Redirecting to results...");
            setTimeout(() => {
              navigate(`/video/${video_id}`);
            }, 1500);
          } else if (statusResponse.status === 'failed') {
            setStatus(`Processing failed: ${statusResponse.message}`);
            setIsUploading(false);
          } else {
            // Still processing, check again in 2 seconds
            setTimeout(checkStatus, 2000);
          }
        };
        
        checkStatus();
      } else if (inputMode === "preset") {
        // Handle preset selection
        setStatus("Loading preset ASL video...");
        
        // Find the preset index
        const presetIndex = presetPhrases.indexOf(selectedPreset);
        const videoFile = `phrase_${String(presetIndex + 1).padStart(2, '0')}.mp4`;
        
        setTimeout(() => {
          navigate(`/video/preset-${presetIndex + 1}`, { 
            state: { 
              isPresetDemo: true, 
              originalText: selectedPreset,
              simplifiedText: selectedPreset,
              videoFile: videoFile,
              signs: getSignsForText(selectedPreset)
            } 
          });
        }, 1500);
      } else if (inputMode === "text") {
        // For custom text input, use generative avatar by default
        setStatus(useAvatar ? "Creating AI avatar ASL video..." : "Creating real-time ASL video from your text...");
        
        try {
          const response = useAvatar
            ? await generativeASLAPI.generateAvatarASL(text)
            : await realtimeASLAPI.generateRealtimeASL(text);
          
          const data = response.data;
          const video_file = data.video_file;
          const duration = data.duration;
          const signs = data.tokens || data.concepts || ['hello'];
          
          setStatus("ASL video created! Redirecting to results...");
          
          setTimeout(() => {
            navigate(`/video/${useAvatar ? 'avatar' : 'realtime'}-${video_file.replace('.mp4', '')}`, { 
              state: { 
                isGenerativeAvatar: useAvatar,
                isRealtimeText: !useAvatar,
                originalText: text,
                simplifiedText: text,
                videoFile: video_file,
                concepts: signs,
                duration: duration
              } 
            });
          }, 1500);
          
        } catch (error) {
          console.error('Real-time ASL generation error:', error);
          setStatus(`Error: ${error.message}`);
          setIsUploading(false);
        }
      }
      
    } catch (error) {
      console.error('Upload error:', error);
      setStatus(`Error: ${error.message}`);
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen pt-32 pb-20 bg-surface-50">
      <div className="container-main max-w-4xl">

        <div className="text-center mb-12 animate-fade-in">
          <h1 className="mb-4">Upload video (legacy)</h1>
          <p className="max-w-xl mx-auto">
            This is the original upload-based workflow. For classroom teaching, use{" "}
            <span className="font-semibold">Create Lesson</span> from the navbar.
          </p>
        </div>

        {/* Input Mode Selection */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-lg border border-primary-200 p-1 flex">
            <button
              onClick={() => setInputMode("video")}
              className={`px-6 py-2 rounded-md font-medium transition-colors ${
                inputMode === "video"
                  ? "bg-brand-500 text-white"
                  : "text-primary-600 hover:bg-primary-50"
              }`}
            >
              🎥 Video Upload
            </button>
            <button
              onClick={() => setInputMode("preset")}
              className={`px-6 py-2 rounded-md font-medium transition-colors ${
                inputMode === "preset"
                  ? "bg-brand-500 text-white"
                  : "text-primary-600 hover:bg-primary-50"
              }`}
            >
              🎯 Preset Phrases
            </button>
            <button
              onClick={() => setInputMode("text")}
              className={`px-6 py-2 rounded-md font-medium transition-colors ${
                inputMode === "text"
                  ? "bg-brand-500 text-white"
                  : "text-primary-600 hover:bg-primary-50"
              }`}
            >
              📝 Custom Text
            </button>
          </div>
        </div>

        <div className="card max-w-2xl mx-auto p-1 animate-slide-up">
          {inputMode === "video" ? (
            // Video Upload Interface
            <div
              className={`
                relative rounded-xl border-2 border-dashed p-12 text-center transition-all duration-200 cursor-pointer
                ${isDragOver
                  ? 'border-brand-500 bg-brand-50'
                  : 'border-primary-200 bg-surface-50 hover:bg-surface-100'}
              `}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onClick={() => fileInputRef.current.click()}
            >
              <input
                type="file"
                ref={fileInputRef}
                accept="video/*"
                className="hidden"
                onChange={(e) => handleFileSelect(e.target.files[0])}
              />

              <div className="flex flex-col items-center gap-4">
                <div className={`
                  w-16 h-16 rounded-full flex items-center justify-center text-3xl transition-colors
                  ${isDragOver ? 'bg-brand-100 text-brand-600' : 'bg-primary-100 text-primary-500'}
                `}>
                  {video ? '🎥' : '☁️'}
                </div>

                {video ? (
                  <div>
                    <h3 className="text-xl font-bold text-primary-900 mb-1">{video.name}</h3>
                    <p className="text-sm text-primary-500">{(video.size / 1024 / 1024).toFixed(2)} MB</p>
                    <button
                      onClick={(e) => { e.stopPropagation(); setVideo(null); }}
                      className="mt-4 text-sm text-error font-medium hover:underline"
                    >
                      Remove file
                    </button>
                  </div>
                ) : (
                  <>
                    <h3 className="text-xl font-bold text-primary-900">
                      Drag & Drop your video here
                    </h3>
                    <p className="text-primary-500">or click to browse files</p>
                  </>
                )}
              </div>
            </div>
          ) : inputMode === "preset" ? (
            // Preset Phrases Interface
            <div className="p-8">
              <div className="flex flex-col items-center gap-4">
                <div className="w-16 h-16 rounded-full bg-primary-100 flex items-center justify-center text-3xl text-primary-500">
                  🎯
                </div>
                <h3 className="text-xl font-bold text-primary-900">
                  Choose an Educational Phrase
                </h3>
                <p className="text-primary-500 text-center max-w-md">
                  Select from our collection of educational phrases with pre-made ASL videos.
                </p>
                
                <select
                  value={selectedPreset}
                  onChange={(e) => setSelectedPreset(e.target.value)}
                  className="w-full p-4 border border-primary-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                >
                  <option value="">Select a phrase...</option>
                  {presetPhrases.map((phrase, index) => (
                    <option key={index} value={phrase}>
                      {phrase}
                    </option>
                  ))}
                </select>
                
                {selectedPreset && (
                  <div className="w-full p-4 bg-primary-50 rounded-lg">
                    <p className="text-sm text-primary-600 mb-2">Selected phrase:</p>
                    <p className="text-primary-900 font-medium">{selectedPreset}</p>
                    <p className="text-xs text-primary-500 mt-2">
                      ASL signs: {getSignsForText(selectedPreset).join(', ').toUpperCase()}
                    </p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            // Custom Text Input Interface
            <div className="p-8">
              <div className="flex flex-col items-center gap-4">
                <div className="w-16 h-16 rounded-full bg-primary-100 flex items-center justify-center text-3xl text-primary-500">
                  📝
                </div>
                <h3 className="text-xl font-bold text-primary-900">
                  Enter Custom Educational Text
                </h3>
                <p className="text-primary-500 text-center max-w-md">
                  Type or paste educational content that you want to convert into ASL narration.
                  The system will match words to available ASL signs.
                </p>
                <div className="w-full flex items-center justify-between bg-white border border-primary-200 rounded-lg px-4 py-3">
                  <div>
                    <div className="font-semibold text-primary-900">AI avatar mode (recommended)</div>
                    <div className="text-xs text-primary-500">
                      Generates a new stick-figure ASL video (no stored clips). Falls back to fingerspelling for unknown words.
                    </div>
                  </div>
                  <label className="inline-flex items-center gap-2 cursor-pointer select-none">
                    <input
                      type="checkbox"
                      checked={useAvatar}
                      onChange={(e) => setUseAvatar(e.target.checked)}
                    />
                    <span className="text-sm font-medium text-primary-700">Use avatar</span>
                  </label>
                </div>
                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Enter your educational text here... For example: 'The sun is a star that provides light and heat to Earth.'"
                  className="w-full h-32 p-4 border border-primary-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                />
                <div className="text-sm text-primary-400">
                  {text.length} characters
                </div>
                {text && (
                  <div className="w-full p-4 bg-primary-50 rounded-lg">
                    <p className="text-sm text-primary-600 mb-2">ASL signs that will be used:</p>
                    <p className="text-primary-900 font-medium">
                      {getSignsForText(text).join(', ').toUpperCase()}
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          <div className="p-8 border-t border-primary-100 mt-1">
            <button
              onClick={handleUpload}
              disabled={(!video && inputMode === "video") || (!text.trim() && inputMode === "text") || (!selectedPreset && inputMode === "preset") || isUploading}
              className={`btn-primary w-full ${((!video && inputMode === "video") || (!text.trim() && inputMode === "text") || (!selectedPreset && inputMode === "preset") || isUploading) ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {isUploading ? 'Processing...' : (
                inputMode === "video" ? 'Start ASL Video Processing' :
                inputMode === "preset" ? 'Load Preset ASL Video' :
                'Create Custom ASL Video'
              )}
            </button>

            {status && (
              <div className="mt-6 flex items-center justify-center gap-3 text-brand-600 font-medium animate-fade-in">
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                {status}
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
