const express = require('express');
const router = express.Router();

// List workspaces
router.get('/', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      'SELECT * FROM workspaces WHERE owner_id = $1 ORDER BY updated_at DESC',
      [req.user.userId]
    );
    res.json({ success: true, data: { workspaces: result.rows, count: result.rows.length } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Create workspace
router.post('/', async (req, res) => {
  const { name, workspace_mode, dataspace_id, layout_config } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO workspaces (owner_id, name, workspace_mode, dataspace_id, layout_config)
       VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [req.user.userId, name, workspace_mode || 'document', dataspace_id, layout_config || {}]
    );
    res.status(201).json({ success: true, data: { workspace: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Get workspace
router.get('/:id', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      'SELECT * FROM workspaces WHERE id = $1 AND owner_id = $2',
      [req.params.id, req.user.userId]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND' } });
    }
    res.json({ success: true, data: { workspace: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Transform workspace mode
router.post('/:id/transform', async (req, res) => {
  const { target_mode, preserve_data } = req.body;
  try {
    const pool = req.app.locals.pool;
    await pool.query(
      `INSERT INTO workspace_transformations (workspace_id, from_mode, to_mode, preserve_data)
       VALUES ($1, (SELECT workspace_mode FROM workspaces WHERE id = $1), $2, $3)`,
      [req.params.id, target_mode, preserve_data !== false]
    );
    const result = await pool.query(
      `UPDATE workspaces SET workspace_mode = $1, updated_at = NOW() WHERE id = $2 AND owner_id = $3 RETURNING *`,
      [target_mode, req.params.id, req.user.userId]
    );
    res.json({ success: true, data: { workspace: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Save workspace state
router.post('/:id/states', async (req, res) => {
  const { state_name, state_data } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO workspace_states (workspace_id, state_name, state_data)
       VALUES ($1, $2, $3) RETURNING *`,
      [req.params.id, state_name, state_data || {}]
    );
    res.status(201).json({ success: true, data: { state: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Add panel
router.post('/:id/panels', async (req, res) => {
  const { panel_type, position, config } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO workspace_panels (workspace_id, panel_type, position, config)
       VALUES ($1, $2, $3, $4) RETURNING *`,
      [req.params.id, panel_type, position || {}, config || {}]
    );
    res.status(201).json({ success: true, data: { panel: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

module.exports = router;
