const express = require('express');
const router = express.Router();

// List construction projects
router.get('/projects', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      'SELECT * FROM construction_projects WHERE owner_id = $1 ORDER BY created_at DESC',
      [req.user.userId]
    );
    res.json({ success: true, data: { projects: result.rows } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Create construction project
router.post('/projects', async (req, res) => {
  const { name, property_id, project_type, start_date, estimated_completion } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO construction_projects (owner_id, name, property_id, project_type, start_date, estimated_completion)
       VALUES ($1, $2, $3, $4, $5, $6) RETURNING *`,
      [req.user.userId, name, property_id, project_type, start_date, estimated_completion]
    );
    res.status(201).json({ success: true, data: { project: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Create estimate
router.post('/estimates', async (req, res) => {
  const { project_id, title, description } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO construction_estimates (project_id, title, description, created_by)
       VALUES ($1, $2, $3, $4) RETURNING *`,
      [project_id, title, description, req.user.userId]
    );
    res.status(201).json({ success: true, data: { estimate: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Add line items to estimate
router.post('/estimates/:id/items', async (req, res) => {
  const { category, description, quantity, unit, unit_price } = req.body;
  try {
    const pool = req.app.locals.pool;
    const total = quantity * unit_price;
    const result = await pool.query(
      `INSERT INTO estimate_line_items (estimate_id, category, description, quantity, unit, unit_price, total_price)
       VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *`,
      [req.params.id, category, description, quantity, unit, unit_price, total]
    );
    res.status(201).json({ success: true, data: { item: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Materials management
router.get('/materials', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query('SELECT * FROM materials ORDER BY name');
    res.json({ success: true, data: { materials: result.rows } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

router.post('/materials', async (req, res) => {
  const { name, category, unit, current_price, supplier } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO materials (name, category, unit, current_price, supplier)
       VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [name, category, unit, current_price, supplier]
    );
    res.status(201).json({ success: true, data: { material: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

module.exports = router;
