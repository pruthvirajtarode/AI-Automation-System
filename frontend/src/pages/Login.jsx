/**
 * Login Page Component
 * Admin authentication with modern design
 */

import React, { useState } from 'react';

function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // Default admin credentials (in production, verify against backend)
  const ADMIN_CREDENTIALS = {
    email: 'admin@techsales.com',
    password: 'Admin@12345',
    name: 'Admin User',
    role: 'Administrator',
  };

  const handleLogin = (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Simulate API call
    setTimeout(() => {
      // Validate credentials
      if (email === ADMIN_CREDENTIALS.email && password === ADMIN_CREDENTIALS.password) {
        // Successful login
        const user = {
          email: ADMIN_CREDENTIALS.email,
          name: ADMIN_CREDENTIALS.name,
          role: ADMIN_CREDENTIALS.role,
        };

        // Store in localStorage for persistence
        localStorage.setItem('authToken', 'demo-token-' + Date.now());
        localStorage.setItem('user', JSON.stringify(user));

        onLogin(user);
        setLoading(false);
      } else {
        setError('Invalid email or password');
        setLoading(false);
      }
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-950 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
      <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
      <div className="absolute bottom-0 left-1/2 w-96 h-96 bg-gradient-to-br from-green-500 to-cyan-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      <div className="w-full max-w-md relative z-10">
        {/* Logo & Title */}
        <div className="text-center mb-12">
          <div className="inline-block mb-6 p-6 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-3xl shadow-2xl transform hover:scale-110 transition-transform duration-300">
            <span className="text-6xl block">🤖</span>
          </div>
          <h2 className="text-4xl font-black text-white mb-2 tracking-tight">AI Automation</h2>
          <p className="text-lg text-cyan-300 font-semibold">Lead Management System</p>
        </div>

        {/* Main Login Card */}
        <div className="relative mb-8">
          <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-3xl blur-2xl opacity-40"></div>
          <div className="relative bg-gradient-to-br from-white to-gray-50 rounded-3xl shadow-2xl p-10 backdrop-blur-xl border border-white/20">
            {/* Header */}
            <div className="mb-10">
              <h3 className="text-3xl font-black text-gray-900 mb-2">Welcome Back</h3>
              <p className="text-gray-600 text-lg">Sign in to your account</p>
            </div>

            {/* Error Message */}
            {error && (
              <div className="mb-8 p-5 bg-red-50 border-2 border-red-200 rounded-2xl transform animate-bounce">
                <div className="flex items-start gap-4">
                  <span className="text-3xl">⚠️</span>
                  <div>
                    <p className="text-red-900 font-bold text-lg">{error}</p>
                    <p className="text-red-700 text-sm mt-1">Please check your credentials and try again</p>
                  </div>
                </div>
              </div>
            )}

            {/* Login Form */}
            <form onSubmit={handleLogin} className="space-y-6">
              {/* Email Field */}
              <div>
                <label className="block text-sm font-black text-gray-800 mb-3 uppercase tracking-[0.2em] ml-1">
                  📧 Email Address
                </label>
                <div className="relative group">
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-400 to-blue-600 rounded-2xl blur opacity-0 group-hover:opacity-20 transition duration-500"></div>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => {
                      setEmail(e.target.value);
                      setError('');
                    }}
                    className="relative w-full px-6 py-4 bg-white/50 backdrop-blur-sm border-2 border-slate-100 rounded-2xl focus:outline-none focus:bg-white focus:border-cyan-500 focus:ring-4 focus:ring-cyan-500/10 transition-all duration-300 text-lg font-medium placeholder-gray-400 hover:border-slate-200"
                    placeholder="your@email.com"
                    disabled={loading}
                  />
                </div>
              </div>

              {/* Password Field */}
              <div>
                <label className="block text-sm font-black text-gray-800 mb-3 uppercase tracking-[0.2em] ml-1">
                  🔐 Password
                </label>
                <div className="relative group">
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-400 to-blue-600 rounded-2xl blur opacity-0 group-hover:opacity-20 transition duration-500"></div>
                  <div className="relative flex items-center">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={password}
                      onChange={(e) => {
                        setPassword(e.target.value);
                        setError('');
                      }}
                      className="w-full px-6 py-4 bg-white/50 backdrop-blur-sm border-2 border-slate-100 rounded-2xl focus:outline-none focus:bg-white focus:border-cyan-500 focus:ring-4 focus:ring-cyan-500/10 transition-all duration-300 text-lg font-medium placeholder-gray-400 hover:border-slate-200"
                      placeholder="••••••••••"
                      disabled={loading}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-4 p-2 text-slate-400 hover:text-cyan-500 transition-colors"
                    >
                      {showPassword ? '👁️' : '👁️‍🗨️'}
                    </button>
                  </div>
                </div>
              </div>

              {/* Login Button */}
              <button
                type="submit"
                disabled={loading}
                className="group relative w-full mt-8 py-5 px-6 bg-slate-950 text-white font-black text-lg rounded-2xl transition-all duration-500 disabled:opacity-50 disabled:cursor-not-allowed shadow-2xl hover:shadow-cyan-500/20 transform hover:-translate-y-1 active:scale-95 flex items-center justify-center gap-3 overflow-hidden"
              >
                {/* Button Glow Effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-blue-600/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

                {/* Shimmer Animation */}
                <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-400 to-transparent opacity-50"></div>

                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-3 border-white border-t-transparent"></div>
                    <span className="tracking-widest uppercase">Verifying...</span>
                  </>
                ) : (
                  <>
                    <span className="text-xl group-hover:rotate-12 transition-transform duration-300">🔑</span>
                    <span className="tracking-widest uppercase">Secure Login</span>
                  </>
                )}
              </button>
            </form>

            {/* Divider */}
            <div className="my-8 flex items-center gap-4">
              <div className="flex-1 h-px bg-gradient-to-r from-transparent to-gray-300"></div>
              <span className="text-gray-500 text-sm font-semibold">Learn More</span>
              <div className="flex-1 h-px bg-gradient-to-l from-transparent to-gray-300"></div>
            </div>

            {/* Features */}
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center p-4 bg-cyan-50 rounded-xl hover:bg-cyan-100 transition-colors">
                <span className="text-3xl block mb-2">⚡</span>
                <p className="text-xs font-bold text-cyan-900">Fast Setup</p>
              </div>
              <div className="text-center p-4 bg-blue-50 rounded-xl hover:bg-blue-100 transition-colors">
                <span className="text-3xl block mb-2">🔐</span>
                <p className="text-xs font-bold text-blue-900">Secure</p>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-xl hover:bg-purple-100 transition-colors">
                <span className="text-3xl block mb-2">📊</span>
                <p className="text-xs font-bold text-purple-900">Analytics</p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center">
          <p className="text-gray-300 text-sm font-medium">
            🌟 AI-Powered Lead Management & Automation System
          </p>
          <p className="text-gray-500 text-xs mt-3">© 2026 AI Automation. All rights reserved.</p>
        </div>
      </div>

      {/* CSS for Blob Animation */}
      <style>{`
        @keyframes blob {
          0%, 100% { transform: translate(0, 0) scale(1); }
          33% { transform: translate(30px, -50px) scale(1.1); }
          66% { transform: translate(-20px, 20px) scale(0.9); }
        }
        .animate-blob {
          animation: blob 7s infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </div>
  );
}

export default LoginPage;
