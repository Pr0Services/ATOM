const express = require('express');
const router = express.Router();

// List files
router.get('/', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      'SELECT * FROM files WHERE owner_id = $1 ORDER BY created_at DESC',
      [req.user.userId]
    );
    res.json({ success: true, data: { files: result.rows } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Upload file metadata
router.post('/', async (req, res) => {
  const { filename, file_type, file_size, storage_path, dataspace_id } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO files (owner_id, filename, file_type, file_size, storage_path, dataspace_id)
       VALUES ($1, $2, $3, $4, $5, $6) RETURNING *`,
      [req.user.userId, filename, file_type, file_size, storage_path, dataspace_id]
    );
    res.status(201).json({ success: true, data: { file: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

module.exports = router;
