const { BaseModel } = require('./BaseModel');

class DataSpace extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id;
    this.owner_id = data.owner_id;
    this.name = data.name;
    this.description = data.description;
    this.dataspace_type = data.dataspace_type;
    this.sphere_id = data.sphere_id;
    this.domain_id = data.domain_id;
    this.parent_id = data.parent_id;
    this.tags = data.tags || [];
    this.metadata = data.metadata || {};
    this.status = data.status || 'active';
  }

  _validate() {
    const errors = [];

    const VALID_TYPES = ['project', 'property', 'client', 'meeting', 'document', 'custom'];
    const VALID_STATUSES = ['active', 'archived'];

    // Owner ID validation
    const ownerError = BaseModel.required(this.owner_id, 'owner_id') ||
                       BaseModel.isUUID(this.owner_id, 'owner_id');
    if (ownerError) errors.push(ownerError);

    // Name validation
    const nameError = BaseModel.required(this.name, 'name') ||
                      BaseModel.minLength(this.name, 2, 'name') ||
                      BaseModel.maxLength(this.name, 200, 'name');
    if (nameError) errors.push(nameError);

    // Type validation
    if (this.dataspace_type) {
      const typeError = BaseModel.inArray(this.dataspace_type, VALID_TYPES, 'dataspace_type');
      if (typeError) errors.push(typeError);
    }

    // Status validation
    const statusError = BaseModel.inArray(this.status, VALID_STATUSES, 'status');
    if (statusError) errors.push(statusError);

    return errors;
  }
}

module.exports = DataSpace;
