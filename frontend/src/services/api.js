/**
 * Frontend API Service
 * Handles all API communication with backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class APIService {
  // Message APIs
  async receiveMessage(message) {
    return this.post('/messages/receive', message);
  }

  async listMessages(customerId, channel, limit = 50) {
    return this.get('/messages/', { customer_id: customerId, channel, limit });
  }

  // Lead APIs
  async createLead(leadData) {
    return this.post('/leads/', leadData);
  }

  async listLeads(filters = {}) {
    return this.get('/leads/', filters);
  }

  async getLead(leadId) {
    return this.get(`/leads/${leadId}`);
  }

  async updateLead(leadId, leadData) {
    return this.put(`/leads/${leadId}`, leadData);
  }

  async qualifyLead(leadId, message) {
    return this.post(`/leads/${leadId}/qualify`, { message_content: message });
  }

  // Customer APIs
  async createCustomer(customerData) {
    return this.post('/crm/customers', customerData);
  }

  async listCustomers(filters = {}) {
    return this.get('/crm/customers', filters);
  }

  async getCustomer(customerId) {
    return this.get(`/crm/customers/${customerId}`);
  }

  async updateCustomer(customerId, customerData) {
    return this.put(`/crm/customers/${customerId}`, customerData);
  }

  async getCustomerHistory(customerId, limit = 50) {
    return this.get(`/crm/customers/${customerId}/history`, { limit });
  }

  // Booking APIs
  async createBooking(bookingData) {
    return this.post('/bookings/', bookingData);
  }

  async listBookings(filters = {}) {
    return this.get('/bookings/', filters);
  }

  async getBooking(bookingId) {
    return this.get(`/bookings/${bookingId}`);
  }

  async updateBooking(bookingId, bookingData) {
    return this.put(`/bookings/${bookingId}`, bookingData);
  }

  async checkAvailability(dateTime, durationMinutes = 30) {
    return this.get('/bookings/availability/check', {
      date_time: dateTime,
      duration_minutes: durationMinutes
    });
  }

  // Task APIs
  async createTask(taskData) {
    return this.post('/tasks/', taskData);
  }

  async listTasks(filters = {}) {
    return this.get('/tasks/', filters);
  }

  async getTask(taskId) {
    return this.get(`/tasks/${taskId}`);
  }

  async updateTask(taskId, taskData) {
    return this.put(`/tasks/${taskId}`, taskData);
  }

  async routeTask(leadId, message, title) {
    return this.post(`/tasks/${leadId}/route`, { message_content: message, title });
  }

  // Follow-up APIs
  async scheduleFollowUp(followUpData) {
    return this.post('/follow-ups/', followUpData);
  }

  async listFollowUps(filters = {}) {
    return this.get('/follow-ups/', filters);
  }

  async createFollowUpSequence(leadId, sequenceType) {
    return this.post(`/follow-ups/${leadId}/sequence/${sequenceType}`);
  }

  async sendPendingFollowUps() {
    return this.post('/follow-ups/send/pending');
  }

  // Utility methods
  async get(endpoint, params = {}) {
    const url = new URL(`${API_BASE_URL}${endpoint}`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

    const response = await fetch(url, {
      method: 'GET',
      headers: this._getHeaders()
    });

    return this._handleResponse(response);
  }

  async post(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: this._getHeaders(),
      body: JSON.stringify(data)
    });

    return this._handleResponse(response);
  }

  async put(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'PUT',
      headers: this._getHeaders(),
      body: JSON.stringify(data)
    });

    return this._handleResponse(response);
  }

  async delete(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'DELETE',
      headers: this._getHeaders()
    });

    return this._handleResponse(response);
  }

  _getHeaders() {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
    };
  }

  async _handleResponse(response) {
    if (response.ok) {
      return await response.json();
    }

    const error = await response.json();
    throw new Error(error.detail || 'API request failed');
  }
}

export default new APIService();
