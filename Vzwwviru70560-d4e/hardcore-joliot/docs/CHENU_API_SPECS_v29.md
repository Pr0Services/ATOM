# CHEÂ·NU API SPECIFICATIONS v29
## Complete Engine Stack API Reference

---

# BASE CONFIGURATION

## Base URL
```
Production: https://api.che-nu.com/v1
Staging: https://api-staging.che-nu.com/v1
```

## Authentication
```http
Authorization: Bearer <jwt_token>
X-Identity-ID: <identity_uuid>
X-Request-ID: <unique_request_id>
```

## Standard Response Format
```json
{
  "success": true,
  "data": {},
  "meta": {
    "request_id": "uuid",
    "timestamp": "ISO8601",
    "version": "v1"
  }
}
```

## Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  },
  "meta": {
    "request_id": "uuid",
    "timestamp": "ISO8601"
  }
}
```

---

# SECTION 1: IDENTITY API

## Create Identity
```http
POST /identities
```
```json
{
  "identity_type": "personal|enterprise|creative|design|architecture|construction",
  "identity_name": "string",
  "config": {}
}
```

## List User Identities
```http
GET /identities
```

## Switch Active Identity
```http
POST /identities/{identity_id}/activate
```

## Get Identity Permissions
```http
GET /identities/{identity_id}/permissions
```

---

# SECTION 2: DATASPACE API

## Create DataSpace
```http
POST /dataspaces
```
```json
{
  "name": "string",
  "description": "string",
  "dataspace_type": "project|property|client|meeting|document|custom",
  "sphere_id": "uuid (optional)",
  "domain_id": "uuid (optional)",
  "parent_id": "uuid (optional)",
  "tags": ["string"],
  "metadata": {}
}
```

## List DataSpaces
```http
GET /dataspaces
```
Query Parameters:
- `sphere_id`: Filter by sphere
- `domain_id`: Filter by domain
- `type`: Filter by type
- `status`: active|archived
- `search`: Full-text search
- `page`: Page number
- `limit`: Items per page (max 100)

## Get DataSpace
```http
GET /dataspaces/{dataspace_id}
```

## Update DataSpace
```http
PATCH /dataspaces/{dataspace_id}
```

## Archive DataSpace
```http
POST /dataspaces/{dataspace_id}/archive
```

## Link DataSpaces
```http
POST /dataspaces/{dataspace_id}/links
```
```json
{
  "target_dataspace_id": "uuid",
  "link_type": "reference|parent|related|derived"
}
```

---

# SECTION 3: THREAD API

## Create Thread
```http
POST /threads
```
```json
{
  "dataspace_id": "uuid (optional)",
  "title": "string",
  "thread_type": "conversation|decision|task|meeting|support",
  "participants": ["user_uuid"]
}
```

## List Threads
```http
GET /threads
```

## Get Thread with Messages
```http
GET /threads/{thread_id}
```

## Add Message to Thread
```http
POST /threads/{thread_id}/messages
```
```json
{
  "message_type": "text|file|action|decision",
  "content": "string",
  "attachments": []
}
```

## Record Decision
```http
POST /threads/{thread_id}/decisions
```
```json
{
  "decision_text": "string",
  "decision_type": "approval|direction|assignment|policy",
  "affected_dataspaces": ["uuid"]
}
```

---

# SECTION 4: WORKSPACE ENGINE API

## Create Workspace
```http
POST /workspaces
```
```json
{
  "name": "string",
  "workspace_mode": "document|board|timeline|spreadsheet|dashboard|diagram|whiteboard|xr|hybrid",
  "dataspace_id": "uuid (optional)",
  "layout_config": {}
}
```

## List Workspaces
```http
GET /workspaces
```

## Get Workspace State
```http
GET /workspaces/{workspace_id}
```

## Update Workspace Mode
```http
POST /workspaces/{workspace_id}/transform
```
```json
{
  "target_mode": "string",
  "preserve_data": true
}
```

## Save Workspace State
```http
POST /workspaces/{workspace_id}/states
```
```json
{
  "state_name": "string (optional)",
  "state_data": {}
}
```

## Get Workspace History
```http
GET /workspaces/{workspace_id}/states
```

## Revert Workspace State
```http
POST /workspaces/{workspace_id}/revert
```
```json
{
  "state_id": "uuid"
}
```

## Add Panel
```http
POST /workspaces/{workspace_id}/panels
```
```json
{
  "panel_type": "editor|preview|chat|files|agents|timeline|canvas",
  "position": {"x": 0, "y": 0, "width": 400, "height": 300},
  "config": {}
}
```

---

# SECTION 5: 1-CLICK ASSISTANT API

## Execute 1-Click Command
```http
POST /oneclick/execute
```
```json
{
  "input": "string (natural language command)",
  "input_type": "prompt|file|context|dataspace",
  "context": {
    "dataspace_id": "uuid (optional)",
    "thread_id": "uuid (optional)",
    "workspace_id": "uuid (optional)"
  },
  "options": {
    "auto_approve": false,
    "output_format": "auto|document|dataspace|dashboard"
  }
}
```

Response:
```json
{
  "execution_id": "uuid",
  "status": "pending|running|completed|needs_approval",
  "workflow": {
    "id": "uuid",
    "name": "string",
    "steps": []
  },
  "estimated_time_seconds": 30
}
```

## Get Execution Status
```http
GET /oneclick/executions/{execution_id}
```

## Approve Execution Step
```http
POST /oneclick/executions/{execution_id}/approve
```
```json
{
  "step_index": 0,
  "modifications": {}
}
```

## Cancel Execution
```http
POST /oneclick/executions/{execution_id}/cancel
```

## List Available Workflows
```http
GET /oneclick/workflows
```
Query Parameters:
- `sphere_id`: Filter by sphere
- `domain_id`: Filter by domain
- `search`: Search workflows

## List Templates
```http
GET /oneclick/templates
```

---

# SECTION 6: BACKSTAGE INTELLIGENCE API

## Get Context Suggestions
```http
POST /backstage/suggest
```
```json
{
  "context_type": "workspace|thread|meeting|workflow",
  "current_state": {},
  "user_intent": "string (optional)"
}
```

Response:
```json
{
  "suggestions": {
    "agents": ["agent_uuid"],
    "dataspaces": ["dataspace_uuid"],
    "templates": ["template_id"],
    "actions": ["action_name"]
  },
  "detected_intent": {
    "primary": "string",
    "confidence": 0.95
  }
}
```

## Classify Content
```http
POST /backstage/classify
```
```json
{
  "content": "string|base64",
  "content_type": "text|file|image|audio"
}
```

## Pre-process Input
```http
POST /backstage/preprocess
```
```json
{
  "input": {},
  "target_workflow": "uuid (optional)"
}
```

---

# SECTION 7: MEMORY & GOVERNANCE API

## Store Memory
```http
POST /memory
```
```json
{
  "memory_type": "short_term|mid_term|long_term",
  "memory_category": "preference|instruction|fact|context|rule",
  "content": "string",
  "dataspace_id": "uuid (optional)",
  "expires_at": "ISO8601 (optional)"
}
```

## List Memory
```http
GET /memory
```
Query Parameters:
- `type`: Filter by memory type
- `category`: Filter by category
- `status`: active|pinned|archived

## Get Memory Item
```http
GET /memory/{memory_id}
```

## Update Memory
```http
PATCH /memory/{memory_id}
```

## Delete Memory
```http
DELETE /memory/{memory_id}
```

## Pin Memory
```http
POST /memory/{memory_id}/pin
```

## Archive Memory
```http
POST /memory/{memory_id}/archive
```

## Get Audit Log
```http
GET /governance/audit
```
Query Parameters:
- `resource_type`: Filter by resource
- `action_type`: Filter by action
- `start_date`: ISO8601
- `end_date`: ISO8601
- `page`: Page number
- `limit`: Items per page

## Request Elevation
```http
POST /governance/elevate
```
```json
{
  "requested_action": "string",
  "resource_type": "string",
  "resource_id": "uuid",
  "reason": "string"
}
```

## Approve Elevation
```http
POST /governance/elevate/{request_id}/approve
```

## Deny Elevation
```http
POST /governance/elevate/{request_id}/deny
```

---

# SECTION 8: AGENT API

## List Agents
```http
GET /agents
```
Query Parameters:
- `level`: L0|L1|L2|L3
- `sphere_id`: Filter by sphere
- `domain_id`: Filter by domain
- `active`: true|false

## Get Agent Details
```http
GET /agents/{agent_id}
```

## Execute Agent
```http
POST /agents/{agent_id}/execute
```
```json
{
  "input": {},
  "context": {
    "thread_id": "uuid (optional)",
    "dataspace_id": "uuid (optional)",
    "workspace_id": "uuid (optional)"
  },
  "options": {
    "stream": false,
    "max_tokens": 4096
  }
}
```

## Stream Agent Execution
```http
POST /agents/{agent_id}/execute/stream
```
Returns Server-Sent Events (SSE)

## Get Agent Execution History
```http
GET /agents/{agent_id}/executions
```

## Configure Agent (User-specific)
```http
POST /agents/{agent_id}/configure
```
```json
{
  "config_key": "string",
  "config_value": {}
}
```

---

# SECTION 9: MEETING API

## Create Meeting
```http
POST /meetings
```
```json
{
  "title": "string",
  "description": "string",
  "meeting_type": "standup|planning|review|brainstorm|decision|workshop",
  "scheduled_start": "ISO8601",
  "scheduled_end": "ISO8601",
  "location": "string (optional)",
  "is_xr_meeting": false,
  "agenda": [],
  "participants": ["user_email"]
}
```

## List Meetings
```http
GET /meetings
```
Query Parameters:
- `status`: scheduled|active|completed
- `from`: ISO8601
- `to`: ISO8601
- `type`: Meeting type

## Get Meeting Details
```http
GET /meetings/{meeting_id}
```

## Start Meeting
```http
POST /meetings/{meeting_id}/start
```

## End Meeting
```http
POST /meetings/{meeting_id}/end
```

## Add Meeting Note
```http
POST /meetings/{meeting_id}/notes
```
```json
{
  "note_type": "general|decision|action|question|idea",
  "content": "string"
}
```

## Create Meeting Task
```http
POST /meetings/{meeting_id}/tasks
```
```json
{
  "title": "string",
  "description": "string",
  "assignee_id": "uuid",
  "due_date": "YYYY-MM-DD",
  "priority": "low|medium|high|urgent"
}
```

## Get Meeting Summary
```http
GET /meetings/{meeting_id}/summary
```

---

# SECTION 10: IMMOBILIER API

## Create Property
```http
POST /immobilier/properties
```
```json
{
  "property_type": "residential|commercial|industrial|land|mixed",
  "ownership_type": "personal|enterprise|investment",
  "address": {
    "line1": "string",
    "line2": "string",
    "city": "string",
    "province": "QC",
    "postal_code": "string"
  },
  "details": {
    "lot_size_sqft": 0,
    "building_size_sqft": 0,
    "year_built": 2000,
    "num_units": 1,
    "num_bedrooms": 0,
    "num_bathrooms": 0
  },
  "financial": {
    "purchase_price": 0,
    "purchase_date": "YYYY-MM-DD",
    "current_value": 0
  }
}
```

## List Properties
```http
GET /immobilier/properties
```

## Get Property Details
```http
GET /immobilier/properties/{property_id}
```

## Update Property
```http
PATCH /immobilier/properties/{property_id}
```

## Add Property Unit
```http
POST /immobilier/properties/{property_id}/units
```

## Create Tenant
```http
POST /immobilier/properties/{property_id}/tenants
```
```json
{
  "unit_id": "uuid (optional)",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string",
  "lease": {
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "monthly_rent": 0,
    "security_deposit": 0
  }
}
```

## Record Rent Payment
```http
POST /immobilier/tenants/{tenant_id}/payments
```
```json
{
  "amount": 0,
  "payment_date": "YYYY-MM-DD",
  "payment_method": "cheque|transfer|cash|interac",
  "period_start": "YYYY-MM-DD",
  "period_end": "YYYY-MM-DD"
}
```

## Create Maintenance Request
```http
POST /immobilier/properties/{property_id}/maintenance
```
```json
{
  "unit_id": "uuid (optional)",
  "title": "string",
  "description": "string",
  "category": "plumbing|electrical|hvac|appliance|structural|other",
  "priority": "low|medium|high|emergency"
}
```

## Get Portfolio Dashboard
```http
GET /immobilier/dashboard
```

## Get Rent Report
```http
GET /immobilier/reports/rent
```
Query Parameters:
- `property_id`: Filter by property
- `from`: Start date
- `to`: End date

---

# SECTION 11: CONSTRUCTION API

## Create Project
```http
POST /construction/projects
```
```json
{
  "name": "string",
  "description": "string",
  "project_type": "new_build|renovation|addition|repair|commercial",
  "property_id": "uuid (optional)",
  "dates": {
    "estimated_start": "YYYY-MM-DD",
    "estimated_end": "YYYY-MM-DD"
  },
  "budget": {
    "estimated": 0
  },
  "compliance": {
    "rbq_license_number": "string",
    "cnesst_registered": false,
    "ccq_compliant": false
  }
}
```

## List Projects
```http
GET /construction/projects
```

## Get Project Details
```http
GET /construction/projects/{project_id}
```

## Create Estimate
```http
POST /construction/projects/{project_id}/estimates
```
```json
{
  "estimate_name": "string",
  "profit_margin": 15.00
}
```

## Add Estimate Line Items
```http
POST /construction/estimates/{estimate_id}/items
```
```json
{
  "items": [
    {
      "category": "materials|labor|equipment|subcontractor|permit",
      "description": "string",
      "quantity": 0,
      "unit": "sqft|lf|each|hour|day|lot",
      "unit_cost": 0
    }
  ]
}
```

## Get Estimate Summary
```http
GET /construction/estimates/{estimate_id}
```

## Submit Estimate for Approval
```http
POST /construction/estimates/{estimate_id}/submit
```

## Search Materials Database
```http
GET /construction/materials
```
Query Parameters:
- `category`: Material category
- `search`: Search term

---

# SECTION 12: OCW API

## Create OCW Session
```http
POST /ocw/sessions
```
```json
{
  "workspace_id": "uuid",
  "session_type": "shareview|whiteboard|cockpit|collaboration"
}
```

## Join Session
```http
POST /ocw/sessions/{session_id}/join
```
```json
{
  "role": "editor|viewer|spectator"
}
```

## Leave Session
```http
POST /ocw/sessions/{session_id}/leave
```

## End Session
```http
POST /ocw/sessions/{session_id}/end
```

## Add Canvas Object
```http
POST /ocw/sessions/{session_id}/objects
```
```json
{
  "object_type": "shape|text|image|drawing|sticky|connector|frame",
  "position": {"x": 0, "y": 0},
  "size": {"width": 100, "height": 100},
  "properties": {}
}
```

## Update Canvas Object
```http
PATCH /ocw/sessions/{session_id}/objects/{object_id}
```

## Delete Canvas Object
```http
DELETE /ocw/sessions/{session_id}/objects/{object_id}
```

## Add Annotation
```http
POST /ocw/sessions/{session_id}/annotations
```
```json
{
  "object_id": "uuid (optional)",
  "annotation_type": "comment|highlight|marker|voice_note",
  "content": "string",
  "position": {"x": 0, "y": 0}
}
```

## Get Session State
```http
GET /ocw/sessions/{session_id}/state
```

## WebSocket Connection
```
wss://api.che-nu.com/v1/ocw/sessions/{session_id}/ws
```

---

# SECTION 13: XR API

## Create XR Room
```http
POST /xr/rooms
```
```json
{
  "name": "string",
  "room_type": "meeting|presentation|brainstorm|walkthrough|showroom",
  "room_template": "conference|amphitheater|open_space|custom",
  "dimensions": {"width": 10, "height": 3, "depth": 10},
  "dataspace_id": "uuid (optional)",
  "meeting_id": "uuid (optional)"
}
```

## List XR Rooms
```http
GET /xr/rooms
```

## Get Room Details
```http
GET /xr/rooms/{room_id}
```

## Add XR Object
```http
POST /xr/rooms/{room_id}/objects
```
```json
{
  "object_type": "model|screen|whiteboard|annotation|furniture",
  "position": {"x": 0, "y": 0, "z": 0},
  "rotation": {"x": 0, "y": 0, "z": 0},
  "scale": {"x": 1, "y": 1, "z": 1},
  "properties": {},
  "source_url": "string (for models)"
}
```

## Start XR Session
```http
POST /xr/rooms/{room_id}/sessions
```

## Join XR Session
```http
POST /xr/sessions/{session_id}/join
```
```json
{
  "avatar_config": {},
  "device_type": "vr_headset|ar_glasses|desktop|mobile"
}
```

## Update Participant Position
```http
PATCH /xr/sessions/{session_id}/position
```
```json
{
  "position": {"x": 0, "y": 0, "z": 0},
  "rotation": {"x": 0, "y": 0, "z": 0}
}
```

## WebSocket Connection (XR)
```
wss://api.che-nu.com/v1/xr/sessions/{session_id}/ws
```

---

# SECTION 14: FILE API

## Upload File
```http
POST /files/upload
```
Content-Type: multipart/form-data
```
file: <binary>
dataspace_id: uuid (optional)
```

## Get File Info
```http
GET /files/{file_id}
```

## Download File
```http
GET /files/{file_id}/download
```

## Transform File
```http
POST /files/{file_id}/transform
```
```json
{
  "transformation_type": "convert|extract|compress|ocr|transcribe",
  "output_format": "string",
  "parameters": {}
}
```

## Get Transformation Status
```http
GET /files/transformations/{transformation_id}
```

---

# SECTION 15: NOTIFICATIONS API

## List Notifications
```http
GET /notifications
```
Query Parameters:
- `unread`: true|false
- `type`: Notification type
- `page`: Page number

## Mark as Read
```http
POST /notifications/{notification_id}/read
```

## Mark All as Read
```http
POST /notifications/read-all
```

## Get Notification Preferences
```http
GET /notifications/preferences
```

## Update Notification Preferences
```http
PATCH /notifications/preferences
```

---

# WEBHOOKS

## Register Webhook
```http
POST /webhooks
```
```json
{
  "url": "https://your-server.com/webhook",
  "events": ["dataspace.created", "meeting.started", "task.completed"],
  "secret": "your_webhook_secret"
}
```

## Webhook Events
- `dataspace.created`
- `dataspace.updated`
- `dataspace.archived`
- `meeting.scheduled`
- `meeting.started`
- `meeting.ended`
- `task.created`
- `task.completed`
- `property.created`
- `tenant.created`
- `payment.received`
- `maintenance.created`
- `maintenance.completed`
- `agent.execution.completed`
- `workflow.completed`

## Webhook Payload Format
```json
{
  "event": "event.name",
  "timestamp": "ISO8601",
  "data": {},
  "identity_id": "uuid"
}
```

---

# RATE LIMITS

| Endpoint Category | Rate Limit |
|------------------|------------|
| Authentication | 10/minute |
| Read Operations | 1000/minute |
| Write Operations | 100/minute |
| Agent Executions | 50/minute |
| File Uploads | 20/minute |
| WebSocket Connections | 10 concurrent |

---

# SDK EXAMPLES

## JavaScript/TypeScript
```typescript
import { ChenuClient } from '@chenu/sdk';

const client = new ChenuClient({
  apiKey: 'your_api_key',
  identityId: 'your_identity_id'
});

// Create DataSpace
const dataspace = await client.dataspaces.create({
  name: 'My Project',
  dataspace_type: 'project'
});

// Execute 1-Click Command
const execution = await client.oneclick.execute({
  input: 'Create a construction estimate from this PDF',
  input_type: 'prompt'
});

// Subscribe to updates
client.on('dataspace.updated', (event) => {
  console.log('DataSpace updated:', event.data);
});
```

## Python
```python
from chenu import ChenuClient

client = ChenuClient(
    api_key='your_api_key',
    identity_id='your_identity_id'
)

# Create DataSpace
dataspace = client.dataspaces.create(
    name='My Project',
    dataspace_type='project'
)

# Execute 1-Click Command
execution = client.oneclick.execute(
    input='Create a construction estimate from this PDF',
    input_type='prompt'
)

# Get properties
properties = client.immobilier.properties.list()
```

---

*CHEÂ·NU API v29 - December 2024*
