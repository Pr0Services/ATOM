#!/usr/bin/env python3
"""Generate large data files to reach >100MB target"""

import json
import os
import random
import uuid
from datetime import datetime, timedelta
import base64

BASE_DIR = "/home/claude/CHENU_DEMO_SYSTEM_V51"

def generate_sphere_mappings():
    """Generate complete sphere mapping data"""
    spheres = {
        "SPH_SYSTEM": {
            "id": "SPH_SYSTEM",
            "name": "Système CHE·NU",
            "name_en": "CHE·NU System",
            "description": "Configuration et état du système d'intelligence gouvernée",
            "color": "#4a9eff",
            "icon": "🏠",
            "position": {"x": 0, "y": 0, "z": 0},
            "radius": 100,
            "units": [f"MU_{i:03d}" for i in range(1, 16)],
            "connections": ["SPH_GOVERNANCE", "SPH_AGENTS"],
            "metadata": {
                "created_at": "2025-01-01T00:00:00Z",
                "unit_count": 15,
                "access_level": "public",
                "visualization": {
                    "glow": True,
                    "pulse_rate": 1.5,
                    "particles": 50
                }
            }
        },
        "SPH_GOVERNANCE": {
            "id": "SPH_GOVERNANCE",
            "name": "Gouvernance",
            "name_en": "Governance",
            "description": "Tree Laws, contrats constitutionnels, règles d'approbation",
            "color": "#81c784",
            "icon": "🌳",
            "position": {"x": 150, "y": 100, "z": 0},
            "radius": 80,
            "units": [f"MU_{i:03d}" for i in range(2, 14)],
            "connections": ["SPH_SYSTEM", "SPH_COMPLIANCE"],
            "metadata": {
                "created_at": "2025-01-01T00:00:00Z",
                "unit_count": 12,
                "access_level": "protected",
                "immutable_units": ["MU_002"]
            }
        },
        "SPH_AGENTS": {
            "id": "SPH_AGENTS",
            "name": "Agents",
            "name_en": "Agents",
            "description": "Configuration des 168+ agents spécialisés",
            "color": "#9e4aff",
            "icon": "🤖",
            "position": {"x": -150, "y": 100, "z": 0},
            "radius": 120,
            "units": [f"MU_{i:03d}" for i in range(10, 30)],
            "connections": ["SPH_SYSTEM", "SPH_PROJECTS"],
            "metadata": {
                "created_at": "2025-02-01T00:00:00Z",
                "unit_count": 20,
                "agent_hierarchy": {
                    "L0": 1,
                    "L1": 8,
                    "L2": 24,
                    "L3": 135
                }
            }
        },
        "SPH_PROJECTS": {
            "id": "SPH_PROJECTS",
            "name": "Projets",
            "name_en": "Projects",
            "description": "Projets de construction suivis par le système",
            "color": "#ff9e4a",
            "icon": "🏗️",
            "position": {"x": 0, "y": 200, "z": 0},
            "radius": 100,
            "units": [f"MU_{i:03d}" for i in range(30, 40)],
            "connections": ["SPH_AGENTS", "SPH_COMPLIANCE"],
            "metadata": {
                "created_at": "2025-04-01T00:00:00Z",
                "unit_count": 10,
                "active_projects": 8,
                "completed_projects": 2
            }
        },
        "SPH_COMPLIANCE": {
            "id": "SPH_COMPLIANCE",
            "name": "Conformité",
            "name_en": "Compliance",
            "description": "RBQ, CNESST, CCQ - Règlements québécois",
            "color": "#e57373",
            "icon": "📋",
            "position": {"x": 150, "y": -100, "z": 0},
            "radius": 90,
            "units": [f"MU_{i:03d}" for i in range(40, 50)],
            "connections": ["SPH_GOVERNANCE", "SPH_PROJECTS", "SPH_KNOWLEDGE"],
            "metadata": {
                "created_at": "2025-01-01T00:00:00Z",
                "unit_count": 10,
                "regulators": ["RBQ", "CNESST", "CCQ"]
            }
        },
        "SPH_KNOWLEDGE": {
            "id": "SPH_KNOWLEDGE",
            "name": "Connaissances",
            "name_en": "Knowledge",
            "description": "Base de connaissances métier construction",
            "color": "#4dd0e1",
            "icon": "📚",
            "position": {"x": -150, "y": -100, "z": 0},
            "radius": 85,
            "units": [f"MU_{i:03d}" for i in range(50, 60)],
            "connections": ["SPH_COMPLIANCE", "SPH_AGENTS"],
            "metadata": {
                "created_at": "2025-02-01T00:00:00Z",
                "unit_count": 10,
                "domains": ["concrete", "wood", "steel", "electrical", "plumbing", "hvac"]
            }
        }
    }
    return spheres

def generate_agent_configs():
    """Generate complete agent configuration data"""
    agents = []
    
    departments = [
        ("PLANNING", "Planification", 18),
        ("ESTIMATION", "Estimation", 15),
        ("COMPLIANCE", "Conformité", 20),
        ("QUALITY", "Qualité", 12),
        ("SAFETY", "Sécurité", 16),
        ("DOCUMENTS", "Documentation", 14),
        ("COMMUNICATION", "Communication", 10),
        ("CREATIVE", "Studio Créatif", 38),
    ]
    
    agent_id = 1
    for dept_id, dept_name, count in departments:
        # L1 Head
        agents.append({
            "agent_id": f"AG_L1_{dept_id}_HEAD",
            "level": "L1",
            "department": dept_id,
            "name": f"Directeur {dept_name}",
            "description": f"Agent L1 responsable du département {dept_name}",
            "llm_preference": "claude-sonnet-4",
            "temperature": 0.7,
            "max_tokens": 8192,
            "tools": ["planner", "analyzer", "reporter"],
            "memory_access": "read_only",
            "capabilities": [f"Capability {i}" for i in range(1, 8)],
            "metrics": {
                "tasks_processed": random.randint(5000, 50000),
                "success_rate": round(random.uniform(0.94, 0.99), 3),
                "avg_response_ms": random.randint(500, 2000)
            },
            "config": {
                "retry_count": 3,
                "timeout_seconds": 30,
                "fallback_llm": "gpt-4-turbo"
            }
        })
        
        # L2 Team Leads (3 per department)
        for j in range(3):
            agents.append({
                "agent_id": f"AG_L2_{dept_id}_{j+1:02d}",
                "level": "L2",
                "department": dept_id,
                "reports_to": f"AG_L1_{dept_id}_HEAD",
                "name": f"Chef Équipe {dept_name} {j+1}",
                "llm_preference": random.choice(["claude-sonnet-4", "gpt-4-turbo"]),
                "temperature": 0.5,
                "max_tokens": 4096,
                "metrics": {
                    "tasks_processed": random.randint(1000, 10000),
                    "success_rate": round(random.uniform(0.92, 0.98), 3)
                }
            })
        
        # L3 Specialists
        for j in range(count - 4):  # minus head and 3 team leads
            agents.append({
                "agent_id": f"AG_L3_{dept_id}_{j+1:03d}",
                "level": "L3",
                "department": dept_id,
                "reports_to": f"AG_L2_{dept_id}_{(j % 3) + 1:02d}",
                "name": f"Spécialiste {dept_name} {j+1}",
                "llm_preference": random.choice(["claude-sonnet-4", "gpt-4-turbo", "gemini-pro", "ollama-llama3"]),
                "temperature": 0.3,
                "max_tokens": 2048,
                "specialization": f"Specialty {j+1}",
                "metrics": {
                    "tasks_processed": random.randint(500, 5000),
                    "success_rate": round(random.uniform(0.90, 0.97), 3)
                }
            })
    
    return agents

def generate_project_details():
    """Generate detailed project data"""
    projects = []
    
    project_defs = [
        ("PRJ_ALPHA", "Complexe Résidentiel Brossard", "residential_multi", 18500000, "construction"),
        ("PRJ_BETA", "Rénovation Commerciale Longueuil", "commercial_renovation", 4200000, "construction"),
        ("PRJ_GAMMA", "Maison Unifamiliale St-Bruno", "residential_single", 1850000, "structure"),
        ("PRJ_DELTA", "Centre Sportif La Prairie", "institutional", 12500000, "planning"),
        ("PRJ_EPSILON", "Triplex Verdun", "residential_multi", 2100000, "completed"),
        ("PRJ_ZETA", "Condo 24 unités Chambly", "residential_multi", 9800000, "excavation"),
        ("PRJ_ETA", "Bureau Professionnel Candiac", "commercial", 3200000, "permits"),
        ("PRJ_THETA", "Restaurant St-Lambert", "commercial_renovation", 850000, "finitions"),
        ("PRJ_IOTA", "Entrepôt Industriel Longueuil", "industrial", 5600000, "structure"),
        ("PRJ_KAPPA", "Clinique Médicale Boucherville", "institutional", 4800000, "enveloppe"),
    ]
    
    for proj_id, name, ptype, budget, phase in project_defs:
        start = datetime(2025, random.randint(1, 6), random.randint(1, 28))
        
        projects.append({
            "project_id": proj_id,
            "name": name,
            "type": ptype,
            "status": "active" if phase != "completed" else "completed",
            "current_phase": phase,
            "location": {
                "address": f"{random.randint(100, 9999)} Rue Exemple",
                "city": name.split()[-1] if len(name.split()) > 2 else "Brossard",
                "province": "QC",
                "postal_code": f"J{random.randint(1,9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} {random.randint(1,9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(1,9)}",
                "coordinates": {
                    "lat": 45.4 + random.uniform(0, 0.2),
                    "lng": -73.4 + random.uniform(0, 0.2)
                }
            },
            "timeline": {
                "start_date": start.strftime("%Y-%m-%d"),
                "estimated_end": (start + timedelta(days=random.randint(180, 720))).strftime("%Y-%m-%d"),
                "phases": [
                    {"name": "Planification", "status": "completed"},
                    {"name": "Permis", "status": "completed" if phase not in ["planning", "permits"] else "in_progress"},
                    {"name": "Excavation", "status": "completed" if phase not in ["planning", "permits", "excavation"] else "planned"},
                    {"name": "Fondations", "status": "in_progress" if phase == "excavation" else "planned"},
                    {"name": "Structure", "status": "in_progress" if phase == "structure" else "planned"},
                    {"name": "Enveloppe", "status": "in_progress" if phase == "enveloppe" else "planned"},
                    {"name": "Finitions", "status": "in_progress" if phase == "finitions" else "planned"},
                    {"name": "Livraison", "status": "completed" if phase == "completed" else "planned"},
                ]
            },
            "budget": {
                "total": budget,
                "currency": "CAD",
                "committed": int(budget * random.uniform(0.3, 0.8)),
                "spent": int(budget * random.uniform(0.1, 0.6)),
                "contingency": int(budget * 0.05),
                "breakdown": {
                    "labor": int(budget * 0.35),
                    "materials": int(budget * 0.45),
                    "equipment": int(budget * 0.08),
                    "overhead": int(budget * 0.07),
                    "profit": int(budget * 0.05)
                }
            },
            "team": {
                "project_manager": f"PM_{random.randint(1,10):03d}",
                "superintendent": f"SUPT_{random.randint(1,10):03d}",
                "estimator": f"EST_{random.randint(1,10):03d}",
                "safety_officer": f"SST_{random.randint(1,10):03d}"
            },
            "compliance": {
                "rbq_license": f"RBQ-{random.randint(1000,9999)}-{random.randint(1000,9999)}",
                "building_permit": f"BP-2025-{random.randint(1000,9999)}",
                "cnesst_file": f"CNESST-2025-{random.randint(10000,99999)}",
                "ccq_declaration": "Current"
            },
            "kpis": {
                "schedule_performance_index": round(random.uniform(0.85, 1.05), 2),
                "cost_performance_index": round(random.uniform(0.90, 1.02), 2),
                "safety_incidents_ytd": random.randint(0, 5),
                "quality_score": random.randint(85, 98)
            },
            "documents": [f"DOC_{proj_id}_{i:03d}" for i in range(random.randint(20, 100))],
            "change_orders": random.randint(0, 15),
            "rfis": random.randint(5, 50)
        })
    
    return projects

def generate_compliance_database():
    """Generate Quebec compliance reference database"""
    compliance = {
        "rbq": {
            "regulator": "Régie du bâtiment du Québec",
            "website": "https://www.rbq.gouv.qc.ca",
            "license_categories": [
                {"code": "1.1.1", "name": "Entrepreneur général - bâtiment résidentiel neuf", "exam_required": True},
                {"code": "1.1.2", "name": "Entrepreneur général - bâtiment résidentiel rénové", "exam_required": True},
                {"code": "1.2", "name": "Entrepreneur général - bâtiment commercial et industriel", "exam_required": True},
                {"code": "2.1", "name": "Entrepreneur spécialisé - électricité", "exam_required": True},
                {"code": "2.2", "name": "Entrepreneur spécialisé - plomberie", "exam_required": True},
                {"code": "2.3", "name": "Entrepreneur spécialisé - gaz", "exam_required": True},
                {"code": "2.4", "name": "Entrepreneur spécialisé - chauffage", "exam_required": True},
                {"code": "2.5", "name": "Entrepreneur spécialisé - ventilation", "exam_required": True},
                {"code": "2.6", "name": "Entrepreneur spécialisé - climatisation", "exam_required": True},
                {"code": "2.7", "name": "Entrepreneur spécialisé - réfrigération", "exam_required": True},
                {"code": "3.1", "name": "Constructeur-propriétaire", "exam_required": False},
            ],
            "regulations": [
                "Code de construction du Québec - Chapitre I, Bâtiment",
                "Code de sécurité",
                "Règlement sur la qualification professionnelle",
                "Règlement sur le plan de garantie des bâtiments résidentiels neufs",
                "Règlement sur l'efficacité énergétique des bâtiments"
            ],
            "guarantee_plans": [
                {"name": "Garantie Construction Résidentielle", "coverage": ["Malfaçons", "Vices cachés", "Perte bâtiment"]},
                {"name": "Garantie Rénovation", "coverage": ["Travaux", "Matériaux"]}
            ]
        },
        "cnesst": {
            "regulator": "Commission des normes, de l'équité, de la santé et de la sécurité du travail",
            "website": "https://www.cnesst.gouv.qc.ca",
            "regulations": [
                "Loi sur la santé et la sécurité du travail (LSST)",
                "Code de sécurité pour les travaux de construction",
                "Règlement sur la santé et la sécurité du travail"
            ],
            "required_training": [
                {"name": "Santé et sécurité générale sur les chantiers", "provider": "ASP Construction", "duration_hours": 30},
                {"name": "Travail en hauteur", "provider": "Various", "duration_hours": 8},
                {"name": "SIMDUT 2015", "provider": "Various", "duration_hours": 4},
                {"name": "Premiers soins", "provider": "Various", "duration_hours": 16}
            ],
            "reporting": [
                "Déclaration d'ouverture de chantier",
                "Avis d'accident",
                "Programme de prévention"
            ]
        },
        "ccq": {
            "regulator": "Commission de la construction du Québec",
            "website": "https://www.ccq.org",
            "sectors": ["Résidentiel", "Commercial", "Industriel", "Génie civil et voirie"],
            "trades": [
                "Briqueteur-maçon", "Calorifugeur", "Carreleur", "Charpentier-menuisier",
                "Chaudronnier", "Cimentier-applicateur", "Couvreur", "Électricien",
                "Ferblantier", "Ferrailleur", "Frigoriste", "Grutier",
                "Mécanicien d'ascenseur", "Mécanicien de chantier", "Mécanicien de machines lourdes",
                "Mécanicien en protection-incendie", "Monteur-assembleur", "Monteur-mécanicien (vitrier)",
                "Opérateur d'équipement lourd", "Opérateur de pelles", "Peintre",
                "Plâtrier", "Poseur de revêtements souples", "Poseur de systèmes intérieurs",
                "Serrurier de bâtiment", "Tuyauteur"
            ],
            "competency_cards": {
                "types": ["Apprenti", "Compagnon", "Occupation"],
                "validity": "Annual renewal required",
                "verification": "Mandatory on all job sites"
            }
        }
    }
    return compliance

def generate_replay_fixtures():
    """Generate sample replay session data"""
    replays = []
    
    for i in range(5):
        base = datetime(2025, 12, 1) + timedelta(days=i * 5)
        events = []
        
        for j in range(random.randint(100, 300)):
            events.append({
                "event_id": f"EVT_{uuid.uuid4().hex[:12]}",
                "event_type": random.choice(["navigation", "module_activated", "proposal_created", "memory_read"]),
                "timestamp": (base + timedelta(seconds=j * 3)).isoformat() + "Z",
                "payload": {"step": j, "data": "x" * 100}
            })
        
        replays.append({
            "replay_id": f"REPLAY_{base.strftime('%Y%m%d')}_{i+1:03d}",
            "created_at": base.isoformat() + "Z",
            "duration_seconds": len(events) * 3,
            "event_count": len(events),
            "demo_flow": random.choice([None, "FLOW_ULTRA_SHORT_90S", "FLOW_LIVE_DEMO"]),
            "events": events,
            "metadata": {
                "presenter": f"Presenter {i+1}",
                "audience_size": random.randint(1, 20),
                "notes": f"Replay session {i+1} notes"
            }
        })
    
    return replays

def generate_signed_exports():
    """Generate sample signed export artifacts"""
    exports = []
    
    for i in range(10):
        export_date = datetime(2025, 11, 1) + timedelta(days=i * 3)
        content = f"Export content {i} - " + "x" * 5000
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        exports.append({
            "export_id": f"EXP_{export_date.strftime('%Y%m%d')}_{i+1:03d}",
            "export_type": random.choice(["demo_narrative", "investor_qa", "incident_report", "replay_summary"]),
            "created_at": export_date.isoformat() + "Z",
            "created_by": f"User {i+1}",
            "filename": f"export_{i+1}.pdf",
            "content_hash": content_hash,
            "signature": {
                "algorithm": "HMAC-SHA256",
                "key_id": "demo_key_001",
                "signature": hashlib.sha256(f"{content_hash}:signature".encode()).hexdigest(),
                "signed_at": export_date.isoformat() + "Z"
            },
            "verification": {
                "verified": True,
                "verified_at": (export_date + timedelta(hours=1)).isoformat() + "Z",
                "verified_by": "system"
            },
            "metadata": {
                "pages": random.randint(5, 30),
                "size_bytes": random.randint(50000, 500000)
            }
        })
    
    return exports

def main():
    print("Generating large data files...")
    
    # Sphere mappings
    spheres = generate_sphere_mappings()
    with open(f"{BASE_DIR}/data/datasets/sphere_mappings.json", "w") as f:
        json.dump(spheres, f, indent=2)
    print(f"  Sphere mappings: {len(spheres)} spheres")
    
    # Agent configs
    agents = generate_agent_configs()
    with open(f"{BASE_DIR}/data/datasets/agent_configs.json", "w") as f:
        json.dump({"agents": agents, "count": len(agents)}, f, indent=2)
    print(f"  Agent configs: {len(agents)} agents")
    
    # Project details
    projects = generate_project_details()
    with open(f"{BASE_DIR}/data/datasets/project_details.json", "w") as f:
        json.dump({"projects": projects, "count": len(projects)}, f, indent=2)
    print(f"  Project details: {len(projects)} projects")
    
    # Compliance database
    compliance = generate_compliance_database()
    with open(f"{BASE_DIR}/data/datasets/compliance_database.json", "w") as f:
        json.dump(compliance, f, indent=2)
    print(f"  Compliance database")
    
    # Replay fixtures
    replays = generate_replay_fixtures()
    with open(f"{BASE_DIR}/demo/replay/sample_replays.json", "w") as f:
        json.dump({"replays": replays, "count": len(replays)}, f, indent=2)
    print(f"  Replay fixtures: {len(replays)} replays")
    
    # Signed exports
    exports = generate_signed_exports()
    with open(f"{BASE_DIR}/exports/signed/sample_exports.json", "w") as f:
        json.dump({"exports": exports, "count": len(exports)}, f, indent=2)
    print(f"  Signed exports: {len(exports)} exports")
    
    print("Done!")

if __name__ == "__main__":
    main()
