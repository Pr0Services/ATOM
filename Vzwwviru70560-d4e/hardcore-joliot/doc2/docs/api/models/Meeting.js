const { BaseModel } = require('./BaseModel');

class Meeting extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id;
    this.owner_id = data.owner_id;
    this.title = data.title;
    this.description = data.description;
    this.start_time = data.start_time;
    this.end_time = data.end_time;
    this.location = data.location;
    this.meeting_type = data.meeting_type || 'general';
    this.status = data.status || 'scheduled';
  }

  _validate() {
    const errors = [];

    const VALID_TYPES = ['general', 'project', 'client', 'internal', 'review', 'planning'];
    const VALID_STATUSES = ['scheduled', 'in_progress', 'completed', 'cancelled'];

    // Owner validation
    const ownerError = BaseModel.required(this.owner_id, 'owner_id') ||
                       BaseModel.isUUID(this.owner_id, 'owner_id');
    if (ownerError) errors.push(ownerError);

    // Title validation
    const titleError = BaseModel.required(this.title, 'title') ||
                       BaseModel.minLength(this.title, 2, 'title');
    if (titleError) errors.push(titleError);

    // Start time validation
    const startError = BaseModel.required(this.start_time, 'start_time');
    if (startError) errors.push(startError);

    // Type validation
    const typeError = BaseModel.inArray(this.meeting_type, VALID_TYPES, 'meeting_type');
    if (typeError) errors.push(typeError);

    // Status validation
    const statusError = BaseModel.inArray(this.status, VALID_STATUSES, 'status');
    if (statusError) errors.push(statusError);

    // Time logic validation
    if (this.start_time && this.end_time) {
      if (new Date(this.start_time) >= new Date(this.end_time)) {
        errors.push('end_time must be after start_time');
      }
    }

    return errors;
  }
}

module.exports = Meeting;
