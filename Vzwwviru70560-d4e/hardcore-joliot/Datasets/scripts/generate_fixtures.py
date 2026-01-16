#!/usr/bin/env python3
"""
CHE·NU Demo System V51 - Fixture Generator
Generates large-scale test fixtures for the demo system.
"""

import json
import os
import random
import uuid
from datetime import datetime, timedelta
import hashlib

BASE_DIR = "/home/claude/CHENU_DEMO_SYSTEM_V51"

def generate_memory_units():
    units = []
    
    unit_defs = [
        ("MU_001", "core", "system", "Identité CHE·NU"),
        ("MU_002", "core", "governance", "Tree Laws"),
        ("MU_003", "contract", "governance", "Contrat Proposition"),
        ("MU_004", "system", "governance", "Système Audit"),
        ("MU_005", "module", "system", "Salle Réflexion"),
        ("MU_006", "module", "system", "Mode Incident"),
        ("MU_007", "module", "system", "Inspecteur Mémoire"),
        ("MU_008", "module", "system", "Demo Replay"),
        ("MU_009", "module", "system", "Mode Présentateur"),
        ("MU_010", "system", "agents", "Hiérarchie Agents"),
        ("MU_011", "system", "agents", "Routage Multi-LLM"),
        ("MU_012", "config", "agents", "Config Agents"),
        ("MU_013", "agent", "agents", "Agent Planning L1"),
        ("MU_014", "agent", "agents", "Agent Estimation L1"),
        ("MU_015", "agent", "agents", "Agent Conformité L1"),
        ("MU_016", "agent", "agents", "Agent Qualité L1"),
        ("MU_017", "agent", "agents", "Agent Sécurité L1"),
        ("MU_018", "agent", "agents", "Agent Documents L1"),
        ("MU_019", "agent", "agents", "Agent Communication L1"),
        ("MU_020", "agent", "agents", "Agent Créatif L1"),
        ("MU_021", "agent", "agents", "Agent Scheduling L2"),
        ("MU_022", "agent", "agents", "Agent RBQ L2"),
        ("MU_023", "agent", "agents", "Calc Béton L3"),
        ("MU_024", "agent", "agents", "Calc Acier L3"),
        ("MU_025", "agent", "agents", "Calc Bois L3"),
        ("MU_026", "agent", "agents", "Calc Électrique L3"),
        ("MU_027", "agent", "agents", "Calc Plomberie L3"),
        ("MU_028", "agent", "agents", "Calc CVAC L3"),
        ("MU_029", "agent", "agents", "Calc Isolation L3"),
        ("MU_030", "project", "projects", "Projet Alpha"),
        ("MU_031", "project", "projects", "Projet Beta"),
        ("MU_032", "project", "projects", "Projet Gamma"),
        ("MU_033", "project", "projects", "Projet Delta"),
        ("MU_034", "project", "projects", "Projet Epsilon"),
        ("MU_035", "project", "projects", "Projet Zeta"),
        ("MU_036", "project", "projects", "Projet Eta"),
        ("MU_037", "project", "projects", "Projet Theta"),
        ("MU_038", "project", "projects", "Projet Iota"),
        ("MU_039", "project", "projects", "Projet Kappa"),
        ("MU_040", "knowledge", "compliance", "Règlement RBQ"),
        ("MU_041", "knowledge", "compliance", "Règlement CNESST"),
        ("MU_042", "knowledge", "compliance", "Règlement CCQ"),
        ("MU_043", "knowledge", "compliance", "Code Construction"),
        ("MU_044", "knowledge", "compliance", "Code Énergie"),
        ("MU_045", "knowledge", "compliance", "Accessibilité"),
        ("MU_046", "knowledge", "compliance", "Code Incendie"),
        ("MU_047", "knowledge", "compliance", "Environnement"),
        ("MU_048", "knowledge", "compliance", "Permis"),
        ("MU_049", "knowledge", "compliance", "Garanties"),
        ("MU_050", "knowledge", "knowledge", "Base Béton"),
        ("MU_051", "knowledge", "knowledge", "Base Bois"),
        ("MU_052", "knowledge", "knowledge", "Base Acier"),
        ("MU_053", "knowledge", "knowledge", "Base Électrique"),
        ("MU_054", "knowledge", "knowledge", "Base Plomberie"),
        ("MU_055", "knowledge", "knowledge", "Base CVAC"),
        ("MU_056", "knowledge", "knowledge", "Base Isolation"),
        ("MU_057", "knowledge", "knowledge", "Base Toiture"),
        ("MU_058", "knowledge", "knowledge", "Base Fenestration"),
        ("MU_059", "knowledge", "knowledge", "Base Finition"),
        ("MU_060", "system", "system", "Life Loop 1"),
        ("MU_061", "system", "system", "Life Loop 2"),
        ("MU_062", "system", "system", "Life Loop 3"),
        ("MU_063", "system", "system", "Life Loop 4"),
        ("MU_064", "vendor", "projects", "Fournisseur Béton"),
        ("MU_065", "vendor", "projects", "Fournisseur Bois"),
        ("MU_066", "vendor", "projects", "Sous-traitant Élec"),
        ("MU_067", "vendor", "projects", "Sous-traitant Plomb"),
        ("MU_068", "vendor", "projects", "Sous-traitant CVAC"),
        ("MU_069", "demo", "system", "Flow Court 90s"),
        ("MU_070", "demo", "system", "Flow Live 15min"),
        ("MU_071", "config", "system", "Config Export"),
        ("MU_072", "config", "system", "Config Signing"),
        ("MU_073", "config", "system", "Config Themes"),
        ("MU_074", "knowledge", "compliance", "Novoclimat 2.0"),
        ("MU_075", "knowledge", "compliance", "LEED Standards"),
    ]
    
    for uid, utype, sphere, title in unit_defs:
        base = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 300))
        units.append({
            "unit_id": uid,
            "type": utype,
            "sphere": sphere,
            "created_at": base.isoformat() + "Z",
            "updated_at": (base + timedelta(days=random.randint(0, 60))).isoformat() + "Z",
            "version": random.randint(1, 10),
            "status": "active",
            "content": {
                "title": title,
                "summary": f"Description détaillée de {title} pour CHE·NU V51",
                "details": {"key": "value", "data": [1, 2, 3]},
                "extended": " ".join(["Lorem ipsum dolor sit amet."] * 50)
            },
            "relations": [{"target": f"MU_{random.randint(1,75):03d}", "type": "relates", "strength": 0.8}],
            "tags": [utype, sphere, "chenu", "v51"],
            "confidence": round(random.uniform(0.85, 1.0), 2),
            "governance": {"approved_by": "system", "approved_at": base.isoformat() + "Z"}
        })
    return units

def generate_decisions():
    decisions = []
    templates = [
        ("DEC_001", "approved", "Approbation Projet Alpha"),
        ("DEC_002", "approved", "Ajout Agent Créatif"),
        ("DEC_003", "rejected", "Modification Tree Law"),
        ("DEC_004", "approved", "Intégration Gemini"),
        ("DEC_005", "approved", "Mise à jour RBQ"),
        ("DEC_006", "pending", "Nouveau Projet Omega"),
        ("DEC_007", "approved", "Export PDF signé"),
        ("DEC_008", "approved", "Mode Incident v2"),
        ("DEC_009", "rejected", "Auto-compaction"),
        ("DEC_010", "approved", "Calculateur CVAC"),
        ("DEC_011", "approved", "Flow Demo 90s"),
        ("DEC_012", "approved", "Sphere Knowledge"),
        ("DEC_013", "pending", "Intégration Ollama"),
        ("DEC_014", "approved", "Novoclimat 2.0"),
        ("DEC_015", "approved", "Replay Forensique"),
    ]
    for dec_id, status, title in templates:
        base = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 350))
        decisions.append({
            "decision_id": dec_id, "status": status, "title": title,
            "created_at": base.isoformat() + "Z",
            "decided_by": "human_operator" if status != "pending" else None,
            "tree_laws_check": {"TL_001": "passed", "TL_002": "passed", "TL_003": "passed"}
        })
    return decisions

def generate_sessions():
    sessions = []
    for i in range(1, 13):
        base = datetime(2025, 1, 1) + timedelta(days=i * 25)
        dur = random.randint(300, 3600)
        sessions.append({
            "session_id": f"SES_{base.strftime('%Y%m%d')}_{i:03d}",
            "started_at": base.isoformat() + "Z",
            "ended_at": (base + timedelta(seconds=dur)).isoformat() + "Z",
            "duration_seconds": dur,
            "user": {"role": random.choice(["investor", "presenter", "developer"]), "name": f"User {i}"},
            "modules_visited": random.sample(["reflection_room", "memory_inspector", "incident_mode"], 2),
            "events_generated": random.randint(50, 500)
        })
    return sessions

def generate_archives():
    archives = []
    templates = [
        ("ARCH_001", "proposal", "Proposition expirée"),
        ("ARCH_002", "proposal", "Proposition rejetée"),
        ("ARCH_003", "session", "Session démo"),
        ("ARCH_004", "export", "Export narratif"),
        ("ARCH_005", "proposal", "Proposition expirée 2"),
        ("ARCH_006", "session", "Session investisseur"),
        ("ARCH_007", "decision", "Décision obsolète"),
        ("ARCH_008", "export", "Rapport incident"),
    ]
    for arch_id, atype, title in templates:
        base = datetime(2024, 9, 1) + timedelta(days=random.randint(0, 120))
        archives.append({
            "archive_id": arch_id, "type": atype, "title": title,
            "archived_at": base.isoformat() + "Z", "reason": "expired"
        })
    return archives

def generate_events(count=2000):
    events = []
    types = [
        ("module_activated", "module"), ("module_closed", "module"),
        ("proposal_created", "proposal"), ("proposal_approved", "proposal"),
        ("memory_read", "memory"), ("navigation", "navigation"),
        ("demo_step_entered", "demo"), ("export_generated", "export")
    ]
    base = datetime(2025, 12, 30, 9, 0, 0)
    for i in range(count):
        etype, cat = random.choice(types)
        events.append({
            "event_id": f"EVT_{uuid.uuid4().hex[:12].upper()}",
            "event_type": etype, "category": cat,
            "timestamp": (base + timedelta(seconds=i * 2)).isoformat() + "Z",
            "actor": random.choice(["user", "system"]),
            "severity": random.choice(["info", "info", "warning", "debug"]),
            "payload": {"index": i, "data": "x" * 200}
        })
    return events

def main():
    print("Generating fixtures...")
    
    units = generate_memory_units()
    with open(f"{BASE_DIR}/data/datasets/memory_units.json", "w") as f:
        json.dump({"memory_units": units, "count": len(units)}, f, indent=2)
    print(f"  {len(units)} memory units")
    
    decisions = generate_decisions()
    with open(f"{BASE_DIR}/data/datasets/decisions.json", "w") as f:
        json.dump({"decisions": decisions, "count": len(decisions)}, f, indent=2)
    print(f"  {len(decisions)} decisions")
    
    sessions = generate_sessions()
    with open(f"{BASE_DIR}/data/datasets/sessions.json", "w") as f:
        json.dump({"sessions": sessions, "count": len(sessions)}, f, indent=2)
    print(f"  {len(sessions)} sessions")
    
    archives = generate_archives()
    with open(f"{BASE_DIR}/data/datasets/archives.json", "w") as f:
        json.dump({"archives": archives, "count": len(archives)}, f, indent=2)
    print(f"  {len(archives)} archives")
    
    events = generate_events(2000)
    with open(f"{BASE_DIR}/data/fixtures/events_large.json", "w") as f:
        json.dump({"events": events, "count": len(events)}, f, indent=2)
    print(f"  {len(events)} events")
    
    print("Done!")

if __name__ == "__main__":
    main()
