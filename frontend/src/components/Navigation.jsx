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
    <nav className="sticky top-2 sm:top-6 z-[100] mx-auto max-w-7xl px-2 sm:px-6">
      <div className="glass-panel rounded-2xl sm:rounded-[2.5rem] px-3 sm:px-8 py-2 sm:py-4 flex justify-between items-center premium-shadow border-slate-200/50">
        {/* Brand */}
        <Link to="/" className="flex items-center gap-2 sm:gap-4 group shrink-0" onClick={() => setIsMenuOpen(false)}>
          <div className="relative">
            <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-xl blur opacity-0 group-hover:opacity-100 transition duration-500"></div>
            <img
              src="/logo.jpeg"
              alt="Digital Dada Logo"
              className="w-8 h-8 sm:w-12 sm:h-12 rounded-lg sm:rounded-xl object-contain relative bg-white p-1 border border-slate-100 shadow-sm transition-transform duration-500 group-hover:scale-110"
            />
          </div>
          <div className="flex flex-col">
            <div className="flex items-baseline leading-none sm:leading-tight">
              <span className="text-sm sm:text-lg font-light text-slate-400 tracking-[0.1em] uppercase block">Digital</span>
              <span className="text-sm sm:text-lg font-black text-slate-900 tracking-[0.05em] uppercase ml-1 sm:ml-1.5">Dada</span>
            </div>
            <span className="text-[7px] sm:text-[10px] font-black text-cyan-600 uppercase tracking-[0.1em] sm:tracking-[0.3em] mt-0.5 opacity-80 whitespace-nowrap">
              AI Operations Agent™
            </span>
          </div>
        </Link>

        {/* Desktop Nav */}
        <div className="hidden lg:flex items-center gap-1 xl:gap-2 bg-slate-100/50 p-1.5 rounded-[2rem] border border-slate-200/30">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`px-3 xl:px-5 py-2.5 rounded-2xl transition-all duration-300 font-black text-[10px] xl:text-xs uppercase tracking-widest flex items-center gap-2 xl:gap-3 group ${isActive(item.path)
                ? 'bg-white text-slate-900 shadow-lg shadow-slate-200/50 scale-105'
                : 'text-slate-500 hover:text-slate-900 hover:bg-white/50'
                }`}
            >
              <div className={`p-1 rounded-lg transition-transform group-hover:scale-110 duration-300 ${isActive(item.path) ? 'bg-slate-50' : ''}`}>
                <item.icon className={`text-lg ${isActive(item.path) ? item.color : 'text-slate-400'}`} />
              </div>
              <span className="hidden xl:inline">{item.label}</span>
              <span className="xl:hidden">{item.label.substring(0, 3)}</span>
            </Link>
          ))}
        </div>

        {/* User Actions & Mobile Toggle */}
        <div className="flex items-center gap-2 sm:gap-4">
          <div className="hidden sm:flex items-center gap-2 bg-slate-100/50 p-1 rounded-2xl border border-slate-200/30">
            <div className="flex items-center gap-2 pl-3 pr-1">
              <div className="text-right hidden lg:block xl:block">
                <p className="text-[8px] font-black text-slate-400 uppercase tracking-[0.1em] leading-none mb-0.5">Active</p>
                <p className="text-[11px] font-black text-slate-800 tracking-tight whitespace-nowrap">{user?.name || 'Admin'}</p>
              </div>
              <div className="w-9 h-9 bg-slate-900 rounded-xl flex items-center justify-center shadow-md border border-white/20 relative group cursor-pointer hover:scale-105 transition-transform duration-300">
                <span className="text-white font-black text-xs z-10">
                  {user?.name?.charAt(0) || 'A'}
                </span>
                <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-500 rounded-full border-2 border-white animate-pulse"></span>
              </div>
            </div>

            <button
              className="w-9 h-9 bg-white hover:bg-rose-50 text-rose-500 rounded-xl flex items-center justify-center transition-all duration-300 active:scale-95 border border-slate-200/50 group"
              onClick={handleLogout}
              title="Logout"
            >
              <HiPower className="text-base group-hover:scale-110 transition-all" />
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
