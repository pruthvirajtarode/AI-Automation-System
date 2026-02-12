/**
 * Bookings Page Component
 * Premium operational scheduling and meeting orchestration
 */

import React, { useState } from 'react';
import { FormValidator } from '../utils/validation';

function BookingsPage() {
  const [bookings, setBookings] = useState([
    { id: 1, title: 'Demo Call - Tech Corp', customer: 'John Smith', date: '2024-01-15', time: '10:00 AM', duration: '30 min', status: 'confirmed', meetingLink: 'https://meet.google.com/abc-123' },
    { id: 2, title: 'Product Review', customer: 'Sarah Johnson', date: '2024-01-16', time: '2:00 PM', duration: '1 hour', status: 'confirmed', meetingLink: 'https://meet.google.com/def-456' },
    { id: 3, title: 'Follow-up Discussion', customer: 'Mike Davis', date: '2024-01-17', time: '11:00 AM', duration: '30 min', status: 'pending', meetingLink: '' },
  ]);

  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    customer: '',
    date: '',
    time: '',
    duration: '30 min',
    meetingLink: '',
  });
  const [formErrors, setFormErrors] = useState({});
  const validator = new FormValidator();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    if (formErrors[name]) {
      setFormErrors({ ...formErrors, [name]: null });
    }
  };

  const handleAddBooking = () => {
    const schema = {
      title: { required: true, minLength: 5 },
      customer: { required: true },
      date: { required: true },
      time: { required: true },
    };

    if (!validator.validate(formData, schema)) {
      setFormErrors(validator.getErrors());
      return;
    }

    const newBooking = {
      id: Date.now(),
      ...formData,
      status: 'pending',
    };

    setBookings([newBooking, ...bookings]);
    setFormData({ title: '', customer: '', date: '', time: '', duration: '30 min', meetingLink: '' });
    setShowModal(false);
  };

  const handleConfirmBooking = (id) => {
    setBookings(bookings.map((b) => (b.id === id ? { ...b, status: 'confirmed' } : b)));
  };

  const handleCancelBooking = (id) => {
    if (window.confirm('Terminate this operational scheduling record?')) {
      setBookings(bookings.filter((b) => b.id !== id));
    }
  };

  const filteredBookings = bookings.filter((booking) => {
    const searchMatch =
      booking.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      booking.customer.toLowerCase().includes(searchTerm.toLowerCase());
    const statusMatch = statusFilter === 'all' || booking.status === statusFilter;
    return searchMatch && statusMatch;
  });

  const upcomingCount = bookings.filter((b) => new Date(b.date) >= new Date()).length;

  return (
    <div className="main-content animate-fade-in">
      <div className="page-container">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
          <div>
            <h1 className="page-title">Meeting Orchestration</h1>
            <p className="page-subtitle">Strategic scheduling and high-value interaction management.</p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="btn-premium btn-premium-cyan"
          >
            + Initialize Engagement
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mb-8 sm:mb-12">
          <div className="card-premium p-4 sm:p-6">
            <p className="text-slate-400 font-bold text-[10px] sm:text-xs uppercase tracking-widest mb-1">Active Records</p>
            <h3 className="text-2xl sm:text-3xl font-black text-slate-900">{bookings.length}</h3>
          </div>
          <div className="card-premium p-4 sm:p-6">
            <p className="text-cyan-500 font-bold text-[10px] sm:text-xs uppercase tracking-widest mb-1">Upcoming</p>
            <h3 className="text-2xl sm:text-3xl font-black text-slate-900">{upcomingCount}</h3>
          </div>
          <div className="card-premium p-4 sm:p-6">
            <p className="text-emerald-500 font-bold text-[10px] sm:text-xs uppercase tracking-widest mb-1">Confirmed</p>
            <h3 className="text-2xl sm:text-3xl font-black text-slate-900">{bookings.filter(b => b.status === 'confirmed').length}</h3>
          </div>
          <div className="card-premium p-4 sm:p-6">
            <p className="text-amber-500 font-bold text-[10px] sm:text-xs uppercase tracking-widest mb-1">Pending</p>
            <h3 className="text-2xl sm:text-3xl font-black text-slate-900">{bookings.filter(b => b.status === 'pending').length}</h3>
          </div>
        </div>

        {/* Filter Toolbar */}
        <div className="card-premium mb-8 sm:mb-12 p-3 sm:p-4">
          <div className="flex flex-col lg:flex-row gap-4 sm:gap-6">
            <div className="flex-1">
              <input
                type="text"
                placeholder="Search meeting or customer..."
                className="form-input-premium py-2 sm:py-3 text-sm"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div className="flex flex-col sm:flex-row gap-4 w-full lg:w-auto">
              <div className="relative w-full sm:w-64">
                <select
                  className="w-full form-input-premium appearance-none py-2 sm:py-3 text-sm"
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <option value="all">Global Status</option>
                  <option value="pending">Awaiting (Pending)</option>
                  <option value="confirmed">Validated (Confirmed)</option>
                </select>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-400">
                  <span className="text-xs">▼</span>
                </div>
              </div>
              <button
                onClick={() => { setSearchTerm(''); setStatusFilter('all'); }}
                className="btn-premium btn-premium-white px-8 py-2 sm:py-3 w-full sm:w-auto"
              >
                Reset
              </button>
            </div>
          </div>
        </div>

        {/* Bookings Display */}
        <div className="grid grid-cols-1 gap-4 sm:gap-6">
          {filteredBookings.map((booking) => (
            <div key={booking.id} className="card-premium group hover-lift p-5 sm:p-8">
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 lg:gap-8">
                <div className="flex-1">
                  <div className="flex items-start sm:items-center gap-4 mb-6">
                    <div className="shrink-0 w-12 h-12 sm:w-14 sm:h-14 bg-slate-50 rounded-2xl flex items-center justify-center text-xl sm:text-2xl shadow-sm border border-slate-100 group-hover:bg-cyan-500 group-hover:text-white transition-colors">
                      📅
                    </div>
                    <div>
                      <h3 className="text-xl sm:text-2xl font-black text-slate-900 group-hover:text-cyan-600 transition-colors leading-tight">
                        {booking.title}
                      </h3>
                      <div className="flex flex-wrap items-center gap-x-4 gap-y-2 mt-1">
                        <span className="text-xs sm:text-sm font-bold text-slate-400">Interaction with: <span className="text-slate-900">{booking.customer}</span></span>
                        <span className={`badge-premium ${booking.status === 'confirmed' ? 'badge-premium-success' : 'badge-premium-warning'}`}>
                          {booking.status}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 sm:gap-8 lg:pl-18">
                    <div>
                      <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest mb-1">Target Date</p>
                      <p className="text-sm font-black text-slate-700">{new Date(booking.date).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })}</p>
                    </div>
                    <div>
                      <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest mb-1">Launch Time</p>
                      <p className="text-sm font-black text-slate-700">{booking.time}</p>
                    </div>
                    <div>
                      <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest mb-1">Duration</p>
                      <p className="text-sm font-black text-slate-700">{booking.duration}</p>
                    </div>
                    <div className="col-span-2 sm:col-span-1">
                      {booking.meetingLink ? (
                        <a href={booking.meetingLink} target="_blank" rel="noreferrer" className="w-full inline-flex items-center justify-center gap-2 bg-cyan-50 text-cyan-600 px-4 py-2 rounded-xl font-black text-[10px] sm:text-xs hover:bg-cyan-100 transition-colors uppercase">
                          <span>🔗</span> JOIN CHANNEL
                        </a>
                      ) : (
                        <span className="text-slate-300 font-bold text-[10px] italic">Channel URL Pending</span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="flex lg:flex-col gap-3 pt-6 lg:pt-0 border-t lg:border-t-0 lg:border-l border-slate-100 lg:pl-8 lg:min-w-[220px]">
                  {booking.status === 'pending' && (
                    <button
                      onClick={() => handleConfirmBooking(booking.id)}
                      className="flex-1 lg:flex-none py-3 sm:py-4 bg-slate-900 text-white rounded-2xl font-black text-[10px] sm:text-xs hover:bg-slate-800 shadow-xl shadow-slate-200 transition-all uppercase tracking-widest"
                    >
                      VALIDATE MEETING
                    </button>
                  )}
                  <button
                    onClick={() => handleCancelBooking(booking.id)}
                    className="flex-1 lg:flex-none py-3 sm:py-4 bg-white text-rose-500 border border-rose-100 rounded-2xl font-black text-[10px] sm:text-xs hover:bg-rose-50 transition-all uppercase tracking-widest"
                  >
                    TERMINATE RECORD
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
          <div className="modal-content-premium max-w-xl">
            <div className="modal-header-premium">
              <h2 className="text-3xl font-black text-slate-900 leading-tight">Channel Initialization</h2>
            </div>
            <div className="modal-body-premium">
              <div className="space-y-6">
                <div>
                  <label className="form-label-premium">Meeting Protocol Name *</label>
                  <input
                    type="text"
                    name="title"
                    placeholder="e.g. Strategic Integration Review"
                    className="form-input-premium"
                    value={formData.title}
                    onChange={handleInputChange}
                  />
                  {formErrors.title && <p className="text-rose-500 text-xs font-black mt-2">{formErrors.title[0]}</p>}
                </div>

                <div>
                  <label className="form-label-premium">Customer Entity *</label>
                  <input
                    type="text"
                    name="customer"
                    className="form-input-premium"
                    value={formData.customer}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="form-label-premium">Target Date *</label>
                    <input type="date" name="date" className="form-input-premium" value={formData.date} onChange={handleInputChange} />
                  </div>
                  <div>
                    <label className="form-label-premium">Launch Time *</label>
                    <input type="time" name="time" className="form-input-premium" value={formData.time} onChange={handleInputChange} />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="form-label-premium">Duration Window</label>
                    <select name="duration" className="form-input-premium appearance-none" value={formData.duration} onChange={handleInputChange}>
                      <option value="15 min">15 minutes (Rapid Sync)</option>
                      <option value="30 min">30 minutes (Standard)</option>
                      <option value="1 hour">1 hour (Deep Review)</option>
                      <option value="2 hours">2 hours (Workshop)</option>
                    </select>
                  </div>
                  <div>
                    <label className="form-label-premium">Communication Link</label>
                    <input type="url" name="meetingLink" placeholder="Zoom/Meet URL" className="form-input-premium" value={formData.meetingLink} onChange={handleInputChange} />
                  </div>
                </div>
              </div>
            </div>
            <div className="modal-footer-premium">
              <button onClick={() => setShowModal(false)} className="btn-premium btn-premium-white">Discard</button>
              <button onClick={handleAddBooking} className="btn-premium btn-premium-cyan">Finalize Schedule</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default BookingsPage;
