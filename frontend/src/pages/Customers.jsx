/**
 * Customers Page Component
 * Premium customer relationship management
 */

import React, { useState } from 'react';
import { FormValidator } from '../utils/validation';

function CustomersPage() {
  const [customers, setCustomers] = useState([
    { id: 1, name: 'Alex Thompson', email: 'alex@techcorp.com', company: 'Tech Corp', phone: '555-1234', status: 'active', tier: 'premium' },
    { id: 2, name: 'Emma Wilson', email: 'emma@finance.com', company: 'Finance Ltd', phone: '555-5678', status: 'active', tier: 'standard' },
    { id: 3, name: 'David Chen', email: 'david@startup.io', company: 'StartUp Inc', phone: '555-9101', status: 'inactive', tier: 'basic' },
  ]);

  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [tierFilter, setTierFilter] = useState('all');
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    phone: '',
    status: 'active',
    tier: 'standard',
  });

  const validator = new FormValidator();

  const openModal = (customer = null) => {
    if (customer) {
      setFormData(customer);
      setEditingId(customer.id);
    } else {
      setFormData({
        name: '',
        email: '',
        company: '',
        phone: '',
        status: 'active',
        tier: 'standard',
      });
      setEditingId(null);
    }
    setFormErrors({});
    setShowModal(true);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    if (formErrors[name]) {
      setFormErrors({ ...formErrors, [name]: null });
    }
  };

  const handleSaveCustomer = () => {
    const schema = {
      name: { required: true, minLength: 2 },
      email: { required: true, type: 'email' },
      company: { required: true },
      phone: { required: true },
    };

    if (!validator.validate(formData, schema)) {
      setFormErrors(validator.getErrors());
      return;
    }

    setLoading(true);
    setTimeout(() => {
      if (editingId) {
        setCustomers(customers.map((c) => (c.id === editingId ? { ...formData, id: editingId } : c)));
      } else {
        setCustomers([{ ...formData, id: Date.now() }, ...customers]);
      }
      setShowModal(false);
      setLoading(false);
    }, 800);
  };

  const handleDeleteCustomer = (id) => {
    if (window.confirm('Terminate customer relationship records?')) {
      setCustomers(customers.filter((c) => c.id !== id));
    }
  };

  const filteredCustomers = customers.filter((customer) => {
    const searchMatch =
      customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      customer.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      customer.company.toLowerCase().includes(searchTerm.toLowerCase());
    const statusMatch = statusFilter === 'all' || customer.status === statusFilter;
    const tierMatch = tierFilter === 'all' || customer.tier === tierFilter;
    return searchMatch && statusMatch && tierMatch;
  });

  return (
    <div className="main-content animate-fade-in">
      <div className="page-container">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
          <div>
            <h1 className="page-title">Entity Directory</h1>
            <p className="page-subtitle">Unified database of all active and historical customer profiles.</p>
          </div>
          <button
            onClick={() => openModal()}
            className="btn-premium btn-premium-cyan"
          >
            + Register New Entity
          </button>
        </div>

        {/* Filters */}
        <div className="card-premium mb-8 sm:mb-12">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 items-end">
            <div className="sm:col-span-2">
              <label className="form-label-premium">Profile Search</label>
              <input
                type="text"
                placeholder="Name, email, organization..."
                className="form-input-premium"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div>
              <label className="form-label-premium">Lifecycle Stage</label>
              <select
                className="form-input-premium appearance-none"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <option value="all">Global (All)</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
            <button
              onClick={() => {
                setSearchTerm('');
                setStatusFilter('all');
                setTierFilter('all');
              }}
              className="btn-premium btn-premium-white w-full sm:w-auto"
            >
              Reset
            </button>
          </div>
        </div>

        {/* Table */}
        <div className="card-premium p-0 overflow-hidden">
          <div className="overflow-x-auto p-2 sm:p-4">
            <table className="table-premium min-w-[900px] lg:min-w-full">
              <thead>
                <tr>
                  <th>Identity</th>
                  <th>Affiliation</th>
                  <th>Communication</th>
                  <th>Lifecycle</th>
                  <th>Tier</th>
                  <th className="text-right">Management</th>
                </tr>
              </thead>
              <tbody>
                {filteredCustomers.map((customer) => (
                  <tr key={customer.id}>
                    <td>
                      <div className="flex items-center gap-4">
                        <div className="w-10 h-10 bg-slate-100 rounded-xl flex items-center justify-center font-black text-slate-400 text-xs">
                          {customer.name.charAt(0)}
                        </div>
                        <div>
                          <p className="font-black text-slate-900 leading-tight">{customer.name}</p>
                          <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Verified Entity</p>
                        </div>
                      </div>
                    </td>
                    <td><span className="font-bold text-slate-600">{customer.company}</span></td>
                    <td>
                      <p className="text-sm font-bold text-slate-800">{customer.email}</p>
                      <p className="text-[10px] text-slate-400 font-medium">{customer.phone}</p>
                    </td>
                    <td>
                      <span className={`badge-premium ${customer.status === 'active' ? 'badge-premium-success' : 'badge-premium-warning'}`}>
                        {customer.status}
                      </span>
                    </td>
                    <td>
                      <span className={`badge-premium ${customer.tier === 'premium' ? 'badge-premium-info' :
                        customer.tier === 'standard' ? 'badge-premium-cyan' :
                          'badge-premium-white border border-slate-200'
                        }`}>
                        {customer.tier}
                      </span>
                    </td>
                    <td className="text-right">
                      <div className="flex justify-end gap-2 pr-2">
                        <button
                          onClick={() => openModal(customer)}
                          className="w-9 h-9 flex items-center justify-center hover:bg-cyan-50 text-cyan-500 rounded-xl transition-colors border border-transparent hover:border-cyan-100"
                        >
                          ✎
                        </button>
                        <button
                          onClick={() => handleDeleteCustomer(customer.id)}
                          className="w-9 h-9 flex items-center justify-center hover:bg-rose-50 text-rose-500 rounded-xl transition-colors border border-transparent hover:border-rose-100"
                        >
                          ✕
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="modal-overlay-premium">
          <div className="modal-content-premium max-w-xl">
            <div className="modal-header-premium">
              <h2 className="text-3xl font-black text-slate-900 leading-tight">
                {editingId ? 'Edit Profile Definition' : 'Define New Entity'}
              </h2>
            </div>
            <div className="modal-body-premium">
              <div className="space-y-6">
                <div>
                  <label className="form-label-premium">Full Legal Name *</label>
                  <input
                    type="text"
                    name="name"
                    className="form-input-premium"
                    value={formData.name}
                    onChange={handleInputChange}
                  />
                  {formErrors.name && <p className="text-rose-500 text-xs font-black mt-2">{formErrors.name[0]}</p>}
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="form-label-premium">Contact Email *</label>
                    <input
                      type="email"
                      name="email"
                      className="form-input-premium"
                      value={formData.email}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div>
                    <label className="form-label-premium">Contact Phone *</label>
                    <input
                      type="tel"
                      name="phone"
                      className="form-input-premium"
                      value={formData.phone}
                      onChange={handleInputChange}
                    />
                  </div>
                </div>

                <div>
                  <label className="form-label-premium">Organization Affiliation *</label>
                  <input
                    type="text"
                    name="company"
                    className="form-input-premium"
                    value={formData.company}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="form-label-premium">Operational Status</label>
                    <select
                      name="status"
                      className="form-input-premium appearance-none"
                      value={formData.status}
                      onChange={handleInputChange}
                    >
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                    </select>
                  </div>
                  <div>
                    <label className="form-label-premium">Account Tier</label>
                    <select
                      name="tier"
                      className="form-input-premium appearance-none"
                      value={formData.tier}
                      onChange={handleInputChange}
                    >
                      <option value="premium">Premium Intelligence</option>
                      <option value="standard">Standard Operation</option>
                      <option value="basic">Baseline Profile</option>
                    </select>
                  </div>
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
                onClick={handleSaveCustomer}
                disabled={loading}
                className="btn-premium btn-premium-cyan"
              >
                {loading ? 'Processing...' : editingId ? 'Commit Changes' : 'Initialize Profile'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default CustomersPage;
