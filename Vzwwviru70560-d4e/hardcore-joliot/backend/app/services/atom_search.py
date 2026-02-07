"""
═══════════════════════════════════════════════════════════════════════════════
AT·OM UNITARY SEARCH — Recherche Bidirectionnelle par Unitarité
═══════════════════════════════════════════════════════════════════════════════

Principe d'Unitarité appliqué au graphe AT·OM:
- Toute relation cause→effet peut être inversée
- La recherche peut partir du résultat pour remonter aux causes
- L'information se conserve dans les deux directions

Flux Normal (Descente):     CAUSE ──────► EFFET
Flux Inverse (Unitarité):   CAUSE ◄────── EFFET

Ce service permet:
1. Recherche descendante (trouver les effets d'une cause)
2. Recherche ascendante (trouver les causes d'un effet)
3. Recherche bidirectionnelle (explorer le graphe complet)
4. Recherche par fréquence harmonique (via harmonic_signatures)

═══════════════════════════════════════════════════════════════════════════════
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Set, Tuple
from uuid import UUID
from enum import Enum
from dataclasses import dataclass, field
import logging

from sqlalchemy import select, and_, or_, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

logger = logging.getLogger("atom.search")


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS & TYPES
# ═══════════════════════════════════════════════════════════════════════════════

class SearchDirection(str, Enum):
    """Direction de recherche dans le graphe causal."""
    FORWARD = "forward"      # Cause → Effet (descente)
    BACKWARD = "backward"    # Effet → Cause (unitarité/remontée)
    BOTH = "both"           # Bidirectionnel


class LinkType(str, Enum):
    """Types de liens causaux."""
    BIO = "BIO"
    TECH = "TECH"
    SOCIAL = "SOCIAL"
    SPIRITUAL = "SPIRITUAL"
    ECO = "ECO"
    SENSORY = "SENSORY"
    CONCEPT = "CONCEPT"
    LOGISTICS = "LOGISTICS"


class Dimension(str, Enum):
    """Dimensions du graphe."""
    PHYSICAL = "PHYSICAL"
    BIOLOGICAL = "BIOLOGICAL"
    SOCIAL = "SOCIAL"
    SPIRITUAL = "SPIRITUAL"
    CONCEPTUAL = "CONCEPTUAL"
    ECOLOGICAL = "ECOLOGICAL"
    LOGISTICAL = "LOGISTICAL"
    SENSORY = "SENSORY"


@dataclass
class SearchResult:
    """Résultat de recherche avec métadonnées."""
    node_id: UUID
    name: str
    dimension: Optional[str]
    epoch: Optional[str]

    # Contexte de recherche
    distance: int = 0  # Distance depuis le nœud source
    direction: str = "forward"  # forward ou backward
    path: List[UUID] = field(default_factory=list)

    # Scores
    relevance_score: float = 1.0
    confidence: float = 0.5

    # Liens
    link_type: Optional[str] = None
    link_strength: float = 1.0


@dataclass
class CausalChain:
    """Chaîne causale complète (histoire)."""
    origin: SearchResult
    chain: List[SearchResult]
    total_strength: float = 1.0
    direction: str = "forward"

    def reverse(self) -> "CausalChain":
        """Inverse la chaîne (unitarité)."""
        reversed_chain = list(reversed(self.chain))
        return CausalChain(
            origin=reversed_chain[0] if reversed_chain else self.origin,
            chain=reversed_chain,
            total_strength=self.total_strength,
            direction="backward" if self.direction == "forward" else "forward"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# UNITARY SEARCH SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

class AtomUnitarySearch:
    """
    Service de recherche unitaire dans le graphe AT·OM.

    Implémente le principe d'unitarité:
    - Chaque recherche peut être inversée
    - L'information ne se perd jamais
    - On peut remonter l'histoire depuis n'importe quel point
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    # ═══════════════════════════════════════════════════════════════════════════
    # RECHERCHE PAR MOT-CLÉ (Rapide)
    # ═══════════════════════════════════════════════════════════════════════════

    async def quick_search(
        self,
        query: str,
        limit: int = 20,
        dimension: Optional[Dimension] = None,
        epoch: Optional[str] = None,
    ) -> List[SearchResult]:
        """
        Recherche rapide par mot-clé.

        Utilise un index trigram pour la recherche floue.
        """
        # Import ici pour éviter les imports circulaires
        from app.models.atom_mapping import ATOMNode

        # Construire la requête
        stmt = select(ATOMNode).where(
            or_(
                ATOMNode.name.ilike(f"%{query}%"),
                ATOMNode.description.ilike(f"%{query}%"),
            )
        )

        # Filtres optionnels
        if dimension:
            stmt = stmt.where(ATOMNode.dimension == dimension.value)
        if epoch:
            stmt = stmt.where(ATOMNode.epoch.ilike(f"%{epoch}%"))

        # Limiter et exécuter
        stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        nodes = result.scalars().all()

        # Convertir en SearchResult
        return [
            SearchResult(
                node_id=node.id,
                name=node.name,
                dimension=node.dimension,
                epoch=node.epoch,
                relevance_score=self._calculate_relevance(query, node.name),
            )
            for node in nodes
        ]

    def _calculate_relevance(self, query: str, name: str) -> float:
        """Calcule un score de pertinence simple."""
        query_lower = query.lower()
        name_lower = name.lower()

        if query_lower == name_lower:
            return 1.0
        elif query_lower in name_lower:
            return 0.8
        elif name_lower in query_lower:
            return 0.6
        else:
            return 0.4

    # ═══════════════════════════════════════════════════════════════════════════
    # RECHERCHE CAUSALE (Forward/Backward)
    # ═══════════════════════════════════════════════════════════════════════════

    async def find_effects(
        self,
        node_id: UUID,
        depth: int = 3,
        link_types: Optional[List[LinkType]] = None,
        min_strength: float = 0.0,
    ) -> List[SearchResult]:
        """
        Recherche DESCENDANTE: trouve les effets d'une cause.

        Suit les liens: trigger_id → result_id
        """
        return await self._traverse_graph(
            start_id=node_id,
            direction=SearchDirection.FORWARD,
            depth=depth,
            link_types=link_types,
            min_strength=min_strength,
        )

    async def find_causes(
        self,
        node_id: UUID,
        depth: int = 3,
        link_types: Optional[List[LinkType]] = None,
        min_strength: float = 0.0,
    ) -> List[SearchResult]:
        """
        Recherche ASCENDANTE (Unitarité): trouve les causes d'un effet.

        Suit les liens INVERSÉS: result_id → trigger_id

        C'est ici qu'on "renverse l'histoire"!
        """
        return await self._traverse_graph(
            start_id=node_id,
            direction=SearchDirection.BACKWARD,
            depth=depth,
            link_types=link_types,
            min_strength=min_strength,
        )

    async def explore_both(
        self,
        node_id: UUID,
        depth: int = 2,
    ) -> Dict[str, List[SearchResult]]:
        """
        Exploration BIDIRECTIONNELLE: causes ET effets.

        Retourne un contexte complet autour d'un nœud.
        """
        causes = await self.find_causes(node_id, depth)
        effects = await self.find_effects(node_id, depth)

        return {
            "causes": causes,
            "effects": effects,
            "total_connections": len(causes) + len(effects),
        }

    async def _traverse_graph(
        self,
        start_id: UUID,
        direction: SearchDirection,
        depth: int,
        link_types: Optional[List[LinkType]] = None,
        min_strength: float = 0.0,
    ) -> List[SearchResult]:
        """
        Traverse le graphe dans une direction donnée.

        Utilise BFS (Breadth-First Search) pour explorer par niveaux.
        """
        from app.models.atom_mapping import ATOMNode, atom_causal_links

        visited: Set[UUID] = set()
        results: List[SearchResult] = []
        current_level: Set[UUID] = {start_id}
        current_depth = 0
        paths: Dict[UUID, List[UUID]] = {start_id: [start_id]}

        while current_level and current_depth < depth:
            next_level: Set[UUID] = set()

            for node_id in current_level:
                if node_id in visited:
                    continue
                visited.add(node_id)

                # Requête selon la direction
                if direction == SearchDirection.FORWARD:
                    # Cause → Effet
                    stmt = select(
                        atom_causal_links.c.result_id,
                        atom_causal_links.c.link_type,
                        atom_causal_links.c.strength,
                        atom_causal_links.c.confidence,
                    ).where(
                        atom_causal_links.c.trigger_id == node_id
                    )
                else:
                    # Effet → Cause (UNITARITÉ)
                    stmt = select(
                        atom_causal_links.c.trigger_id,
                        atom_causal_links.c.link_type,
                        atom_causal_links.c.strength,
                        atom_causal_links.c.confidence,
                    ).where(
                        atom_causal_links.c.result_id == node_id
                    )

                # Filtrer par type de lien
                if link_types:
                    type_values = [lt.value for lt in link_types]
                    stmt = stmt.where(
                        atom_causal_links.c.link_type.in_(type_values)
                    )

                # Filtrer par force minimale
                if min_strength > 0:
                    stmt = stmt.where(
                        atom_causal_links.c.strength >= min_strength
                    )

                result = await self.db.execute(stmt)
                links = result.fetchall()

                for link in links:
                    target_id = link[0]
                    link_type = link[1]
                    strength = link[2]
                    confidence = link[3]

                    if target_id not in visited:
                        next_level.add(target_id)

                        # Construire le chemin
                        new_path = paths.get(node_id, []) + [target_id]
                        paths[target_id] = new_path

                        # Récupérer les infos du nœud cible
                        node_stmt = select(ATOMNode).where(ATOMNode.id == target_id)
                        node_result = await self.db.execute(node_stmt)
                        target_node = node_result.scalar_one_or_none()

                        if target_node:
                            results.append(SearchResult(
                                node_id=target_id,
                                name=target_node.name,
                                dimension=target_node.dimension,
                                epoch=target_node.epoch,
                                distance=current_depth + 1,
                                direction=direction.value,
                                path=new_path,
                                link_type=link_type,
                                link_strength=strength,
                                confidence=confidence,
                            ))

            current_level = next_level
            current_depth += 1

        # Trier par distance puis par force
        results.sort(key=lambda r: (r.distance, -r.link_strength))

        return results

    # ═══════════════════════════════════════════════════════════════════════════
    # RECHERCHE PAR CHAÎNE CAUSALE
    # ═══════════════════════════════════════════════════════════════════════════

    async def find_causal_chain(
        self,
        from_id: UUID,
        to_id: UUID,
        max_depth: int = 5,
    ) -> Optional[CausalChain]:
        """
        Trouve une chaîne causale entre deux nœuds.

        Utilise BFS bidirectionnel pour optimiser.
        """
        from app.models.atom_mapping import ATOMNode, atom_causal_links

        # BFS depuis les deux extrémités
        forward_visited: Dict[UUID, List[UUID]] = {from_id: [from_id]}
        backward_visited: Dict[UUID, List[UUID]] = {to_id: [to_id]}

        forward_frontier: Set[UUID] = {from_id}
        backward_frontier: Set[UUID] = {to_id}

        for depth in range(max_depth):
            # Expansion forward
            new_forward: Set[UUID] = set()
            for node_id in forward_frontier:
                stmt = select(atom_causal_links.c.result_id).where(
                    atom_causal_links.c.trigger_id == node_id
                )
                result = await self.db.execute(stmt)

                for (next_id,) in result:
                    if next_id not in forward_visited:
                        forward_visited[next_id] = forward_visited[node_id] + [next_id]
                        new_forward.add(next_id)

                        # Vérifier intersection
                        if next_id in backward_visited:
                            # Chemin trouvé!
                            full_path = forward_visited[next_id] + backward_visited[next_id][::-1][1:]
                            return await self._build_chain(full_path)

            forward_frontier = new_forward

            # Expansion backward
            new_backward: Set[UUID] = set()
            for node_id in backward_frontier:
                stmt = select(atom_causal_links.c.trigger_id).where(
                    atom_causal_links.c.result_id == node_id
                )
                result = await self.db.execute(stmt)

                for (prev_id,) in result:
                    if prev_id not in backward_visited:
                        backward_visited[prev_id] = backward_visited[node_id] + [prev_id]
                        new_backward.add(prev_id)

                        # Vérifier intersection
                        if prev_id in forward_visited:
                            full_path = forward_visited[prev_id] + backward_visited[prev_id][::-1][1:]
                            return await self._build_chain(full_path)

            backward_frontier = new_backward

        return None  # Pas de chemin trouvé

    async def _build_chain(self, path: List[UUID]) -> CausalChain:
        """Construit une CausalChain depuis un chemin."""
        from app.models.atom_mapping import ATOMNode

        results = []
        for i, node_id in enumerate(path):
            stmt = select(ATOMNode).where(ATOMNode.id == node_id)
            result = await self.db.execute(stmt)
            node = result.scalar_one_or_none()

            if node:
                results.append(SearchResult(
                    node_id=node_id,
                    name=node.name,
                    dimension=node.dimension,
                    epoch=node.epoch,
                    distance=i,
                    path=path[:i+1],
                ))

        return CausalChain(
            origin=results[0] if results else None,
            chain=results,
            direction="forward",
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # RECHERCHE PAR FRÉQUENCE HARMONIQUE
    # ═══════════════════════════════════════════════════════════════════════════

    async def find_by_harmonic(
        self,
        frequency: int,
        tolerance: int = 10,
        limit: int = 20,
    ) -> List[SearchResult]:
        """
        Recherche par signature harmonique.

        Trouve les nœuds dont la vibration correspond à une fréquence.

        Fréquences Sephiroth:
        - 999 Hz: Kether (Source)
        - 888 Hz: Chokmah
        - 777 Hz: Binah
        - 666 Hz: Netzach
        - 555 Hz: Chesed
        - 444 Hz: Tiphereth (Point 0)
        - 333 Hz: Geburah
        - 222 Hz: Hod
        - 111 Hz: Yesod
        - 68 Hz: Malkuth
        """
        from app.models.atom_mapping import ATOMNode, AtomHarmonicSignature

        # Recherche dans les signatures harmoniques
        stmt = select(AtomHarmonicSignature).where(
            AtomHarmonicSignature.numeric_signatures.contains(
                {"base_frequency": frequency}
            )
        ).limit(limit)

        # Note: Cette requête JSONB peut nécessiter un index GIN
        # Pour l'instant, fallback sur une recherche plus basique

        result = await self.db.execute(stmt)
        signatures = result.scalars().all()

        results = []
        for sig in signatures:
            node_stmt = select(ATOMNode).where(ATOMNode.id == sig.node_id)
            node_result = await self.db.execute(node_stmt)
            node = node_result.scalar_one_or_none()

            if node:
                results.append(SearchResult(
                    node_id=node.id,
                    name=node.name,
                    dimension=node.dimension,
                    epoch=node.epoch,
                    relevance_score=sig.confidence,
                ))

        return results

    # ═══════════════════════════════════════════════════════════════════════════
    # INVERSION TEMPORELLE (UNITARITÉ COMPLÈTE)
    # ═══════════════════════════════════════════════════════════════════════════

    async def reverse_history(
        self,
        node_id: UUID,
        depth: int = 10,
    ) -> CausalChain:
        """
        RENVERSE L'HISTOIRE depuis un point donné.

        Remonte toute la chaîne causale jusqu'à l'origine.

        C'est l'implémentation pure du principe d'unitarité:
        depuis n'importe quel effet, on peut reconstruire
        toutes les causes qui y ont mené.
        """
        causes = await self.find_causes(node_id, depth=depth)

        # Trier par distance (plus loin = plus ancien)
        causes.sort(key=lambda c: -c.distance)

        # Construire la chaîne inversée
        # L'origine est la cause la plus lointaine
        if causes:
            origin = causes[-1]  # Plus ancienne cause
            chain = list(reversed(causes))  # Du plus ancien au plus récent
        else:
            # Pas de causes trouvées, le nœud est l'origine
            from app.models.atom_mapping import ATOMNode
            stmt = select(ATOMNode).where(ATOMNode.id == node_id)
            result = await self.db.execute(stmt)
            node = result.scalar_one_or_none()

            origin = SearchResult(
                node_id=node_id,
                name=node.name if node else "Unknown",
                dimension=node.dimension if node else None,
                epoch=node.epoch if node else None,
            )
            chain = [origin]

        return CausalChain(
            origin=origin,
            chain=chain,
            direction="backward",
        )


# ═══════════════════════════════════════════════════════════════════════════════
# FACTORY FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def get_atom_search(db: AsyncSession) -> AtomUnitarySearch:
    """Factory pour créer le service de recherche."""
    return AtomUnitarySearch(db)


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "AtomUnitarySearch",
    "get_atom_search",
    "SearchDirection",
    "SearchResult",
    "CausalChain",
    "LinkType",
    "Dimension",
]
