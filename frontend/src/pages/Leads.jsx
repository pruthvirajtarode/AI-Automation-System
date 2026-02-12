/**
 * Leads Page Component
 * Premium lead management interface
 */

import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { FormValidator } from '../utils/validation';

function LeadsPage() {
  const location = useLocation();
  const [leads, setLeads] = useState([
    { id: 1, customer: { name: 'John Smith', company: 'Tech Corp' }, status: 'qualified', priority: 'high', quality_score: 85 },
    { id: 2, customer: { name: 'Sarah Johnson', company: 'Finance Ltd' }, status: 'contacted', priority: 'medium', quality_score: 72 },
    { id: 3, customer: { name: 'Mike Davis', company: 'Design Co' }, status: 'new', priority: 'low', quality_score: 45 },
  ]);
  const [filters, setFilters] = useState({ status: 'all', priority: 'all', search: '' });
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({ name: '', email: '', company: '', phone: '' });
  const [formErrors, setFormErrors] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    if (params.get('add') === 'true') {
      setShowModal(true);
    }
  }, [location]);

  const validator = new FormValidator();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    if (formErrors[name]) {
      setFormErrors({ ...formErrors, [name]: null });
    }
  };

  const handleAddLead = () => {
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
      const newLead = {
        id: leads.length + 1,
        customer: { name: formData.name, company: formData.company },
        status: 'new',
        priority: 'medium',
        quality_score: 50,
      };
      setLeads([newLead, ...leads]);
      setFormData({ name: '', email: '', company: '', phone: '' });
      setShowModal(false);
      setLoading(false);
    }, 800);
  };

  const filteredLeads = leads.filter((lead) => {
    const statusMatch = filters.status === 'all' || lead.status === filters.status;
    const priorityMatch = filters.priority === 'all' || lead.priority === filters.priority;
    const searchMatch = lead.customer.name.toLowerCase().includes(filters.search.toLowerCase()) ||
      lead.customer.company.toLowerCase().includes(filters.search.toLowerCase());
    return statusMatch && priorityMatch && searchMatch;
  });

  return (
    <div className="main-content animate-fade-in">
      <div className="page-container">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
          <div>
            <h1 className="page-title">Lead Intelligence</h1>
            <p className="page-subtitle">Track, analyze and convert your high-value opportunities.</p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="btn-premium btn-premium-cyan"
          >
            + Register New Lead
          </button>
        </div>

        {/* Filters */}
        <div className="card-premium mb-8 sm:mb-12">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 items-end">
            <div className="sm:col-span-2">
              <label className="form-label-premium">Search Intelligence</label>
              <input
                type="text"
                placeholder="Search identity..."
                className="form-input-premium"
                value={filters.search}
                onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              />
            </div>
            <div>
              <label className="form-label-premium">Status</label>
              <select
                className="form-input-premium appearance-none"
                value={filters.status}
                onChange={(e) => setFilters({ ...filters, status: e.target.value })}
              >
                <option value="all">All Statuses</option>
                <option value="new">Uncontacted</option>
                <option value="contacted">In Discussion</option>
                <option value="qualified">Qualified</option>
              </select>
            </div>
            <button
              onClick={() => setFilters({ status: 'all', priority: 'all', search: '' })}
              className="btn-premium btn-premium-white w-full sm:w-auto"
            >
              Reset
            </button>
          </div>
        </div>

        {/* Leads Table */}
        <div className="card-premium p-0 overflow-hidden">
          <div className="overflow-x-auto p-2 sm:p-4">
            <table className="table-premium min-w-[800px] lg:min-w-full">
              <thead>
                <tr>
                  <th>Identity</th>
                  <th>Organization</th>
                  <th>Intelligence Status</th>
                  <th>Confidence</th>
                  <th className="text-right">Management</th>
                </tr>
              </thead>
              <tbody>
                {filteredLeads.map((lead) => (
                  <tr key={lead.id}>
                    <td>
                      <div className="flex items-center gap-4">
                        <div className="w-10 h-10 bg-slate-100 rounded-xl flex items-center justify-center font-black text-slate-400 text-xs">
                          {lead.customer?.name.charAt(0)}
                        </div>
                        <span className="font-black text-slate-900">{lead.customer?.name}</span>
                      </div>
                    </td>
                    <td><span className="font-bold text-slate-600">{lead.customer?.company}</span></td>
                    <td>
                      <span className={`badge-premium ${lead.status === 'qualified' ? 'badge-premium-success' :
                        lead.status === 'contacted' ? 'badge-premium-info' :
                          'badge-premium-warning'
                        }`}>
                        {lead.status}
                      </span>
                    </td>
                    <td>
                      <div className="flex items-center gap-3">
                        <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden w-20 sm:w-24">
                          <div
                            className={`h-full rounded-full ${lead.quality_score > 70 ? 'bg-emerald-500' :
                              lead.quality_score > 40 ? 'bg-amber-500' : 'bg-rose-500'
                              }`}
                            style={{ width: `${lead.quality_score}%` }}
                          ></div>
                        </div>
                        <span className="font-black text-slate-900 text-xs">{lead.quality_score}%</span>
                      </div>
                    </td>
                    <td className="text-right">
                      <div className="flex justify-end gap-2 pr-2">
                        <button className="px-3 py-1.5 hover:bg-slate-50 transition-all rounded-xl border border-slate-100 font-bold text-slate-600 text-[10px] uppercase">
                          Engage
                        </button>
                        <button className="px-3 py-1.5 bg-slate-900 text-white hover:bg-slate-800 transition-all rounded-xl font-bold text-[10px] uppercase shadow-lg">
                          Insight
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
          <div className="modal-content-premium max-w-lg">
            <div className="modal-header-premium">
              <h2 className="text-3xl font-black text-slate-900 leading-tight">Identify New Opportunity</h2>
            </div>
            <div className="modal-body-premium">
              <div className="space-y-6">
                <div>
                  <label className="form-label-premium">Lead Full Identity *</label>
                  <input
                    type="text"
                    name="name"
                    placeholder="e.g. Johnathan Smith"
                    className="form-input-premium"
                    value={formData.name}
                    onChange={handleInputChange}
                  />
                  {formErrors.name && <p className="text-rose-500 text-xs font-black mt-2 ml-1">{formErrors.name[0]}</p>}
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="form-label-premium">Corporate Email *</label>
                    <input
                      type="email"
                      name="email"
                      placeholder="name@company.com"
                      className="form-input-premium"
                      value={formData.email}
                      onChange={handleInputChange}
                    />
                    {formErrors.email && <p className="text-rose-500 text-xs font-black mt-2 ml-1">Valid email required</p>}
                  </div>
                  <div>
                    <label className="form-label-premium">Phone Reference</label>
                    <input
                      type="tel"
                      name="phone"
                      placeholder="+1 (555) 000-0000"
                      className="form-input-premium"
                      value={formData.phone}
                      onChange={handleInputChange}
                    />
                  </div>
                </div>

                <div>
                  <label className="form-label-premium">Organization / Entity *</label>
                  <input
                    type="text"
                    name="company"
                    placeholder="Company Legal Name"
                    className="form-input-premium"
                    value={formData.company}
                    onChange={handleInputChange}
                  />
                  {formErrors.company && <p className="text-rose-500 text-xs font-black mt-2 ml-1">Entity name required</p>}
                </div>
              </div>
            </div>
            <div className="modal-footer-premium">
              <button
                onClick={() => {
                  setShowModal(false);
                  setFormErrors({});
                }}
                className="btn-premium btn-premium-white"
              >
                Cancel
              </button>
              <button
                onClick={handleAddLead}
                disabled={loading}
                className="btn-premium btn-premium-cyan"
              >
                {loading ? 'Processing...' : 'Register Opportunity'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default LeadsPage;
