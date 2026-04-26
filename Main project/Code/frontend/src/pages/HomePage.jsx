import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="min-h-screen pt-24 pb-20">

      {/* HERO SECTION */}
      <section className="container-main pt-12 md:pt-20 pb-24 md:pb-32 grid md:grid-cols-2 gap-12 items-center animate-fade-in">
        <div className="text-left space-y-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-50 border border-brand-100 text-brand-700 text-sm font-semibold tracking-wide shadow-sm">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-500"></span>
            </span>
            ASL Classroom Accessibility Platform
          </div>

          <h1 className="text-primary-900 leading-[1.1] tracking-tight">
            Make Your Classroom Accessible
            <span className="block text-gradient">for Every Student</span>
          </h1>

          <p className="text-lg md:text-xl text-primary-600 max-w-lg leading-relaxed">
            Convert lessons into <strong>ASL-supported visual content</strong> for hearing-impaired students.
            Create clear, classroom-ready materials in minutes.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 pt-4">
            <Link to="/create-lesson" className="btn-primary group">
              Create Lesson
              <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
            </Link>
            <Link to="/create-lesson?demo=1" className="btn-secondary">Try Demo Lesson</Link>
          </div>

          <div className="pt-8 flex items-center gap-4 text-sm text-primary-500 font-medium">
            <div className="flex -space-x-2">
              {[1, 2, 3].map(i => (
                <div key={i} className="w-8 h-8 rounded-full bg-primary-200 border-2 border-white"></div>
              ))}
            </div>
            <p>Designed for real classroom teaching</p>
          </div>
        </div>

        {/* Hero Visual Placeholder */}
        <div className="relative hidden md:block animate-slide-up">
          <div className="absolute inset-0 bg-brand-200 rounded-3xl rotate-6 opacity-30 blur-2xl"></div>
          <div className="relative bg-white rounded-2xl shadow-float border border-primary-100 p-2 overflow-hidden transform transition-transform hover:scale-[1.02] duration-500">
            <div className="aspect-video bg-primary-50 rounded-xl flex items-center justify-center relative overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-tr from-brand-50 to-primary-50 opacity-50"></div>
              <div className="text-6xl group-hover:scale-110 transition-transform duration-700">📚</div>

              {/* Simulated Interface Elements */}
              <div className="absolute bottom-4 left-4 right-4 bg-white/90 backdrop-blur px-4 py-3 rounded-xl shadow-sm flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-brand-100 flex items-center justify-center text-xs">TEACH</div>
                <div className="h-2 bg-primary-100 rounded-full flex-1">
                  <div className="h-full w-2/3 bg-brand-500 rounded-full"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FEATURE CARDS */}
      <section className="container-main pb-16">
        <div className="grid md:grid-cols-3 gap-6">
          <FeatureCard
            icon="🧑‍🏫"
            title="Create ASL Lesson"
            description="Turn lesson text into an ASL-supported video experience with student-friendly wording."
          />
          <FeatureCard
            icon="📖"
            title="Visual Story Teaching"
            description="Use story and vocabulary templates to explain concepts clearly and consistently."
          />
          <FeatureCard
            icon="🤝"
            title="Inclusive Classroom Support"
            description="Switch between Teacher Mode and Student Mode to match how you teach in real time."
          />
        </div>
      </section>

      {/* PROCESS SECTION */}
      <section id="how-it-works" className="bg-surface-50 py-24 border-y border-primary-100/50">
        <div className="container-main">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="mb-4">Built for classroom flow</h2>
            <p className="text-primary-600">
              Create a lesson, generate ASL-supported visuals, then teach with controls designed
              for real students.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <StepCard
              number="01"
              icon="📝"
              title="Create Lesson"
              description="Write or paste your lesson, then choose a teaching template (story, vocabulary, or simple explanation)."
              delay="0"
            />
            <StepCard
              number="02"
              icon="🧠"
              title="Generate ASL Support"
              description="The system simplifies language and generates an ASL-supported visual output for each part of the lesson."
              delay="100"
            />
            <StepCard
              number="03"
              icon="✨"
              title="Teach & Practice"
              description="Use Teacher Mode to highlight words and repeat tricky parts. Switch to Student Mode for a clean view."
              delay="200"
            />
          </div>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="card p-7 hover:shadow-float transition-all duration-300">
      <div className="w-12 h-12 bg-brand-50 rounded-xl flex items-center justify-center text-2xl mb-4">
        {icon}
      </div>
      <h3 className="text-lg font-bold mb-2 text-primary-900">{title}</h3>
      <p className="text-sm text-primary-600 leading-relaxed">{description}</p>
    </div>
  )
}

function StepCard({ number, icon, title, description, delay }) {
  return (
    <div
      className="card hover:shadow-float p-8 transition-all duration-300 group"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-start justify-between mb-6">
        <div className="w-12 h-12 bg-brand-50 rounded-xl flex items-center justify-center text-2xl mb-4 group-hover:bg-brand-600 group-hover:text-white transition-colors duration-300">
          {icon}
        </div>
        <span className="font-heading font-bold text-4xl text-primary-100 group-hover:text-brand-100 transition-colors">
          {number}
        </span>
      </div>

      <h3 className="text-xl font-bold mb-3 text-primary-900">{title}</h3>
      <p className="text-primary-600 leading-relaxed text-sm">{description}</p>
    </div>
  );
}
