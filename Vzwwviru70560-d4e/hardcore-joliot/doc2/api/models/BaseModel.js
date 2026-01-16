/**
 * Base Model with validation utilities
 */
class BaseModel {
  constructor(data = {}) {
    this.created_at = data.created_at || new Date().toISOString();
    this.updated_at = data.updated_at || new Date().toISOString();
  }

  validate() {
    const errors = [];
    
    // Override in child classes
    const childErrors = this._validate();
    if (childErrors && childErrors.length > 0) {
      errors.push(...childErrors);
    }

    if (errors.length > 0) {
      throw new ValidationError(errors);
    }

    return true;
  }

  _validate() {
    // To be implemented by child classes
    return [];
  }

  static required(value, field) {
    if (!value || (typeof value === 'string' && value.trim() === '')) {
      return `${field} is required`;
    }
    return null;
  }

  static email(value, field) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (value && !emailRegex.test(value)) {
      return `${field} must be a valid email`;
    }
    return null;
  }

  static minLength(value, min, field) {
    if (value && value.length < min) {
      return `${field} must be at least ${min} characters`;
    }
    return null;
  }

  static maxLength(value, max, field) {
    if (value && value.length > max) {
      return `${field} must be no more than ${max} characters`;
    }
    return null;
  }

  static isUUID(value, field) {
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    if (value && !uuidRegex.test(value)) {
      return `${field} must be a valid UUID`;
    }
    return null;
  }

  static inArray(value, array, field) {
    if (value && !array.includes(value)) {
      return `${field} must be one of: ${array.join(', ')}`;
    }
    return null;
  }
}

class ValidationError extends Error {
  constructor(errors) {
    super('Validation failed');
    this.name = 'ValidationError';
    this.errors = errors;
  }
}

module.exports = { BaseModel, ValidationError };
