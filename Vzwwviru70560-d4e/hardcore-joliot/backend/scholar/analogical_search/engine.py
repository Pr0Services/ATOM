"""
============================================================================
CHE·NU™ V69 — SCHOLAR ANALOGICAL SEARCH ENGINE
============================================================================
Spec: GPT1/CHE-NU_SCH_ANALOGICAL_SEARCH_ENGINE.md

Principle: Identify mathematically equivalent problems.

Steps (per spec):
- Extraction topologique
- Pattern matching (>85%)
- Suggestions transversales

UX: Recherche par pattern, pas par domaine.
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
import logging
import hashlib
import math

from ..models import (
    TopologicalPattern,
    AnalogicalMatch,
    CausalNode,
    CausalLink,
    generate_id,
)

logger = logging.getLogger(__name__)


# ============================================================================
# PATTERN EXTRACTOR
# ============================================================================

class TopologicalExtractor:
    """
    Extract topological patterns from causal structures.
    
    Per spec: Extraction topologique
    """
    
    def __init__(self):
        self._pattern_cache: Dict[str, TopologicalPattern] = {}
    
    def extract_pattern(
        self,
        nodes: List[CausalNode],
        links: List[CausalLink],
        source_domain: str = "",
    ) -> TopologicalPattern:
        """Extract topological pattern from a subgraph"""
        pattern_id = generate_id()
        
        # Build adjacency info
        node_ids = {n.node_id for n in nodes}
        in_degree = {nid: 0 for nid in node_ids}
        out_degree = {nid: 0 for nid in node_ids}
        
        for link in links:
            if link.source_id in node_ids:
                out_degree[link.source_id] += 1
            if link.target_id in node_ids:
                in_degree[link.target_id] += 1
        
        # Compute structural features
        features = {
            "node_count": len(nodes),
            "edge_count": len(links),
            "avg_in_degree": sum(in_degree.values()) / max(len(nodes), 1),
            "avg_out_degree": sum(out_degree.values()) / max(len(nodes), 1),
            "max_in_degree": max(in_degree.values()) if in_degree else 0,
            "max_out_degree": max(out_degree.values()) if out_degree else 0,
            "source_count": sum(1 for d in in_degree.values() if d == 0),  # Nodes with no incoming
            "sink_count": sum(1 for d in out_degree.values() if d == 0),  # Nodes with no outgoing
            "density": len(links) / max(len(nodes) * (len(nodes) - 1), 1),
        }
        
        # Compute structure hash (for quick comparison)
        degree_sequence = sorted([
            (in_degree.get(nid, 0), out_degree.get(nid, 0))
            for nid in node_ids
        ])
        structure_hash = hashlib.sha256(
            str(degree_sequence).encode()
        ).hexdigest()[:16]
        
        pattern = TopologicalPattern(
            pattern_id=pattern_id,
            name=f"pattern_{pattern_id[:8]}",
            node_count=len(nodes),
            edge_count=len(links),
            structure_hash=structure_hash,
            features=features,
            source_domain=source_domain,
        )
        
        self._pattern_cache[pattern_id] = pattern
        return pattern
    
    def get_pattern(self, pattern_id: str) -> Optional[TopologicalPattern]:
        """Get cached pattern"""
        return self._pattern_cache.get(pattern_id)


# ============================================================================
# PATTERN MATCHER
# ============================================================================

class PatternMatcher:
    """
    Match patterns across domains.
    
    Per spec: Pattern matching (>85%)
    """
    
    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
    
    def compute_similarity(
        self,
        pattern_a: TopologicalPattern,
        pattern_b: TopologicalPattern,
    ) -> float:
        """Compute similarity between two patterns"""
        features_a = pattern_a.features
        features_b = pattern_b.features
        
        # Feature-based similarity
        feature_similarities = []
        
        for key in features_a.keys():
            if key in features_b:
                val_a = features_a[key]
                val_b = features_b[key]
                
                if val_a == 0 and val_b == 0:
                    sim = 1.0
                else:
                    max_val = max(abs(val_a), abs(val_b), 1)
                    sim = 1 - abs(val_a - val_b) / max_val
                
                feature_similarities.append(sim)
        
        # Average feature similarity
        if not feature_similarities:
            return 0.0
        
        feature_sim = sum(feature_similarities) / len(feature_similarities)
        
        # Structure hash bonus (exact match = +0.1)
        hash_bonus = 0.1 if pattern_a.structure_hash == pattern_b.structure_hash else 0
        
        return min(feature_sim + hash_bonus, 1.0)
    
    def find_matches(
        self,
        query_pattern: TopologicalPattern,
        candidate_patterns: List[TopologicalPattern],
        top_n: int = 10,
    ) -> List[AnalogicalMatch]:
        """
        Find matching patterns.
        
        Per spec: Pattern matching (>85%)
        """
        matches = []
        
        for candidate in candidate_patterns:
            # Skip same pattern
            if candidate.pattern_id == query_pattern.pattern_id:
                continue
            
            similarity = self.compute_similarity(query_pattern, candidate)
            
            if similarity >= self.similarity_threshold:
                match = AnalogicalMatch(
                    match_id=generate_id(),
                    pattern_a=query_pattern.pattern_id,
                    pattern_b=candidate.pattern_id,
                    similarity_score=similarity,
                    matched_features=self._get_matched_features(query_pattern, candidate),
                    domain_a=query_pattern.source_domain,
                    domain_b=candidate.source_domain,
                    mapping_explanation=self._generate_explanation(query_pattern, candidate, similarity),
                )
                matches.append(match)
        
        # Sort by similarity
        matches.sort(key=lambda m: m.similarity_score, reverse=True)
        return matches[:top_n]
    
    def _get_matched_features(
        self,
        pattern_a: TopologicalPattern,
        pattern_b: TopologicalPattern,
    ) -> List[str]:
        """Get list of well-matched features"""
        matched = []
        
        for key in pattern_a.features.keys():
            if key in pattern_b.features:
                val_a = pattern_a.features[key]
                val_b = pattern_b.features[key]
                
                max_val = max(abs(val_a), abs(val_b), 1)
                sim = 1 - abs(val_a - val_b) / max_val
                
                if sim >= 0.9:
                    matched.append(key)
        
        return matched
    
    def _generate_explanation(
        self,
        pattern_a: TopologicalPattern,
        pattern_b: TopologicalPattern,
        similarity: float,
    ) -> str:
        """Generate human-readable explanation"""
        explanations = []
        
        if pattern_a.node_count == pattern_b.node_count:
            explanations.append(f"Same number of nodes ({pattern_a.node_count})")
        
        if pattern_a.edge_count == pattern_b.edge_count:
            explanations.append(f"Same number of edges ({pattern_a.edge_count})")
        
        if pattern_a.structure_hash == pattern_b.structure_hash:
            explanations.append("Identical topological structure")
        
        if pattern_a.source_domain != pattern_b.source_domain:
            explanations.append(
                f"Cross-domain match: {pattern_a.source_domain} ↔ {pattern_b.source_domain}"
            )
        
        return f"Similarity: {similarity:.1%}. " + "; ".join(explanations)


# ============================================================================
# ANALOGICAL SEARCH ENGINE
# ============================================================================

class AnalogicalSearchEngine:
    """
    Search engine for finding structural analogies.
    
    Per spec UX: Recherche par pattern, pas par domaine
    """
    
    def __init__(
        self,
        similarity_threshold: float = 0.85,
    ):
        self.extractor = TopologicalExtractor()
        self.matcher = PatternMatcher(similarity_threshold)
        
        # Pattern library
        self._patterns: Dict[str, TopologicalPattern] = {}
        self._patterns_by_domain: Dict[str, Set[str]] = {}
    
    def index_pattern(
        self,
        nodes: List[CausalNode],
        links: List[CausalLink],
        domain: str,
        name: str = None,
    ) -> TopologicalPattern:
        """Extract and index a pattern"""
        pattern = self.extractor.extract_pattern(nodes, links, domain)
        
        if name:
            pattern.name = name
        
        self._patterns[pattern.pattern_id] = pattern
        
        if domain not in self._patterns_by_domain:
            self._patterns_by_domain[domain] = set()
        self._patterns_by_domain[domain].add(pattern.pattern_id)
        
        logger.info(f"Indexed pattern {pattern.pattern_id} from domain {domain}")
        return pattern
    
    def search(
        self,
        query_nodes: List[CausalNode],
        query_links: List[CausalLink],
        exclude_domain: str = None,
        top_n: int = 10,
    ) -> List[AnalogicalMatch]:
        """
        Search for analogous patterns.
        
        Per spec: Suggestions transversales
        """
        # Extract query pattern
        query_pattern = self.extractor.extract_pattern(query_nodes, query_links)
        
        # Get candidate patterns
        candidates = list(self._patterns.values())
        
        if exclude_domain:
            candidates = [
                p for p in candidates
                if p.source_domain != exclude_domain
            ]
        
        # Find matches
        matches = self.matcher.find_matches(query_pattern, candidates, top_n)
        
        logger.info(f"Found {len(matches)} analogical matches")
        return matches
    
    def search_by_pattern_id(
        self,
        pattern_id: str,
        exclude_same_domain: bool = True,
        top_n: int = 10,
    ) -> List[AnalogicalMatch]:
        """Search using an existing pattern"""
        query_pattern = self._patterns.get(pattern_id)
        if not query_pattern:
            return []
        
        candidates = list(self._patterns.values())
        
        if exclude_same_domain:
            candidates = [
                p for p in candidates
                if p.source_domain != query_pattern.source_domain
            ]
        
        return self.matcher.find_matches(query_pattern, candidates, top_n)
    
    def get_cross_domain_suggestions(
        self,
        domain: str,
        top_n_per_pattern: int = 3,
    ) -> Dict[str, List[AnalogicalMatch]]:
        """
        Get cross-domain suggestions for all patterns in a domain.
        
        Per spec: Suggestions transversales
        """
        pattern_ids = self._patterns_by_domain.get(domain, set())
        suggestions = {}
        
        for pid in pattern_ids:
            matches = self.search_by_pattern_id(
                pid,
                exclude_same_domain=True,
                top_n=top_n_per_pattern,
            )
            if matches:
                suggestions[pid] = matches
        
        return suggestions
    
    def get_stats(self) -> Dict[str, Any]:
        """Get search engine statistics"""
        return {
            "total_patterns": len(self._patterns),
            "domains": list(self._patterns_by_domain.keys()),
            "patterns_per_domain": {
                d: len(pids) for d, pids in self._patterns_by_domain.items()
            },
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_extractor() -> TopologicalExtractor:
    """Create a topological extractor"""
    return TopologicalExtractor()


def create_matcher(threshold: float = 0.85) -> PatternMatcher:
    """Create a pattern matcher"""
    return PatternMatcher(threshold)


def create_search_engine(threshold: float = 0.85) -> AnalogicalSearchEngine:
    """Create an analogical search engine"""
    return AnalogicalSearchEngine(threshold)
