#!/usr/bin/env python3
"""
CHE·NU — R&D Linter (Auto)
Purpose:
- Lint R&D proposals to prevent drift, duplication, and forbidden inter-sphere connections.
- Enforce: user-type first, need format, sphere freeze, allowed connection types, human validation, autonomy isolation.

Usage:
  python chenu_rnd_lint.py --in proposal.md
  python chenu_rnd_lint.py --in proposal.md --json-out report.json
  python chenu_rnd_lint.py --in proposal.md --fail-on-warn

Expected input format (in proposal.md):
  USER TYPE: ...
  CONTEXT: ...
  HUMAN ACTION: ...
  NEED: ...
  WHAT MUST NEVER BE AUTOMATED: ...
  FAILURE RISK: ...
  SPHERES: Personal, Scholar, ...
  CONNECTION TYPE: Projection | Request | Reference | Delegation
  HUMAN VALIDATION: ...
  UNDO/REVERSIBILITY: ...
  REDUNDANCY CHECK: ...

You can also include multiple proposals in one file by repeating the block fields.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

FROZEN_SPHERES = {
    "Personal",
    "Business",
    "Government & Institutions",
    "Creative Studio",
    "Community",
    "Social & Media",
    "Entertainment",
    "My Team",
    "Scholar",
}

ALLOWED_CONNECTION_TYPES = {"Projection", "Request", "Reference", "Delegation"}

REQUIRED_FIELDS = [
    "USER TYPE",
    "CONTEXT",
    "HUMAN ACTION",
    "NEED",
    "WHAT MUST NEVER BE AUTOMATED",
    "FAILURE RISK",
    "SPHERES",
    # CONNECTION TYPE is required ONLY if inter-sphere is claimed; we still lint it if present.
    "HUMAN VALIDATION",
    "UNDO/REVERSIBILITY",
    "REDUNDANCY CHECK",
]

# Heuristics: terms that often signal forbidden automation or drift.
FORBIDDEN_AUTOMATION_PATTERNS = [
    r"\bauto[- ]?execute\b",
    r"\bautomatic(ally)?\b",
    r"\bsilent action\b",
    r"\bbackground sync\b",
    r"\bwithout (explicit )?approval\b",
    r"\bauto[- ]?publish\b",
    r"\bauto[- ]?post\b",
    r"\bauto[- ]?merge\b",
    r"\bauto[- ]?commit\b",
    r"\bself[- ]?approve\b",
    r"\bdecide(s|d)? on behalf\b",
    r"\boptimi[sz]e engagement\b",
    r"\binfinite scroll\b",
]

# High-risk phrases specific to My Team automation drift
MYTEAM_RISK_PATTERNS = [
    r"\bassign(s|ed|ing)? automatically\b",
    r"\bauto[- ]?delegate\b",
    r"\bteam decision\b",
    r"\bgroup voice\b",
    r"\bresolve conflict(s)? automatically\b",
    r"\bprioriti[sz]e automatically\b",
    r"\bschedule automatically\b",
]

# Minimal requirement: human validation must show explicit gating language
HUMAN_GATING_HINTS = [
    "explicit",
    "approve",
    "confirm",
    "human",
    "review",
    "validation",
    "click",
    "per-action",
]

@dataclass
class Finding:
    level: str  # "ERROR" | "WARN" | "INFO"
    code: str
    message: str
    suggestion: Optional[str] = None
    line: Optional[int] = None

@dataclass
class ProposalReport:
    proposal_index: int
    findings: List[Finding]
    extracted: Dict[str, str]

def normalize_key(k: str) -> str:
    return re.sub(r"\s+", " ", k.strip().upper())

def split_into_proposals(text: str) -> List[Tuple[int, int, str]]:
    """
    Split text into proposal blocks.
    Heuristic: each time we see "USER TYPE:" start a new block.
    Returns list of (start_line, end_line, block_text).
    """
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines) if re.match(r"^\s*USER TYPE\s*:", ln, flags=re.I)]
    if not starts:
        return [(0, len(lines) - 1 if lines else 0, text)]
    blocks = []
    for idx, s in enumerate(starts):
        e = (starts[idx + 1] - 1) if idx + 1 < len(starts) else (len(lines) - 1)
        block = "\n".join(lines[s : e + 1])
        blocks.append((s + 1, e + 1, block))  # 1-indexed line numbers
    return blocks

def parse_fields(block: str) -> Dict[str, str]:
    """
    Parse "KEY: value" lines. Multi-line values supported until next KEY: line.
    """
    lines = block.splitlines()
    fields: Dict[str, List[str]] = {}
    current_key: Optional[str] = None

    key_re = re.compile(r"^\s*([A-Z][A-Z0-9 \&/\-]+?)\s*:\s*(.*)\s*$", re.I)

    for ln in lines:
        m = key_re.match(ln)
        if m:
            current_key = normalize_key(m.group(1))
            fields.setdefault(current_key, [])
            if m.group(2):
                fields[current_key].append(m.group(2).strip())
        else:
            if current_key is not None:
                # continuation line
                fields[current_key].append(ln.strip())

    return {k: "\n".join(v).strip() for k, v in fields.items()}

def find_line_of_key(block: str, key: str) -> Optional[int]:
    lines = block.splitlines()
    pat = re.compile(rf"^\s*{re.escape(key)}\s*:", flags=re.I)
    for i, ln in enumerate(lines, start=1):
        if pat.match(ln):
            return i
    return None

def lint_block(block_text: str, block_start_line: int, proposal_index: int) -> ProposalReport:
    extracted = parse_fields(block_text)
    findings: List[Finding] = []

    # 1) Required fields
    for rf in REQUIRED_FIELDS:
        k = normalize_key(rf)
        if k not in extracted or not extracted[k].strip():
            findings.append(
                Finding(
                    level="ERROR",
                    code="RND_MISSING_FIELD",
                    message=f"Missing required field: {rf}",
                    suggestion=f"Add a line: '{rf}: ...' (must be explicit).",
                    line=block_start_line,
                )
            )

    # 2) Spheres freeze
    spheres_raw = extracted.get("SPHERES", "")
    spheres = [s.strip() for s in re.split(r"[,\n]", spheres_raw) if s.strip()]
    if spheres:
        unknown = [s for s in spheres if s not in FROZEN_SPHERES]
        if unknown:
            findings.append(
                Finding(
                    level="ERROR",
                    code="RND_UNKNOWN_SPHERE",
                    message=f"Unknown or non-frozen sphere(s) detected: {unknown}. Only the 9 frozen spheres are allowed.",
                    suggestion=f"Use only: {sorted(FROZEN_SPHERES)}",
                    line=block_start_line + (find_line_of_key(block_text, "SPHERES") or 0) - 1,
                )
            )
        if len(set(spheres)) > 4:
            findings.append(
                Finding(
                    level="WARN",
                    code="RND_TOO_MANY_SPHERES",
                    message=f"Proposal references {len(set(spheres))} spheres. R&D guideline recommends max 3–4 spheres per need.",
                    suggestion="Split into smaller proposals or reduce coupling.",
                    line=block_start_line + (find_line_of_key(block_text, "SPHERES") or 0) - 1,
                )
            )

    # 3) Connection type validity (if present)
    conn_type = extracted.get("CONNECTION TYPE", "").strip()
    if conn_type:
        if conn_type not in ALLOWED_CONNECTION_TYPES:
            findings.append(
                Finding(
                    level="ERROR",
                    code="RND_BAD_CONNECTION_TYPE",
                    message=f"Invalid CONNECTION TYPE '{conn_type}'. Allowed: {sorted(ALLOWED_CONNECTION_TYPES)}",
                    suggestion="Classify as Projection, Request, Reference, or Delegation.",
                    line=block_start_line + (find_line_of_key(block_text, "CONNECTION TYPE") or 0) - 1,
                )
            )
    else:
        # If multiple spheres are mentioned, strongly encourage specifying connection type explicitly
        if len(set(spheres)) >= 2:
            findings.append(
                Finding(
                    level="WARN",
                    code="RND_MISSING_CONNECTION_TYPE",
                    message="Multiple spheres listed but CONNECTION TYPE is missing. Inter-sphere links must be classified.",
                    suggestion="Add: 'CONNECTION TYPE: Projection|Request|Reference|Delegation'.",
                    line=block_start_line,
                )
            )

    # 4) Human validation gating must be explicit
    hv = extracted.get("HUMAN VALIDATION", "")
    if hv:
        hv_low = hv.lower()
        if not any(h in hv_low for h in HUMAN_GATING_HINTS):
            findings.append(
                Finding(
                    level="ERROR",
                    code="RND_NO_EXPLICIT_HUMAN_GATE",
                    message="HUMAN VALIDATION does not clearly state explicit per-action approval (human gated).",
                    suggestion="Specify: 'explicit per-action approval', 'human click', 'review then approve', and where it is logged.",
                    line=block_start_line + (find_line_of_key(block_text, "HUMAN VALIDATION") or 0) - 1,
                )
            )

    # 5) Undo/reversibility must be explicit
    undo = extracted.get("UNDO/REVERSIBILITY", "")
    if undo and len(undo.strip()) < 8:
        findings.append(
            Finding(
                level="ERROR",
                code="RND_UNDO_TOO_VAGUE",
                message="UNDO/REVERSIBILITY is too vague. Must describe how rollback occurs (undo_patch/log).",
                suggestion="Describe undo mechanism (undo log, patch, version restore) and scope.",
                line=block_start_line + (find_line_of_key(block_text, "UNDO/REVERSIBILITY") or 0) - 1,
            )
        )

    # 6) Redundancy check must not be empty/vague
    red = extracted.get("REDUNDANCY CHECK", "")
    if red and len(red.strip()) < 8:
        findings.append(
            Finding(
                level="WARN",
                code="RND_REDUNDANCY_VAGUE",
                message="REDUNDANCY CHECK looks too short. Must reference existing modules/paths checked.",
                suggestion="State what you compared against (module names, endpoints, tables).",
                line=block_start_line + (find_line_of_key(block_text, "REDUNDANCY CHECK") or 0) - 1,
            )
        )

    # 7) Automation/drift pattern scan
    all_text = block_text.lower()
    for pat in FORBIDDEN_AUTOMATION_PATTERNS:
        if re.search(pat, all_text, flags=re.I):
            findings.append(
                Finding(
                    level="ERROR",
                    code="RND_FORBIDDEN_AUTOMATION",
                    message=f"Forbidden automation/drift indicator found: pattern '{pat}'. CHE·NU forbids silent/automatic execution.",
                    suggestion="Move execution to AUTONOMY zone (isolated), then require explicit human validation before apply.",
                    line=block_start_line,
                )
            )
            break

    # 8) My Team special ban (if sphere includes My Team)
    if "My Team" in spheres:
        for pat in MYTEAM_RISK_PATTERNS:
            if re.search(pat, all_text, flags=re.I):
                findings.append(
                    Finding(
                        level="ERROR",
                        code="RND_MYTEAM_AUTOMATION_RISK",
                        message=f"My Team automation risk detected: pattern '{pat}'. My Team must not automate anything.",
                        suggestion="Rewrite as explicit human delegation with a single owner and per-action approvals.",
                        line=block_start_line,
                    )
                )
                break

    # 9) Informational: if no errors, suggest OK
    if not any(f.level == "ERROR" for f in findings):
        findings.append(
            Finding(
                level="INFO",
                code="RND_OK",
                message="No blocking violations found. Proposal is admissible as an R&D hypothesis (not implementation).",
                suggestion="Proceed to human review and, if approved, implement via Human Validation Gate (quarantine → validate → apply).",
                line=block_start_line,
            )
        )

    return ProposalReport(proposal_index=proposal_index, findings=findings, extracted=extracted)

def summarize(reports: List[ProposalReport]) -> Tuple[int, int, int]:
    errors = sum(1 for r in reports for f in r.findings if f.level == "ERROR")
    warns = sum(1 for r in reports for f in r.findings if f.level == "WARN")
    infos = sum(1 for r in reports for f in r.findings if f.level == "INFO")
    return errors, warns, infos

def main() -> int:
    ap = argparse.ArgumentParser(description="CHE·NU R&D Linter")
    ap.add_argument("--in", dest="inp", required=True, help="Input proposal file (md/txt)")
    ap.add_argument("--json-out", dest="json_out", default=None, help="Write JSON report to this path")
    ap.add_argument("--fail-on-warn", action="store_true", help="Exit nonzero if WARN exists")
    args = ap.parse_args()

    p = Path(args.inp)
    if not p.exists():
        print(f"[ERROR] Input file not found: {p}", file=sys.stderr)
        return 2

    text = p.read_text(encoding="utf-8", errors="replace")
    blocks = split_into_proposals(text)

    reports: List[ProposalReport] = []
    for i, (start_ln, _end_ln, blk) in enumerate(blocks, start=1):
        reports.append(lint_block(blk, start_ln, i))

    errors, warns, infos = summarize(reports)

    # Human-readable output
    print(f"CHE·NU R&D Lint Report — proposals={len(reports)} errors={errors} warns={warns} infos={infos}\n")
    for rep in reports:
        print(f"--- Proposal #{rep.proposal_index} ---")
        # Show minimal extracted header
        ut = rep.extracted.get("USER TYPE", "").strip()[:80]
        scope = rep.extracted.get("SPHERES", "").strip().replace("\n", "; ")[:80]
        if ut:
            print(f"USER TYPE: {ut}")
        if scope:
            print(f"SPHERES: {scope}")
        for f in rep.findings:
            loc = f" (line {f.line})" if f.line else ""
            print(f"{f.level}: {f.code}{loc} — {f.message}")
            if f.suggestion:
                print(f"  ↳ fix: {f.suggestion}")
        print()

    # JSON output
    if args.json_out:
        out = {
            "summary": {"proposals": len(reports), "errors": errors, "warns": warns, "infos": infos},
            "reports": [
                {
                    "proposal_index": r.proposal_index,
                    "findings": [asdict(f) for f in r.findings],
                    "extracted": r.extracted,
                }
                for r in reports
            ],
        }
        Path(args.json_out).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote JSON report: {args.json_out}")

    # Exit codes
    if errors > 0:
        return 1
    if args.fail_on_warn and warns > 0:
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
