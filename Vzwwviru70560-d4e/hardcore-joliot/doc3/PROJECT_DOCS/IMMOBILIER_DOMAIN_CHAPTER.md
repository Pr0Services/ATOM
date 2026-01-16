# IMMOBILIER DOMAIN â€” COMPLETE SPECIFICATION

## Chapter 61: Immobilier Domain Overview

### Introduction

The Immobilier Domain represents CHEÂ·NU's comprehensive property management capability, designed to handle the complete lifecycle of real estate ownership, rental operations, and property development. Unlike other domains that exist within single spheres, Immobilier operates as a **cross-sphere domain**, functioning differently within Personal (MAISON) and Enterprise (ENTREPRISE) contexts while maintaining unified data structures and agent architectures.

### Domain Definition

The Immobilier Domain is CHEÂ·NU's dedicated property management system. It is NOT a sphereâ€”it is a specialized domain that manifests within existing spheres:

- **Within MAISON (Personal Sphere)**: Manages personal properties including primary residences, secondary homes, condos, duplexes, triplexes, land parcels, and investment properties owned by individuals.

- **Within ENTREPRISE (Enterprise Sphere)**: Handles professional property management operations including multi-unit buildings, commercial properties, rental portfolios, tenant management, and real estate investment analysis.

This dual-context architecture enables seamless scaling from individual homeowners to professional property management companies within the same unified system.

### Core Capabilities

**Personal Context (MAISON)**
- Property document management and organization
- Insurance policy tracking and renewal reminders
- Tax assessment and payment scheduling
- Mortgage tracking and amortization visualization
- Maintenance scheduling and history
- Renovation project planning
- Property value estimation and market tracking
- Utility management and consumption analysis
- Security system integration
- Home automation coordination

**Enterprise Context (ENTREPRISE)**
- Multi-property portfolio management
- Tenant database and communication
- Lease contract lifecycle management
- Rent collection and payment tracking
- Maintenance request processing
- Inspection scheduling and documentation
- Financial reporting and ROI analysis
- Vacancy management and marketing
- Compliance and regulatory tracking
- Property acquisition analysis

---

## Chapter 62: Immobilier DataSpace Architecture

### DataSpace Concept

Every property within CHEÂ·NU exists as its own dedicated DataSpace. This architectural decision ensures that all information related to a property remains contextually connected while enabling sophisticated cross-property analysis and reporting.

### Personal Property DataSpace Structure

```
Property DataSpace: [Property Name]
â”œâ”€â”€ ðŸ“„ Documents/
â”‚   â”œâ”€â”€ Ownership/
â”‚   â”‚   â”œâ”€â”€ deed.pdf
â”‚   â”‚   â”œâ”€â”€ survey.pdf
â”‚   â”‚   â””â”€â”€ title_insurance.pdf
â”‚   â”œâ”€â”€ Insurance/
â”‚   â”‚   â”œâ”€â”€ homeowners_policy.pdf
â”‚   â”‚   â””â”€â”€ flood_insurance.pdf
â”‚   â”œâ”€â”€ Taxes/
â”‚   â”‚   â”œâ”€â”€ assessment_2024.pdf
â”‚   â”‚   â””â”€â”€ payment_receipts/
â”‚   â”œâ”€â”€ Mortgage/
â”‚   â”‚   â”œâ”€â”€ loan_agreement.pdf
â”‚   â”‚   â””â”€â”€ amortization_schedule.xlsx
â”‚   â””â”€â”€ Utilities/
â”‚       â”œâ”€â”€ hydro_contracts/
â”‚       â””â”€â”€ gas_contracts/
â”œâ”€â”€ ðŸ–¼ï¸ Media/
â”‚   â”œâ”€â”€ Photos/
â”‚   â”‚   â”œâ”€â”€ exterior/
â”‚   â”‚   â”œâ”€â”€ interior/
â”‚   â”‚   â””â”€â”€ damage_documentation/
â”‚   â”œâ”€â”€ Videos/
â”‚   â”‚   â””â”€â”€ property_walkthrough.mp4
â”‚   â””â”€â”€ XR_Scenes/
â”‚       â”œâ”€â”€ renovation_visualization.xr
â”‚       â””â”€â”€ space_planning.xr
â”œâ”€â”€ ðŸ”§ Maintenance/
â”‚   â”œâ”€â”€ scheduled_tasks/
â”‚   â”œâ”€â”€ completed_history/
â”‚   â”œâ”€â”€ contractor_contacts/
â”‚   â””â”€â”€ warranties/
â”œâ”€â”€ ðŸ—ï¸ Renovations/
â”‚   â”œâ”€â”€ current_projects/
â”‚   â”œâ”€â”€ completed_projects/
â”‚   â”œâ”€â”€ planned_projects/
â”‚   â””â”€â”€ permits/
â”œâ”€â”€ ðŸ’° Finance/
â”‚   â”œâ”€â”€ expenses/
â”‚   â”œâ”€â”€ improvements_log/
â”‚   â”œâ”€â”€ value_tracking/
â”‚   â””â”€â”€ tax_deductions/
â”œâ”€â”€ ðŸ“… Calendar/
â”‚   â”œâ”€â”€ maintenance_schedule/
â”‚   â”œâ”€â”€ inspection_dates/
â”‚   â””â”€â”€ payment_deadlines/
â”œâ”€â”€ ðŸ“ Notes/
â”‚   â””â”€â”€ agent_outputs/
â””â”€â”€ ðŸ”— Linked_Spaces/
    â”œâ”€â”€ family_members/
    â””â”€â”€ related_projects/
```

### Enterprise Property DataSpace Structure

Enterprise DataSpaces extend the personal structure with additional business-critical components:

```
Enterprise Property DataSpace: [Building/Portfolio Name]
â”œâ”€â”€ [All Personal Structure Elements]
â”œâ”€â”€ ðŸ‘¥ Tenants/
â”‚   â”œâ”€â”€ [Unit_101]/
â”‚   â”‚   â”œâ”€â”€ tenant_profile.json
â”‚   â”‚   â”œâ”€â”€ lease_agreement.pdf
â”‚   â”‚   â”œâ”€â”€ payment_history/
â”‚   â”‚   â”œâ”€â”€ communication_log/
â”‚   â”‚   â””â”€â”€ maintenance_requests/
â”‚   â”œâ”€â”€ [Unit_102]/
â”‚   â””â”€â”€ [Unit_103]/
â”œâ”€â”€ ðŸ“‹ Leases/
â”‚   â”œâ”€â”€ active/
â”‚   â”œâ”€â”€ expired/
â”‚   â”œâ”€â”€ templates/
â”‚   â””â”€â”€ renewal_queue/
â”œâ”€â”€ ðŸ’³ Payments/
â”‚   â”œâ”€â”€ rent_tracking/
â”‚   â”œâ”€â”€ security_deposits/
â”‚   â”œâ”€â”€ late_fees/
â”‚   â””â”€â”€ payment_plans/
â”œâ”€â”€ ðŸ” Inspections/
â”‚   â”œâ”€â”€ move_in/
â”‚   â”œâ”€â”€ move_out/
â”‚   â”œâ”€â”€ annual/
â”‚   â””â”€â”€ complaint_based/
â”œâ”€â”€ ðŸ“Š Analytics/
â”‚   â”œâ”€â”€ occupancy_rates/
â”‚   â”œâ”€â”€ revenue_analysis/
â”‚   â”œâ”€â”€ expense_breakdown/
â”‚   â””â”€â”€ roi_calculations/
â”œâ”€â”€ ðŸ“£ Marketing/
â”‚   â”œâ”€â”€ listings/
â”‚   â”œâ”€â”€ photos_staging/
â”‚   â””â”€â”€ virtual_tours/
â””â”€â”€ âš–ï¸ Compliance/
    â”œâ”€â”€ licenses/
    â”œâ”€â”€ certifications/
    â””â”€â”€ regulatory_filings/
```

### DataSpace Engine Integration

The Immobilier Domain integrates deeply with CHEÂ·NU's DataSpace Engine through:

**Automatic Classification**: Documents uploaded to property DataSpaces are automatically classified and filed in appropriate categories using AI-powered document analysis.

**Cross-Property Queries**: Users can query across all properties simultaneously ("Show all maintenance due this month across all properties").

**Temporal Tracking**: All changes are version-controlled, enabling historical analysis of property evolution.

**Smart Linking**: Properties automatically link to relevant entities (contractors, tenants, family members) creating a rich knowledge graph.

---

## Chapter 63: Immobilier Agents

### Agent Hierarchy

The Immobilier Domain implements a specialized agent hierarchy following CHEÂ·NU's L0-L3 governance structure:

### L3 â€” Domain Coordinator Agent

**Immobilier Domain Coordinator**
- Role: Orchestrates all property-related operations across the domain
- Responsibilities:
  - Coordinates between Personal and Enterprise contexts
  - Escalates complex decisions to appropriate human authorities
  - Maintains domain-wide compliance standards
  - Generates portfolio-level insights and reports
- Elevation: Reports to MAISON or ENTREPRISE sphere coordinators depending on context

### L2 â€” Specialist Agents

**Property Manager Agent**
- Context: Both Personal and Enterprise
- Capabilities:
  - Comprehensive property oversight
  - Document organization and retrieval
  - Deadline tracking and reminders
  - Value estimation and market analysis
  - Integration with Finance Domain for property-specific accounting
- Personality: Meticulous, proactive, detail-oriented
- Communication: Professional, clear, actionable

**Maintenance Coordinator Agent**
- Context: Both Personal and Enterprise
- Capabilities:
  - Maintenance scheduling and prioritization
  - Contractor coordination and dispatch
  - Work order management
  - Warranty tracking
  - Preventive maintenance planning
  - Integration with Construction Domain for major repairs
- Personality: Efficient, systematic, safety-conscious
- Communication: Technical when needed, clear instructions

**Renovation Advisor Agent**
- Context: Both Personal and Enterprise
- Capabilities:
  - Renovation planning and budgeting
  - Permit requirement identification
  - Contractor recommendation
  - Design suggestion generation
  - ROI analysis for improvements
  - Integration with Architecture Domain for design work
- Personality: Creative, practical, budget-conscious
- Communication: Inspirational yet realistic

**Tenant Communication Agent** (Enterprise Only)
- Context: Enterprise only
- Capabilities:
  - Professional tenant communication
  - Lease explanation and negotiation support
  - Complaint handling and resolution
  - Move-in/move-out coordination
  - Community announcement management
- Personality: Diplomatic, professional, empathetic
- Communication: Warm but businesslike

### L1 â€” Task Execution Agents

**Document Filing Agent**
- Automatically categorizes and files incoming property documents

**Payment Tracking Agent**
- Monitors rent payments, mortgage payments, and utility bills

**Inspection Scheduler Agent**
- Coordinates property inspection schedules

**Maintenance Request Router Agent**
- Triages and routes maintenance requests to appropriate handlers

**Lease Renewal Agent**
- Tracks lease expirations and initiates renewal workflows

### L0 â€” Interface Agents

**Property Dashboard Agent**
- Presents unified property views to users

**Notification Agent**
- Delivers timely alerts about property matters

**Search Agent**
- Handles property-related search queries

### Agent Governance

All Immobilier agents operate within CHEÂ·NU's governance framework:

- **Action Logging**: Every agent action is logged with timestamp, context, and justification
- **Elevation Protocols**: Financial decisions above threshold require human approval
- **Privacy Protection**: Tenant data is protected; agents cannot share between unrelated contexts
- **Audit Trail**: Complete audit trail for regulatory compliance

---

## Chapter 64: Immobilier Workflows

### Personal Property Workflows

#### Workflow 1: Property Onboarding

**Trigger**: User adds new property to Personal Sphere

**Steps**:
1. **Property Registration**
   - Property Manager Agent collects basic property information
   - Creates dedicated DataSpace for property
   - Establishes folder structure

2. **Document Collection**
   - Agent prompts for essential documents (deed, insurance, mortgage)
   - Document Filing Agent processes and categorizes uploads
   - Extracts key dates and amounts for tracking

3. **Financial Setup**
   - Integration with Finance Domain established
   - Mortgage tracking configured if applicable
   - Property tax calendar created

4. **Maintenance Baseline**
   - Maintenance Coordinator creates property maintenance profile
   - Suggests initial inspection checklist
   - Establishes seasonal maintenance calendar

5. **Media Collection**
   - Agent prompts for property photos
   - XR scene generation offered for space planning

**Completion**: Property fully integrated, dashboard populated, reminders active

#### Workflow 2: Maintenance Cycle

**Trigger**: Scheduled maintenance due OR maintenance issue reported

**Steps**:
1. **Issue Identification**
   - User reports issue OR scheduled maintenance triggered
   - Maintenance Coordinator assesses urgency and category

2. **Action Planning**
   - For DIY tasks: Provides instructions and material lists
   - For contractor tasks: Suggests appropriate contractors from database
   - For emergency: Escalates immediately with emergency contacts

3. **Scheduling**
   - Coordinates with user calendar
   - Schedules contractor if needed
   - Sends reminders as date approaches

4. **Execution Tracking**
   - Tracks work in progress
   - Documents completion with photos
   - Records costs in Finance integration

5. **Follow-up**
   - Schedules any required follow-up
   - Updates maintenance history
   - Adjusts future maintenance predictions

#### Workflow 3: Renovation Planning

**Trigger**: User expresses renovation interest

**Steps**:
1. **Scope Definition**
   - Renovation Advisor gathers project goals
   - Identifies affected areas and systems
   - Assesses structural implications

2. **Design Phase**
   - Integration with Architecture Domain for design concepts
   - XR visualization generation for approval
   - Material and finish selection assistance

3. **Budgeting**
   - Cost estimation with market-rate data
   - ROI analysis for value-add improvements
   - Financing options if needed

4. **Permit Analysis**
   - Identifies required permits (Quebec RBQ compliance)
   - Tracks permit application status
   - Schedules required inspections

5. **Contractor Coordination**
   - Integration with Construction Domain
   - Bid collection and comparison
   - Contract review assistance

6. **Project Execution**
   - Timeline tracking
   - Payment milestone management
   - Quality checkpoint documentation

7. **Completion**
   - Final inspection coordination
   - Document archival (permits, warranties)
   - Property value update

### Enterprise Property Workflows

#### Workflow 4: Tenant Onboarding

**Trigger**: New lease signed

**Steps**:
1. **Lease Processing**
   - Lease Renewal Agent processes signed agreement
   - Extracts key terms, dates, amounts
   - Creates tenant profile in property DataSpace

2. **Welcome Package**
   - Tenant Communication Agent generates welcome materials
   - Provides building rules, emergency contacts, utility setup
   - Schedules move-in inspection

3. **Financial Setup**
   - Payment Tracking Agent configures rent tracking
   - Security deposit recorded
   - First payment scheduled

4. **Move-in Inspection**
   - Inspection Scheduler coordinates date
   - Generates inspection checklist
   - Documents property condition with photos/video

5. **Access Provisioning**
   - Key/access code documentation
   - Parking assignment if applicable
   - Building amenity access

#### Workflow 5: Rent/Payment Tracking

**Trigger**: Monthly rent cycle

**Steps**:
1. **Payment Monitoring**
   - Payment Tracking Agent monitors for incoming payments
   - Matches payments to expected amounts
   - Records in tenant payment history

2. **Reminder Sequence** (if payment not received)
   - Day 1 of grace period: Friendly reminder
   - Day 5: Payment required notice
   - Day 10: Late fee warning
   - Day 15: Formal late notice with fee

3. **Issue Resolution**
   - Payment plan negotiation if needed
   - Partial payment handling
   - Escalation protocols for non-payment

4. **Financial Integration**
   - Updates Finance Domain with revenue
   - Generates receipts for tenants
   - Reconciles with bank deposits

#### Workflow 6: Property Inspection

**Trigger**: Scheduled inspection OR complaint-based inspection

**Steps**:
1. **Scheduling**
   - Tenant Communication Agent coordinates with tenant
   - Respects notice requirements (Quebec: 24 hours minimum)
   - Confirms appointment

2. **Preparation**
   - Generates inspection checklist based on property type
   - Loads previous inspection data for comparison
   - Prepares documentation tools

3. **Execution**
   - Guided inspection workflow
   - Photo/video documentation
   - Note-taking with voice transcription

4. **Report Generation**
   - Comprehensive inspection report created
   - Issue categorization (immediate, routine, cosmetic)
   - Work order generation for identified issues

5. **Follow-up**
   - Tenant notification of findings
   - Maintenance scheduling for issues
   - Documentation archival

#### Workflow 7: Financial Reporting

**Trigger**: Monthly/quarterly/annual reporting cycle

**Steps**:
1. **Data Collection**
   - Aggregates income across all units
   - Consolidates expenses by category
   - Collects maintenance costs

2. **Analysis**
   - Occupancy rate calculation
   - Revenue vs. projection comparison
   - Expense variance analysis
   - Cash flow statement generation

3. **Report Generation**
   - Property-level P&L statements
   - Portfolio summary report
   - Tax preparation documents
   - Investor reports if applicable

4. **Insight Generation**
   - Identifies optimization opportunities
   - Predicts upcoming major expenses
   - Suggests rent adjustment recommendations

---

## Chapter 65: Immobilier Engine Integration

### Core Engine Integrations

The Immobilier Domain integrates with all major CHEÂ·NU engines:

#### DataSpace Engine
- Property DataSpaces managed through DataSpace Engine
- Cross-property queries enabled
- Version control for all documents
- Smart linking between properties and entities

#### Thread Engine
- Property-related conversations tracked as threads
- Tenant communication history preserved
- Contractor correspondence organized
- Decision audit trails maintained

#### Workspace Engine
- Property workspaces for focused management
- Multi-property portfolio workspaces
- Renovation project workspaces
- Transaction workspaces for acquisitions

#### File Transformation Engine
- Property documents converted between formats
- Photo optimization for storage
- Report generation in multiple formats
- Contract template population

#### Finance Domain Engine
- Property-specific accounting
- Rental income tracking
- Expense categorization
- Tax document preparation
- ROI and cash flow analysis
- Mortgage amortization tracking

#### Construction Domain Integration
- Major renovation coordination
- Contractor database sharing
- Material cost integration
- Permit workflow coordination
- Quality standards compliance

#### Architecture Domain Integration
- Design services for renovations
- Space planning tools
- XR visualization generation
- Building code compliance checking

#### Multi-Identity Engine
- Property ownership structures (personal, corporate, trust)
- Tenant identity management
- Contractor profile management
- Role-based access for property managers

#### XR Spatial Engine
- Property 3D modeling
- Renovation visualization
- Virtual staging for vacant units
- Before/after comparisons
- Space planning tools

---

## Chapter 66: Immobilier XR Integration

### Extended Reality Capabilities

The Immobilier Domain leverages CHEÂ·NU's XR Spatial Engine for powerful property visualization:

#### Property Visualization

**3D Property Modeling**
- Automatic floor plan generation from photos
- 3D model creation from video walkthroughs
- Accurate measurement extraction
- Material and finish capture

**Virtual Tours**
- Generate shareable virtual property tours
- Hotspot annotations for features
- Guided tour path creation
- Integration with listing platforms

#### Renovation Visualization

**Before/After Comparison**
- Current state capture
- Proposed renovation overlay
- Side-by-side comparison views
- Animated transformation sequences

**Design Preview**
- Material and color changes
- Furniture and fixture placement
- Lighting simulation
- Structural modification visualization

**Cost Overlay**
- Visual cost breakdown by area
- Material cost per square foot
- Labor cost estimates
- Total project cost visualization

#### Space Planning

**Furniture Layout**
- Drag-and-drop furniture placement
- Scale-accurate visualization
- Traffic flow analysis
- Optimization suggestions

**Storage Solutions**
- Custom storage design
- Space utilization analysis
- Organization system planning

#### Enterprise XR Applications

**Vacant Unit Staging**
- Virtual furniture staging for listings
- Multiple style options
- Cost-effective marketing solution

**Property Inspection**
- AR-guided inspection checklists
- Issue annotation directly on 3D model
- Historical comparison views

**Maintenance Training**
- AR maintenance guides
- Equipment location overlay
- Repair procedure visualization

---

## Chapter 67: Immobilier User Experience

### Dashboard Views

#### Personal Property Dashboard

**Overview Card**
- Property photo/thumbnail
- Current estimated value
- Next action required
- Alerts and notifications

**Financial Summary**
- Monthly costs breakdown
- Mortgage remaining
- Property tax status
- Insurance renewal date

**Maintenance Status**
- Upcoming maintenance tasks
- Overdue items (highlighted)
- Recent completions
- Contractor activity

**Document Quick Access**
- Recently accessed documents
- Important documents pinned
- Search functionality
- Upload new document

#### Enterprise Portfolio Dashboard

**Portfolio Overview**
- Total units managed
- Occupancy rate
- Monthly revenue
- Vacancy alerts

**Property Grid**
- All properties at a glance
- Status indicators
- Quick action menus
- Filter and sort options

**Financial Performance**
- Revenue vs. expenses graph
- Collection rate
- Upcoming payments due
- Cash flow projection

**Tenant Overview**
- Active tenants count
- Lease renewals upcoming
- Open maintenance requests
- Communication queue

**Alerts & Tasks**
- Priority items requiring attention
- Scheduled inspections
- Lease expirations
- Compliance deadlines

### Mobile Experience

**Property Access**
- Quick property switching
- Essential info at fingertips
- Emergency contacts one tap away

**On-Site Tools**
- Camera integration for documentation
- GPS verification for inspections
- Offline access to critical documents
- Quick note and voice memo

**Tenant Communication**
- In-app messaging
- Push notification delivery
- Call logging
- Communication history

### Natural Language Interface

Users can interact with Immobilier through natural conversation:

- "What maintenance is due on the Brossard duplex?"
- "Show me all properties with lease renewals in the next 90 days"
- "Create a renovation plan for the kitchen in my primary residence"
- "What's my total rental income across all properties this year?"
- "Schedule an inspection for Unit 204 next Thursday"
- "Generate a virtual tour for the vacant commercial space"

---

## Chapter 68: Immobilier Compliance (Quebec Focus)

### Regulatory Framework

The Immobilier Domain maintains compliance with Quebec's property and rental regulations:

#### RÃ©gie du bÃ¢timent du QuÃ©bec (RBQ)
- Contractor license verification
- Permit requirement identification
- Construction code compliance
- Inspection coordination

#### Tribunal administratif du logement (TAL)
- Lease template compliance
- Rent increase guidelines
- Tenant rights adherence
- Dispute process guidance

#### Municipal Regulations
- Zoning compliance awareness
- Property tax integration
- Building permit tracking
- Certificate of occupancy management

### Enterprise Compliance Features

**Document Retention**
- Automatic retention period tracking
- Compliant document archival
- Audit-ready organization

**Tenant Notification Compliance**
- Notice period calculations
- Required format templates
- Delivery tracking
- Documentation for disputes

**Financial Compliance**
- Rent increase limit calculations
- Security deposit regulations
- Receipt generation
- Tax document preparation

---

## Chapter 69: Immobilier Cross-Domain Interactions

### Domain Interconnections

The Immobilier Domain creates rich connections across CHEÂ·NU's ecosystem:

#### Finance Domain
- Property accounting integration
- Tax optimization suggestions
- Investment analysis
- Cash flow management
- Budget planning

#### Construction Domain
- Renovation project execution
- Contractor coordination
- Material procurement
- Quality management
- Safety compliance

#### Architecture Domain
- Design services
- Space planning
- Building code compliance
- Permit documentation

#### Social Domain
- Tenant relationships
- Contractor networks
- Community connections

#### Creative Domain
- Property marketing materials
- Listing photography
- Virtual staging
- Promotional content

#### Scholar Domain
- Market research
- Property law learning
- Investment education
- Industry trends

### Integration Example: Complete Renovation Flow

1. **Immobilier**: Identifies renovation need, initiates project
2. **Architecture**: Creates design concept, generates plans
3. **Construction**: Coordinates execution, manages contractors
4. **Finance**: Tracks budget, processes payments
5. **Creative**: Generates marketing content if property is rental
6. **Immobilier**: Archives documentation, updates property value

---

## Chapter 70: Immobilier Glossary

**DataSpace**: A dedicated data container for a property containing all related documents, media, and metadata.

**Property Manager Agent**: L2 agent responsible for comprehensive property oversight.

**Maintenance Coordinator Agent**: L2 agent managing all maintenance operations.

**Renovation Advisor Agent**: L2 agent specializing in improvement planning.

**Tenant Communication Agent**: L2 agent (Enterprise only) handling tenant relations.

**TAL**: Tribunal administratif du logement â€” Quebec's rental housing tribunal.

**RBQ**: RÃ©gie du bÃ¢timent du QuÃ©bec â€” Quebec's construction regulatory body.

**XR Scene**: Extended Reality visualization of a property space.

**Property Onboarding**: Workflow for adding a new property to CHEÂ·NU.

**Tenant Onboarding**: Workflow for adding a new tenant to a rental property.

---

*End of Immobilier Domain Chapters*
