#!/usr/bin/env python3
"""
CHE·NU — R&D LINT CANONIQUE (ALL-IN-ONE)
Version: 1.0
Modes:
  - chenu_rnd              → vérifie conformité R&D + freeze
  - compare_repo           → détecte doublons avec repo existant
  - chenu_rnd + compare    → MODE OFFICIEL COMPLET (recommandé)

PHILOSOPHY:
- Humans define needs
- R&D validates hypotheses
- Architecture is frozen
- Automation is isolated
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Set

# ─────────────────────────────────────────────
# CONFIG CANONIQUE (INTÉGRÉE)
# ─────────────────────────────────────────────

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
    "HUMAN VALIDATION",
    "UNDO/REVERSIBILITY",
    "REDUNDANCY CHECK",
]

FORBIDDEN_AUTOMATION_PATTERNS = [
    r"\bauto\b",
    r"\bautomatic\b",
    r"\bsilent\b",
    r"\bwithout approval\b",
    r"\bself[- ]?execute\b",
    r"\boptimi[sz]e engagement\b",
]

MYTEAM_BANNED = [
    r"\bassign automatically\b",
    r"\bgroup decision\b",
    r"\bteam decides\b",
    r"\bschedule automatically\b",
]

REPO_SCAN_EXT = {".py", ".ts", ".js", ".sql", ".md"}

# ─────────────────────────────────────────────
# DATA STRUCTURES
# ─────────────────────────────────────────────

@dataclass
class Finding:
    level: str
    code: str
    message: str
    hint: str = ""

@dataclass
class Report:
    proposal_id: int
    findings: List[Finding]
    extracted: Dict[str, str]

# ─────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────

def parse_proposals(text: str) -> List[str]:
    blocks = re.split(r"\n(?=USER TYPE\s*:)", text, flags=re.I)
    return [b.strip() for b in blocks if b.strip()]

def extract_fields(block: str) -> Dict[str, str]:
    data = {}
    current = None
    for line in block.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            key = k.strip().upper()
            if key in REQUIRED_FIELDS or key in ["SPHERES", "CONNECTION TYPE"]:
                current = key
                data[current] = v.strip()
        elif current:
            data[current] += " " + line.strip()
    return data

def scan_repo(repo_path: Path) -> Set[str]:
    """Scan existing repo for token overlap detection"""
    tokens = set()
    for root, _, files in os.walk(repo_path):
        for f in files:
            if Path(f).suffix in REPO_SCAN_EXT:
                try:
                    txt = Path(root, f).read_text(errors="ignore")
                    for w in re.findall(r"[A-Za-z_]{5,}", txt):
                        tokens.add(w.lower())
                except:
                    pass
    return tokens

# ─────────────────────────────────────────────
# LINT CORE
# ─────────────────────────────────────────────

def lint(block: str, repo_tokens: Set[str] | None, idx: int) -> Report:
    findings = []
    data = extract_fields(block)

    # 1) Required fields
    for f in REQUIRED_FIELDS:
        if f not in data or not data[f].strip():
            findings.append(Finding(
                "ERROR", "MISSING_FIELD",
                f"Missing required field: {f}",
                "Add explicit content"
            ))

    # 2) Sphere freeze
    spheres = [s.strip() for s in data.get("SPHERES", "").split(",") if s.strip()]
    for s in spheres:
        if s not in FROZEN_SPHERES:
            findings.append(Finding(
                "ERROR", "INVALID_SPHERE",
                f"Sphere '{s}' is not frozen/allowed",
                "Use official 9 spheres only"
            ))

    # 3) Too many spheres
    if len(spheres) > 4:
        findings.append(Finding(
            "WARN", "TOO_MANY_SPHERES",
            f"Proposal references {len(spheres)} spheres (max 3-4 recommended)",
            "Split into smaller proposals"
        ))

    # 4) Connection type
    if len(spheres) > 1:
        ct = data.get("CONNECTION TYPE", "")
        if ct not in ALLOWED_CONNECTION_TYPES:
            findings.append(Finding(
                "ERROR", "BAD_CONNECTION",
                "Invalid or missing CONNECTION TYPE",
                "Must be Projection / Request / Reference / Delegation"
            ))

    # 5) Automation patterns
    txt = block.lower()
    for p in FORBIDDEN_AUTOMATION_PATTERNS:
        if re.search(p, txt):
            findings.append(Finding(
                "ERROR", "AUTOMATION_DETECTED",
                f"Forbidden automation pattern detected ({p})",
                "Move to autonomy zone + human validation"
            ))
            break

    # 6) My Team hard ban
    if "My Team" in spheres:
        for p in MYTEAM_BANNED:
            if re.search(p, txt):
                findings.append(Finding(
                    "ERROR", "MYTEAM_AUTOMATION",
                    "My Team automation detected",
                    "Rewrite as explicit human delegation"
                ))
                break

    # 7) Human validation must be explicit
    hv = data.get("HUMAN VALIDATION", "").lower()
    if hv and not any(kw in hv for kw in ["explicit", "approve", "click", "review", "confirm"]):
        findings.append(Finding(
            "ERROR", "VAGUE_VALIDATION",
            "HUMAN VALIDATION does not clearly state explicit approval",
            "Add: 'explicit per-action approval', 'user clicks', etc."
        ))

    # 8) Undo must be substantial
    undo = data.get("UNDO/REVERSIBILITY", "")
    if undo and len(undo.strip()) < 10:
        findings.append(Finding(
            "ERROR", "VAGUE_UNDO",
            "UNDO/REVERSIBILITY too vague (must describe mechanism)",
            "Specify: undo_patch, rollback method, audit log"
        ))

    # 9) Repo duplication check
    if repo_tokens:
        need = data.get("NEED", "").lower()
        collisions = [w for w in need.split() if w in repo_tokens and len(w) > 4]
        if len(collisions) > 3:
            findings.append(Finding(
                "WARN", "POSSIBLE_DUPLICATE",
                f"Need overlaps with existing repo concepts: {set(collisions)}",
                "Verify redundancy manually against existing modules"
            ))

    # 10) Success if no errors
    if not any(f.level == "ERROR" for f in findings):
        findings.append(Finding(
            "INFO", "RND_OK",
            "Proposal valid as R&D hypothesis",
            "Proceed to human review and implement via canonical validation gate"
        ))

    return Report(idx, findings, data)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="CHE·NU R&D Lint (All-In-One)",
        epilog="Modes: chenu_rnd | compare_repo | both (recommended)"
    )
    ap.add_argument("--in", dest="input", required=True, help="R&D proposal file (.md)")
    ap.add_argument("--repo", help="Existing repo path for duplication check")
    ap.add_argument("--json", help="Write JSON report to file")
    ap.add_argument("--fail-on-warn", action="store_true", help="Exit 1 if warnings exist")
    args = ap.parse_args()

    # Read proposal
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] File not found: {args.input}", file=sys.stderr)
        return 2

    text = input_path.read_text(errors="ignore")
    proposals = parse_proposals(text)

    # Scan repo if provided
    repo_tokens = None
    if args.repo:
        repo_path = Path(args.repo)
        if not repo_path.exists():
            print(f"[WARN] Repo path not found: {args.repo}", file=sys.stderr)
        else:
            print(f"[INFO] Scanning repo for token overlap: {args.repo}")
            repo_tokens = scan_repo(repo_path)
            print(f"[INFO] Found {len(repo_tokens)} unique tokens in repo")

    # Lint all proposals
    reports = []
    errors = 0
    warnings = 0

    for i, p in enumerate(proposals, 1):
        r = lint(p, repo_tokens, i)
        reports.append(r)
        errors += sum(1 for f in r.findings if f.level == "ERROR")
        warnings += sum(1 for f in r.findings if f.level == "WARN")

    # Human-readable output
    print(f"\n{'='*70}")
    print(f"CHE·NU R&D LINT REPORT")
    print(f"{'='*70}")
    print(f"Proposals: {len(proposals)}")
    print(f"Errors:    {errors}")
    print(f"Warnings:  {warnings}")
    print(f"{'='*70}\n")

    for r in reports:
        user_type = r.extracted.get("USER TYPE", "Unknown")[:50]
        spheres = r.extracted.get("SPHERES", "")[:60]
        
        print(f"--- PROPOSAL #{r.proposal_id} ---")
        print(f"USER TYPE: {user_type}")
        if spheres:
            print(f"SPHERES: {spheres}")
        
        for f in r.findings:
            symbol = "❌" if f.level == "ERROR" else "⚠️" if f.level == "WARN" else "✅"
            print(f"{symbol} [{f.level}] {f.code}: {f.message}")
            if f.hint:
                print(f"    → {f.hint}")
        print()

    # JSON output
    if args.json:
        output = {
            "summary": {
                "proposals": len(proposals),
                "errors": errors,
                "warnings": warnings
            },
            "reports": [asdict(r) for r in reports]
        }
        Path(args.json).write_text(
            json.dumps(output, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"[INFO] JSON report written to: {args.json}\n")

    # Exit codes
    if errors > 0:
        return 1
    if args.fail_on_warn and warnings > 0:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
