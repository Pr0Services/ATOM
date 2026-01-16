# CHE·NU API Documentation V51

## Endpoints

### Memory Units
- `GET /api/v1/memory/units` - List all units
- `GET /api/v1/memory/units/:id` - Get single unit
- `GET /api/v1/memory/spheres` - List spheres

### Proposals
- `GET /api/v1/proposals` - List proposals
- `POST /api/v1/proposals` - Create proposal (requires human approval)
- `PUT /api/v1/proposals/:id/approve` - Approve (human only)
- `PUT /api/v1/proposals/:id/reject` - Reject (human only)

### Events
- `GET /api/v1/events` - List events
- `GET /api/v1/events/timeline` - Get timeline view

### Exports
- `POST /api/v1/exports/narrative` - Generate narrative
- `POST /api/v1/exports/incident` - Generate incident report
- `GET /api/v1/exports/:id/verify` - Verify signature

## Authentication
Demo mode: No authentication required
Production: OAuth 2.0 + API keys
