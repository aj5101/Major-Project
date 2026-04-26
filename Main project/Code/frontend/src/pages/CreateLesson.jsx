import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { generativeASLAPI, realtimeASLAPI, aiLessonAPI } from "../services/api";

const LESSON_TEMPLATES = [
  {
    id: "story",
    title: "Story Lesson",
    icon: "📖",
    helper:
      "Great for narratives. Keep sentences short and concrete.",
    starterTitle: "Animals story",
    starterText:
      "A cat walks to the school. The cat sees a dog. The dog runs. The cat is happy.",
  },
  {
    id: "vocabulary",
    title: "Vocabulary Lesson",
    icon: "🧩",
    helper:
      "Great for introducing new words. Use simple definitions and examples.",
    starterTitle: "Classroom vocabulary",
    starterText:
      "Water is important. Water helps our body. We drink water every day.",
  },
  {
    id: "simple",
    title: "Simple Explanation",
    icon: "🧑‍🏫",
    helper:
      "Great for a quick concept. One idea per sentence.",
    starterTitle: "Quick science",
    starterText:
      "The sun is a star. The sun gives light. The sun gives heat.",
  },
];

const DEMO_LESSONS = [
  {
    id: "demo-1",
    title: "Demo: Short practice",
    text: "The boy is playing. Water is important.",
  },
  {
    id: "demo-2",
    title: "Demo: Animals story",
    text: "A cat walks. A dog runs. The cat is happy.",
  },
  {
    id: "demo-3",
    title: "Demo: Classroom routine",
    text: "Hello students. Open your book. We learn together.",
  },
];

function splitIntoSentences(raw) {
  const cleaned = (raw || "").replace(/\s+/g, " ").trim();
  if (!cleaned) return [];

  // Split by punctuation, keep it simple and predictable.
  const parts = cleaned
    .split(/(?<=[.!?])\s+/)
    .map((s) => s.trim())
    .filter(Boolean);

  // If teacher pasted a single long paragraph without punctuation, chunk it.
  if (parts.length <= 1 && cleaned.split(" ").length > 16) {
    const words = cleaned.split(" ");
    const chunks = [];
    const chunkSize = 10;
    for (let i = 0; i < words.length; i += chunkSize) {
      chunks.push(words.slice(i, i + chunkSize).join(" "));
    }
    return chunks;
  }

  return parts;
}

function simplifyForStudents(sentence) {
  // Keep this intentionally lightweight to avoid overcomplicating backend.
  // The backend pipeline still does its own simplification where relevant.
  return (sentence || "")
    .replace(/\btherefore\b/gi, "so")
    .replace(/\bhowever\b/gi, "but")
    .replace(/\bapproximately\b/gi, "about")
    .replace(/\butilize\b/gi, "use")
    .replace(/\s+/g, " ")
    .trim();
}

export default function CreateLesson() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [lessonTitle, setLessonTitle] = useState("");
  const [lessonText, setLessonText] = useState("");
  const [templateId, setTemplateId] = useState("simple");
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);
  const [aiAvailable, setAiAvailable] = useState(false);
  const [useAIGeneration, setUseAIGeneration] = useState(true);

  const selectedTemplate = useMemo(
    () => LESSON_TEMPLATES.find((t) => t.id === templateId) || LESSON_TEMPLATES[2],
    [templateId]
  );

  useEffect(() => {
    const demo = searchParams.get("demo");
    if (!demo) return;
    const idx = Math.max(1, Math.min(3, Number(demo))) - 1;
    const picked = DEMO_LESSONS[idx];
    setLessonTitle(picked.title);
    setLessonText(picked.text);
  }, [searchParams]);

  // Check AI availability on component mount
  useEffect(() => {
    const checkAIAvailability = async () => {
      try {
        const response = await aiLessonAPI.getAIStatus();
        setAiAvailable(response.data.ai_available);
        if (!response.data.ai_available) {
          setStatus("AI generation unavailable - using rule-based simplification");
        }
      } catch (error) {
        console.warn("Failed to check AI availability:", error);
        setAiAvailable(false);
      }
    };
    checkAIAvailability();
  }, []);

  const applyTemplateStarter = () => {
    setLessonTitle(selectedTemplate.starterTitle);
    setLessonText(selectedTemplate.starterText);
  };

  const buildLessonPayload = () => {
    const sentences = splitIntoSentences(lessonText);
    return {
      lesson_title: (lessonTitle || "").trim() || "Untitled lesson",
      sentences: sentences.map((s) => ({
        text: s,
        simplified: simplifyForStudents(s),
      })),
    };
  };

  const generateLesson = async ({ previewOnly }) => {
    const trimmedText = (lessonText || "").trim();
    if (!trimmedText) return;

    setBusy(true);
    const title = (lessonTitle || "").trim() || "Untitled lesson";
    
    if (previewOnly) {
      setStatus("🤖 AI processing lesson...");
    } else {
      setStatus("🤖 Generating AI-powered ASL lesson...");
    }

    try {
      // Use the new AI lesson generation API
      const response = await aiLessonAPI.generateASLLesson(title, trimmedText, useAIGeneration);
      const data = response.data;

      if (!data.success) {
        throw new Error(data.message || "Failed to generate lesson");
      }

      setStatus("✨ Lesson created! Loading result...");

      // Prepare lesson data for navigation
      const lessonData = data.lesson_data;
      const videoData = data.video_data;
      const imageData = data.image_data;

      // Create enhanced sentence structure
      const enhancedSentences = lessonData.sentences.map((sentence, index) => ({
        id: `sentence-${index}`,
        original: sentence.original,
        simplified: sentence.simplified,
        aslSequence: sentence.asl_sequence,
        words: sentence.asl_sequence,
        timestamp: index * 3.0, // Estimate 3 seconds per sentence
      }));

      const videoId = videoData ? `ai-lesson-${videoData.video_file.replace(".mp4", "")}` : `ai-lesson-${Date.now()}`;
      
      navigate(`/lesson/${videoId}`, {
        state: {
          lessonMode: true,
          lessonTitle: lessonData.lesson_title,
          sentences: enhancedSentences,
          originalText: enhancedSentences.map((s) => s.original).join(" "),
          simplifiedText: enhancedSentences.map((s) => s.simplified).join(" "),
          videoFile: videoData?.video_file,
          videoData: videoData,
          imageData: imageData,
          isAIGenerated: true,
          aiAvailable: data.ai_available,
          duration: videoData?.duration || enhancedSentences.length * 3.0,
          previewOnly: !!previewOnly,
          fallbackUsed: lessonData.fallback_used || false,
        },
      });

    } catch (error) {
      console.error("AI lesson generation failed:", error);
      const msg = error.message || "Failed to create lesson";
      if (msg.toLowerCase().includes("network") || msg.toLowerCase().includes("timeout")) {
        setStatus("❌ Cannot reach the backend server. Make sure it is running on port 8000.");
      } else {
        setStatus(`❌ ${msg}`);
      }
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen pt-32 pb-20 bg-surface-50">
      <div className="container-main max-w-5xl">
        <div className="text-center mb-10 animate-fade-in">
          <h1 className="mb-3">Create Lesson</h1>
          <p className="max-w-2xl mx-auto text-primary-600">
            Write your lesson once, then teach it visually with ASL-supported output and classroom-friendly controls.
          </p>
        </div>

        <div className="grid lg:grid-cols-[1.2fr_0.8fr] gap-6 items-start">
          {/* Lesson form */}
          <div className="card p-7 animate-slide-up">
            {/* AI Status Indicator */}
            <div className="mb-6 p-4 rounded-lg border bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${aiAvailable ? 'bg-green-500 animate-pulse' : 'bg-yellow-500'}`}></div>
                  <div>
                    <div className="font-semibold text-sm text-gray-800">
                      {aiAvailable ? '🤖 AI Generation Active' : '🔄 Using Rule-Based Generation'}
                    </div>
                    <div className="text-xs text-gray-600">
                      {aiAvailable 
                        ? 'Powered by Google Gemini AI for optimal ASL simplification' 
                        : 'AI service unavailable - using smart text simplification'}
                    </div>
                  </div>
                </div>
                {aiAvailable && (
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={useAIGeneration}
                      onChange={(e) => setUseAIGeneration(e.target.checked)}
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-700">Use AI</span>
                  </label>
                )}
              </div>
            </div>
            <div className="grid sm:grid-cols-2 gap-4">
              <div className="sm:col-span-2">
                <label className="text-sm font-semibold text-primary-800">Lesson Title</label>
                <input
                  value={lessonTitle}
                  onChange={(e) => setLessonTitle(e.target.value)}
                  placeholder="e.g., Water is important"
                  className="mt-2 w-full p-3 border border-primary-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white"
                />
              </div>

              <div className="sm:col-span-2">
                <label className="text-sm font-semibold text-primary-800">Lesson Content</label>
                <textarea
                  value={lessonText}
                  onChange={(e) => setLessonText(e.target.value)}
                  placeholder="Write 2–6 short sentences. One idea per sentence."
                  className="mt-2 w-full h-44 p-3 border border-primary-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white"
                />
                <div className="mt-2 text-xs text-primary-500">
                  Tip: Use short sentences. This helps students follow signs more easily.
                </div>
              </div>
            </div>

            <div className="mt-6 flex flex-col sm:flex-row gap-3">
              <button
                onClick={() => generateLesson({ previewOnly: false })}
                disabled={busy || !lessonText.trim()}
                className={`btn-primary flex-1 ${busy || !lessonText.trim() ? "opacity-50 cursor-not-allowed" : ""}`}
              >
                {busy ? "🤖 Generating..." : `🤖 Generate AI ASL Lesson`}
              </button>
              <button
                onClick={() => generateLesson({ previewOnly: true })}
                disabled={busy || !lessonText.trim()}
                className={`btn-secondary flex-1 ${busy || !lessonText.trim() ? "opacity-50 cursor-not-allowed" : ""}`}
              >
                Preview Lesson
              </button>
            </div>

            {status && (
              <div className="mt-5 text-sm text-primary-700 bg-primary-50 border border-primary-100 rounded-lg px-4 py-3">
                {status}
              </div>
            )}
          </div>

          {/* Templates + demo */}
          <div className="space-y-6">
            {/* AI Features */}
            <div className="card p-6 bg-gradient-to-br from-blue-50 to-purple-50 border-blue-200">
              <h3 className="mb-3 flex items-center gap-2">
                <span>✨</span> AI-Powered Features
              </h3>
              <div className="space-y-3">
                <div className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">✓</span>
                  <div>
                    <div className="font-medium text-sm text-gray-800">Smart Simplification</div>
                    <div className="text-xs text-gray-600">AI converts complex text to ASL-friendly grammar</div>
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">✓</span>
                  <div>
                    <div className="font-medium text-sm text-gray-800">Visual Word Mapping</div>
                    <div className="text-xs text-gray-600">Selects words with common ASL signs</div>
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">✓</span>
                  <div>
                    <div className="font-medium text-sm text-gray-800">Sentence Breakdown</div>
                    <div className="text-xs text-gray-600">Optimizes sentence length for signing</div>
                  </div>
                </div>
              </div>
              
              {aiAvailable && (
                <div className="mt-4 p-3 bg-white rounded-lg border border-blue-200">
                  <div className="text-xs font-medium text-blue-800 mb-1">💡 Pro Tip</div>
                  <div className="text-xs text-gray-700">
                    Write naturally and let AI handle the ASL optimization. Focus on clear concepts over grammar.
                  </div>
                </div>
              )}
            </div>

            <div className="card p-6">
              <h3 className="mb-3 flex items-center gap-2">
                <span>🧠</span> Preset templates
              </h3>
              <div className="space-y-2">
                {LESSON_TEMPLATES.map((t) => (
                  <button
                    key={t.id}
                    onClick={() => setTemplateId(t.id)}
                    className={`w-full text-left px-4 py-3 rounded-xl border transition-all ${
                      templateId === t.id
                        ? "border-brand-300 bg-brand-50"
                        : "border-primary-200 bg-white hover:bg-primary-50"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="font-semibold text-primary-900 flex items-center gap-2">
                        <span>{t.icon}</span> {t.title}
                      </div>
                      {templateId === t.id && (
                        <span className="text-xs font-bold text-brand-700 bg-white px-2 py-1 rounded border border-brand-200">
                          Selected
                        </span>
                      )}
                    </div>
                    <div className="text-xs text-primary-600 mt-1">{t.helper}</div>
                  </button>
                ))}
              </div>

              <button onClick={applyTemplateStarter} className="btn-secondary w-full mt-4">
                Use template starter
              </button>
            </div>

            <div className="card p-6">
              <h3 className="mb-3 flex items-center gap-2">
                <span>🎒</span> Demo classroom lessons
              </h3>
              <div className="space-y-2">
                {DEMO_LESSONS.map((d) => (
                  <button
                    key={d.id}
                    onClick={() => {
                      setLessonTitle(d.title);
                      setLessonText(d.text);
                    }}
                    className="w-full text-left px-4 py-3 rounded-xl border border-primary-200 bg-white hover:bg-primary-50 transition-colors"
                  >
                    <div className="font-semibold text-primary-900">{d.title}</div>
                    <div className="text-xs text-primary-600 mt-1 line-clamp-2">{d.text}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="mt-10 text-center text-sm text-primary-500">
          Prefer video uploads? You can still use the old flow at{" "}
          <button onClick={() => navigate("/upload")} className="underline hover:text-primary-700">
            /upload
          </button>
          .
        </div>
      </div>
    </div>
  );
}

