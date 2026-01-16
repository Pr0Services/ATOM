const express = require('express');
const router = express.Router();

// Create OCW session
router.post('/sessions', async (req, res) => {
  const { session_name, dataspace_id, canvas_config } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO ocw_sessions (owner_id, session_name, dataspace_id, canvas_config)
       VALUES ($1, $2, $3, $4) RETURNING *`,
      [req.user.userId, session_name, dataspace_id, canvas_config || {}]
    );
    res.status(201).json({ success: true, data: { session: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// List OCW sessions
router.get('/sessions', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      'SELECT * FROM ocw_sessions WHERE owner_id = $1 ORDER BY created_at DESC',
      [req.user.userId]
    );
    res.json({ success: true, data: { sessions: result.rows } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Get session with participants
router.get('/sessions/:id', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const session = await pool.query(
      'SELECT * FROM ocw_sessions WHERE id = $1',
      [req.params.id]
    );
    const participants = await pool.query(
      'SELECT * FROM ocw_participants WHERE session_id = $1',
      [req.params.id]
    );
    res.json({ success: true, data: { session: session.rows[0], participants: participants.rows } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Add participant
router.post('/sessions/:id/participants', async (req, res) => {
  const { user_id, role } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO ocw_participants (session_id, user_id, role)
       VALUES ($1, $2, $3) RETURNING *`,
      [req.params.id, user_id, role || 'participant']
    );
    res.status(201).json({ success: true, data: { participant: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Add canvas object
router.post('/sessions/:id/objects', async (req, res) => {
  const { object_type, position, content } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO ocw_canvas_objects (session_id, object_type, position, content, created_by)
       VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [req.params.id, object_type, position || {}, content || {}, req.user.userId]
    );
    res.status(201).json({ success: true, data: { object: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Add annotation
router.post('/sessions/:id/annotations', async (req, res) => {
  const { canvas_object_id, annotation_type, content } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO ocw_annotations (session_id, canvas_object_id, annotation_type, content, created_by)
       VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [req.params.id, canvas_object_id, annotation_type, content, req.user.userId]
    );
    res.status(201).json({ success: true, data: { annotation: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

module.exports = router;
