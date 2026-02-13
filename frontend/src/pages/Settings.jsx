/**
 * Settings Page Component
 * System orchestration and global configuration
 */

import React, { useState } from 'react';
import { FormValidator } from '../utils/validation';
import {
  HiBuildingOffice2,
  HiKey,
  HiBell
} from "react-icons/hi2";

function SettingsPage() {
  const [activeTab, setActiveTab] = useState('general');
  const [saveStatus, setSaveStatus] = useState('');

  // ... (previous state declarations stay the same)
  const [general, setGeneral] = useState({
    companyName: 'Tech Sales Inc',
    email: 'admin@techsales.com',
    phone: '555-0100',
    website: 'https://techsales.com',
    timezone: 'UTC',
    language: 'English',
  });

  const [api, setApi] = useState({
    apiKey: 'sk_live_51PzaE1I4rZ9...',
    secretKey: 'wh_secret_82x1... ',
    webhookUrl: 'https://api.techsales.com/webhooks',
    enableWebhooks: true,
  });

  const [notifications, setNotifications] = useState({
    emailNotifications: true,
    smsNotifications: false,
    leadAlerts: true,
    taskReminders: true,
    meetingReminders: true,
    newsDigest: true,
  });

  const [formErrors, setFormErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const validator = new FormValidator();

  const handleGeneralChange = (field, value) => {
    setGeneral({ ...general, [field]: value });
    if (formErrors[field]) setFormErrors({ ...formErrors, [field]: null });
  };

  const notifyProgress = (callback) => {
    setLoading(true);
    setTimeout(() => {
      setSaveStatus('success');
      setLoading(false);
      setTimeout(() => setSaveStatus(''), 4000);
      if (callback) callback();
    }, 800);
  };

  const handleSaveGeneral = () => {
    const schema = {
      companyName: { required: true },
      email: { required: true, type: 'email' },
      phone: { required: true },
    };
    if (!validator.validate(general, schema)) {
      setFormErrors(validator.getErrors());
      return;
    }
    notifyProgress();
  };

  return (
    <div className="main-content animate-fade-in">
      <div className="page-container max-w-5xl">
        {/* Header */}
        <div className="mb-8 sm:mb-12 flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <h1 className="page-title">System Configuration</h1>
            <p className="page-subtitle">Calibrate your operational parameters and global settings.</p>
          </div>
          {saveStatus === 'success' && (
            <div className="bg-emerald-50 text-emerald-600 px-6 py-2 rounded-2xl font-black text-[10px] uppercase tracking-widest animate-bounce w-fit">
              ✓ Synchronized
            </div>
          )}
        </div>

        {/* Tab Navigation */}
        <div className="overflow-x-auto pb-4 sm:pb-0 mb-8 sm:mb-12 -mx-4 px-4 sm:mx-0 sm:px-0">
          <div className="flex gap-3 sm:gap-4 bg-slate-100/50 p-2 rounded-2xl sm:rounded-[2rem] w-fit min-w-full sm:min-w-0">
            {[
              { id: 'general', label: 'Core Identity', icon: HiBuildingOffice2, color: 'text-cyan-500' },
              { id: 'api', label: 'Integration API', icon: HiKey, color: 'text-indigo-500' },
              { id: 'notifications', label: 'Intelligence Alerts', icon: HiBell, color: 'text-rose-500' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 sm:gap-3 px-3 sm:px-8 py-2.5 sm:py-3.5 rounded-xl sm:rounded-[1.5rem] font-black text-[10px] sm:text-xs uppercase tracking-wider transition-all whitespace-nowrap ${activeTab === tab.id
                  ? 'bg-white text-slate-900 shadow-xl shadow-slate-200 scale-105'
                  : 'text-slate-500 hover:text-slate-900'
                  }`}
              >
                <tab.icon className={`text-base sm:text-lg ${activeTab === tab.id ? tab.color : 'text-slate-400'}`} style={{ filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))' }} />
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Settings Content */}
        <div className="card-premium p-4 sm:p-10">
          {activeTab === 'general' && (
            <div className="space-y-10">
              <div className="border-b border-slate-100 pb-6">
                <h3 className="text-2xl font-black text-slate-900 mb-1">General Protocol</h3>
                <p className="text-slate-400 text-sm font-bold uppercase tracking-widest">Base Identity Configuration</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <label className="form-label-premium">Corporate Entity Designation *</label>
                  <input
                    type="text"
                    className="form-input-premium"
                    value={general.companyName}
                    onChange={(e) => handleGeneralChange('companyName', e.target.value)}
                  />
                  {formErrors.companyName && <p className="text-rose-500 text-xs font-black mt-2">{formErrors.companyName[0]}</p>}
                </div>
                <div>
                  <label className="form-label-premium">Operational Domain (URL)</label>
                  <input
                    type="url"
                    className="form-input-premium"
                    value={general.website}
                    onChange={(e) => handleGeneralChange('website', e.target.value)}
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <label className="form-label-premium">Primary Communications Email *</label>
                  <input
                    type="email"
                    className="form-input-premium"
                    value={general.email}
                    onChange={(e) => handleGeneralChange('email', e.target.value)}
                  />
                </div>
                <div>
                  <label className="form-label-premium">Voice/SMS Uplink</label>
                  <input
                    type="tel"
                    className="form-input-premium"
                    value={general.phone}
                    onChange={(e) => handleGeneralChange('phone', e.target.value)}
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <label className="form-label-premium">Temporal Synchronization (Timezone)</label>
                  <select className="form-input-premium appearance-none" value={general.timezone} onChange={(e) => handleGeneralChange('timezone', e.target.value)}>
                    <option value="UTC">UTC (Standard)</option>
                    <option value="EST">Eastern Time</option>
                    <option value="PST">Pacific Time</option>
                  </select>
                </div>
                <div>
                  <label className="form-label-premium">Linguistic Protocol</label>
                  <select className="form-input-premium appearance-none" value={general.language} onChange={(e) => handleGeneralChange('language', e.target.value)}>
                    <option value="English">English (Global)</option>
                    <option value="Spanish">Spanish</option>
                    <option value="French">French</option>
                  </select>
                </div>
              </div>

              <div className="pt-8 border-t border-slate-100 flex gap-4">
                <button onClick={handleSaveGeneral} disabled={loading} className="btn-premium btn-premium-primary px-12">
                  {loading ? 'Synchronizing...' : 'Save Configuration'}
                </button>
                <button className="btn-premium btn-premium-white px-8">Reset Defaults</button>
              </div>
            </div>
          )}

          {activeTab === 'api' && (
            <div className="space-y-10">
              <div className="border-b border-slate-100 pb-6">
                <h3 className="text-2xl font-black text-slate-900 mb-1">Integration Layer</h3>
                <p className="text-slate-400 text-sm font-bold uppercase tracking-widest">Interface & Protocol Keys</p>
              </div>

              <div className="bg-amber-50 p-6 rounded-3xl border border-amber-100 flex gap-6 items-start">
                <div className="text-2xl">⚠️</div>
                <p className="text-amber-800 text-sm font-bold leading-relaxed">
                  Cryptographic keys provide direct access to your subsystem. Ensure isolation within your CI/CD pipeline and never leak keys to client-side environments.
                </p>
              </div>

              <div className="space-y-8">
                <div>
                  <label className="form-label-premium">Public Interface Key (API KEY)</label>
                  <div className="flex gap-4">
                    <input type="password" readOnly value={api.apiKey} className="form-input-premium flex-1 font-mono tracking-widest" />
                    <button className="btn-premium btn-premium-white px-6">Reveal</button>
                    <button className="btn-premium btn-premium-white px-6">Rotate</button>
                  </div>
                </div>

                <div>
                  <label className="form-label-premium">Subsystem Webhook Endpoint</label>
                  <input
                    type="url"
                    placeholder="https://your-server.com/webhooks"
                    className="form-input-premium"
                    value={api.webhookUrl}
                    onChange={(e) => setApi({ ...api, webhookUrl: e.target.value })}
                  />
                </div>

                <div className="flex items-center gap-4 bg-slate-50 p-6 rounded-3xl">
                  <div className={`w-12 h-6 rounded-full transition-all cursor-pointer relative ${api.enableWebhooks ? 'bg-cyan-500' : 'bg-slate-300'}`} onClick={() => setApi({ ...api, enableWebhooks: !api.enableWebhooks })}>
                    <div className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${api.enableWebhooks ? 'left-7' : 'left-1'}`}></div>
                  </div>
                  <div>
                    <p className="text-sm font-black text-slate-900">Active Webhook Pipeline</p>
                    <p className="text-xs text-slate-400 font-bold uppercase tracking-widest">Toggle real-time event streaming</p>
                  </div>
                </div>
              </div>

              <div className="pt-8 border-t border-slate-100">
                <button onClick={() => notifyProgress()} disabled={loading} className="btn-premium btn-premium-cyan px-12">
                  Update API Layer
                </button>
              </div>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="space-y-10">
              <div className="border-b border-slate-100 pb-6">
                <h3 className="text-2xl font-black text-slate-900 mb-1">Intelligence Relay</h3>
                <p className="text-slate-400 text-sm font-bold uppercase tracking-widest">Automated Alerting Protocols</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                <div className="space-y-8">
                  <h4 className="text-xs font-black text-slate-400 uppercase tracking-widest mb-6 border-l-4 border-cyan-500 pl-4">Channel Routing</h4>
                  {[
                    { key: 'emailNotifications', label: 'Electronic Mail (SMTP)', icon: '📧' },
                    { key: 'smsNotifications', label: 'Cellular Uplink (SMS)', icon: '📱' }
                  ].map((chan) => (
                    <div key={chan.key} className="flex items-center justify-between p-4 hover:bg-slate-50 rounded-2xl transition-all cursor-pointer" onClick={() => setNotifications({ ...notifications, [chan.key]: !notifications[chan.key] })}>
                      <div className="flex items-center gap-4">
                        <span className="text-xl">{chan.icon}</span>
                        <span className="font-black text-slate-900 text-sm uppercase tracking-wider">{chan.label}</span>
                      </div>
                      <div className={`w-10 h-5 rounded-full transition-all relative ${notifications[chan.key] ? 'bg-emerald-500' : 'bg-slate-200'}`}>
                        <div className={`absolute top-0.5 w-4 h-4 bg-white rounded-full transition-all ${notifications[chan.key] ? 'left-5.5' : 'left-0.5'}`}></div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="space-y-8">
                  <h4 className="text-xs font-black text-slate-400 uppercase tracking-widest mb-6 border-l-4 border-amber-500 pl-4">Trigger Sensitivity</h4>
                  {[
                    { key: 'leadAlerts', label: 'Lead Ingestion Pulse' },
                    { key: 'taskReminders', label: 'Task Execution Sync' },
                    { key: 'meetingReminders', label: 'Meeting Initialization' }
                  ].map((trigger) => (
                    <div key={trigger.key} className="flex items-center justify-between p-4 hover:bg-slate-50 rounded-2xl transition-all cursor-pointer" onClick={() => setNotifications({ ...notifications, [trigger.key]: !notifications[trigger.key] })}>
                      <span className="font-black text-slate-700 text-sm uppercase tracking-wider">{trigger.label}</span>
                      <div className={`w-10 h-5 rounded-full transition-all relative ${notifications[trigger.key] ? 'bg-amber-500' : 'bg-slate-200'}`}>
                        <div className={`absolute top-0.5 w-4 h-4 bg-white rounded-full transition-all ${notifications[trigger.key] ? 'left-5.5' : 'left-0.5'}`}></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-8 border-t border-slate-100">
                <button onClick={() => notifyProgress()} disabled={loading} className="btn-premium btn-premium-primary px-12">
                  Save Relay Preferences
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SettingsPage;
