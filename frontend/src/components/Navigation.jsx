import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  HiChartBar,
  HiFire,
  HiUsers,
  HiClipboardDocumentList,
  HiCalendarDays,
  HiCog6Tooth,
  HiPower,
  HiBars3,
  HiXMark
} from "react-icons/hi2";

function Navigation({ user, onLogout }) {
  const location = useLocation();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  const navItems = [
    { label: 'Dashboard', path: '/', icon: HiChartBar, color: 'text-cyan-500' },
    { label: 'Leads', path: '/leads', icon: HiFire, color: 'text-rose-500' },
    { label: 'Customers', path: '/customers', icon: HiUsers, color: 'text-indigo-500' },
    { label: 'Tasks', path: '/tasks', icon: HiClipboardDocumentList, color: 'text-amber-500' },
    { label: 'Bookings', path: '/bookings', icon: HiCalendarDays, color: 'text-emerald-500' },
    { label: 'Settings', path: '/settings', icon: HiCog6Tooth, color: 'text-slate-500' },
  ];

  const handleLogout = () => {
    if (onLogout) onLogout();
    navigate('/');
  };

  return (
    <nav className="sticky top-4 sm:top-6 z-[100] mx-auto max-w-7xl px-4 sm:px-6">
      <div className="glass-panel rounded-3xl sm:rounded-[2.5rem] px-4 sm:px-8 py-3 sm:py-4 flex justify-between items-center premium-shadow border-slate-200/50">
        {/* Brand */}
        <Link to="/" className="flex items-center gap-4 group shrink-0" onClick={() => setIsMenuOpen(false)}>
          {/* Stylized D Logo SVG */}
          <div className="flex items-center gap-3">
            <svg
              width="44"
              height="44"
              viewBox="0 0 100 100"
              className="transform group-hover:scale-110 transition-transform duration-500 drop-shadow-sm"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M20 20H55C71.5685 20 85 33.4315 85 50C85 66.5685 71.5685 80 55 80H20V20Z"
                stroke="black"
                strokeWidth="12"
                strokeLinejoin="round"
              />
              <path
                d="M42 38H55C61.6274 38 67 43.3726 67 50C67 56.6274 61.6274 62 55 62H42V38Z"
                stroke="black"
                strokeWidth="8"
                strokeLinejoin="round"
              />
            </svg>
            <div className="flex flex-col">
              <div className="flex items-baseline">
                <span className="text-xl font-light text-slate-400 tracking-[0.1em] uppercase">Digital</span>
                <span className="text-xl font-black text-slate-900 tracking-[0.05em] uppercase ml-1.5">Dada</span>
              </div>
              <span className="text-[10px] font-black text-cyan-600 uppercase tracking-[0.3em] mt-0.5 opacity-80">
                AI Operations Agent™
              </span>
            </div>
          </div>
        </Link>

        {/* Desktop Nav */}
        <div className="hidden lg:flex items-center gap-2 bg-slate-100/50 p-2 rounded-[2rem] border border-slate-200/30">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`px-6 py-3 rounded-2xl transition-all duration-300 font-black text-xs uppercase tracking-widest flex items-center gap-3 group ${isActive(item.path)
                ? 'bg-white text-slate-900 shadow-xl shadow-slate-200/50 scale-105'
                : 'text-slate-500 hover:text-slate-900 hover:bg-white/50'
                }`}
            >
              <div className={`p-1.5 rounded-lg transition-transform group-hover:scale-110 duration-300 ${isActive(item.path) ? 'bg-slate-50' : ''}`}>
                <item.icon className={`text-xl ${isActive(item.path) ? item.color : 'text-slate-400'}`} style={{ filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.1))' }} />
              </div>
              {item.label}
            </Link>
          ))}
        </div>

        {/* User Actions & Mobile Toggle */}
        <div className="flex items-center gap-4 sm:gap-6">
          <div className="hidden md:flex items-center gap-2 bg-slate-100/50 p-1.5 rounded-2xl border border-slate-200/30">
            <div className="flex items-center gap-3 pl-4 pr-2">
              <div className="text-right hidden xl:block">
                <p className="text-[9px] font-black text-slate-400 uppercase tracking-[0.2em] leading-none mb-1">Session Active</p>
                <p className="text-xs font-black text-slate-800 tracking-tight">{user?.name || 'Administrator'}</p>
              </div>
              <div className="w-10 h-10 bg-gradient-to-br from-slate-800 to-slate-950 rounded-xl flex items-center justify-center shadow-lg border border-white/20 relative group cursor-pointer hover:scale-105 transition-transform duration-300">
                <div className="absolute inset-0 bg-gradient-to-tr from-cyan-500/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                <span className="text-white font-black text-xs z-10">
                  {user?.name?.charAt(0) || 'A'}
                </span>
                {/* Active Pulse */}
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-emerald-500 rounded-full border-2 border-white animate-pulse"></span>
              </div>
            </div>

            <button
              className="w-10 h-10 bg-white hover:bg-rose-50 text-rose-500 rounded-xl flex items-center justify-center transition-all duration-300 active:scale-95 shadow-sm hover:shadow-md border border-slate-200/50 group"
              onClick={handleLogout}
              title="Terminate Session"
            >
              <HiPower className="text-lg group-hover:scale-110 group-hover:rotate-12 transition-all" />
            </button>
          </div>

          {/* Mobile Menu Toggle */}
          <button
            className="lg:hidden w-10 h-10 bg-slate-100 text-slate-600 rounded-xl flex items-center justify-center transition-all active:scale-90"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <HiXMark className="text-2xl" /> : <HiBars3 className="text-2xl" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {isMenuOpen && (
        <div className="lg:hidden absolute top-full left-4 right-4 mt-4 glass-panel rounded-3xl p-4 shadow-2xl animate-modal-in border-slate-200/50">
          <div className="flex flex-col gap-2">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setIsMenuOpen(false)}
                className={`w-full p-4 rounded-xl transition-all font-black text-sm uppercase tracking-widest flex items-center gap-4 ${isActive(item.path)
                  ? 'bg-slate-900 text-white'
                  : 'text-slate-600 bg-slate-50 hover:bg-slate-100'
                  }`}
              >
                <div className={`p-1.5 rounded-lg ${isActive(item.path) ? 'bg-white/10' : 'bg-white shadow-sm'}`}>
                  <item.icon className={`text-xl ${isActive(item.path) ? 'text-white' : item.color}`} />
                </div>
                {item.label}
              </Link>
            ))}

            <div className="mt-4 pt-4 border-t border-slate-100">
              <div className="flex items-center justify-between px-2">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-slate-900 rounded-xl flex items-center justify-center text-white font-black">
                    {user?.name?.charAt(0) || 'A'}
                  </div>
                  <div>
                    <p className="text-xs font-black text-slate-900">{user?.name || 'Administrator'}</p>
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Active Session</p>
                  </div>
                </div>
                <button
                  onClick={handleLogout}
                  className="w-10 h-10 bg-rose-50 text-rose-500 rounded-xl flex items-center justify-center"
                >
                  <HiPower className="text-xl" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}

export default Navigation;
