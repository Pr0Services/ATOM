const express = require('express');
const router = express.Router();

// Create backstage context
router.post('/contexts', async (req, res) => {
  const { thread_id, preparation_data } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO backstage_contexts (thread_id, user_id, preparation_data)
       VALUES ($1, $2, $3) RETURNING *`,
      [thread_id, req.user.userId, preparation_data || {}]
    );
    res.status(201).json({ success: true, data: { context: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Add preparation step
router.post('/preparations', async (req, res) => {
  const { context_id, step_type, step_data } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO backstage_preparations (context_id, step_type, step_data)
       VALUES ($1, $2, $3) RETURNING *`,
      [context_id, step_type, step_data || {}]
    );
    res.status(201).json({ success: true, data: { preparation: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Add classification
router.post('/classifications', async (req, res) => {
  const { context_id, classification_type, confidence, tags } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO backstage_classifications (context_id, classification_type, confidence, tags)
       VALUES ($1, $2, $3, $4) RETURNING *`,
      [context_id, classification_type, confidence || 0.5, tags || []]
    );
    res.status(201).json({ success: true, data: { classification: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

module.exports = router;
