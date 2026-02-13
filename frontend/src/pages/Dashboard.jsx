import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import {
  HiFire,
  HiBolt,
  HiCheckCircle,
  HiCalendarDays,
  HiArrowRight
} from "react-icons/hi2";

function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    totalLeads: 124,
    qualifiedLeads: 42,
    pendingTasks: 8,
    upcomingBookings: 3
  });
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);

  // Chart Data for Business Performance
  const performanceData = [
    { name: 'Mon', leads: 4, sales: 2 },
    { name: 'Tue', leads: 7, sales: 4 },
    { name: 'Wed', leads: 5, sales: 3 },
    { name: 'Thu', leads: 12, sales: 8 },
    { name: 'Fri', leads: 9, sales: 6 },
    { name: 'Sat', leads: 15, sales: 11 },
    { name: 'Sun', leads: 18, sales: 14 },
  ];

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);

      // Simulation of data fetching
      setStats({
        totalLeads: 124,
        qualifiedLeads: 42,
        pendingTasks: 8,
        upcomingBookings: 3
      });

      setRecentActivity([
        { id: 1, customer: { name: 'John Smith', company: 'Tech Corp' }, status: 'qualified', quality_score: 85, created_at: new Date() },
        { id: 2, customer: { name: 'Sarah Johnson', company: 'Finance Ltd' }, status: 'contacted', quality_score: 72, created_at: new Date() },
        { id: 3, customer: { name: 'Mike Davis', company: 'Design Co' }, status: 'new', quality_score: 45, created_at: new Date() },
      ]);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-slate-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-cyan-500 mx-auto mb-6"></div>
          <p className="text-slate-500 font-bold text-xl">Initializing Intelligent Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content animate-fade-in">
      <div className="page-container">
        {/* Page Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-16">
          <div className="flex items-center gap-6">
            <div className="hidden sm:block w-px h-16 bg-gradient-to-b from-transparent via-slate-200 to-transparent"></div>
            <div>
              <div className="flex items-center gap-3 mb-3">
                <span className="bg-slate-900 text-white px-3 py-1 rounded-md text-[10px] font-black uppercase tracking-[0.2em] shadow-lg">
                  Main Hub
                </span>
                <span className="text-slate-400 text-[10px] font-bold uppercase tracking-[0.2em]">
                  System Status: Operational
                </span>
              </div>
              <h1 className="text-4xl sm:text-5xl font-black text-slate-900 tracking-tight mb-2">
                Business Intelligence <span className="text-slate-400 font-light">Suite</span>
              </h1>
              <p className="text-slate-500 font-medium tracking-wide">
                Unified monitoring for <span className="text-slate-900 font-bold">Digital Dada Agent™</span> ecosystems.
              </p>
            </div>
          </div>
          <div className="flex gap-4">
            <button
              onClick={() => navigate('/leads?add=true')}
              className="bg-slate-900 text-white px-8 py-4 rounded-2xl font-black text-xs uppercase tracking-[0.2em] hover:bg-slate-800 transition-all shadow-xl active:scale-95"
            >
              + Create Lead
            </button>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 xs:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-8 mb-8 sm:mb-12">
          {/* Card: Leads */}
          <div className="card-premium group hover-lift">
            <div className="flex justify-between items-start mb-4 sm:mb-6">
              <div className="w-10 h-10 sm:w-14 sm:h-14 bg-cyan-50 rounded-xl sm:rounded-2xl flex items-center justify-center group-hover:bg-cyan-500 transition-colors duration-300 shadow-sm border border-cyan-100 group-hover:border-transparent">
                <HiFire className="text-xl sm:text-2xl text-cyan-600 group-hover:text-white group-hover:scale-110 transition-all duration-300" style={{ filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.1))' }} />
              </div>
              <span className="text-emerald-500 font-black text-[10px] sm:text-sm bg-emerald-50 px-2 sm:px-3 py-1 rounded-lg">+12%</span>
            </div>
            <p className="text-slate-400 font-bold text-[10px] sm:text-sm uppercase tracking-widest mb-1">Leads</p>
            <h3 className="text-2xl sm:text-4xl font-black text-slate-900 tracking-tight">{stats.totalLeads}</h3>
          </div>

          {/* Card: Qualified */}
          <div className="card-premium group hover-lift">
            <div className="flex justify-between items-start mb-4 sm:mb-6">
              <div className="w-10 h-10 sm:w-14 sm:h-14 bg-indigo-50 rounded-xl sm:rounded-2xl flex items-center justify-center group-hover:bg-indigo-500 transition-colors duration-300 shadow-sm border border-indigo-100 group-hover:border-transparent">
                <HiBolt className="text-xl sm:text-2xl text-indigo-600 group-hover:text-white group-hover:scale-110 transition-all duration-300" style={{ filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.1))' }} />
              </div>
              <span className="text-indigo-500 font-black text-[10px] sm:text-sm bg-indigo-50 px-2 sm:px-3 py-1 rounded-lg">High</span>
            </div>
            <p className="text-slate-400 font-bold text-[10px] sm:text-sm uppercase tracking-widest mb-1">Qualified</p>
            <h3 className="text-2xl sm:text-4xl font-black text-slate-900 tracking-tight">{stats.qualifiedLeads}</h3>
          </div>

          {/* Card: Tasks */}
          <div className="card-premium group hover-lift">
            <div className="flex justify-between items-start mb-4 sm:mb-6">
              <div className="w-10 h-10 sm:w-14 sm:h-14 bg-amber-50 rounded-xl sm:rounded-2xl flex items-center justify-center group-hover:bg-amber-500 transition-colors duration-300 shadow-sm border border-amber-100 group-hover:border-transparent">
                <HiCheckCircle className="text-xl sm:text-2xl text-amber-600 group-hover:text-white group-hover:scale-110 transition-all duration-300" style={{ filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.1))' }} />
              </div>
              <span className="text-rose-500 font-black text-[10px] sm:text-sm bg-rose-50 px-2 sm:px-3 py-1 rounded-lg">Soon</span>
            </div>
            <p className="text-slate-400 font-bold text-[10px] sm:text-sm uppercase tracking-widest mb-1">Tasks</p>
            <h3 className="text-2xl sm:text-4xl font-black text-slate-900 tracking-tight">{stats.pendingTasks}</h3>
          </div>

          {/* Card: Meetings */}
          <div className="card-premium group hover-lift">
            <div className="flex justify-between items-start mb-4 sm:mb-6">
              <div className="w-10 h-10 sm:w-14 sm:h-14 bg-emerald-50 rounded-xl sm:rounded-2xl flex items-center justify-center group-hover:bg-emerald-500 transition-colors duration-300 shadow-sm border border-emerald-100 group-hover:border-transparent">
                <HiCalendarDays className="text-xl sm:text-2xl text-emerald-600 group-hover:text-white group-hover:scale-110 transition-all duration-300" style={{ filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.1))' }} />
              </div>
              <span className="text-slate-500 font-black text-[10px] sm:text-sm bg-slate-50 px-2 sm:px-3 py-1 rounded-lg">2PM</span>
            </div>
            <p className="text-slate-400 font-bold text-[10px] sm:text-sm uppercase tracking-widest mb-1">Bookings</p>
            <h3 className="text-2xl sm:text-4xl font-black text-slate-900 tracking-tight">{stats.upcomingBookings}</h3>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8 mb-8 sm:mb-12">
          <div className="lg:col-span-2 card-premium">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-8 gap-4">
              <div>
                <h3 className="text-xl sm:text-2xl font-black text-slate-900">Lead Conversion</h3>
                <p className="text-slate-500 font-medium text-sm">Performance analysis (7d)</p>
              </div>
              <select className="bg-slate-50 border-none rounded-xl px-4 py-2 font-bold text-xs outline-none cursor-pointer w-fit">
                <option>Last 7 Days</option>
                <option>Last 30 Days</option>
              </select>
            </div>
            <div className="h-[250px] sm:h-[350px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={performanceData}>
                  <defs>
                    <linearGradient id="colorLeads" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis
                    dataKey="name"
                    axisLine={false}
                    tickLine={false}
                    tick={{ fill: '#94a3b8', fontSize: 10, fontWeight: 700 }}
                    dy={10}
                  />
                  <YAxis
                    axisLine={false}
                    tickLine={false}
                    tick={{ fill: '#94a3b8', fontSize: 10, fontWeight: 700 }}
                  />
                  <Tooltip
                    contentStyle={{ borderRadius: '1.5rem', border: 'none', boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.1)' }}
                  />
                  <Area
                    type="monotone"
                    dataKey="leads"
                    stroke="#0ea5e9"
                    strokeWidth={4}
                    fillOpacity={1}
                    fill="url(#colorLeads)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card-premium flex flex-col justify-between">
            <div>
              <h3 className="text-xl sm:text-2xl font-black text-slate-900">Intelligence Actions</h3>
              <p className="text-slate-500 font-medium text-sm mb-6 sm:mb-8">Workflow optimization</p>

              <div className="space-y-3 sm:space-y-4">
                {[
                  { label: 'Review Tasks', path: '/tasks', icon: '📋' },
                  { label: 'Calendar View', path: '/bookings', icon: '📅' },
                  { label: 'Automation', path: '/settings', icon: '⚙️' }
                ].map((action) => (
                  <button
                    key={action.path}
                    onClick={() => navigate(action.path)}
                    className="w-full flex items-center justify-between p-3 sm:p-4 bg-slate-50 rounded-2xl hover:bg-slate-100 transition-colors group"
                  >
                    <div className="flex items-center gap-3 sm:gap-4">
                      <div className="w-8 h-8 sm:w-10 sm:h-10 bg-white rounded-xl flex items-center justify-center text-sm sm:text-lg shadow-sm">{action.icon}</div>
                      <span className="font-bold text-slate-700 text-sm">{action.label}</span>
                    </div>
                    <span className="text-slate-400 group-hover:translate-x-1 transition-transform">→</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="mt-8 pt-6 sm:pt-8 border-t border-slate-100">
              <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-3xl p-5 sm:p-6 text-white relative overflow-hidden">
                <div className="relative z-10">
                  <h4 className="font-black text-lg sm:text-xl mb-1">Business Engine</h4>
                  <p className="text-slate-400 text-[10px] mb-4 uppercase tracking-widest">AI Optimization Active</p>
                  <button className="w-full py-2.5 sm:py-3 bg-cyan-500 rounded-xl font-black text-[10px] sm:text-xs hover:bg-cyan-400 transition-colors uppercase tracking-widest">
                    View Systems API
                  </button>
                </div>
                <div className="absolute top-[-20%] right-[-10%] w-32 h-32 bg-cyan-500/20 rounded-full blur-3xl text-xs"></div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activity Table */}
        <div className="card-premium">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-8 sm:mb-10 gap-4">
            <div>
              <h3 className="text-xl sm:text-2xl font-black text-slate-900">Lead Intelligence</h3>
              <p className="text-slate-500 font-medium text-sm">Latest qualified interactions</p>
            </div>
            <button onClick={() => navigate('/leads')} className="text-cyan-600 font-black text-xs sm:text-sm hover:underline w-fit">
              View All Leads →
            </button>
          </div>

          <div className="overflow-x-auto -mx-5 px-5">
            <table className="table-premium min-w-[700px] lg:min-w-full text-sm">
              <thead>
                <tr>
                  <th>Qualified Identity</th>
                  <th>Affiliation</th>
                  <th>Status</th>
                  <th>Lead Quality</th>
                  <th>Engagement</th>
                </tr>
              </thead>
              <tbody>
                {recentActivity.map((activity) => (
                  <tr key={activity.id}>
                    <td>
                      <div className="flex items-center gap-3 sm:gap-4">
                        <div className="w-9 h-9 sm:w-10 sm:h-10 bg-slate-100 rounded-xl flex items-center justify-center font-black text-slate-400 text-xs sm:text-sm">
                          {activity.customer?.name.charAt(0)}
                        </div>
                        <div>
                          <p className="font-black text-slate-900 text-xs sm:text-sm">{activity.customer?.name}</p>
                          <p className="text-[8px] sm:text-[10px] text-slate-400 font-bold uppercase tracking-wider">Investor</p>
                        </div>
                      </div>
                    </td>
                    <td><span className="font-bold text-slate-600 text-xs sm:text-sm">{activity.customer?.company}</span></td>
                    <td>
                      <span className={`badge-premium ${activity.status === 'qualified' ? 'badge-premium-success' :
                        activity.status === 'contacted' ? 'badge-premium-info' :
                          'badge-premium-warning'
                        }`}>
                        {activity.status}
                      </span>
                    </td>
                    <td>
                      <div className="flex items-center gap-3">
                        <div className="flex-1 h-1 bg-slate-100 rounded-full overflow-hidden w-16 sm:w-24">
                          <div
                            className="h-full bg-cyan-500 rounded-full"
                            style={{ width: `${activity.quality_score}%` }}
                          ></div>
                        </div>
                        <span className="font-black text-slate-900 text-[10px] sm:text-xs text-xs">{activity.quality_score}%</span>
                      </div>
                    </td>
                    <td>
                      <button className="px-3 sm:px-4 py-1.5 sm:py-2 hover:bg-slate-50 rounded-xl transition-colors font-bold text-cyan-600 border border-slate-100 text-[10px] sm:text-xs">
                        Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
