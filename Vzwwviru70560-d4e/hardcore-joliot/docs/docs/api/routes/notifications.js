const express = require('express');
const router = express.Router();

// Get notifications
router.get('/', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      'SELECT * FROM notifications WHERE user_id = $1 ORDER BY created_at DESC LIMIT 50',
      [req.user.userId]
    );
    res.json({ success: true, data: { notifications: result.rows } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Mark as read
router.patch('/:id/read', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      'UPDATE notifications SET is_read = true WHERE id = $1 AND user_id = $2 RETURNING *',
      [req.params.id, req.user.userId]
    );
    res.json({ success: true, data: { notification: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

module.exports = router;
