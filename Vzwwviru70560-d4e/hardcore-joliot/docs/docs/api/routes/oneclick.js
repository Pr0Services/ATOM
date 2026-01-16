const express = require('express');
const router = express.Router();
const { executeGovernedPipeline } = require('../middleware/governed_execution');

// Execute 1-click command
router.post('/execute', async (req, res) => {
  const { input, input_type, context, options } = req.body;
  try {
    const pool = req.app.locals.pool;
    
    // Create execution record
    const execResult = await pool.query(
      `INSERT INTO oneclick_executions (user_id, input_text, input_type, status, context)
       VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [req.user.userId, input, input_type || 'prompt', 'pending', context || {}]
    );
    
    const execution = execResult.rows[0];
    
    // Execute via Governed Pipeline
    try {
      const pipelineContext = {
        user_id: req.user.userId,
        identity_id: context?.identity_id,
        sphere_id: context?.sphere_id,
        dataspace_id: context?.dataspace_id,
        thread_id: context?.thread_id,
        agents: context?.agents || []
      };
      
      const result = await executeGovernedPipeline(input, pipelineContext, pool);
      
      await pool.query(
        `UPDATE oneclick_executions SET status = $1, result_data = $2, completed_at = NOW() WHERE id = $3`,
        ['completed', result, execution.id]
      );
      
      res.json({ success: true, data: { execution_id: execution.id, status: 'completed', result } });
    } catch (error) {
      await pool.query(
        `UPDATE oneclick_executions SET status = $1, error_message = $2, completed_at = NOW() WHERE id = $3`,
        ['failed', error.message, execution.id]
      );
      throw error;
    }
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'EXECUTION_ERROR', message: error.message } });
  }
});

// List workflows
router.get('/workflows', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      'SELECT * FROM oneclick_workflows WHERE owner_id = $1 OR is_public = true ORDER BY usage_count DESC',
      [req.user.userId]
    );
    res.json({ success: true, data: { workflows: result.rows } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Create workflow template
router.post('/templates', async (req, res) => {
  const { name, description, template_config } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO oneclick_templates (name, description, template_config, created_by)
       VALUES ($1, $2, $3, $4) RETURNING *`,
      [name, description, template_config || {}, req.user.userId]
    );
    res.status(201).json({ success: true, data: { template: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

module.exports = router;
