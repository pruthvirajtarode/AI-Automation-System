/**
 * Form Validation Utilities
 * Comprehensive validation functions for forms
 */

export const ValidationRules = {
  // Email validation
  isValidEmail: (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },

  // Phone validation
  isValidPhone: (phone) => {
    const phoneRegex = /^[0-9+\-\s()]{10,}$/;
    return phoneRegex.test(phone);
  },

  // URL validation
  isValidURL: (url) => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  },

  // Not empty
  isNotEmpty: (value) => {
    return value && value.trim().length > 0;
  },

  // Min length
  minLength: (value, length) => {
    return value && value.length >= length;
  },

  // Max length
  maxLength: (value, length) => {
    return value && value.length <= length;
  },

  // Number check
  isNumber: (value) => {
    return !isNaN(value) && isFinite(value);
  },

  // Positive number
  isPositiveNumber: (value) => {
    return !isNaN(value) && isFinite(value) && value > 0;
  },

  // Date validation
  isValidDate: (dateString) => {
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
  },

  // Future date
  isFutureDate: (dateString) => {
    const date = new Date(dateString);
    return date > new Date();
  },

  // Company name format
  isValidCompanyName: (name) => {
    return name && name.length >= 2 && name.length <= 100;
  },

  // Password strength
  isStrongPassword: (password) => {
    return (
      password &&
      password.length >= 8 &&
      /[A-Z]/.test(password) &&
      /[0-9]/.test(password) &&
      /[!@#$%^&*]/.test(password)
    );
  },
};

export const ValidationMessages = {
  required: 'This field is required',
  invalidEmail: 'Please enter a valid email address',
  invalidPhone: 'Please enter a valid phone number',
  invalidURL: 'Please enter a valid URL',
  minLength: (length) => `Must be at least ${length} characters`,
  maxLength: (length) => `Must not exceed ${length} characters`,
  invalidNumber: 'Please enter a valid number',
  negativeNumber: 'Please enter a positive number',
  invalidDate: 'Please enter a valid date',
  futureDate: 'Date must be in the future',
  invalidCompanyName: 'Company name must be between 2 and 100 characters',
  weakPassword: 'Password must contain 8+ characters, uppercase, number, and special character',
};

export class FormValidator {
  constructor() {
    this.errors = {};
  }

  validate(formData, schema) {
    this.errors = {};

    for (const [field, rules] of Object.entries(schema)) {
      const value = formData[field];

      // Required validation
      if (rules.required && !ValidationRules.isNotEmpty(value)) {
        this.addError(field, ValidationMessages.required);
        continue;
      }

      // Skip other validations if field is empty but not required
      if (!ValidationRules.isNotEmpty(value) && !rules.required) {
        continue;
      }

      // Email validation
      if (rules.type === 'email' && !ValidationRules.isValidEmail(value)) {
        this.addError(field, ValidationMessages.invalidEmail);
      }

      // Phone validation
      if (rules.type === 'phone' && !ValidationRules.isValidPhone(value)) {
        this.addError(field, ValidationMessages.invalidPhone);
      }

      // URL validation
      if (rules.type === 'url' && !ValidationRules.isValidURL(value)) {
        this.addError(field, ValidationMessages.invalidURL);
      }

      // Min length validation
      if (rules.minLength && !ValidationRules.minLength(value, rules.minLength)) {
        this.addError(field, ValidationMessages.minLength(rules.minLength));
      }

      // Max length validation
      if (rules.maxLength && !ValidationRules.maxLength(value, rules.maxLength)) {
        this.addError(field, ValidationMessages.maxLength(rules.maxLength));
      }

      // Number validation
      if (rules.type === 'number' && !ValidationRules.isNumber(value)) {
        this.addError(field, ValidationMessages.invalidNumber);
      }

      // Positive number validation
      if (rules.positive && !ValidationRules.isPositiveNumber(value)) {
        this.addError(field, ValidationMessages.negativeNumber);
      }

      // Custom validation
      if (rules.custom && typeof rules.custom === 'function') {
        if (!rules.custom(value)) {
          this.addError(field, rules.customMessage || 'Invalid value');
        }
      }
    }

    return this.isValid();
  }

  addError(field, message) {
    this.errors[field] = this.errors[field] || [];
    if (!this.errors[field].includes(message)) {
      this.errors[field].push(message);
    }
  }

  getErrors() {
    return this.errors;
  }

  getFieldErrors(field) {
    return this.errors[field] || [];
  }

  hasErrors(field) {
    return field ? !!this.errors[field] : Object.keys(this.errors).length > 0;
  }

  isValid() {
    return Object.keys(this.errors).length === 0;
  }

  clear() {
    this.errors = {};
  }
}

export default ValidationRules;
