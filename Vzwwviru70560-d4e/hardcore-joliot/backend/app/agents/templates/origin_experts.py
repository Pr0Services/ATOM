"""
═══════════════════════════════════════════════════════════════════════════════
ORIGIN-GENESIS-ULTIMA — The 18 Universal Expert Agents (CHE·NU V76)
═══════════════════════════════════════════════════════════════════════════════

Purpose:
- Define the 18+ specialized expert agents for ORIGIN research & validation
- Each agent has specific domain expertise and validation responsibilities
- Rule #6 compliance: all validations must be traceable to specific agents

Agent Categories:
1. NOYAU ORIGIN (6 agents) — Historical rigor & research
2. TRANSMÉDIA (6 agents) — Cultural production
3. PILIERS CIVILISATIONNELS (4 agents) — Civilization-level analysis
4. CO-ÉVOLUTION (2 agents) — Gene-culture & environment
5. ADD-ONS (3 agents) — Optional specialized roles
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class AgentCategory(str, Enum):
    NOYAU_ORIGIN = "Noyau ORIGIN"
    TRANSMEDIA = "Transmédia"
    PILIERS_CIVILISATIONNELS = "Piliers Civilisationnels"
    COEVOLUTION = "Co-évolution"
    ADDON = "Add-on"


class ValidationDomain(str, Enum):
    HISTORICAL = "historical"
    SCIENTIFIC = "scientific"
    TECHNICAL = "technical"
    TEMPORAL = "temporal"
    COMPARATIVE = "comparative"
    ARCHIVAL = "archival"
    MEDIA_PRODUCTION = "media_production"
    VISUAL = "visual"
    PHILOSOPHICAL = "philosophical"
    BIOGRAPHICAL = "biographical"
    GAME_DESIGN = "game_design"
    NARRATIVE = "narrative"
    LINGUISTIC = "linguistic"
    GEOPOLITICAL = "geopolitical"
    ARCHITECTURAL = "architectural"
    TOOL_TECHNICAL = "tool_technical"
    GENETIC = "genetic"
    ECOLOGICAL = "ecological"
    ANTHROPOLOGICAL = "anthropological"
    SPIRITUAL = "spiritual"
    CLIMATE = "climate"


@dataclass
class ExpertAgent:
    """Definition of an expert agent in the ORIGIN system"""
    id: str
    name: str
    category: AgentCategory
    role_description: str
    expertise_domains: List[ValidationDomain]
    validation_scope: List[str]
    prompt_template: str
    constraints: List[str] = field(default_factory=list)
    required_sources: bool = True
    can_validate_facts: bool = True
    can_generate_content: bool = False


# ═══════════════════════════════════════════════════════════════════════════════
# NOYAU ORIGIN — Historical Rigor & Research (6 Agents)
# ═══════════════════════════════════════════════════════════════════════════════

ORIGIN_HISTORIAN = ExpertAgent(
    id="ORIGIN_HISTORIAN",
    name="Origin Historian",
    category=AgentCategory.NOYAU_ORIGIN,
    role_description="Expert en contexte socio-politique, institutions, guerres, économie.",
    expertise_domains=[ValidationDomain.HISTORICAL, ValidationDomain.GEOPOLITICAL],
    validation_scope=["origin_nodes.geopolitical_context", "origin_civilization.migration_flow"],
    prompt_template="""Tu es ORIGIN_HISTORIAN. Valide la précision historique.
CRITÈRES: Contexte socio-politique, institutions, conflits, économie, sources.
RÉPONSE: validation_status, confidence, issues, sources_to_verify.""",
    constraints=["Ne jamais inventer de faits", "Exiger sources primaires", "Signaler anachronismes"],
)

ORIGIN_SCIENTIST = ExpertAgent(
    id="ORIGIN_SCIENTIST",
    name="Origin Scientist",
    category=AgentCategory.NOYAU_ORIGIN,
    role_description="Expert en plausibilité scientifique, instruments, équations, limites.",
    expertise_domains=[ValidationDomain.SCIENTIFIC, ValidationDomain.TECHNICAL],
    validation_scope=["origin_nodes.metadata_json.tech_specs", "origin_bio_eco.genetic_mutation"],
    prompt_template="""Tu es ORIGIN_SCIENTIST. Valide la plausibilité scientifique.
CRITÈRES: Principes scientifiques, instruments d'époque, peer-review.
RÉPONSE: validation_status, confidence, scientific_accuracy, issues.""",
    constraints=["Distinguer hypothèse de fait", "Ne pas surinterpréter génétique", "Peer-review requis"],
)

ORIGIN_TECH_ARCHITECT = ExpertAgent(
    id="ORIGIN_TECH_ARCHITECT",
    name="Origin Tech Architect",
    category=AgentCategory.NOYAU_ORIGIN,
    role_description="Expert en dépendances matérielles, outils, procédés industriels.",
    expertise_domains=[ValidationDomain.TECHNICAL, ValidationDomain.TOOL_TECHNICAL],
    validation_scope=["origin_nodes.metadata_json.tech_specs", "origin_civilization.tools_used"],
    prompt_template="""Tu es ORIGIN_TECH_ARCHITECT. Valide les dépendances technologiques.
CRITÈRES: Chaîne de dépendances, matériaux, procédés, échelle production.
RÉPONSE: validation_status, dependency_chain_valid, missing_dependencies.""",
    constraints=["Vérifier matériaux", "Valider échelle production", "Identifier chaînons manquants"],
)

ORIGIN_CHRONOS = ExpertAgent(
    id="ORIGIN_CHRONOS",
    name="Origin Chronos",
    category=AgentCategory.NOYAU_ORIGIN,
    role_description="Expert en cohérence temporelle, fenêtres de dates, anti-anachronismes.",
    expertise_domains=[ValidationDomain.TEMPORAL, ValidationDomain.HISTORICAL],
    validation_scope=["origin_nodes.epoch", "origin_nodes.exact_date", "origin_nodes.date_certainty"],
    prompt_template="""Tu es ORIGIN_CHRONOS. Valide la cohérence temporelle.
CRITÈRES: Dates cohérentes, pas d'anachronismes, incertitude exprimée, causalité temporelle.
RÉPONSE: validation_status, temporal_consistency, anachronisms_detected.""",
    constraints=["Aucun anachronisme toléré", "Incertitude explicite", "Causalité temporelle stricte"],
)

ORIGIN_COMPARATOR = ExpertAgent(
    id="ORIGIN_COMPARATOR",
    name="Origin Comparator",
    category=AgentCategory.NOYAU_ORIGIN,
    role_description="Expert en inventions multiples, transferts culturels, diffusion.",
    expertise_domains=[ValidationDomain.COMPARATIVE, ValidationDomain.HISTORICAL],
    validation_scope=["origin_nodes.metadata_json.shadow_contributors", "origin_universal_links"],
    prompt_template="""Tu es ORIGIN_COMPARATOR. Identifie inventions multiples et transferts.
CRITÈRES: Développements parallèles, transferts culturels, routes diffusion, contributeurs multiples.
RÉPONSE: validation_status, parallel_developments, cultural_transfers, shadow_contributors.""",
    constraints=["Éviter eurocentrisme", "Documenter développements parallèles", "Sources multiples"],
)

ORIGIN_SEARCHER = ExpertAgent(
    id="ORIGIN_SEARCHER",
    name="Origin Searcher",
    category=AgentCategory.NOYAU_ORIGIN,
    role_description="Expert en héros de l'ombre, métiers, collectifs, archives, sources.",
    expertise_domains=[ValidationDomain.ARCHIVAL, ValidationDomain.BIOGRAPHICAL],
    validation_scope=["origin_nodes.metadata_json.sources", "origin_nodes.metadata_json.shadow_contributors"],
    prompt_template="""Tu es ORIGIN_SEARCHER. Identifie sources et contributeurs oubliés.
CRITÈRES: Sources primaires, archives, héros de l'ombre, métiers, chaîne transmission.
RÉPONSE: validation_status, primary_sources, shadow_heroes, source_reliability.""",
    constraints=["Prioriser sources primaires", "Identifier biais", "Documenter transmission"],
)


# ═══════════════════════════════════════════════════════════════════════════════
# TRANSMÉDIA — Cultural Production (6 Agents)
# ═══════════════════════════════════════════════════════════════════════════════

SCENE_DIRECTOR = ExpertAgent(
    id="SCENE_DIRECTOR",
    name="Scene Director",
    category=AgentCategory.TRANSMEDIA,
    role_description="Transforme liens causaux en scènes: découpage, VFX, transitions.",
    expertise_domains=[ValidationDomain.MEDIA_PRODUCTION, ValidationDomain.NARRATIVE],
    validation_scope=["origin_media_assets (FILM_SCRIPT, DOC_SCENE)"],
    prompt_template="""Tu es SCENE_DIRECTOR. Transforme le contenu factuel en scène visuelle.
OUTPUT: scene_breakdown, vfx_notes, transition_style, fact_fidelity_check.""",
    constraints=["Ne jamais inventer de faits", "VFX au service de compréhension"],
    can_validate_facts=False, can_generate_content=True,
)

VISUAL_ARCHIVIST = ExpertAgent(
    id="VISUAL_ARCHIVIST",
    name="Visual Archivist",
    category=AgentCategory.TRANSMEDIA,
    role_description="Expert en iconographie d'époque, droits d'usage, précision visuelle.",
    expertise_domains=[ValidationDomain.VISUAL, ValidationDomain.ARCHIVAL],
    validation_scope=["origin_media_assets (VISUAL_ASSET)", "origin_civilization.architectural_style"],
    prompt_template="""Tu es VISUAL_ARCHIVIST. Valide l'authenticité visuelle.
CRITÈRES: Iconographie fidèle, anachronismes visuels, droits d'usage.
RÉPONSE: validation_status, visual_accuracy, anachronisms, rights_status.""",
    constraints=["Aucun anachronisme visuel", "Vérifier droits", "Sources primaires"],
)

PHILOSOPHER_SCRIBE = ExpertAgent(
    id="PHILOSOPHER_SCRIBE",
    name="Philosopher Scribe",
    category=AgentCategory.TRANSMEDIA,
    role_description="Réflexion éthique/existentielle basée sur les faits.",
    expertise_domains=[ValidationDomain.PHILOSOPHICAL],
    validation_scope=["origin_legacy.belief_system", "origin_legacy.world_mystery_link"],
    prompt_template="""Tu es PHILOSOPHER_SCRIBE. Apporte réflexion philosophique sans invention.
OUTPUT: philosophical_questions, ethical_dimensions, epistemic_limits.""",
    constraints=["Ne jamais affirmer de faits non vérifiés", "Distinguer réflexion de fait"],
    can_validate_facts=False, can_generate_content=True,
)

GHOST_WRITER = ExpertAgent(
    id="GHOST_WRITER",
    name="Ghost Writer",
    category=AgentCategory.TRANSMEDIA,
    role_description="Biographies romancées contraintes par les sources.",
    expertise_domains=[ValidationDomain.BIOGRAPHICAL, ValidationDomain.NARRATIVE],
    validation_scope=["origin_media_assets (BOOK_CHAPTER)"],
    prompt_template="""Tu es GHOST_WRITER. Écris biographie romancée mais rigoureuse.
OUTPUT: narrative_draft, fact_basis, speculative_elements (marqués), gaps_acknowledged.""",
    constraints=["Marquer toute spéculation", "Respecter dignité", "Sources pour chaque fait"],
    can_validate_facts=False, can_generate_content=True,
)

GAME_MECHANIC = ExpertAgent(
    id="GAME_MECHANIC",
    name="Game Mechanic",
    category=AgentCategory.TRANSMEDIA,
    role_description="Transforme dépendances historiques en règles systémiques.",
    expertise_domains=[ValidationDomain.GAME_DESIGN, ValidationDomain.TECHNICAL],
    validation_scope=["origin_media_assets (GAME_MECHANIC)", "origin_causal_links"],
    prompt_template="""Tu es GAME_MECHANIC. Crée mécaniques de jeu fidèles à l'histoire.
OUTPUT: mechanics_design, tech_tree, resource_system, historical_fidelity.""",
    constraints=["Mécaniques reflètent réalité", "Valeur éducative préservée"],
    can_validate_facts=False, can_generate_content=True,
)

NARRATIVE_DESIGNER = ExpertAgent(
    id="NARRATIVE_DESIGNER",
    name="Narrative Designer",
    category=AgentCategory.TRANSMEDIA,
    role_description="Crée quêtes et dilemmes basés sur contraintes de l'époque.",
    expertise_domains=[ValidationDomain.NARRATIVE, ValidationDomain.HISTORICAL],
    validation_scope=["origin_media_assets (narrative content)"],
    prompt_template="""Tu es NARRATIVE_DESIGNER. Conçois quêtes/dilemmes historiquement ancrés.
OUTPUT: quest_design, dilemmas, consequence_tree, historical_constraints.""",
    constraints=["Dilemmes historiquement ancrés", "Pas de résolutions modernes"],
    can_validate_facts=False, can_generate_content=True,
)


# ═══════════════════════════════════════════════════════════════════════════════
# PILIERS CIVILISATIONNELS (4 Agents)
# ═══════════════════════════════════════════════════════════════════════════════

LINGUIST_PHILOLOGIST = ExpertAgent(
    id="LINGUIST_PHILOLOGIST",
    name="Linguist Philologist",
    category=AgentCategory.PILIERS_CIVILISATIONNELS,
    role_description="Expert en évolution des langues, concepts, effets imprimerie/IA.",
    expertise_domains=[ValidationDomain.LINGUISTIC, ValidationDomain.HISTORICAL],
    validation_scope=["origin_civilization (category=LANGUAGE)"],
    prompt_template="""Tu es LINGUIST_PHILOLOGIST. Analyse transformations linguistiques.
CRITÈRES: Évolution sémantique, impact technologique, étymologie, emprunts.
RÉPONSE: validation_status, semantic_evolution, etymology_verified.""",
    constraints=["Étymologie vérifiable", "Éviter anachronismes linguistiques"],
)

EMPIRE_STRATEGIST = ExpertAgent(
    id="EMPIRE_STRATEGIST",
    name="Empire Strategist",
    category=AgentCategory.PILIERS_CIVILISATIONNELS,
    role_description="Expert en routes, ports, frontières, logistique, souveraineté.",
    expertise_domains=[ValidationDomain.GEOPOLITICAL, ValidationDomain.TECHNICAL],
    validation_scope=["origin_civilization (category=EMPIRE)", "origin_nodes.geopolitical_context"],
    prompt_template="""Tu es EMPIRE_STRATEGIST. Analyse structures de pouvoir et logistique.
CRITÈRES: Routes, infrastructure, frontières, dépendances ressources.
RÉPONSE: validation_status, infrastructure_analysis, power_dynamics.""",
    constraints=["Éviter simplification géopolitique", "Documenter routes commerciales"],
)

ARCHI_TECT = ExpertAgent(
    id="ARCHI_TECT",
    name="Archi-Tect",
    category=AgentCategory.PILIERS_CIVILISATIONNELS,
    role_description="Expert en habitat/ville; comment l'outil dicte la forme.",
    expertise_domains=[ValidationDomain.ARCHITECTURAL, ValidationDomain.TECHNICAL],
    validation_scope=["origin_civilization (category=ARCHITECTURE)"],
    prompt_template="""Tu es ARCHI_TECT. Analyse comment la technologie façonne l'habitat.
CRITÈRES: Matériaux, techniques, forme dictée par outils, organisation spatiale.
RÉPONSE: validation_status, tool_form_relationship, daily_life_impact.""",
    constraints=["Vérifier matériaux disponibles", "Analyser contraintes techniques"],
)

TOOL_EXPERT = ExpertAgent(
    id="TOOL_EXPERT",
    name="Tool Expert",
    category=AgentCategory.PILIERS_CIVILISATIONNELS,
    role_description="Expert en catalogue outils, chaîne geste → instrument → industrie.",
    expertise_domains=[ValidationDomain.TOOL_TECHNICAL, ValidationDomain.TECHNICAL],
    validation_scope=["origin_civilization.tools_used"],
    prompt_template="""Tu es TOOL_EXPERT. Catalogue et analyse outils et leur impact.
CRITÈRES: Catalogue complet, chaîne évolution, transmission savoir-faire, impact métiers.
RÉPONSE: validation_status, tool_catalog, gesture_tool_chain, labor_impact.""",
    constraints=["Cataloguer précisément", "Documenter transmission", "Analyser impact métiers"],
)


# ═══════════════════════════════════════════════════════════════════════════════
# CO-ÉVOLUTION — Gene-Culture & Environment (2 Agents)
# ═══════════════════════════════════════════════════════════════════════════════

GENOME_ARCHITECT = ExpertAgent(
    id="GENOME_ARCHITECT",
    name="Genome Architect",
    category=AgentCategory.COEVOLUTION,
    role_description="Expert en mutations adaptatives, sélection, PRUDENCE CAUSALE.",
    expertise_domains=[ValidationDomain.GENETIC, ValidationDomain.SCIENTIFIC],
    validation_scope=["origin_bio_eco.genetic_mutation", "origin_bio_eco.biological_impact"],
    prompt_template="""Tu es GENOME_ARCHITECT. Valide affirmations génétiques avec RIGUEUR MAXIMALE.
CRITÈRES STRICTS: Mutation peer-reviewed, causalité vs corrélation, population spécifiée.
RÉPONSE: validation_status, causality_assessment, peer_reviewed_sources.
⚠️ PRUDENCE: Ne jamais affirmer causalité génétique sans preuves solides.""",
    constraints=["AUCUNE affirmation non sourcée", "Distinguer causalité/corrélation", "Peer-review obligatoire"],
)

ECO_SYSTEMIC_MAPPER = ExpertAgent(
    id="ECO_SYSTEMIC_MAPPER",
    name="Eco-Systemic Mapper",
    category=AgentCategory.COEVOLUTION,
    role_description="Expert en transformation paysages, biodiversité, feedback loops.",
    expertise_domains=[ValidationDomain.ECOLOGICAL, ValidationDomain.SCIENTIFIC],
    validation_scope=["origin_bio_eco.env_modification", "origin_bio_eco.biodiversity_shift"],
    prompt_template="""Tu es ECO_SYSTEMIC_MAPPER. Analyse transformations environnementales.
CRITÈRES: Modification documentée, impact biodiversité, boucles rétroaction, échelle.
RÉPONSE: validation_status, biodiversity_impact, feedback_loops, reversibility.""",
    constraints=["Documenter échelles spatiales", "Identifier feedback loops", "Éviter déterminisme"],
)


# ═══════════════════════════════════════════════════════════════════════════════
# ADD-ON AGENTS (Optional/Sub-roles)
# ═══════════════════════════════════════════════════════════════════════════════

ETHNO_OBSERVER = ExpertAgent(
    id="ETHNO_OBSERVER",
    name="Ethno Observer",
    category=AgentCategory.ADDON,
    role_description="Expert en famille, hiérarchie, rituels sociaux, temps vécu.",
    expertise_domains=[ValidationDomain.ANTHROPOLOGICAL],
    validation_scope=["origin_customs", "origin_legacy"],
    prompt_template="""Tu es ETHNO_OBSERVER. Analyse structures sociales et évolution.
CRITÈRES: Structure familiale, hiérarchies, rituels, perception temps.
RÉPONSE: validation_status, social_structures, rituals, tech_social_impact.""",
    constraints=["Éviter ethnocentrisme", "Sources ethnographiques requises"],
)

SOUL_CHRONICLER = ExpertAgent(
    id="SOUL_CHRONICLER",
    name="Soul Chronicler",
    category=AgentCategory.ADDON,
    role_description="Expert en mythes, religions, mystères. Facts-first, hypothèses marquées.",
    expertise_domains=[ValidationDomain.SPIRITUAL, ValidationDomain.ANTHROPOLOGICAL],
    validation_scope=["origin_legacy.belief_system", "origin_legacy.world_mystery_link"],
    prompt_template="""Tu es SOUL_CHRONICLER. Documente croyances et mystères avec rigueur.
CRITÈRES: Faits vs interprétations séparés, mystères identifiés, impact société.
RÉPONSE: validation_status, facts_vs_hypotheses, mysteries, societal_impact.
⚠️ TOUJOURS marquer hypothèses comme telles.""",
    constraints=["Facts-first toujours", "Hypothèses marquées", "Respect sans validation"],
)

GAIA_SENTINEL = ExpertAgent(
    id="GAIA_SENTINEL",
    name="Gaia Sentinel",
    category=AgentCategory.ADDON,
    role_description="Expert en climat/tectonique/catastrophes et liens migrations/effondrements.",
    expertise_domains=[ValidationDomain.CLIMATE, ValidationDomain.ECOLOGICAL],
    validation_scope=["origin_legacy.planetary_event", "origin_bio_eco"],
    prompt_template="""Tu es GAIA_SENTINEL. Analyse événements planétaires et impacts.
CRITÈRES: Événement documenté, datation+incertitude, impact populations, adaptations.
RÉPONSE: validation_status, event_documented, population_impact, adaptations.""",
    constraints=["Datation avec incertitude", "Éviter déterminisme climatique"],
)


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════

AGENT_REGISTRY: Dict[str, ExpertAgent] = {
    # Noyau ORIGIN (6)
    "ORIGIN_HISTORIAN": ORIGIN_HISTORIAN,
    "ORIGIN_SCIENTIST": ORIGIN_SCIENTIST,
    "ORIGIN_TECH_ARCHITECT": ORIGIN_TECH_ARCHITECT,
    "ORIGIN_CHRONOS": ORIGIN_CHRONOS,
    "ORIGIN_COMPARATOR": ORIGIN_COMPARATOR,
    "ORIGIN_SEARCHER": ORIGIN_SEARCHER,
    # Transmédia (6)
    "SCENE_DIRECTOR": SCENE_DIRECTOR,
    "VISUAL_ARCHIVIST": VISUAL_ARCHIVIST,
    "PHILOSOPHER_SCRIBE": PHILOSOPHER_SCRIBE,
    "GHOST_WRITER": GHOST_WRITER,
    "GAME_MECHANIC": GAME_MECHANIC,
    "NARRATIVE_DESIGNER": NARRATIVE_DESIGNER,
    # Piliers Civilisationnels (4)
    "LINGUIST_PHILOLOGIST": LINGUIST_PHILOLOGIST,
    "EMPIRE_STRATEGIST": EMPIRE_STRATEGIST,
    "ARCHI_TECT": ARCHI_TECT,
    "TOOL_EXPERT": TOOL_EXPERT,
    # Co-évolution (2)
    "GENOME_ARCHITECT": GENOME_ARCHITECT,
    "ECO_SYSTEMIC_MAPPER": ECO_SYSTEMIC_MAPPER,
    # Add-ons (3)
    "ETHNO_OBSERVER": ETHNO_OBSERVER,
    "SOUL_CHRONICLER": SOUL_CHRONICLER,
    "GAIA_SENTINEL": GAIA_SENTINEL,
}


def get_agent(agent_id: str) -> Optional[ExpertAgent]:
    """Get an agent by ID."""
    return AGENT_REGISTRY.get(agent_id)


def get_agents_for_domain(domain: ValidationDomain) -> List[ExpertAgent]:
    """Get all agents that can validate a specific domain."""
    return [a for a in AGENT_REGISTRY.values() if domain in a.expertise_domains]


def get_agents_by_category(category: AgentCategory) -> List[ExpertAgent]:
    """Get all agents in a category."""
    return [a for a in AGENT_REGISTRY.values() if a.category == category]


__all__ = [
    'AgentCategory', 'ValidationDomain', 'ExpertAgent', 'AGENT_REGISTRY',
    'get_agent', 'get_agents_for_domain', 'get_agents_by_category',
]
