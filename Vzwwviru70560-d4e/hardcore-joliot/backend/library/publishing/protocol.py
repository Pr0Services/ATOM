"""
============================================================================
CHE·NU™ V69 — LIBRARY SEMANTIC PUBLISHING PROTOCOL
============================================================================
Spec: GPT1/CHE-NU_LIB_SEMANTIC_PUBLISHING_PROTOCOL.md

Objective: Standardize upload, validation, and publication of works in
the Universal Literature Zone.

Pipeline (per spec):
1. Upload
2. Normalization (markdown → canonical text layout)
3. OPA Screening (security & legality rules)
4. Semantic Indexing (vector + tags)
5. Artifact Signing (immutable signature)
6. Publish (network & discovery)
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
import logging
import re

from ..models import (
    BookArtifact,
    ChapterChunk,
    PublishingStatus,
    LicenseType,
    generate_id,
    compute_hash,
    sign_artifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# TEXT NORMALIZER
# ============================================================================

class TextNormalizer:
    """
    Normalize text to canonical layout.
    
    Per spec step 2: Normalization (markdown → canonical text layout)
    """
    
    def normalize(self, raw_text: str) -> str:
        """Normalize raw text"""
        text = raw_text
        
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove excessive whitespace
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Trim lines
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        return text.strip()
    
    def split_into_chunks(
        self,
        text: str,
        chunk_size: int = 2000,
    ) -> List[str]:
        """Split text into chunks for chapters"""
        # Simple paragraph-based splitting
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for para in paragraphs:
            para_size = len(para)
            
            if current_size + para_size > chunk_size and current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = [para]
                current_size = para_size
            else:
                current_chunk.append(para)
                current_size += para_size
        
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks


# ============================================================================
# OPA SCREENER
# ============================================================================

@dataclass
class ScreeningResult:
    """Result of OPA screening"""
    passed: bool
    flags: List[str] = field(default_factory=list)
    reason: str = ""


class OPAScreener:
    """
    Screen content with OPA rules.
    
    Per spec step 3: OPA Screening
    Per spec governance:
    - Interdire la violence actionable, la fraude, l'exploitation ciblée
    - Autoriser fiction, satire, politique, philosophie
    - Transparence: l'auteur voit les raisons d'un blocage/flag
    """
    
    # Blocked patterns (actionable violence, fraud, exploitation)
    BLOCKED_PATTERNS = [
        r'\b(instructions?\s+pour\s+fabriquer|how\s+to\s+make)\s+(bombe|explosive|arme)',
        r'\b(numéro\s+carte|credit\s+card\s+number)\b.*\d{4}',
        r'\b(harcèlement|stalking)\s+de\s+\w+',
    ]
    
    # Warning patterns (review needed)
    WARNING_PATTERNS = [
        r'\b(violence\s+graphique|graphic\s+violence)\b',
        r'\b(contenu\s+explicite|explicit\s+content)\b',
    ]
    
    def __init__(self, custom_rules: List[Dict] = None):
        self.custom_rules = custom_rules or []
    
    def screen(self, text: str, metadata: Dict = None) -> ScreeningResult:
        """Screen text content"""
        text_lower = text.lower()
        flags = []
        
        # Check blocked patterns
        for pattern in self.BLOCKED_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return ScreeningResult(
                    passed=False,
                    flags=["blocked_content"],
                    reason=f"Content matches blocked pattern: {pattern[:50]}..."
                )
        
        # Check warning patterns
        for pattern in self.WARNING_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                flags.append("content_warning")
        
        # Custom rules
        for rule in self.custom_rules:
            if rule.get("pattern") and re.search(rule["pattern"], text_lower):
                if rule.get("action") == "block":
                    return ScreeningResult(
                        passed=False,
                        flags=["custom_block"],
                        reason=rule.get("reason", "Custom rule violation")
                    )
                elif rule.get("action") == "flag":
                    flags.append(rule.get("flag", "custom_flag"))
        
        return ScreeningResult(passed=True, flags=flags)


# ============================================================================
# SEMANTIC INDEXER
# ============================================================================

class SemanticIndexer:
    """
    Index content semantically.
    
    Per spec step 4: Semantic Indexing (Module 14: vecteur + tags)
    """
    
    # Simple keyword extraction (in production: use embeddings)
    SEMANTIC_TAGS = {
        "fiction": ["roman", "histoire", "personnage", "intrigue", "récit"],
        "science": ["recherche", "étude", "données", "hypothèse", "expérience"],
        "philosophy": ["pensée", "réflexion", "existence", "éthique", "vérité"],
        "history": ["époque", "événement", "civilisation", "guerre", "révolution"],
        "poetry": ["vers", "rime", "poème", "strophe", "métaphore"],
        "education": ["apprendre", "cours", "leçon", "exercice", "formation"],
    }
    
    def index(self, text: str, title: str = "") -> Dict[str, Any]:
        """Index text content"""
        text_lower = text.lower()
        combined = f"{title.lower()} {text_lower}"
        
        # Extract tags
        tags = []
        for category, keywords in self.SEMANTIC_TAGS.items():
            if any(kw in combined for kw in keywords):
                tags.append(category)
        
        # Generate mock vector (in production: use real embeddings)
        vector = self._generate_mock_vector(combined)
        
        return {
            "tags": tags,
            "vector": vector,
            "word_count": len(text.split()),
            "indexed_at": datetime.utcnow().isoformat(),
        }
    
    def _generate_mock_vector(self, text: str, dim: int = 128) -> List[float]:
        """Generate mock semantic vector"""
        import hashlib
        
        # Create deterministic vector from text hash
        h = hashlib.sha256(text.encode()).hexdigest()
        vector = []
        
        for i in range(0, min(len(h), dim * 2), 2):
            val = int(h[i:i+2], 16) / 255.0
            vector.append(val)
        
        # Pad if needed
        while len(vector) < dim:
            vector.append(0.5)
        
        return vector[:dim]
    
    def similarity(self, vector_a: List[float], vector_b: List[float]) -> float:
        """Compute cosine similarity between vectors"""
        if not vector_a or not vector_b:
            return 0.0
        
        dot = sum(a * b for a, b in zip(vector_a, vector_b))
        norm_a = sum(a * a for a in vector_a) ** 0.5
        norm_b = sum(b * b for b in vector_b) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot / (norm_a * norm_b)


# ============================================================================
# PUBLISHING PIPELINE
# ============================================================================

class PublishingPipeline:
    """
    Main publishing pipeline.
    
    Per spec pipeline: Upload → Normalization → OPA → Indexing → Signing → Publish
    """
    
    def __init__(self):
        self.normalizer = TextNormalizer()
        self.screener = OPAScreener()
        self.indexer = SemanticIndexer()
        
        # Storage
        self._books: Dict[str, BookArtifact] = {}
    
    def upload(
        self,
        title: str,
        author_id: str,
        raw_text: str,
        language: str = "fr",
        license_type: LicenseType = LicenseType.ALL_RIGHTS_RESERVED,
    ) -> BookArtifact:
        """
        Step 1: Upload a book.
        """
        book = BookArtifact(
            book_id=generate_id(),
            title=title,
            author_id=author_id,
            language_original=language,
            license=license_type,
            status=PublishingStatus.UPLOADED,
        )
        
        # Store raw text temporarily
        book.chapters = [ChapterChunk(
            chunk_id=generate_id(),
            chapter_no=0,
            order_index=0,
            text=raw_text,
            word_count=len(raw_text.split()),
        )]
        
        self._books[book.book_id] = book
        logger.info(f"Book {book.book_id} uploaded: {title}")
        return book
    
    def normalize(self, book_id: str) -> BookArtifact:
        """
        Step 2: Normalize text.
        """
        book = self._books.get(book_id)
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        # Get raw text
        raw_text = book.chapters[0].text if book.chapters else ""
        
        # Normalize
        normalized = self.normalizer.normalize(raw_text)
        
        # Split into chunks
        chunk_texts = self.normalizer.split_into_chunks(normalized)
        
        # Create chapter chunks
        book.chapters = []
        for i, chunk_text in enumerate(chunk_texts):
            chunk = ChapterChunk(
                chunk_id=generate_id(),
                chapter_no=i + 1,
                order_index=i,
                text=chunk_text,
                word_count=len(chunk_text.split()),
            )
            book.chapters.append(chunk)
        
        book.status = PublishingStatus.NORMALIZED
        logger.info(f"Book {book_id} normalized: {len(book.chapters)} chunks")
        return book
    
    def screen(self, book_id: str) -> Tuple[BookArtifact, ScreeningResult]:
        """
        Step 3: OPA screening.
        """
        book = self._books.get(book_id)
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        # Screen all chunks
        all_text = "\n".join(c.text for c in book.chapters)
        result = self.screener.screen(all_text, {"title": book.title})
        
        if result.passed:
            book.status = PublishingStatus.SCREENED
            logger.info(f"Book {book_id} passed screening")
        else:
            book.status = PublishingStatus.FLAGGED
            logger.warning(f"Book {book_id} flagged: {result.reason}")
        
        return book, result
    
    def index_semantically(self, book_id: str) -> BookArtifact:
        """
        Step 4: Semantic indexing.
        """
        book = self._books.get(book_id)
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        # Index full text
        all_text = "\n".join(c.text for c in book.chapters)
        index_data = self.indexer.index(all_text, book.title)
        
        book.semantic_vector = index_data["vector"]
        book.semantic_index_ref = f"index://{book_id}"
        
        # Index individual chunks
        for chunk in book.chapters:
            chunk_index = self.indexer.index(chunk.text)
            chunk.semantic_tags = chunk_index["tags"]
        
        book.status = PublishingStatus.INDEXED
        logger.info(f"Book {book_id} indexed: tags={index_data['tags']}")
        return book
    
    def sign_artifact(self, book_id: str, signer_id: str = "system") -> BookArtifact:
        """
        Step 5: Sign artifact.
        """
        book = self._books.get(book_id)
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        # Sign each chunk
        for chunk in book.chapters:
            chunk_sig = sign_artifact({
                "chunk_id": chunk.chunk_id,
                "text_hash": compute_hash(chunk.text),
                "book_id": book_id,
            }, signer_id)
            # Store sig in rights
            chunk.rights["signature"] = chunk_sig
        
        # Sign book
        book_sig = sign_artifact({
            "book_id": book.book_id,
            "title": book.title,
            "author_id": book.author_id,
            "chunk_count": len(book.chapters),
        }, signer_id)
        
        book.signatures.append({
            "signer": signer_id,
            "signature": book_sig,
            "timestamp": datetime.utcnow().isoformat(),
        })
        
        book.status = PublishingStatus.SIGNED
        logger.info(f"Book {book_id} signed by {signer_id}")
        return book
    
    def publish(self, book_id: str) -> BookArtifact:
        """
        Step 6: Publish.
        """
        book = self._books.get(book_id)
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        if book.status != PublishingStatus.SIGNED:
            raise ValueError(f"Book {book_id} must be signed before publishing")
        
        book.status = PublishingStatus.PUBLISHED
        book.published_at = datetime.utcnow()
        
        logger.info(f"Book {book_id} published: {book.title}")
        return book
    
    def run_full_pipeline(
        self,
        title: str,
        author_id: str,
        raw_text: str,
        language: str = "fr",
    ) -> Tuple[BookArtifact, bool, str]:
        """
        Run complete pipeline.
        
        Returns (book, success, message)
        """
        # Step 1: Upload
        book = self.upload(title, author_id, raw_text, language)
        
        # Step 2: Normalize
        book = self.normalize(book.book_id)
        
        # Step 3: Screen
        book, screening = self.screen(book.book_id)
        if not screening.passed:
            return book, False, f"Screening failed: {screening.reason}"
        
        # Step 4: Index
        book = self.index_semantically(book.book_id)
        
        # Step 5: Sign
        book = self.sign_artifact(book.book_id)
        
        # Step 6: Publish
        book = self.publish(book.book_id)
        
        return book, True, "Published successfully"
    
    def search(
        self,
        query: str,
        threshold: float = 0.5,
    ) -> List[Tuple[BookArtifact, float]]:
        """
        Search books by semantic query.
        
        Per spec: semantic_query, similarity_threshold
        """
        # Index query
        query_index = self.indexer.index(query)
        query_vector = query_index["vector"]
        
        results = []
        for book in self._books.values():
            if book.status == PublishingStatus.PUBLISHED:
                sim = self.indexer.similarity(query_vector, book.semantic_vector)
                if sim >= threshold:
                    results.append((book, sim))
        
        # Sort by similarity
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def get_book(self, book_id: str) -> Optional[BookArtifact]:
        """Get book by ID"""
        return self._books.get(book_id)


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_pipeline() -> PublishingPipeline:
    """Create publishing pipeline"""
    return PublishingPipeline()


def create_screener(custom_rules: List[Dict] = None) -> OPAScreener:
    """Create OPA screener"""
    return OPAScreener(custom_rules)


def create_indexer() -> SemanticIndexer:
    """Create semantic indexer"""
    return SemanticIndexer()
