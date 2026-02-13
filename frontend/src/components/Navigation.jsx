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
    <header className="sticky top-0 z-[100] w-full bg-white border-b border-slate-100 shadow-sm transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16 sm:h-20">
          {/* Brand */}
          <Link to="/" className="flex items-center gap-3 group shrink-0" onClick={() => setIsMenuOpen(false)}>
            <div className="relative">
              <img
                src="/logo.jpeg"
                alt="Digital Dada Logo"
                className="w-8 h-8 sm:w-10 sm:h-10 rounded-lg object-contain bg-white transition-transform duration-500 group-hover:scale-110"
              />
            </div>
            <div className="hidden xs:flex flex-col">
              <div className="flex items-baseline leading-none">
                <span className="text-base sm:text-lg font-black text-slate-900 tracking-tight uppercase">Digital Dada</span>
              </div>
              <span className="text-[7px] sm:text-[9px] font-bold text-cyan-600 uppercase tracking-[0.1em] mt-0.5 opacity-80 whitespace-nowrap">
                AI Operations Agent™
              </span>
            </div>
          </Link>

          {/* Desktop Nav Items */}
          <div className="hidden lg:flex items-center gap-1 xl:gap-2 h-full">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`h-full px-3 xl:px-4 flex flex-col items-center justify-center gap-1 border-b-2 transition-all duration-300 group ${isActive(item.path)
                  ? 'border-cyan-500 text-slate-900'
                  : 'border-transparent text-slate-500 hover:text-slate-900 hover:border-slate-200'
                  }`}
              >
                <item.icon className="text-xl transition-transform group-hover:scale-110" />
                <span className="text-[10px] font-black uppercase tracking-widest">{item.label}</span>
              </Link>
            ))}
          </div>

          {/* User Actions & Mobile Toggle */}
          <div className="flex items-center gap-2 sm:gap-4">
            <div className="hidden sm:flex items-center gap-4">
              <div className="text-right hidden xl:block border-r border-slate-100 pr-4">
                <p className="text-[9px] font-black text-slate-400 uppercase tracking-widest leading-none mb-0.5">Administrator</p>
                <p className="text-xs font-black text-slate-800 tracking-tight">{user?.name || 'Admin User'}</p>
              </div>

              <button
                onClick={handleLogout}
                className="bg-slate-900 text-white px-5 py-2.5 rounded-xl font-black text-[10px] uppercase tracking-widest hover:bg-slate-800 transition-all flex items-center gap-2 shadow-lg shadow-slate-200"
              >
                <HiPower className="text-sm" />
                <span>Logout</span>
              </button>
            </div>

            {/* Mobile Menu Toggle */}
            <button
              className="lg:hidden w-10 h-10 bg-slate-50 text-slate-600 rounded-xl flex items-center justify-center transition-all active:scale-90 border border-slate-100"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <HiXMark className="text-2xl" /> : <HiBars3 className="text-2xl" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {isMenuOpen && (
        <div className="lg:hidden absolute top-full left-0 right-0 bg-white border-b border-slate-100 shadow-2xl animate-fade-in">
          <div className="flex flex-col p-4 gap-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setIsMenuOpen(false)}
                className={`w-full p-4 rounded-xl transition-all font-black text-sm uppercase tracking-widest flex items-center gap-4 ${isActive(item.path)
                  ? 'bg-slate-900 text-white shadow-lg'
                  : 'text-slate-600 hover:bg-slate-50'
                  }`}
              >
                <div className={`p-1.5 rounded-lg ${isActive(item.path) ? 'bg-white/10' : 'bg-slate-100'}`}>
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
                    <p className="text-sm font-black text-slate-900">{user?.name || 'Administrator'}</p>
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
    </header>
  );
}

export default Navigation;
