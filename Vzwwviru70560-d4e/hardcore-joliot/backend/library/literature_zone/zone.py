"""
============================================================================
CHE·NU™ V69 — LIBRARY UNIVERSAL LITERATURE ZONE (ULZ)
============================================================================
Spec: GPT1/CHE-NU_LIB_UNIVERSAL_LITERATURE_ZONE.md

Concept: La Littera-Lattice - Un livre n'est plus un PDF mort, mais un
organisme culturel connecté.

Features:
- Creative Companion (AI collaborative, non-substitutive)
- Auto-Illustration XR (immersive reading)
- Semantic Translation (by intention, not word)
- WorldEngine connections (livre connecté)

Principle: L'IA ne remplace jamais l'auteur
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
import logging

from ..models import (
    BookArtifact,
    ChapterChunk,
    CreativeSuggestion,
    ConsistencyIssue,
    SemanticTranslation,
    SuggestionType,
    ReaderProfile,
    XRSceneManifest,
    generate_id,
    compute_hash,
    sign_artifact,
)

from ..publishing.protocol import PublishingPipeline
from ..immersive_reading.engine import ImmersiveReadingEngine
from ..author_equity.system import AuthorEquitySystem

logger = logging.getLogger(__name__)


# ============================================================================
# CREATIVE COMPANION
# ============================================================================

class CreativeCompanion:
    """
    AI collaborative assistant for authors.
    
    Per spec: L'IA ne remplace jamais l'auteur: elle agit comme compagnon de création.
    
    Features:
    - Analyse structurelle
    - Suggestions stylistiques optionnelles
    - Détection d'incohérences
    - AUCUNE réécriture automatique sans validation humaine
    """
    
    def __init__(self):
        self._suggestions: Dict[str, List[CreativeSuggestion]] = {}  # book_id → suggestions
        self._issues: Dict[str, List[ConsistencyIssue]] = {}  # book_id → issues
        
        # Character tracking for consistency
        self._characters: Dict[str, Dict[str, Dict]] = {}  # book_id → {name: attributes}
    
    def analyze_structure(self, book: BookArtifact) -> Dict[str, Any]:
        """
        Analyze book structure.
        
        Per spec: Analyse structurelle (rythme, arcs narratifs, logique interne)
        """
        chapters = book.chapters
        
        # Word count analysis
        word_counts = [c.word_count for c in chapters]
        avg_length = sum(word_counts) / len(word_counts) if word_counts else 0
        
        # Find short/long chapters
        short_chapters = [i for i, wc in enumerate(word_counts) if wc < avg_length * 0.5]
        long_chapters = [i for i, wc in enumerate(word_counts) if wc > avg_length * 1.5]
        
        return {
            "total_chapters": len(chapters),
            "total_words": sum(word_counts),
            "avg_chapter_length": avg_length,
            "short_chapters": short_chapters,
            "long_chapters": long_chapters,
            "rhythm_analysis": "balanced" if not short_chapters and not long_chapters else "varied",
        }
    
    def suggest_style(
        self,
        book_id: str,
        chunk: ChapterChunk,
    ) -> List[CreativeSuggestion]:
        """
        Generate style suggestions.
        
        Per spec: Suggestions stylistiques optionnelles
        IMPORTANT: auto_applied is ALWAYS False
        """
        suggestions = []
        text = chunk.text
        
        # Check for passive voice overuse
        passive_indicators = ["est été", "a été", "sont été", "was", "were"]
        passive_count = sum(text.lower().count(p) for p in passive_indicators)
        
        if passive_count > 5:
            suggestions.append(CreativeSuggestion(
                suggestion_id=generate_id(),
                book_id=book_id,
                chunk_id=chunk.chunk_id,
                suggestion_type=SuggestionType.STYLE,
                description="Consider reducing passive voice for more dynamic prose",
                auto_applied=False,  # NEVER auto-apply
            ))
        
        # Check for repetition
        words = text.lower().split()
        word_freq = {}
        for w in words:
            if len(w) > 5:  # Only meaningful words
                word_freq[w] = word_freq.get(w, 0) + 1
        
        repeated = [w for w, c in word_freq.items() if c > 3]
        if repeated:
            suggestions.append(CreativeSuggestion(
                suggestion_id=generate_id(),
                book_id=book_id,
                chunk_id=chunk.chunk_id,
                suggestion_type=SuggestionType.STYLE,
                description=f"Word repetition detected: {', '.join(repeated[:3])}",
                auto_applied=False,
            ))
        
        # Store suggestions
        if book_id not in self._suggestions:
            self._suggestions[book_id] = []
        self._suggestions[book_id].extend(suggestions)
        
        return suggestions
    
    def detect_inconsistencies(
        self,
        book: BookArtifact,
    ) -> List[ConsistencyIssue]:
        """
        Detect inconsistencies.
        
        Per spec: Détection d'incohérences (personnages, chronologie, concepts)
        """
        issues = []
        book_id = book.book_id
        
        # Extract character names (simplified)
        import re
        all_text = " ".join(c.text for c in book.chapters)
        
        # Find capitalized names
        potential_names = set(re.findall(r'\b[A-Z][a-z]+\b', all_text))
        
        # Track character attributes (simplified)
        for name in potential_names:
            # Find descriptions near name
            pattern = f"{name}.*?(homme|femme|grand|petit|jeune|vieux|man|woman|tall|short)"
            matches = re.findall(pattern, all_text[:5000], re.IGNORECASE)
            
            if name not in self._characters.get(book_id, {}):
                if book_id not in self._characters:
                    self._characters[book_id] = {}
                self._characters[book_id][name] = {"descriptions": matches}
        
        # Check for contradictions (simplified - would be more sophisticated in production)
        contradictions = {
            ("grand", "petit"), ("tall", "short"),
            ("jeune", "vieux"), ("young", "old"),
            ("homme", "femme"), ("man", "woman"),
        }
        
        for name, attrs in self._characters.get(book_id, {}).items():
            descs = attrs.get("descriptions", [])
            desc_set = set(d.lower() for d in descs)
            
            for contra in contradictions:
                if contra[0] in desc_set and contra[1] in desc_set:
                    issue = ConsistencyIssue(
                        issue_id=generate_id(),
                        book_id=book_id,
                        issue_type="character",
                        description=f"Possible contradiction for {name}: described as both {contra[0]} and {contra[1]}",
                    )
                    issues.append(issue)
        
        # Store issues
        if book_id not in self._issues:
            self._issues[book_id] = []
        self._issues[book_id].extend(issues)
        
        return issues
    
    def get_suggestions(self, book_id: str) -> List[CreativeSuggestion]:
        """Get all suggestions for a book"""
        return self._suggestions.get(book_id, [])
    
    def accept_suggestion(self, suggestion_id: str, book_id: str) -> bool:
        """Mark suggestion as accepted (human decision)"""
        suggestions = self._suggestions.get(book_id, [])
        for s in suggestions:
            if s.suggestion_id == suggestion_id:
                s.accepted = True
                return True
        return False
    
    def reject_suggestion(self, suggestion_id: str, book_id: str) -> bool:
        """Mark suggestion as rejected (human decision)"""
        suggestions = self._suggestions.get(book_id, [])
        for s in suggestions:
            if s.suggestion_id == suggestion_id:
                s.accepted = False
                return True
        return False


# ============================================================================
# SEMANTIC TRANSLATOR
# ============================================================================

class SemanticTranslator:
    """
    Translate by intention, not by word.
    
    Per spec: Traduction par intention, conservation du rythme, métaphores, poésie
    """
    
    # Supported languages
    LANGUAGES = ["fr", "en", "es", "de", "it", "pt", "zh", "ja", "ar", "ru"]
    
    def __init__(self):
        self._translations: Dict[str, List[SemanticTranslation]] = {}
    
    def translate(
        self,
        book_id: str,
        chunk: ChapterChunk,
        source_lang: str,
        target_lang: str,
    ) -> SemanticTranslation:
        """
        Translate chunk semantically.
        
        Per spec: Lecture instantanée en 100+ langues
        """
        # Mock translation (in production: use actual translation model)
        # The key is preserving rhythm and metaphors
        
        translated_text = f"[{target_lang.upper()}] {chunk.text[:100]}..."  # Mock
        
        translation = SemanticTranslation(
            translation_id=generate_id(),
            book_id=book_id,
            chunk_id=chunk.chunk_id,
            source_language=source_lang,
            target_language=target_lang,
            translated_text=translated_text,
            rhythm_preserved=True,
            metaphors_adapted=True,
        )
        
        # Sign translation
        translation.signature = sign_artifact({
            "translation_id": translation.translation_id,
            "source": source_lang,
            "target": target_lang,
        }, "semantic_translator")
        
        # Store
        if book_id not in self._translations:
            self._translations[book_id] = []
        self._translations[book_id].append(translation)
        
        return translation
    
    def get_translations(
        self,
        book_id: str,
        target_lang: str = None,
    ) -> List[SemanticTranslation]:
        """Get translations for a book"""
        translations = self._translations.get(book_id, [])
        
        if target_lang:
            translations = [t for t in translations if t.target_language == target_lang]
        
        return translations


# ============================================================================
# WORLD CONNECTOR
# ============================================================================

class WorldConnector:
    """
    Connect books to WorldEngine and real data.
    
    Per spec: Le Livre Connecté
    - Lien avec la réalité (WorldEngine)
    - Lien avec l'histoire (Module 19)
    - Indicateur de faisabilité
    """
    
    def __init__(self):
        self._world_links: Dict[str, List[Dict]] = {}  # book_id → links
    
    def add_world_link(
        self,
        book_id: str,
        passage_ref: str,
        link_type: str,  # simulation, historical, factual
        target_ref: str,
        description: str = "",
    ) -> Dict[str, Any]:
        """
        Add world link to a passage.
        
        Per spec: Un passage peut pointer vers une simulation réelle
        """
        link = {
            "link_id": generate_id(),
            "passage_ref": passage_ref,
            "link_type": link_type,
            "target_ref": target_ref,
            "description": description,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        if book_id not in self._world_links:
            self._world_links[book_id] = []
        self._world_links[book_id].append(link)
        
        return link
    
    def check_feasibility(
        self,
        book_id: str,
        passage_ref: str,
    ) -> Dict[str, Any]:
        """
        Check feasibility of a concept in a passage.
        
        Per spec: Indicateur de faisabilité
        """
        # Mock feasibility check
        return {
            "passage_ref": passage_ref,
            "feasibility_score": 0.7,
            "analysis": "Concept appears technically plausible with current technology",
            "related_simulations": [],
        }
    
    def get_alternative_scenarios(
        self,
        book_id: str,
        passage_ref: str,
    ) -> List[Dict[str, Any]]:
        """
        Get alternative scenarios for a passage.
        
        Per spec: Scénarios alternatifs
        """
        return [
            {
                "scenario_id": generate_id(),
                "description": "Alternative outcome A",
                "probability": 0.3,
            },
            {
                "scenario_id": generate_id(),
                "description": "Alternative outcome B",
                "probability": 0.2,
            },
        ]
    
    def get_world_links(self, book_id: str) -> List[Dict]:
        """Get all world links for a book"""
        return self._world_links.get(book_id, [])


# ============================================================================
# UNIVERSAL LITERATURE ZONE
# ============================================================================

class UniversalLiteratureZone:
    """
    The Littera-Lattice - Main library system.
    
    Per spec: Un livre n'est plus un PDF mort, mais un organisme culturel connecté.
    """
    
    def __init__(self):
        self.publishing = PublishingPipeline()
        self.immersive = ImmersiveReadingEngine()
        self.equity = AuthorEquitySystem()
        self.companion = CreativeCompanion()
        self.translator = SemanticTranslator()
        self.world = WorldConnector()
    
    def publish_book(
        self,
        title: str,
        author_id: str,
        raw_text: str,
        language: str = "fr",
    ) -> Tuple[BookArtifact, bool, str]:
        """Publish a book through the full pipeline"""
        # Run publishing pipeline
        book, success, message = self.publishing.run_full_pipeline(
            title, author_id, raw_text, language
        )
        
        if success:
            # Setup equity
            self.equity.setup_book(book.book_id, author_id)
            
            # Run companion analysis
            self.companion.analyze_structure(book)
            for chunk in book.chapters:
                self.companion.suggest_style(book.book_id, chunk)
            self.companion.detect_inconsistencies(book)
        
        return book, success, message
    
    def read_immersive(
        self,
        book_id: str,
        reader_id: str,
        chunk_index: int = 0,
    ) -> Optional[Tuple[ChapterChunk, XRSceneManifest]]:
        """Read a book with immersive XR experience"""
        book = self.publishing.get_book(book_id)
        if not book or chunk_index >= len(book.chapters):
            return None
        
        chunk = book.chapters[chunk_index]
        manifest = self.immersive.generate_scene(chunk, reader_id)
        
        return chunk, manifest
    
    def translate_for_reader(
        self,
        book_id: str,
        target_language: str,
    ) -> List[SemanticTranslation]:
        """Translate book for a reader"""
        book = self.publishing.get_book(book_id)
        if not book:
            return []
        
        translations = []
        for chunk in book.chapters:
            trans = self.translator.translate(
                book_id,
                chunk,
                book.language_original,
                target_language,
            )
            translations.append(trans)
        
        return translations
    
    def tip_author(
        self,
        reader_id: str,
        book_id: str,
        amount: float,
        chunk_id: str = None,
    ):
        """Send tip to author"""
        return self.equity.process_tip(reader_id, book_id, amount, chunk_id)
    
    def search_books(
        self,
        query: str,
        threshold: float = 0.5,
    ) -> List[Tuple[BookArtifact, float]]:
        """Search books semantically"""
        return self.publishing.search(query, threshold)
    
    def get_companion_feedback(
        self,
        book_id: str,
    ) -> Dict[str, Any]:
        """Get creative companion feedback for a book"""
        book = self.publishing.get_book(book_id)
        if not book:
            return {}
        
        return {
            "structure": self.companion.analyze_structure(book),
            "suggestions": [
                {
                    "id": s.suggestion_id,
                    "type": s.suggestion_type.value,
                    "description": s.description,
                    "accepted": s.accepted,
                }
                for s in self.companion.get_suggestions(book_id)
            ],
            "issues": [
                {
                    "id": i.issue_id,
                    "type": i.issue_type,
                    "description": i.description,
                    "resolved": i.resolved,
                }
                for i in self.companion._issues.get(book_id, [])
            ],
        }
    
    def connect_to_world(
        self,
        book_id: str,
        passage_ref: str,
        simulation_ref: str,
    ) -> Dict[str, Any]:
        """Connect passage to WorldEngine simulation"""
        return self.world.add_world_link(
            book_id,
            passage_ref,
            "simulation",
            simulation_ref,
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get zone statistics"""
        books = list(self.publishing._books.values())
        published = [b for b in books if b.status.value == "published"]
        
        return {
            "total_books": len(books),
            "published_books": len(published),
            "total_authors": len(set(b.author_id for b in books)),
            "total_words": sum(
                sum(c.word_count for c in b.chapters)
                for b in published
            ),
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_literature_zone() -> UniversalLiteratureZone:
    """Create Universal Literature Zone"""
    return UniversalLiteratureZone()


def create_companion() -> CreativeCompanion:
    """Create Creative Companion"""
    return CreativeCompanion()


def create_translator() -> SemanticTranslator:
    """Create Semantic Translator"""
    return SemanticTranslator()
