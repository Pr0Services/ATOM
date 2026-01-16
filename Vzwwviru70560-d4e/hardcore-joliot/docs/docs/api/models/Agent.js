const { BaseModel } = require('./BaseModel');

class Agent extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id;
    this.agent_code = data.agent_code;
    this.agent_name = data.agent_name;
    this.agent_level = data.agent_level;
    this.sphere = data.sphere;
    this.domain = data.domain;
    this.description = data.description;
    this.capabilities = data.capabilities || [];
    this.cost_tier = data.cost_tier || 1;
    this.is_active = data.is_active !== false;
  }

  _validate() {
    const errors = [];

    const VALID_LEVELS = ['L0', 'L1', 'L2', 'L3'];
    const VALID_SPHERES = ['personal', 'business', 'government', 'creative', 'community', 'social', 'entertainment', 'myteam'];

    // Agent code validation
    const codeError = BaseModel.required(this.agent_code, 'agent_code');
    if (codeError) errors.push(codeError);

    // Name validation
    const nameError = BaseModel.required(this.agent_name, 'agent_name');
    if (nameError) errors.push(nameError);

    // Level validation
    const levelError = BaseModel.required(this.agent_level, 'agent_level') ||
                       BaseModel.inArray(this.agent_level, VALID_LEVELS, 'agent_level');
    if (levelError) errors.push(levelError);

    // Sphere validation (optional)
    if (this.sphere) {
      const sphereError = BaseModel.inArray(this.sphere, VALID_SPHERES, 'sphere');
      if (sphereError) errors.push(sphereError);
    }

    // Cost tier validation
    if (this.cost_tier < 1 || this.cost_tier > 5) {
      errors.push('cost_tier must be between 1 and 5');
    }

    return errors;
  }
}

module.exports = Agent;
