const express = require('express');
const router = express.Router();

// Create XR room
router.post('/rooms', async (req, res) => {
  const { name, room_type, dataspace_id, scene_config } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO xr_rooms (owner_id, name, room_type, dataspace_id, scene_config)
       VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [req.user.userId, name, room_type || 'standard', dataspace_id, scene_config || {}]
    );
    res.status(201).json({ success: true, data: { room: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// List XR rooms
router.get('/rooms', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      'SELECT * FROM xr_rooms WHERE owner_id = $1 OR is_public = true ORDER BY created_at DESC',
      [req.user.userId]
    );
    res.json({ success: true, data: { rooms: result.rows } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Add object to XR room
router.post('/rooms/:id/objects', async (req, res) => {
  const { object_type, position, rotation, scale, properties } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO xr_objects (room_id, object_type, position, rotation, scale, properties)
       VALUES ($1, $2, $3, $4, $5, $6) RETURNING *`,
      [req.params.id, object_type, position || {}, rotation || {}, scale || {}, properties || {}]
    );
    res.status(201).json({ success: true, data: { object: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Create XR session
router.post('/sessions', async (req, res) => {
  const { room_id, session_name } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO xr_sessions (room_id, session_name, host_id)
       VALUES ($1, $2, $3) RETURNING *`,
      [room_id, session_name, req.user.userId]
    );
    res.status(201).json({ success: true, data: { session: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Join XR session
router.post('/sessions/:id/join', async (req, res) => {
  const { avatar_config } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO xr_session_participants (session_id, user_id, avatar_config)
       VALUES ($1, $2, $3) RETURNING *`,
      [req.params.id, req.user.userId, avatar_config || {}]
    );
    res.status(201).json({ success: true, data: { participant: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

module.exports = router;
