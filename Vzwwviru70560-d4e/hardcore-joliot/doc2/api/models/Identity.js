const { BaseModel } = require('./BaseModel');

class Identity extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id;
    this.user_id = data.user_id;
    this.identity_type = data.identity_type;
    this.identity_name = data.identity_name;
    this.is_active = data.is_active !== false;
    this.config = data.config || {};
  }

  _validate() {
    const errors = [];

    const VALID_TYPES = ['personal', 'enterprise', 'creative', 'design', 'architecture', 'construction'];

    // User ID validation
    const userIdError = BaseModel.required(this.user_id, 'user_id') ||
                        BaseModel.isUUID(this.user_id, 'user_id');
    if (userIdError) errors.push(userIdError);

    // Identity type validation
    const typeError = BaseModel.required(this.identity_type, 'identity_type') ||
                      BaseModel.inArray(this.identity_type, VALID_TYPES, 'identity_type');
    if (typeError) errors.push(typeError);

    // Identity name validation
    const nameError = BaseModel.required(this.identity_name, 'identity_name') ||
                      BaseModel.minLength(this.identity_name, 2, 'identity_name');
    if (nameError) errors.push(nameError);

    return errors;
  }
}

module.exports = Identity;
