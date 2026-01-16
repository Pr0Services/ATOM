const { BaseModel } = require('./BaseModel');

class Thread extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id;
    this.owner_id = data.owner_id;
    this.dataspace_id = data.dataspace_id;
    this.title = data.title;
    this.thread_type = data.thread_type;
    this.budget_tokens = data.budget_tokens || 10000;
    this.tokens_used = data.tokens_used || 0;
    this.status = data.status || 'active';
  }

  _validate() {
    const errors = [];

    const VALID_TYPES = ['conversation', 'decision', 'task', 'meeting', 'support'];
    const VALID_STATUSES = ['active', 'completed', 'archived'];

    // Owner validation
    const ownerError = BaseModel.required(this.owner_id, 'owner_id') ||
                       BaseModel.isUUID(this.owner_id, 'owner_id');
    if (ownerError) errors.push(ownerError);

    // Title validation
    const titleError = BaseModel.required(this.title, 'title') ||
                       BaseModel.minLength(this.title, 2, 'title');
    if (titleError) errors.push(titleError);

    // Type validation
    if (this.thread_type) {
      const typeError = BaseModel.inArray(this.thread_type, VALID_TYPES, 'thread_type');
      if (typeError) errors.push(typeError);
    }

    // Status validation
    const statusError = BaseModel.inArray(this.status, VALID_STATUSES, 'status');
    if (statusError) errors.push(statusError);

    // Budget validation
    if (this.budget_tokens < 0) {
      errors.push('budget_tokens must be positive');
    }

    if (this.tokens_used < 0) {
      errors.push('tokens_used must be positive');
    }

    if (this.tokens_used > this.budget_tokens) {
      errors.push('tokens_used cannot exceed budget_tokens');
    }

    return errors;
  }
}

module.exports = Thread;
