# CHE·NU Semantic Encoding System

## Overview

The Semantic Encoding System is a core component of CHE·NU that provides a standardized, compact way to express human intent for AI agent processing. It bridges the gap between natural language requests (L0) and machine-executable instructions (L2) through a semantic layer (L1).

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENCODING PIPELINE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  L0: HUMAN INTENT                                                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ "Analyze the meeting notes and extract key decisions    │    │
│  │  with associated risks"                                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│                           │                                      │
│                           ▼                                      │
│  L1: SEMANTIC ENCODING                                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ {                                                        │    │
│  │   ACT: "ANA",                                           │    │
│  │   SRC: "MTG",                                           │    │
│  │   SCOPE: "SEL",                                         │    │
│  │   MODE: "ANA",                                          │    │
│  │   FOCUS: ["DEC", "RISK"],                               │    │
│  │   TRACE: 1                                              │    │
│  │ }                                                        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                           │                                      │
│                           ▼                                      │
│  L2: BINARY ENCODING                                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ E1301825Jk                                              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Encoding Structure

### Required Fields

| Field | Description | Values |
|-------|-------------|--------|
| ACT | Action type | SUM, EXT, STR, CMP, ANA, GEN, DEC, PLN, REF, VER, MAP, CLS |
| SRC | Source type | SEL, DOC, WS, MTG, EXT, MIX |
| SCOPE | Operation scope | SEL, DOC, WS, MTG, LOCK |
| MODE | Processing mode | ANA, PREP, DRAFT, CHECK, NONE |

### Optional Fields

| Field | Description | Values |
|-------|-------------|--------|
| FOCUS | Focus areas (max 5) | FACT, RISK, CONS, OPP, NEXT, DEC, GAP, OPT |
| OUT | Output format | MD, JSON, HTML, TXT, TABLE, CHART |
| LEN | Length hint | XS, S, M, L, XL, AUTO |
| RW | Rewrite flag | 0, 1 |
| UNC | Uncertainty flag | 0, 1 |
| SENS | Sensitive flag | 0, 1 |
| TRACE | Trace flag | 0, 1 |

### Action Types (ACT)

- **SUM**: Summarize content
- **EXT**: Extract specific information
- **STR**: Structure/format content
- **CMP**: Compare items
- **ANA**: Analyze in depth
- **GEN**: Generate new content
- **DEC**: Make/support decisions
- **PLN**: Create plans
- **REF**: Reference/cite
- **VER**: Verify/validate
- **MAP**: Map relationships
- **CLS**: Classify/categorize

### Source Types (SRC)

- **SEL**: Selected text/content
- **DOC**: Full document
- **WS**: Workspace context
- **MTG**: Meeting notes/transcript
- **EXT**: External sources
- **MIX**: Mixed sources

### Scope Levels (SCOPE)

- **SEL**: Selection only
- **DOC**: Document scope
- **WS**: Workspace scope
- **MTG**: Meeting scope
- **LOCK**: Locked/restricted scope (governance)

### Processing Modes (MODE)

- **ANA**: Analysis (read-only)
- **PREP**: Preparation
- **DRAFT**: Draft creation
- **CHECK**: Verification/review
- **NONE**: No specific mode

## EQS (Encoding Quality Score)

The EQS measures encoding quality on a 0-100 scale.

### Components

1. **Compression (35%)**: Token reduction ratio
   - ≤10% = 100 points
   - ≤20% = 95 points
   - ≤30% = 85 points
   - ≤50% = 70 points
   - >50% = 40 points

2. **Scope Control (25%)**: SCOPE + MODE strictness
   - LOCK = 100 points
   - SEL = 85 points
   - DOC = 70 points
   - MTG = 60 points
   - WS = 40 points
   - Penalties for RW=1 in ANA mode

3. **Focus Clarity (20%)**: Optimal FOCUS count
   - 2 items = 95 points (optimal)
   - 3 items = 90 points
   - 1 item = 75 points
   - 0 items = 60 points
   - 4+ items = decreasing

4. **Risk Management (20%)**: Governance flags
   - TRACE=1 = +15 points
   - UNC=1 = +10 points
   - SENS=1 + LOCK = +10 points
   - RW=1 without TRACE = -20 points

### Grades

| Score | Grade | Emoji |
|-------|-------|-------|
| 80-100 | Optimal | 🟢🟢 |
| 60-79 | Good | 🟢 |
| 30-59 | OK | 🟠 |
| 0-29 | Poor | 🔴 |

## Governance Rules (Tree Laws)

1. **SENS=1 requires LOCK scope**: Sensitive operations must be locked
2. **RW=1 forbidden in ANA mode**: Cannot rewrite during analysis
3. **SCOPE=LOCK forbids WS source**: Locked scope cannot access workspace
4. **FOCUS limited to 5 items**: Maximum cognitive focus
5. **TRACE required for SENS=1 or RW=1**: Audit trail mandatory

## Binary Encoding Format

The binary format provides compact representation:

```
E 1 3 0 1 8 2 5 J k
│ │ │ │ │ │ │ │ └─┴─ Checksum (2 chars)
│ │ │ │ │ │ │ └───── FOCUS item indices
│ │ │ │ │ │ └─────── FOCUS count
│ │ │ │ │ └───────── Flags (RW|UNC|SENS|TRACE)
│ │ │ │ └─────────── MODE index
│ │ │ └───────────── SCOPE index
│ │ └─────────────── SRC index
│ └───────────────── ACT index
└─────────────────── Version marker
```

## Thread Management

Threads track the complete encoding lifecycle:

```typescript
interface ChenuThread {
  id: string;              // thread_xxxxxxxxxxxx
  human: string;           // Original intent
  encoded: SemanticEncoding;
  optimized?: SemanticEncoding;
  binary?: string;
  eqs: number;
  state: ThreadState;      // draft → analyzed → proposed → accepted → executed → archived
  versions: ThreadVersion[];
  sphereId?: string;
  projectId?: string;
  agentId?: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}
```

### Thread States

1. **draft**: Initial creation
2. **analyzed**: Encoding validated and optimized
3. **proposed**: Ready for human review
4. **accepted**: Human approved
5. **executed**: Agent processed
6. **archived**: Completed/stored

## Agent Compatibility

Agents declare their encoding capabilities:

```typescript
interface AgentEncodingSpec {
  id: string;
  name: string;
  actions: ACT[];           // Supported actions
  sources: SRC[];           // Supported sources
  maxFocus?: number;        // Max FOCUS items
  minEncodingLevel: 'L1' | 'L2';
  sphere?: string;          // Sphere specialization
}
```

### Compatibility Check

1. ACT must be in agent's actions list
2. SRC must be in agent's sources list
3. FOCUS count ≤ agent's maxFocus (if defined)
4. Encoding level must meet agent's minimum

## Presets

Pre-configured encoding templates:

### Universal Presets

| Name | ACT | SRC | SCOPE | MODE | FOCUS |
|------|-----|-----|-------|------|-------|
| quick-summary | SUM | DOC | SEL | ANA | - |
| meeting-analysis | ANA | MTG | SEL | ANA | DEC, NEXT |
| risk-assessment | ANA | DOC | LOCK | CHECK | RISK, GAP |

### Construction Sphere

| Name | ACT | SRC | SCOPE | MODE | FOCUS | Flags |
|------|-----|-----|-------|------|-------|-------|
| rbq-compliance | VER | DOC | LOCK | CHECK | RISK, GAP | SENS, TRACE |
| cnesst-safety | VER | DOC | LOCK | CHECK | RISK | SENS, TRACE |
| ccq-verify | VER | DOC | LOCK | CHECK | FACT, GAP | SENS, TRACE |

### Finance Sphere

| Name | ACT | SRC | SCOPE | MODE | FOCUS | Flags |
|------|-----|-----|-------|------|-------|-------|
| financial-analysis | ANA | DOC | LOCK | CHECK | FACT, RISK | SENS, TRACE |
| budget-review | CMP | DOC | LOCK | CHECK | FACT, GAP | TRACE |

## API Reference

### Validation

```typescript
validateEncoding(encoding: SemanticEncoding): ValidationResult
```

### EQS Computation

```typescript
computeEQS(humanTokens: number, encodedTokens: number, encoding: SemanticEncoding): number
computeEQSFull(...): EQSResult
```

### Optimization

```typescript
optimizeEncoding(encoding: SemanticEncoding): SemanticEncoding
optimizeEncodingFull(encoding: SemanticEncoding): OptimizationResult
```

### Binary Encoding

```typescript
toBinary(encoding: SemanticEncoding): string
fromBinary(binary: string): SemanticEncoding
```

### Thread Management

```typescript
createThread(options: CreateThreadOptions): ChenuThread
getThread(id: string): ChenuThread | undefined
updateThread(id: string, updates: ThreadUpdate): ChenuThread | undefined
listThreads(filters?: ThreadFilters): ChenuThread[]
```

### Agent Matching

```typescript
checkCompatibility(encoding: SemanticEncoding, agent: AgentEncodingSpec): CompatibilityResult
findCompatibleAgents(encoding: SemanticEncoding, sphereId?: string): AgentEncodingSpec[]
```

## Best Practices

1. **Start with presets**: Use sphere-specific presets as starting points
2. **Optimize before execution**: Always run optimization for better EQS
3. **Use LOCK for sensitive data**: Enable governance controls
4. **Limit FOCUS to 2-3 items**: Optimal clarity
5. **Enable TRACE for audit**: Required for compliance
6. **Validate before saving**: Catch issues early

## Integration Example

```typescript
// 1. Get preset
const preset = getPreset('meeting-analysis');

// 2. Customize
const encoding: SemanticEncoding = {
  ...preset.encoding,
  FOCUS: ['DEC', 'RISK', 'NEXT'],
  TRACE: 1,
};

// 3. Validate
const validation = validateEncoding(encoding);
if (!validation.valid) throw new Error(validation.errors[0]);

// 4. Optimize
const { optimized, changes } = optimizeEncodingFull(encoding);

// 5. Compute EQS
const eqs = computeEQSFull(humanTokens, 50, optimized);
console.log(`EQS: ${eqs.score} (${eqs.grade})`);

// 6. Find agent
const agents = findCompatibleAgents(optimized, 'construction');
const agent = agents[0];

// 7. Create thread
const thread = createThread({
  human: 'Analyze meeting notes...',
  encoding: optimized,
  sphereId: 'construction',
});

// 8. Execute with agent
// ... agent processing ...

// 9. Update state
updateThread(thread.id, { state: 'executed' });
```

## Version History

- **v1.0**: Initial encoding system
- **v1.1**: Added EQS computation, binary encoding
- **v1.2**: Added thread management, governance rules
- **v1.3**: Added agent compatibility, presets

---

*Part of the CHE·NU Platform - Pro-Service Construction*
