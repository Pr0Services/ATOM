const express = require('express');
const router = express.Router();

// List properties
router.get('/', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      'SELECT * FROM properties WHERE owner_id = $1 ORDER BY created_at DESC',
      [req.user.userId]
    );
    res.json({ success: true, data: { properties: result.rows } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Create property
router.post('/', async (req, res) => {
  const { address, property_type, purchase_price, current_value } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO properties (owner_id, address, property_type, purchase_price, current_value)
       VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [req.user.userId, address, property_type, purchase_price, current_value]
    );
    res.status(201).json({ success: true, data: { property: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Get property units
router.get('/:id/units', async (req, res) => {
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      'SELECT * FROM property_units WHERE property_id = $1',
      [req.params.id]
    );
    res.json({ success: true, data: { units: result.rows } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Add tenant
router.post('/:id/tenants', async (req, res) => {
  const { unit_id, name, email, phone, lease_start, lease_end, monthly_rent } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO tenants (property_id, unit_id, name, email, phone, lease_start, lease_end, monthly_rent)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING *`,
      [req.params.id, unit_id, name, email, phone, lease_start, lease_end, monthly_rent]
    );
    res.status(201).json({ success: true, data: { tenant: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Record rent payment
router.post('/:id/payments', async (req, res) => {
  const { tenant_id, amount, payment_date, payment_method } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO rent_payments (property_id, tenant_id, amount, payment_date, payment_method)
       VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [req.params.id, tenant_id, amount, payment_date, payment_method || 'transfer']
    );
    res.status(201).json({ success: true, data: { payment: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

// Maintenance requests
router.post('/:id/maintenance', async (req, res) => {
  const { unit_id, title, description, priority } = req.body;
  try {
    const pool = req.app.locals.pool;
    const result = await pool.query(
      `INSERT INTO maintenance_requests (property_id, unit_id, title, description, priority, reported_by)
       VALUES ($1, $2, $3, $4, $5, $6) RETURNING *`,
      [req.params.id, unit_id, title, description, priority || 'medium', req.user.userId]
    );
    res.status(201).json({ success: true, data: { request: result.rows[0] } });
  } catch (error) {
    res.status(500).json({ success: false, error: { code: 'SERVER_ERROR', message: error.message } });
  }
});

module.exports = router;
