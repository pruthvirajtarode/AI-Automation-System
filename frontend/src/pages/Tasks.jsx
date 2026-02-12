/**
 * Tasks Page Component
 * Premium task orchestration and lifecycle management
 */

import React, { useState } from 'react';

function TasksPage() {
  const [tasks, setTasks] = useState([
    { id: 1, title: 'Follow up with John Smith', assigned: 'You', status: 'pending', priority: 'high', dueDate: '2024-01-15' },
    { id: 2, title: 'Send proposal to Tech Corp', assigned: 'Sarah', status: 'in-progress', priority: 'high', dueDate: '2024-01-12' },
    { id: 3, title: 'Schedule demo call', assigned: 'Mike', status: 'completed', priority: 'medium', dueDate: '2024-01-10' },
    { id: 4, title: 'Update CRM with new leads', assigned: 'You', status: 'pending', priority: 'low', dueDate: '2024-01-20' },
    { id: 5, title: 'Prepare quarterly report', assigned: 'Emma', status: 'in-progress', priority: 'medium', dueDate: '2024-01-18' },
  ]);

  const [filterBy, setFilterBy] = useState('all');
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    assigned: 'You',
    priority: 'medium',
    dueDate: '',
  });

  const filteredTasks = tasks.filter((task) => {
    if (filterBy === 'all') return true;
    return task.status === filterBy;
  });

  const handleAddTask = () => {
    if (!formData.title.trim() || !formData.dueDate) return;

    const newTask = {
      id: Date.now(),
      ...formData,
      status: 'pending',
    };

    setTasks([newTask, ...tasks]);
    setFormData({ title: '', assigned: 'You', priority: 'medium', dueDate: '' });
    setShowModal(false);
  };

  const handleStatusChange = (taskId, newStatus) => {
    setTasks(tasks.map((task) => (task.id === taskId ? { ...task, status: newStatus } : task)));
  };

  const handleDeleteTask = (taskId) => {
    if (window.confirm('Delete this task definition?')) {
      setTasks(tasks.filter((task) => task.id !== taskId));
    }
  };

  const stats = {
    total: tasks.length,
    pending: tasks.filter((t) => t.status === 'pending').length,
    inProgress: tasks.filter((t) => t.status === 'in-progress').length,
    completed: tasks.filter((t) => t.status === 'completed').length,
  };

  const isOverdue = (dueDate) => new Date(dueDate) < new Date();

  return (
    <div className="main-content animate-fade-in">
      <div className="page-container">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
          <div>
            <h1 className="page-title">Task Orchestration</h1>
            <p className="page-subtitle">Coordinate team initiatives and monitor operational progress.</p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="btn-premium btn-premium-cyan"
          >
            + New Objective
          </button>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mb-8 sm:mb-12">
          <div className="card-premium p-4 sm:p-6">
            <p className="text-slate-400 font-bold text-[10px] sm:text-xs uppercase tracking-widest mb-1">Total Pipeline</p>
            <h3 className="text-2xl sm:text-3xl font-black text-slate-900">{stats.total}</h3>
          </div>
          <div className="card-premium p-4 sm:p-6">
            <p className="text-amber-500 font-bold text-[10px] sm:text-xs uppercase tracking-widest mb-1">Awaiting Action</p>
            <h3 className="text-2xl sm:text-3xl font-black text-slate-900">{stats.pending}</h3>
          </div>
          <div className="card-premium p-4 sm:p-6">
            <p className="text-cyan-500 font-bold text-[10px] sm:text-xs uppercase tracking-widest mb-1">In Execution</p>
            <h3 className="text-2xl sm:text-3xl font-black text-slate-900">{stats.inProgress}</h3>
          </div>
          <div className="card-premium p-4 sm:p-6">
            <p className="text-emerald-500 font-bold text-[10px] sm:text-xs uppercase tracking-widest mb-1">Finalized</p>
            <h3 className="text-2xl sm:text-3xl font-black text-slate-900">{stats.completed}</h3>
          </div>
        </div>

        {/* Filter Toolbar */}
        <div className="flex flex-wrap gap-2 sm:gap-3 mb-8 sm:mb-12 bg-white/50 p-2 rounded-2xl border border-slate-200/50 w-full sm:w-fit">
          {['all', 'pending', 'in-progress', 'completed'].map((status) => (
            <button
              key={status}
              onClick={() => setFilterBy(status)}
              className={`flex-1 sm:flex-none px-4 sm:px-6 py-2 sm:py-2.5 rounded-xl font-black text-[10px] sm:text-xs uppercase tracking-wider transition-all ${filterBy === status
                ? 'bg-slate-900 text-white shadow-lg shadow-slate-200'
                : 'text-slate-500 hover:bg-white hover:text-slate-900'
                }`}
            >
              {status.replace('-', ' ')}
            </button>
          ))}
        </div>

        {/* Task Cards */}
        <div className="grid grid-cols-1 gap-4 sm:gap-6">
          {filteredTasks.map((task) => (
            <div key={task.id} className="card-premium group hover-lift p-5 sm:p-8">
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
                <div className="flex-1">
                  <div className="flex items-start sm:items-center gap-3 sm:gap-4 mb-3">
                    <span className={`shrink-0 w-3 h-3 rounded-full mt-1.5 sm:mt-0 ${task.status === 'completed' ? 'bg-emerald-500' :
                      task.status === 'in-progress' ? 'bg-cyan-500' : 'bg-amber-500'
                      }`}></span>
                    <h3 className="text-xl sm:text-2xl font-black text-slate-900 group-hover:text-cyan-600 transition-colors leading-tight">
                      {task.title}
                    </h3>
                    <span className={`shrink-0 badge-premium hidden xs:inline-flex ${task.priority === 'high' ? 'badge-premium-warning' : 'badge-premium-info'
                      }`}>
                      {task.priority}
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-4 sm:gap-8">
                    <div className="flex items-center gap-2">
                      <div className="w-7 h-7 sm:w-8 sm:h-8 bg-slate-100 rounded-lg flex items-center justify-center text-[10px] sm:text-xs font-black text-slate-400">
                        {task.assigned.charAt(0)}
                      </div>
                      <span className="text-xs sm:text-sm font-bold text-slate-600 truncate max-w-[120px]">@{task.assigned}</span>
                    </div>
                    <div className={`flex items-center gap-2 text-[10px] sm:text-sm font-bold ${isOverdue(task.dueDate) && task.status !== 'completed' ? 'text-rose-500' : 'text-slate-400'
                      }`}>
                      <span>📅</span>
                      <span>{new Date(task.dueDate).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}</span>
                      {isOverdue(task.dueDate) && task.status !== 'completed' && <span className="bg-rose-50 px-2 py-0.5 rounded text-[8px] uppercase font-black">Overdue</span>}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 sm:gap-4 pt-4 lg:pt-0 border-t lg:border-t-0 lg:border-l border-slate-100 lg:pl-6">
                  <div className="relative flex-1 lg:flex-none">
                    <select
                      value={task.status}
                      onChange={(e) => handleStatusChange(task.id, e.target.value)}
                      className="w-full lg:w-auto form-input-premium py-2 sm:py-3 text-[10px] font-black uppercase tracking-widest appearance-none bg-slate-50 border-none cursor-pointer pr-10"
                    >
                      <option value="pending">Awaiting</option>
                      <option value="in-progress">Executing</option>
                      <option value="completed">Finalized</option>
                    </select>
                    <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-400">
                      <span className="text-xs">▼</span>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDeleteTask(task.id)}
                    className="shrink-0 w-10 h-10 flex items-center justify-center text-rose-300 hover:text-rose-500 hover:bg-rose-50 rounded-xl transition-all border border-transparent hover:border-rose-100"
                  >
                    ✕
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="modal-overlay-premium">
          <div className="modal-content-premium max-w-lg">
            <div className="modal-header-premium">
              <h2 className="text-3xl font-black text-slate-900 leading-tight">Define Perspective</h2>
            </div>
            <div className="modal-body-premium">
              <div className="space-y-6">
                <div>
                  <label className="form-label-premium">Initiative Title *</label>
                  <input
                    type="text"
                    placeholder="e.g. Technical integration review"
                    className="form-input-premium"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="form-label-premium">Owner Assignment</label>
                    <select
                      className="form-input-premium appearance-none"
                      value={formData.assigned}
                      onChange={(e) => setFormData({ ...formData, assigned: e.target.value })}
                    >
                      <option value="You">Operations (You)</option>
                      <option value="Sarah">Sarah J.</option>
                      <option value="Mike">Mike D.</option>
                      <option value="Emma">Emma W.</option>
                    </select>
                  </div>
                  <div>
                    <label className="form-label-premium">Priority Level</label>
                    <select
                      className="form-input-premium appearance-none"
                      value={formData.priority}
                      onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    >
                      <option value="low">Low Impact</option>
                      <option value="medium">Medium Urgency</option>
                      <option value="high">Critical Path</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="form-label-premium">Target Date *</label>
                  <input
                    type="date"
                    className="form-input-premium"
                    value={formData.dueDate}
                    onChange={(e) => setFormData({ ...formData, dueDate: e.target.value })}
                  />
                </div>
              </div>
            </div>
            <div className="modal-footer-premium">
              <button
                onClick={() => setShowModal(false)}
                className="btn-premium btn-premium-white"
              >
                Discard
              </button>
              <button
                onClick={handleAddTask}
                className="btn-premium btn-premium-cyan"
              >
                Launch Initiative
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default TasksPage;
