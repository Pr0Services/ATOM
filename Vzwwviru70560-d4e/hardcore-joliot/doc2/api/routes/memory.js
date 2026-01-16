const express = require('express');
const router = express.Router();

// Get memory items
router.get('/', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      'SELECT * FROM memory_items WHERE user_id = $1 ORDER BY importance DESC, created_at DESC',
      [req.user.userId]
    );
    res.json({ success: true, data: { items: result.rows } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Add memory item
router.post('/', async (req, res) => {
  const { content, memory_type, importance, tags } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO memory_items (user_id, content, memory_type, importance, tags)
       VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [req.user.userId, content, memory_type || 'general', importance || 5, tags || []]
    );
    res.status(201).json({ success: true, data: { item: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

module.exports = router;
