import { useMemo, useState } from "react";
import { generativeASLAPI } from "../services/api";

const VOCAB_CATEGORIES = [
  {
    id: "animals",
    title: "Animals",
    icon: "🐾",
    words: ["cat", "dog", "bird", "fish", "cow"],
  },
  {
    id: "actions",
    title: "Actions",
    icon: "🏃",
    words: ["walk", "run", "play", "drink", "read"],
  },
  {
    id: "school",
    title: "School",
    icon: "🏫",
    words: ["school", "teacher", "student", "book", "learn"],
  },
];

export default function Vocabulary() {
  const [activeCategory, setActiveCategory] = useState("animals");
  const [activeWord, setActiveWord] = useState("cat");
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);

  const [videoFile, setVideoFile] = useState(null);
  const [videoType, setVideoType] = useState(null); // "generative"

  const category = useMemo(
    () => VOCAB_CATEGORIES.find((c) => c.id === activeCategory) || VOCAB_CATEGORIES[0],
    [activeCategory]
  );

  const loadWord = async (word) => {
    setActiveWord(word);
    setBusy(true);
    setStatus(`Generating ASL for "${word}"...`);
    setVideoFile(null);
    setVideoType(null);

    try {
      const response = await generativeASLAPI.generateAvatarASL(word);
      const data = response.data;
      setVideoFile(data.video_file);
      setVideoType("generative");
      setStatus(`Ready: "${word}"`);
    } catch (e) {
      setStatus(`Error: ${e.message || "Failed to load word"}`);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen pt-32 pb-20 bg-surface-50">
      <div className="container-main max-w-6xl">
        <div className="text-center mb-10 animate-fade-in">
          <h1 className="mb-3">Vocabulary Builder</h1>
          <p className="max-w-2xl mx-auto text-primary-600">
            Click a word to see it in ASL. Use this for warm-ups, practice, and quick checks during class.
          </p>
        </div>

        <div className="grid lg:grid-cols-[0.9fr_1.1fr] gap-6 items-start">
          {/* Categories */}
          <div className="card p-6">
            <h3 className="mb-4 flex items-center gap-2">
              <span>📚</span> Categories
            </h3>
            <div className="grid sm:grid-cols-3 lg:grid-cols-1 gap-3">
              {VOCAB_CATEGORIES.map((c) => (
                <button
                  key={c.id}
                  onClick={() => {
                    setActiveCategory(c.id);
                    const firstWord = c.words[0];
                    loadWord(firstWord);
                  }}
                  className={`px-4 py-3 rounded-xl border text-left transition-all ${
                    activeCategory === c.id
                      ? "border-brand-300 bg-brand-50"
                      : "border-primary-200 bg-white hover:bg-primary-50"
                  }`}
                >
                  <div className="font-semibold text-primary-900 flex items-center gap-2">
                    <span>{c.icon}</span> {c.title}
                  </div>
                  <div className="text-xs text-primary-600 mt-1">{c.words.length} words</div>
                </button>
              ))}
            </div>
          </div>

          {/* Word grid + preview */}
          <div className="space-y-6">
            <div className="card p-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
                <h3 className="flex items-center gap-2">
                  <span>{category.icon}</span> {category.title} words
                </h3>
                <div className="text-xs text-primary-500">
                  Tip: Ask students to repeat the sign 2–3 times.
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
                {category.words.map((w) => (
                  <button
                    key={w}
                    onClick={() => loadWord(w)}
                    className={`px-3 py-3 rounded-xl border text-sm font-semibold transition-colors ${
                      activeWord === w
                        ? "border-brand-300 bg-brand-50 text-brand-800"
                        : "border-primary-200 bg-white hover:bg-primary-50 text-primary-800"
                    }`}
                  >
                    {w}
                  </button>
                ))}
              </div>
            </div>

            <div className="card p-1 overflow-hidden">
              <div className="aspect-video bg-black rounded-xl overflow-hidden relative">
                {videoFile && videoType === "generative" ? (
                  <video controls className="w-full h-full">
                    <source
                      src={`http://127.0.0.1:8000/api/generated/generative/${videoFile}`}
                      type="video/mp4"
                    />
                    Your browser does not support the video tag.
                  </video>
                ) : (
                  <div className="w-full h-full flex flex-col items-center justify-center text-white/90 p-8 text-center">
                    <div className="text-5xl mb-3">🤟</div>
                    <div className="font-bold text-lg">Select a word to preview ASL</div>
                    <div className="text-sm text-white/70 mt-1">
                      {busy ? "Generating video..." : "Videos are generated using your existing ASL avatar pipeline."}
                    </div>
                  </div>
                )}

                <div className="absolute top-4 left-4 bg-black/50 backdrop-blur px-3 py-1 rounded-lg text-white text-xs font-bold uppercase tracking-wider">
                  {activeWord}
                </div>
              </div>
            </div>

            {status && (
              <div className="text-sm text-primary-700 bg-primary-50 border border-primary-100 rounded-lg px-4 py-3">
                {status}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

