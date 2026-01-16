"""
CHE·NU V68 Transport Agents Registry
Division Cinetique Urbaine - 50 Agents Specialises

AGENT CATEGORIES:
1. Agents "Sonde" (10 agents) - Analyse des deplacements
2. Agents "Optimiseurs" (15 agents) - Reduction trafic, maximisation remplissage
3. Agents "Dispatch" (15 agents) - Gestion temps reel, sous-traitance
4. Agents "Flow" (10 agents) - Visualisation et monitoring

GOVERNANCE COMPLIANCE:
- Rule #1: Dispatch haute valeur + sous-traitance require human gate
- Rule #4: NO AI-to-AI orchestration
- Rule #5: No ranking by performance/rating
- Rule #6: Full traceability
"""

from typing import List, Dict, Any
from uuid import uuid4


def get_transport_agents() -> List[Dict[str, Any]]:
    """
    50 Transport & Logistics sphere agents
    Division Cinetique Urbaine
    """
    return [
        # ====================================================================
        # AGENTS SONDE (10) - Analyse des deplacements
        # ====================================================================
        {
            "name": "transport_pattern_analyzer",
            "display_name": "Pattern Analyzer",
            "description": "Analyse les patterns de deplacement recurrents",
            "capabilities": ["analysis", "data_processing"],
            "requires_human_gate": False
        },
        {
            "name": "transport_stagnation_detector",
            "display_name": "Stagnation Detector",
            "description": "Detecte les points de stagnation et goulots",
            "capabilities": ["analysis", "classification"],
            "requires_human_gate": False
        },
        {
            "name": "transport_peak_predictor",
            "display_name": "Peak Hour Predictor",
            "description": "Predit les heures de pointe par zone",
            "capabilities": ["analysis", "recommendation"],
            "requires_human_gate": False
        },
        {
            "name": "transport_demand_forecaster",
            "display_name": "Demand Forecaster",
            "description": "Prevision de la demande de transport",
            "capabilities": ["analysis", "data_processing"],
            "requires_human_gate": False
        },
        {
            "name": "transport_route_analyzer",
            "display_name": "Route Analyzer",
            "description": "Analyse l'efficacite des itineraires",
            "capabilities": ["analysis", "recommendation"],
            "requires_human_gate": False
        },
        {
            "name": "transport_zone_monitor",
            "display_name": "Zone Monitor",
            "description": "Surveille les zones Che-Nu en temps reel",
            "capabilities": ["data_processing", "classification"],
            "requires_human_gate": False
        },
        {
            "name": "transport_seasonal_analyzer",
            "display_name": "Seasonal Analyzer",
            "description": "Analyse les variations saisonnieres",
            "capabilities": ["analysis", "summarization"],
            "requires_human_gate": False
        },
        {
            "name": "transport_client_behavior",
            "display_name": "Client Behavior Analyst",
            "description": "Analyse les comportements clients",
            "capabilities": ["analysis", "classification"],
            "requires_human_gate": False
        },
        {
            "name": "transport_emissions_tracker",
            "display_name": "Emissions Tracker",
            "description": "Suivi des emissions CO2 par trajet",
            "capabilities": ["data_processing", "analysis"],
            "requires_human_gate": False
        },
        {
            "name": "transport_cost_analyzer",
            "display_name": "Cost Analyzer",
            "description": "Analyse des couts de transport",
            "capabilities": ["analysis", "data_processing"],
            "requires_human_gate": False
        },

        # ====================================================================
        # AGENTS OPTIMISEURS (15) - Reduction trafic, maximisation remplissage
        # ====================================================================
        {
            "name": "transport_fill_rate_optimizer",
            "display_name": "Fill Rate Optimizer",
            "description": "Maximise le taux de remplissage des vehicules",
            "capabilities": ["recommendation", "analysis"],
            "requires_human_gate": False
        },
        {
            "name": "transport_pooling_suggester",
            "display_name": "Pooling Suggester",
            "description": "Suggere des opportunites de mutualisation",
            "capabilities": ["recommendation", "analysis"],
            "requires_human_gate": False
        },
        {
            "name": "transport_covoiturage_matcher",
            "display_name": "Covoiturage Matcher",
            "description": "Match les opportunites de covoiturage",
            "capabilities": ["recommendation", "data_processing"],
            "requires_human_gate": False
        },
        {
            "name": "transport_route_optimizer",
            "display_name": "Route Optimizer",
            "description": "Optimise les itineraires multi-stops",
            "capabilities": ["recommendation", "analysis"],
            "requires_human_gate": False
        },
        {
            "name": "transport_load_balancer",
            "display_name": "Load Balancer",
            "description": "Equilibre la charge entre vehicules",
            "capabilities": ["recommendation", "data_processing"],
            "requires_human_gate": False
        },
        {
            "name": "transport_fuel_optimizer",
            "display_name": "Fuel Optimizer",
            "description": "Optimise la consommation de carburant",
            "capabilities": ["recommendation", "analysis"],
            "requires_human_gate": False
        },
        {
            "name": "transport_time_optimizer",
            "display_name": "Time Optimizer",
            "description": "Minimise les temps de trajet",
            "capabilities": ["recommendation", "analysis"],
            "requires_human_gate": False
        },
        {
            "name": "transport_eco_router",
            "display_name": "Eco Router",
            "description": "Suggere des routes ecologiques",
            "capabilities": ["recommendation", "analysis"],
            "requires_human_gate": False
        },
        {
            "name": "transport_delivery_window",
            "display_name": "Delivery Window Optimizer",
            "description": "Optimise les creneaux de livraison",
            "capabilities": ["recommendation", "content_planning"],
            "requires_human_gate": False
        },
        {
            "name": "transport_return_load",
            "display_name": "Return Load Finder",
            "description": "Trouve des charges pour les retours a vide",
            "capabilities": ["research", "recommendation"],
            "requires_human_gate": False
        },
        {
            "name": "transport_fleet_optimizer",
            "display_name": "Fleet Optimizer",
            "description": "Optimise l'utilisation de la flotte",
            "capabilities": ["recommendation", "analysis"],
            "requires_human_gate": False
        },
        {
            "name": "transport_maintenance_scheduler",
            "display_name": "Maintenance Scheduler",
            "description": "Planifie les maintenances optimales",
            "capabilities": ["content_planning", "recommendation"],
            "requires_human_gate": False
        },
        {
            "name": "transport_driver_matcher",
            "display_name": "Driver Matcher",
            "description": "Match chauffeurs et vehicules",
            "capabilities": ["recommendation", "data_processing"],
            "requires_human_gate": False
        },
        {
            "name": "transport_capacity_planner",
            "display_name": "Capacity Planner",
            "description": "Planifie les besoins en capacite",
            "capabilities": ["content_planning", "analysis"],
            "requires_human_gate": False
        },
        {
            "name": "transport_congestion_avoider",
            "display_name": "Congestion Avoider",
            "description": "Evite les zones de congestion",
            "capabilities": ["recommendation", "analysis"],
            "requires_human_gate": False
        },

        # ====================================================================
        # AGENTS DISPATCH (15) - Gestion temps reel, sous-traitance
        # ====================================================================
        {
            "name": "transport_dispatcher",
            "display_name": "Main Dispatcher",
            "description": "Dispatch principal des trajets",
            "capabilities": ["data_processing", "recommendation"],
            "requires_human_gate": False
        },
        {
            "name": "transport_urgent_dispatcher",
            "display_name": "Urgent Dispatcher",
            "description": "Gestion des demandes urgentes",
            "capabilities": ["prioritization", "recommendation"],
            "requires_human_gate": False
        },
        {
            "name": "transport_soustraitance_manager",
            "display_name": "Sous-traitance Manager",
            "description": "Gestion des partenaires Uber/Taxi",
            "capabilities": ["data_processing", "recommendation"],
            "requires_human_gate": True,  # GOVERNANCE Rule #1
            "human_gate_capabilities": ["data_processing"]
        },
        {
            "name": "transport_overflow_handler",
            "display_name": "Overflow Handler",
            "description": "Gere les debordements de capacite",
            "capabilities": ["recommendation", "data_processing"],
            "requires_human_gate": True,  # May trigger sous-traitance
            "human_gate_capabilities": ["data_processing"]
        },
        {
            "name": "transport_realtime_adjuster",
            "display_name": "Real-time Adjuster",
            "description": "Ajustements en temps reel",
            "capabilities": ["data_processing", "recommendation"],
            "requires_human_gate": False
        },
        {
            "name": "transport_delay_manager",
            "display_name": "Delay Manager",
            "description": "Gestion des retards et replanification",
            "capabilities": ["data_processing", "notification_draft"],
            "requires_human_gate": True,
            "human_gate_capabilities": ["notification_draft"]
        },
        {
            "name": "transport_priority_handler",
            "display_name": "Priority Handler",
            "description": "Gestion des livraisons prioritaires",
            "capabilities": ["prioritization", "recommendation"],
            "requires_human_gate": False
        },
        {
            "name": "transport_rerouter",
            "display_name": "Dynamic Rerouter",
            "description": "Reroutage dynamique en cas d'incident",
            "capabilities": ["recommendation", "data_processing"],
            "requires_human_gate": False
        },
        {
            "name": "transport_partner_coordinator",
            "display_name": "Partner Coordinator",
            "description": "Coordination avec partenaires externes",
            "capabilities": ["data_processing", "message_draft"],
            "requires_human_gate": True,
            "human_gate_capabilities": ["message_draft"]
        },
        {
            "name": "transport_incident_responder",
            "display_name": "Incident Responder",
            "description": "Reponse aux incidents de transport",
            "capabilities": ["prioritization", "recommendation"],
            "requires_human_gate": False
        },
        {
            "name": "transport_handoff_coordinator",
            "display_name": "Handoff Coordinator",
            "description": "Coordination des transferts entre vehicules",
            "capabilities": ["data_processing", "recommendation"],
            "requires_human_gate": False
        },
        {
            "name": "transport_pickup_scheduler",
            "display_name": "Pickup Scheduler",
            "description": "Planification des collectes",
            "capabilities": ["content_planning", "recommendation"],
            "requires_human_gate": False
        },
        {
            "name": "transport_delivery_tracker",
            "display_name": "Delivery Tracker",
            "description": "Suivi des livraisons en temps reel",
            "capabilities": ["data_processing", "notification_draft"],
            "requires_human_gate": True,
            "human_gate_capabilities": ["notification_draft"]
        },
        {
            "name": "transport_eta_calculator",
            "display_name": "ETA Calculator",
            "description": "Calcul precis des heures d'arrivee",
            "capabilities": ["analysis", "data_processing"],
            "requires_human_gate": False
        },
        {
            "name": "transport_proof_of_delivery",
            "display_name": "POD Manager",
            "description": "Gestion des preuves de livraison",
            "capabilities": ["document_processing", "data_processing"],
            "requires_human_gate": False
        },

        # ====================================================================
        # AGENTS FLOW (10) - Visualisation et monitoring
        # ====================================================================
        {
            "name": "transport_flow_visualizer",
            "display_name": "Flow Visualizer",
            "description": "Visualisation des flux de transport",
            "capabilities": ["design_assist", "data_processing"],
            "requires_human_gate": False
        },
        {
            "name": "transport_friction_monitor",
            "display_name": "Friction Monitor",
            "description": "Monitore les zones de friction",
            "capabilities": ["analysis", "data_processing"],
            "requires_human_gate": False
        },
        {
            "name": "transport_fluidity_scorer",
            "display_name": "Fluidity Scorer",
            "description": "Calcule le score de fluidite global",
            "capabilities": ["scoring", "analysis"],
            "requires_human_gate": False
        },
        {
            "name": "transport_kpi_tracker",
            "display_name": "KPI Tracker",
            "description": "Suivi des indicateurs de performance",
            "capabilities": ["analysis", "data_processing"],
            "requires_human_gate": False
        },
        {
            "name": "transport_heatmap_generator",
            "display_name": "Heatmap Generator",
            "description": "Genere des cartes de chaleur du trafic",
            "capabilities": ["design_assist", "data_processing"],
            "requires_human_gate": False
        },
        {
            "name": "transport_alert_manager",
            "display_name": "Alert Manager",
            "description": "Gestion des alertes de transport",
            "capabilities": ["notification_draft", "prioritization"],
            "requires_human_gate": True,
            "human_gate_capabilities": ["notification_draft"]
        },
        {
            "name": "transport_dashboard_builder",
            "display_name": "Dashboard Builder",
            "description": "Construction de tableaux de bord",
            "capabilities": ["design_assist", "content_planning"],
            "requires_human_gate": False
        },
        {
            "name": "transport_report_generator",
            "display_name": "Report Generator",
            "description": "Generation de rapports de transport",
            "capabilities": ["text_generation", "analysis"],
            "requires_human_gate": False
        },
        {
            "name": "transport_trend_analyzer",
            "display_name": "Trend Analyzer",
            "description": "Analyse des tendances de transport",
            "capabilities": ["analysis", "summarization"],
            "requires_human_gate": False
        },
        {
            "name": "transport_sustainability_reporter",
            "display_name": "Sustainability Reporter",
            "description": "Rapports sur l'impact environnemental",
            "capabilities": ["text_generation", "analysis"],
            "requires_human_gate": False
        },
    ]


# Constants
TRANSPORT_AGENT_COUNT = 50
TRANSPORT_CATEGORIES = {
    "sonde": 10,      # Analyse des deplacements
    "optimiseurs": 15, # Reduction trafic
    "dispatch": 15,   # Gestion temps reel
    "flow": 10        # Visualisation
}


def validate_transport_agents() -> bool:
    """Validate that we have exactly 50 transport agents"""
    agents = get_transport_agents()
    return len(agents) == TRANSPORT_AGENT_COUNT
