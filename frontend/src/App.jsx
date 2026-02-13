/**
 * Frontend React Application
 * AI-Powered Lead Automation System
 * Admin Dashboard with Authentication
 */

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './styles/index.css';

// Pages
import LoginPage from './pages/Login';
import Dashboard from './pages/Dashboard';
import LeadsPage from './pages/Leads';
import CustomersPage from './pages/Customers';
import TasksPage from './pages/Tasks';
import BookingsPage from './pages/Bookings';
import SettingsPage from './pages/Settings';

// Components
import Navigation from './components/Navigation';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check if user is already logged in on component mount
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const authToken = localStorage.getItem('authToken');

    if (storedUser && authToken) {
      try {
        setUser(JSON.parse(storedUser));
        setIsLoggedIn(true);
      } catch (error) {
        console.error('Failed to restore user session:', error);
        localStorage.removeItem('user');
        localStorage.removeItem('authToken');
      }
    }

    setLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    console.log('User logged out successfully');
    setIsLoggedIn(false);
    setUser(null);
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gradient-to-r from-slate-800 to-slate-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-cyan-500 mx-auto mb-4"></div>
          <p className="text-gray-300 text-lg">Loading...</p>
        </div>
      </div>
    );
  }

  // If not logged in, show login page
  if (!isLoggedIn) {
    return <LoginPage onLogin={handleLogin} />;
  }

  // If logged out, show logout screen
  if (isLoggedIn === false && user === null) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-50 p-6">
        <div className="max-w-md w-full glass-panel rounded-[3rem] p-12 text-center premium-shadow">
          <div className="w-24 h-24 bg-slate-900 rounded-[2rem] flex items-center justify-center mx-auto mb-8 shadow-2xl relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-tr from-cyan-500/20 to-transparent"></div>
            <span className="text-5xl group-hover:scale-110 transition-transform duration-500">🤖</span>
          </div>
          <h1 className="text-4xl font-black text-slate-900 mb-4 tracking-tight">Session Ended</h1>
          <p className="text-slate-500 mb-10 text-lg font-medium leading-relaxed">
            You've been successfully logged out of the Digital Dada Agent™.
          </p>
          <button
            onClick={() => {
              setIsLoggedIn(true);
              setUser({ name: 'Admin User', email: 'admin@techsales.com', role: 'Administrator' });
            }}
            className="w-full btn-premium btn-premium-cyan group"
          >
            <span className="mr-3 group-hover:rotate-12 transition-transform">🔑</span>
            Login Again
          </button>
        </div>
      </div>
    );
  }

  // Logged in - show dashboard
  return (
    <Router>
      <div className="app">
        <Navigation user={user} onLogout={handleLogout} />
        <div className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/leads" element={<LeadsPage />} />
            <Route path="/customers" element={<CustomersPage />} />
            <Route path="/tasks" element={<TasksPage />} />
            <Route path="/bookings" element={<BookingsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
