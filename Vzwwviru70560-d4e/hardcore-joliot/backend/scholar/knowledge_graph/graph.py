"""
============================================================================
CHE·NU™ V69 — SCHOLAR CAUSAL KNOWLEDGE GRAPH
============================================================================
Spec: GPT1/CHE-NU_SCH_CAUSAL_KNOWLEDGE_GRAPH.md

Objective: Replace keyword search with navigation by verified cause-effect relations.

Description (per spec):
- Nœud = Découverte / Artifact
- Lien = Preuve causale (p-value, source, reproductibilité)
- Couleur/Épaisseur = Force et certitude causale

UX (WebXR):
- Zoom sémantique, filtres par domaine/pattern
- Split-view analogique
- Timeline causale

Governance:
- Liaisons validées via OPA + Reproducibility Worker
- Signatures immuables des liens
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import logging
import json
import math

from ..models import (
    CausalNode,
    CausalLink,
    CausalLinkStrength,
    VerificationStatus,
    generate_id,
    compute_hash,
)

logger = logging.getLogger(__name__)


# ============================================================================
# CAUSAL KNOWLEDGE GRAPH
# ============================================================================

class CausalKnowledgeGraph:
    """
    Global Causal Knowledge Graph for discovery exploration.
    
    Per spec: Explorer de graphes 3D (WebXR)
    """
    
    def __init__(self):
        self._nodes: Dict[str, CausalNode] = {}
        self._links: Dict[str, CausalLink] = {}
        
        # Indexes
        self._nodes_by_domain: Dict[str, Set[str]] = {}
        self._links_by_source: Dict[str, Set[str]] = {}
        self._links_by_target: Dict[str, Set[str]] = {}
    
    # =========================================================================
    # NODE MANAGEMENT
    # =========================================================================
    
    def add_node(self, node: CausalNode) -> str:
        """Add a discovery node to the graph"""
        self._nodes[node.node_id] = node
        
        # Index by domain
        if node.domain not in self._nodes_by_domain:
            self._nodes_by_domain[node.domain] = set()
        self._nodes_by_domain[node.domain].add(node.node_id)
        
        logger.info(f"Added node {node.node_id}: {node.title}")
        return node.node_id
    
    def get_node(self, node_id: str) -> Optional[CausalNode]:
        """Get node by ID"""
        return self._nodes.get(node_id)
    
    def get_nodes_by_domain(self, domain: str) -> List[CausalNode]:
        """Get all nodes in a domain"""
        node_ids = self._nodes_by_domain.get(domain, set())
        return [self._nodes[nid] for nid in node_ids if nid in self._nodes]
    
    def search_nodes(
        self,
        query: str = None,
        domain: str = None,
        status: VerificationStatus = None,
        min_reproducibility: float = None,
    ) -> List[CausalNode]:
        """Search nodes with filters"""
        results = list(self._nodes.values())
        
        if domain:
            results = [n for n in results if n.domain == domain]
        
        if status:
            results = [n for n in results if n.status == status]
        
        if min_reproducibility is not None:
            results = [n for n in results if n.reproducibility_score >= min_reproducibility]
        
        if query:
            query_lower = query.lower()
            results = [
                n for n in results
                if query_lower in n.title.lower() or
                query_lower in n.description.lower() or
                any(query_lower in kw.lower() for kw in n.keywords)
            ]
        
        return results
    
    # =========================================================================
    # LINK MANAGEMENT
    # =========================================================================
    
    def add_link(
        self,
        source_id: str,
        target_id: str,
        p_value: float,
        effect_size: float,
        sources: List[str] = None,
        reproducibility_score: float = 0.0,
    ) -> Optional[CausalLink]:
        """
        Add a causal link between nodes.
        
        Per spec: Lien = Preuve causale (p-value, source, reproductibilité)
        """
        if source_id not in self._nodes or target_id not in self._nodes:
            logger.error(f"Cannot create link: source or target not found")
            return None
        
        link = CausalLink(
            link_id=generate_id(),
            source_id=source_id,
            target_id=target_id,
            p_value=p_value,
            effect_size=effect_size,
            sources=sources or [],
            reproducibility_score=reproducibility_score,
        )
        
        # Compute strength (updates XR color/thickness)
        link.compute_strength()
        
        # Store
        self._links[link.link_id] = link
        
        # Index
        if source_id not in self._links_by_source:
            self._links_by_source[source_id] = set()
        self._links_by_source[source_id].add(link.link_id)
        
        if target_id not in self._links_by_target:
            self._links_by_target[target_id] = set()
        self._links_by_target[target_id].add(link.link_id)
        
        logger.info(
            f"Added causal link {link.link_id}: "
            f"{source_id} -> {target_id} (p={p_value}, strength={link.strength.value})"
        )
        
        return link
    
    def get_link(self, link_id: str) -> Optional[CausalLink]:
        """Get link by ID"""
        return self._links.get(link_id)
    
    def get_links_from(self, node_id: str) -> List[CausalLink]:
        """Get all links originating from a node"""
        link_ids = self._links_by_source.get(node_id, set())
        return [self._links[lid] for lid in link_ids if lid in self._links]
    
    def get_links_to(self, node_id: str) -> List[CausalLink]:
        """Get all links pointing to a node"""
        link_ids = self._links_by_target.get(node_id, set())
        return [self._links[lid] for lid in link_ids if lid in self._links]
    
    def verify_link(
        self,
        link_id: str,
        verifier_id: str,
        signature: str,
    ) -> bool:
        """
        Verify a causal link.
        
        Per spec: Liaisons validées via OPA + Reproducibility Worker
        """
        link = self._links.get(link_id)
        if not link:
            return False
        
        link.verified = True
        link.signed_by = verifier_id
        link.signature = signature
        
        logger.info(f"Link {link_id} verified by {verifier_id}")
        return True
    
    # =========================================================================
    # GRAPH TRAVERSAL
    # =========================================================================
    
    def get_causal_path(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 5,
    ) -> Optional[List[str]]:
        """Find causal path between two nodes (BFS)"""
        if source_id not in self._nodes or target_id not in self._nodes:
            return None
        
        visited = {source_id}
        queue = [(source_id, [source_id])]
        
        while queue:
            current, path = queue.pop(0)
            
            if current == target_id:
                return path
            
            if len(path) >= max_depth:
                continue
            
            for link in self.get_links_from(current):
                next_node = link.target_id
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append((next_node, path + [next_node]))
        
        return None
    
    def get_causal_neighborhood(
        self,
        node_id: str,
        depth: int = 2,
    ) -> Tuple[List[CausalNode], List[CausalLink]]:
        """Get nodes and links within N hops of a node"""
        if node_id not in self._nodes:
            return [], []
        
        visited_nodes = {node_id}
        collected_links = set()
        frontier = {node_id}
        
        for _ in range(depth):
            new_frontier = set()
            
            for nid in frontier:
                # Outgoing links
                for link in self.get_links_from(nid):
                    collected_links.add(link.link_id)
                    if link.target_id not in visited_nodes:
                        visited_nodes.add(link.target_id)
                        new_frontier.add(link.target_id)
                
                # Incoming links
                for link in self.get_links_to(nid):
                    collected_links.add(link.link_id)
                    if link.source_id not in visited_nodes:
                        visited_nodes.add(link.source_id)
                        new_frontier.add(link.source_id)
            
            frontier = new_frontier
        
        nodes = [self._nodes[nid] for nid in visited_nodes if nid in self._nodes]
        links = [self._links[lid] for lid in collected_links if lid in self._links]
        
        return nodes, links
    
    def get_strongest_causes(
        self,
        node_id: str,
        top_n: int = 5,
    ) -> List[Tuple[CausalNode, CausalLink]]:
        """Get the strongest causal predecessors of a node"""
        incoming = self.get_links_to(node_id)
        
        # Sort by effect size * (1 - p_value)
        scored = [
            (link, link.effect_size * (1 - link.p_value))
            for link in incoming
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for link, _ in scored[:top_n]:
            source_node = self._nodes.get(link.source_id)
            if source_node:
                results.append((source_node, link))
        
        return results
    
    # =========================================================================
    # XR EXPORT
    # =========================================================================
    
    def export_for_xr(
        self,
        domain_filter: str = None,
        min_strength: CausalLinkStrength = None,
    ) -> Dict[str, Any]:
        """
        Export graph data for XR visualization.
        
        Per spec UX: Explorateur de graphes 3D (WebXR)
        """
        nodes = list(self._nodes.values())
        links = list(self._links.values())
        
        if domain_filter:
            node_ids = self._nodes_by_domain.get(domain_filter, set())
            nodes = [n for n in nodes if n.node_id in node_ids]
            links = [l for l in links if l.source_id in node_ids and l.target_id in node_ids]
        
        if min_strength:
            strength_order = [
                CausalLinkStrength.WEAK,
                CausalLinkStrength.MODERATE,
                CausalLinkStrength.STRONG,
                CausalLinkStrength.VERY_STRONG,
            ]
            min_idx = strength_order.index(min_strength)
            links = [l for l in links if strength_order.index(l.strength) >= min_idx]
        
        return {
            "schema_version": "v1",
            "type": "causal_knowledge_graph",
            "nodes": [
                {
                    "id": n.node_id,
                    "title": n.title,
                    "domain": n.domain,
                    "position": n.xr_position,
                    "status": n.status.value,
                    "reproducibility": n.reproducibility_score,
                }
                for n in nodes
            ],
            "links": [
                {
                    "id": l.link_id,
                    "source": l.source_id,
                    "target": l.target_id,
                    "strength": l.strength.value,
                    "color": l.xr_color,
                    "thickness": l.xr_thickness,
                    "verified": l.verified,
                }
                for l in links
            ],
            "metadata": {
                "total_nodes": len(nodes),
                "total_links": len(links),
                "domains": list(self._nodes_by_domain.keys()),
            },
        }
    
    # =========================================================================
    # TIMELINE
    # =========================================================================
    
    def get_causal_timeline(
        self,
        node_id: str,
        direction: str = "backward",  # backward = causes, forward = effects
    ) -> List[Tuple[CausalNode, datetime, int]]:
        """
        Get causal timeline for a discovery.
        
        Per spec: Timeline causale
        """
        results = []
        visited = set()
        
        def traverse(current_id: str, depth: int):
            if current_id in visited:
                return
            visited.add(current_id)
            
            node = self._nodes.get(current_id)
            if node:
                results.append((node, node.created_at, depth))
            
            if direction == "backward":
                for link in self.get_links_to(current_id):
                    traverse(link.source_id, depth + 1)
            else:
                for link in self.get_links_from(current_id):
                    traverse(link.target_id, depth + 1)
        
        traverse(node_id, 0)
        
        # Sort by date
        results.sort(key=lambda x: x[1])
        return results
    
    # =========================================================================
    # STATS
    # =========================================================================
    
    def get_stats(self) -> Dict[str, Any]:
        """Get graph statistics"""
        verified_links = sum(1 for l in self._links.values() if l.verified)
        verified_nodes = sum(1 for n in self._nodes.values() if n.status == VerificationStatus.VERIFIED)
        
        return {
            "total_nodes": len(self._nodes),
            "total_links": len(self._links),
            "verified_links": verified_links,
            "verified_nodes": verified_nodes,
            "domains": list(self._nodes_by_domain.keys()),
            "domain_counts": {
                domain: len(nodes)
                for domain, nodes in self._nodes_by_domain.items()
            },
            "strength_distribution": {
                s.value: sum(1 for l in self._links.values() if l.strength == s)
                for s in CausalLinkStrength
            },
        }


# ============================================================================
# SPLIT-VIEW ANALYZER
# ============================================================================

class SplitViewAnalyzer:
    """
    Analyze analogies between domains.
    
    Per spec: Split-view analogique (biologie ↔ ingénierie)
    """
    
    def __init__(self, graph: CausalKnowledgeGraph):
        self.graph = graph
    
    def find_analogies(
        self,
        domain_a: str,
        domain_b: str,
        min_similarity: float = 0.7,
    ) -> List[Dict[str, Any]]:
        """Find structural analogies between two domains"""
        nodes_a = self.graph.get_nodes_by_domain(domain_a)
        nodes_b = self.graph.get_nodes_by_domain(domain_b)
        
        analogies = []
        
        for node_a in nodes_a:
            for node_b in nodes_b:
                similarity = self._compute_structural_similarity(node_a, node_b)
                
                if similarity >= min_similarity:
                    analogies.append({
                        "node_a": node_a.node_id,
                        "node_b": node_b.node_id,
                        "title_a": node_a.title,
                        "title_b": node_b.title,
                        "similarity": similarity,
                    })
        
        # Sort by similarity
        analogies.sort(key=lambda x: x["similarity"], reverse=True)
        return analogies
    
    def _compute_structural_similarity(
        self,
        node_a: CausalNode,
        node_b: CausalNode,
    ) -> float:
        """Compute structural similarity between two nodes"""
        # Get neighborhoods
        nodes_a, links_a = self.graph.get_causal_neighborhood(node_a.node_id, depth=2)
        nodes_b, links_b = self.graph.get_causal_neighborhood(node_b.node_id, depth=2)
        
        # Compare structures
        in_degree_a = len(self.graph.get_links_to(node_a.node_id))
        out_degree_a = len(self.graph.get_links_from(node_a.node_id))
        in_degree_b = len(self.graph.get_links_to(node_b.node_id))
        out_degree_b = len(self.graph.get_links_from(node_b.node_id))
        
        # Jaccard-like similarity on degree
        degree_sim = 1 - abs(
            (in_degree_a + out_degree_a) - (in_degree_b + out_degree_b)
        ) / max(in_degree_a + out_degree_a + in_degree_b + out_degree_b, 1)
        
        # Keyword overlap
        keywords_a = set(node_a.keywords)
        keywords_b = set(node_b.keywords)
        
        if keywords_a or keywords_b:
            keyword_sim = len(keywords_a & keywords_b) / len(keywords_a | keywords_b)
        else:
            keyword_sim = 0
        
        # Combined similarity
        return 0.7 * degree_sim + 0.3 * keyword_sim


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_knowledge_graph() -> CausalKnowledgeGraph:
    """Create a causal knowledge graph"""
    return CausalKnowledgeGraph()


def create_split_view_analyzer(graph: CausalKnowledgeGraph) -> SplitViewAnalyzer:
    """Create a split-view analyzer"""
    return SplitViewAnalyzer(graph)
