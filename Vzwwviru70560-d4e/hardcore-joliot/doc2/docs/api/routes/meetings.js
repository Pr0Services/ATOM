const express = require('express');
const router = express.Router();

// List meetings
router.get('/', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const { sphere_id, dataspace_id, start_date, end_date } = req.query;
    
    let query = 'SELECT * FROM meetings WHERE owner_id = $1';
    const params = [req.user.userId];
    let paramIndex = 2;
    
    if (sphere_id) {
      query += ` AND sphere_id = $${paramIndex}`;
      params.push(sphere_id);
      paramIndex++;
    }
    
    if (dataspace_id) {
      query += ` AND dataspace_id = $${paramIndex}`;
      params.push(dataspace_id);
      paramIndex++;
    }
    
    query += ' ORDER BY start_time DESC';
    
    const result = await pool.query(query, params);
    res.json({
      success: true,
      data: { meetings: result.rows, count: result.rows.length },
      meta: { request_id: req.id, timestamp: new Date().toISOString() }
    });
  } catch (error) {
    console.error('List meetings error:', error);
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Create meeting
router.post('/', async (req, res) => {
  const { title, description, start_time, end_time, location, meeting_type, dataspace_id, sphere_id } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO meetings (owner_id, title, description, start_time, end_time, location, meeting_type, dataspace_id, sphere_id)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING *`,
      [req.user.userId, title, description, start_time, end_time, location, meeting_type || 'general', dataspace_id, sphere_id]
    );
    res.status(201).json({
      success: true,
      data: { meeting: result.rows[0] },
      meta: { request_id: req.id, timestamp: new Date().toISOString() }
    });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Get meeting
router.get('/:id', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      'SELECT * FROM meetings WHERE id = $1 AND owner_id = $2',
      [req.params.id, req.user.userId]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Meeting not found' } });
    }
    res.json({ success: true, data: { meeting: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Add participant
router.post('/:id/participants', async (req, res) => {
  const { user_id, role, status } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO meeting_participants (meeting_id, user_id, role, status)
       VALUES ($1, $2, $3, $4) RETURNING *`,
      [req.params.id, user_id, role || 'participant', status || 'invited']
    );
    res.status(201).json({ success: true, data: { participant: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Add note
router.post('/:id/notes', async (req, res) => {
  const { content, note_type } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO meeting_notes (meeting_id, author_id, content, note_type)
       VALUES ($1, $2, $3, $4) RETURNING *`,
      [req.params.id, req.user.userId, content, note_type || 'general']
    );
    res.status(201).json({ success: true, data: { note: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Add task from meeting
router.post('/:id/tasks', async (req, res) => {
  const { title, description, assigned_to, due_date } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO meeting_tasks (meeting_id, title, description, assigned_to, due_date, created_by)
       VALUES ($1, $2, $3, $4, $5, $6) RETURNING *`,
      [req.params.id, title, description, assigned_to, due_date, req.user.userId]
    );
    res.status(201).json({ success: true, data: { task: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

module.exports = router;
