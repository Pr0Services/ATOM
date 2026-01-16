const { BaseModel } = require('./BaseModel');

class User extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id;
    this.email = data.email;
    this.password_hash = data.password_hash;
    this.full_name = data.full_name;
    this.is_active = data.is_active !== false;
    this.last_login = data.last_login;
  }

  _validate() {
    const errors = [];

    // Email validation
    const emailError = BaseModel.required(this.email, 'email') || 
                       BaseModel.email(this.email, 'email');
    if (emailError) errors.push(emailError);

    // Full name validation
    const nameError = BaseModel.required(this.full_name, 'full_name') ||
                      BaseModel.minLength(this.full_name, 2, 'full_name');
    if (nameError) errors.push(nameError);

    return errors;
  }

  toJSON() {
    return {
      id: this.id,
      email: this.email,
      full_name: this.full_name,
      is_active: this.is_active,
      last_login: this.last_login,
      created_at: this.created_at,
      updated_at: this.updated_at
    };
  }
}

module.exports = User;
