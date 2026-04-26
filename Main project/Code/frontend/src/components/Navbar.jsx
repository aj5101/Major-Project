import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-primary-100 transition-all duration-300">
      <div className="container-main h-20 flex justify-between items-center">
        {/* Brand */}
        <Link to="/" className="flex items-center gap-3 group">
          <span className="text-3xl transform group-hover:scale-110 transition-transform duration-300">🤟</span>
          <div className="flex flex-col">
            <span className="font-heading font-bold text-xl text-primary-900 leading-none tracking-tight group-hover:text-brand-600 transition-colors">
              ASL Classroom
            </span>
            <span className="text-xs font-semibold text-brand-500 uppercase tracking-wider">
              Accessibility Platform
            </span>
          </div>
        </Link>

        {/* Navigation */}
        <div className="flex gap-2 items-center">
          <NavLink to="/" isActive={isActive('/')} icon="🏠">Home</NavLink>
          <div className="w-px h-6 bg-primary-200 mx-2"></div>
          <NavLink to="/create-lesson" isActive={isActive('/create-lesson')} icon="🧑‍🏫">Create Lesson</NavLink>
          <NavLink to="/vocabulary" isActive={isActive('/vocabulary')} icon="📚">Vocabulary</NavLink>
          <NavLink to="/admin" isActive={isActive('/admin')} icon="⚙️">Admin</NavLink>
        </div>
      </div>
    </nav>
  );
}

function NavLink({ to, children, isActive, icon }) {
  return (
    <Link
      to={to}
      className={`
        px-4 py-2.5 rounded-xl font-medium text-sm transition-all duration-200 flex items-center gap-2
        ${isActive
          ? 'bg-brand-50 text-brand-700 font-semibold shadow-sm ring-1 ring-brand-200'
          : 'text-primary-600 hover:bg-primary-50 hover:text-primary-900'}
      `}
    >
      <span className="text-base opactiy-80">{icon}</span>
      {children}
    </Link>
  );
}
