"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V78 — Scholar Sphere Router
═══════════════════════════════════════════════════════════════════════════════

Endpoints: 20
Target Profile: David (Cardiologue-Chercheur)

Features:
- Literature search (PubMed, Google Scholar)
- Reference management
- Manuscript collaboration
- Citation formatting
- Research notes
- Conference abstracts
- Peer review tracking

R&D RULES ENFORCED:
- Rule #1: Human Sovereignty → Checkpoints on submit/publish
- Rule #5: NO RANKING → Chronological + alphabetical only
- Rule #6: Traceability → id, created_by, created_at on all entities
"""

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from uuid import UUID, uuid4
from enum import Enum

router = APIRouter()


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class ReferenceType(str, Enum):
    JOURNAL_ARTICLE = "journal_article"
    BOOK = "book"
    BOOK_CHAPTER = "book_chapter"
    CONFERENCE_PAPER = "conference_paper"
    THESIS = "thesis"
    PREPRINT = "preprint"
    WEBSITE = "website"
    REPORT = "report"


class CitationStyle(str, Enum):
    APA = "apa"
    MLA = "mla"
    CHICAGO = "chicago"
    VANCOUVER = "vancouver"
    HARVARD = "harvard"
    IEEE = "ieee"


class ManuscriptStatus(str, Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    REVISION = "revision"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    PUBLISHED = "published"
    REJECTED = "rejected"


class NoteType(str, Enum):
    LITERATURE_REVIEW = "literature_review"
    METHODOLOGY = "methodology"
    RESULTS = "results"
    DISCUSSION = "discussion"
    GENERAL = "general"


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class LiteratureSearchResult(BaseModel):
    """Result from literature search."""
    pmid: Optional[str] = None  # PubMed ID
    doi: Optional[str] = None
    title: str
    authors: List[str]
    journal: Optional[str]
    year: int
    abstract: Optional[str]
    keywords: List[str] = []
    source: str  # pubmed, scholar, crossref
    url: Optional[str]


class ReferenceCreate(BaseModel):
    """Create a reference."""
    reference_type: ReferenceType
    title: str
    authors: List[str]
    year: int
    journal: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    url: Optional[str] = None
    abstract: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class ReferenceResponse(BaseModel):
    """Reference with metadata."""
    id: UUID
    reference_type: ReferenceType
    title: str
    authors: List[str]
    year: int
    journal: Optional[str]
    volume: Optional[str]
    issue: Optional[str]
    pages: Optional[str]
    doi: Optional[str]
    pmid: Optional[str]
    url: Optional[str]
    abstract: Optional[str]
    keywords: List[str]
    notes: Optional[str]
    tags: List[str]
    # Collections
    collections: List[str]
    # Citation count in user's manuscripts
    citation_count: int
    # Traceability
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class ManuscriptCreate(BaseModel):
    """Create a manuscript."""
    title: str
    abstract: Optional[str] = None
    manuscript_type: str = "research_article"  # research_article, review, case_study, etc.
    target_journal: Optional[str] = None
    co_authors: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)


class ManuscriptResponse(BaseModel):
    """Manuscript with metadata."""
    id: UUID
    title: str
    abstract: Optional[str]
    manuscript_type: str
    status: ManuscriptStatus
    target_journal: Optional[str]
    co_authors: List[str]
    keywords: List[str]
    # Sections
    sections: Dict[str, str]  # intro, methods, results, discussion, etc.
    # References used
    references: List[UUID]
    # Submission tracking
    submitted_at: Optional[datetime]
    revision_count: int
    # Traceability
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class ResearchNoteCreate(BaseModel):
    """Create a research note."""
    title: str
    content: str
    note_type: NoteType = NoteType.GENERAL
    linked_references: List[UUID] = Field(default_factory=list)
    linked_manuscript: Optional[UUID] = None
    tags: List[str] = Field(default_factory=list)


class ResearchNoteResponse(BaseModel):
    """Research note with metadata."""
    id: UUID
    title: str
    content: str
    note_type: NoteType
    linked_references: List[UUID]
    linked_manuscript: Optional[UUID]
    tags: List[str]
    # Traceability
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class CitationOutput(BaseModel):
    """Formatted citation."""
    reference_id: UUID
    style: CitationStyle
    formatted: str
    in_text: str  # (Author, Year) or [1] depending on style


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATA STORE
# ═══════════════════════════════════════════════════════════════════════════════

_references: Dict[UUID, dict] = {}
_manuscripts: Dict[UUID, dict] = {}
_research_notes: Dict[UUID, dict] = {}
_collections: Dict[UUID, List[UUID]] = {}  # collection_id -> reference_ids
_literature_alerts: Dict[UUID, dict] = {}
_pending_checkpoints: Dict[UUID, dict] = {}


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def get_mock_user_id() -> UUID:
    return UUID("00000000-0000-0000-0000-000000000001")


def create_checkpoint(action: str, resource_type: str, resource_id: UUID, reason: str) -> dict:
    """Create checkpoint for human approval (R&D Rule #1)."""
    checkpoint = {
        "checkpoint_id": uuid4(),
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "reason": reason,
        "options": ["approve", "reject"],
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    _pending_checkpoints[checkpoint["checkpoint_id"]] = checkpoint
    return checkpoint


def format_citation_apa(ref: dict) -> tuple:
    """Format reference in APA style."""
    authors = ref["authors"]
    if len(authors) == 1:
        author_str = authors[0]
    elif len(authors) == 2:
        author_str = f"{authors[0]} & {authors[1]}"
    elif len(authors) > 2:
        author_str = f"{authors[0]} et al."
    else:
        author_str = "Unknown"
    
    year = ref["year"]
    title = ref["title"]
    journal = ref.get("journal", "")
    
    formatted = f"{author_str} ({year}). {title}."
    if journal:
        formatted += f" {journal}."
    
    in_text = f"({author_str.split(',')[0].split(' ')[-1]}, {year})"
    
    return formatted, in_text


def format_citation_vancouver(ref: dict, number: int = 1) -> tuple:
    """Format reference in Vancouver style."""
    authors = ref["authors"]
    if len(authors) > 6:
        author_str = ", ".join(authors[:6]) + ", et al"
    else:
        author_str = ", ".join(authors)
    
    formatted = f"{author_str}. {ref['title']}. {ref.get('journal', '')}. {ref['year']}."
    in_text = f"[{number}]"
    
    return formatted, in_text


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/health", tags=["Health"])
async def scholar_health():
    """Health check for Scholar sphere."""
    return {
        "status": "healthy",
        "sphere": "scholar",
        "version": "78.0.0",
        "endpoints": 20,
        "features": [
            "literature_search",
            "reference_management",
            "manuscript_collaboration",
            "citation_formatting",
            "research_notes"
        ],
        "citation_styles": [s.value for s in CitationStyle],
        "rd_rules": {
            "rule_1": "Human Sovereignty (checkpoints on submit)",
            "rule_5": "Chronological ordering (no engagement ranking)",
            "rule_6": "Full Traceability"
        },
        "timestamp": datetime.utcnow().isoformat()
    }


# ═══════════════════════════════════════════════════════════════════════════════
# LITERATURE SEARCH ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/literature/search", response_model=List[LiteratureSearchResult], tags=["Literature"])
async def search_literature(
    query: str = Query(..., min_length=2),
    source: str = Query("pubmed", regex="^(pubmed|scholar|crossref)$"),
    limit: int = Query(20, ge=1, le=100),
    year_from: Optional[int] = None,
    year_to: Optional[int] = None
):
    """
    Search scientific literature.
    
    Sources:
    - pubmed: PubMed/MEDLINE
    - scholar: Google Scholar
    - crossref: CrossRef
    
    Note: This is a mock implementation. Real implementation would call external APIs.
    """
    # Mock results for demonstration
    mock_results = [
        {
            "pmid": "12345678",
            "doi": "10.1000/example",
            "title": f"Research on {query}: A comprehensive review",
            "authors": ["Smith J", "Johnson M", "Williams K"],
            "journal": "Journal of Medical Research",
            "year": 2024,
            "abstract": f"This study examines {query} in detail...",
            "keywords": [query, "research", "medical"],
            "source": source,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/12345678/"
        },
        {
            "pmid": "87654321",
            "doi": "10.1001/example2",
            "title": f"Novel findings in {query} research",
            "authors": ["Chen D", "Brown A"],
            "journal": "Nature Medicine",
            "year": 2023,
            "abstract": f"We present new discoveries regarding {query}...",
            "keywords": [query, "novel", "discovery"],
            "source": source,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/87654321/"
        }
    ]
    
    # Apply year filters
    if year_from:
        mock_results = [r for r in mock_results if r["year"] >= year_from]
    if year_to:
        mock_results = [r for r in mock_results if r["year"] <= year_to]
    
    return mock_results[:limit]


@router.post("/literature/alerts", tags=["Literature"])
async def create_literature_alert(
    query: str = Query(..., min_length=2),
    frequency: str = Query("weekly", regex="^(daily|weekly|monthly)$")
):
    """Create an alert for new publications matching query."""
    user_id = get_mock_user_id()
    now = datetime.utcnow()
    
    alert = {
        "id": uuid4(),
        "query": query,
        "frequency": frequency,
        "is_active": True,
        "last_run": None,
        "results_count": 0,
        "created_by": user_id,
        "created_at": now
    }
    
    _literature_alerts[alert["id"]] = alert
    
    return {"message": "Literature alert created", "alert_id": alert["id"]}


@router.get("/literature/alerts", tags=["Literature"])
async def list_literature_alerts():
    """List active literature alerts."""
    user_id = get_mock_user_id()
    
    alerts = [a for a in _literature_alerts.values() if a["created_by"] == user_id]
    # Chronological order (R&D Rule #5)
    alerts.sort(key=lambda x: x["created_at"], reverse=True)
    
    return alerts


# ═══════════════════════════════════════════════════════════════════════════════
# REFERENCE MANAGEMENT ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/references", response_model=List[ReferenceResponse], tags=["References"])
async def list_references(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    tag: Optional[str] = None,
    year: Optional[int] = None,
    sort_by: str = Query("created_at", regex="^(created_at|year|title)$")
):
    """
    List references.
    
    ⚠️ R&D Rule #5: Sorted by created_at (chronological) or alphabetically.
                   NO engagement/citation ranking.
    """
    user_id = get_mock_user_id()
    
    refs = [r for r in _references.values() if r["created_by"] == user_id]
    
    if tag:
        refs = [r for r in refs if tag in r.get("tags", [])]
    if year:
        refs = [r for r in refs if r["year"] == year]
    
    # Sort (R&D Rule #5 compliant)
    if sort_by == "created_at":
        refs.sort(key=lambda x: x["created_at"], reverse=True)
    elif sort_by == "year":
        refs.sort(key=lambda x: x["year"], reverse=True)
    elif sort_by == "title":
        refs.sort(key=lambda x: x["title"].lower())
    
    return refs[offset:offset + limit]


@router.post("/references", response_model=ReferenceResponse, status_code=201, tags=["References"])
async def create_reference(data: ReferenceCreate):
    """Add a reference to library."""
    user_id = get_mock_user_id()
    now = datetime.utcnow()
    
    ref = {
        "id": uuid4(),
        **data.dict(),
        "collections": [],
        "citation_count": 0,
        "created_by": user_id,
        "created_at": now,
        "updated_at": now
    }
    
    _references[ref["id"]] = ref
    return ref


@router.get("/references/{ref_id}", response_model=ReferenceResponse, tags=["References"])
async def get_reference(ref_id: UUID):
    """Get reference by ID."""
    if ref_id not in _references:
        raise HTTPException(status_code=404, detail="Reference not found")
    return _references[ref_id]


@router.post("/references/import", tags=["References"])
async def import_references(
    source: str = Query(..., regex="^(pubmed|bibtex|ris|endnote)$"),
    data: str = Query(..., description="Import data (PMID, BibTeX, etc.)")
):
    """
    Import references from external source.
    
    Sources:
    - pubmed: PubMed ID (PMID)
    - bibtex: BibTeX format
    - ris: RIS format
    - endnote: EndNote XML
    """
    user_id = get_mock_user_id()
    now = datetime.utcnow()
    
    # Mock import - would parse actual formats in real implementation
    imported_ref = {
        "id": uuid4(),
        "reference_type": ReferenceType.JOURNAL_ARTICLE,
        "title": f"Imported reference from {source}",
        "authors": ["Imported Author"],
        "year": 2024,
        "journal": "Imported Journal",
        "volume": None,
        "issue": None,
        "pages": None,
        "doi": None,
        "pmid": data if source == "pubmed" else None,
        "url": None,
        "abstract": None,
        "keywords": [],
        "notes": f"Imported from {source}",
        "tags": ["imported"],
        "collections": [],
        "citation_count": 0,
        "created_by": user_id,
        "created_at": now,
        "updated_at": now
    }
    
    _references[imported_ref["id"]] = imported_ref
    
    return {"message": "Reference imported", "reference_id": imported_ref["id"]}


# ═══════════════════════════════════════════════════════════════════════════════
# CITATION FORMATTING ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/references/{ref_id}/cite", response_model=CitationOutput, tags=["Citations"])
async def format_citation(
    ref_id: UUID,
    style: CitationStyle = Query(CitationStyle.APA)
):
    """Format a reference as a citation in specified style."""
    if ref_id not in _references:
        raise HTTPException(status_code=404, detail="Reference not found")
    
    ref = _references[ref_id]
    
    if style == CitationStyle.APA:
        formatted, in_text = format_citation_apa(ref)
    elif style == CitationStyle.VANCOUVER:
        formatted, in_text = format_citation_vancouver(ref)
    else:
        # Default to APA for other styles (would implement all in real version)
        formatted, in_text = format_citation_apa(ref)
    
    return {
        "reference_id": ref_id,
        "style": style,
        "formatted": formatted,
        "in_text": in_text
    }


@router.post("/references/bibliography", tags=["Citations"])
async def generate_bibliography(
    reference_ids: List[UUID],
    style: CitationStyle = Query(CitationStyle.APA)
):
    """Generate formatted bibliography from list of references."""
    bibliography = []
    
    for ref_id in reference_ids:
        if ref_id in _references:
            ref = _references[ref_id]
            if style == CitationStyle.APA:
                formatted, _ = format_citation_apa(ref)
            elif style == CitationStyle.VANCOUVER:
                formatted, _ = format_citation_vancouver(ref, len(bibliography) + 1)
            else:
                formatted, _ = format_citation_apa(ref)
            bibliography.append(formatted)
    
    return {
        "style": style,
        "count": len(bibliography),
        "bibliography": bibliography
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MANUSCRIPT ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/manuscripts", response_model=List[ManuscriptResponse], tags=["Manuscripts"])
async def list_manuscripts(
    status: Optional[ManuscriptStatus] = None,
    limit: int = Query(20, ge=1, le=100)
):
    """
    List manuscripts.
    
    ⚠️ R&D Rule #5: Chronological order.
    """
    user_id = get_mock_user_id()
    
    manuscripts = [m for m in _manuscripts.values() if m["created_by"] == user_id]
    
    if status:
        manuscripts = [m for m in manuscripts if m["status"] == status]
    
    # Chronological (R&D Rule #5)
    manuscripts.sort(key=lambda x: x["updated_at"], reverse=True)
    
    return manuscripts[:limit]


@router.post("/manuscripts", response_model=ManuscriptResponse, status_code=201, tags=["Manuscripts"])
async def create_manuscript(data: ManuscriptCreate):
    """Create a new manuscript (starts in DRAFT)."""
    user_id = get_mock_user_id()
    now = datetime.utcnow()
    
    manuscript = {
        "id": uuid4(),
        **data.dict(),
        "status": ManuscriptStatus.DRAFT,
        "sections": {
            "introduction": "",
            "methods": "",
            "results": "",
            "discussion": "",
            "conclusion": ""
        },
        "references": [],
        "submitted_at": None,
        "revision_count": 0,
        "created_by": user_id,
        "created_at": now,
        "updated_at": now
    }
    
    _manuscripts[manuscript["id"]] = manuscript
    return manuscript


@router.get("/manuscripts/{manuscript_id}", response_model=ManuscriptResponse, tags=["Manuscripts"])
async def get_manuscript(manuscript_id: UUID):
    """Get manuscript by ID."""
    if manuscript_id not in _manuscripts:
        raise HTTPException(status_code=404, detail="Manuscript not found")
    return _manuscripts[manuscript_id]


@router.put("/manuscripts/{manuscript_id}/section", tags=["Manuscripts"])
async def update_manuscript_section(
    manuscript_id: UUID,
    section: str = Query(..., regex="^(introduction|methods|results|discussion|conclusion|abstract)$"),
    content: str = Query(...)
):
    """Update a section of the manuscript."""
    if manuscript_id not in _manuscripts:
        raise HTTPException(status_code=404, detail="Manuscript not found")
    
    manuscript = _manuscripts[manuscript_id]
    
    if manuscript["status"] not in [ManuscriptStatus.DRAFT, ManuscriptStatus.REVISION]:
        raise HTTPException(status_code=400, detail="Can only edit drafts or revisions")
    
    if section == "abstract":
        manuscript["abstract"] = content
    else:
        manuscript["sections"][section] = content
    
    manuscript["updated_at"] = datetime.utcnow()
    
    return {"message": f"Section '{section}' updated"}


@router.post("/manuscripts/{manuscript_id}/submit", tags=["Manuscripts"])
async def submit_manuscript(manuscript_id: UUID):
    """
    Submit manuscript to journal (requires checkpoint).
    
    ⚠️ R&D Rule #1: Submission requires human approval.
    """
    if manuscript_id not in _manuscripts:
        raise HTTPException(status_code=404, detail="Manuscript not found")
    
    manuscript = _manuscripts[manuscript_id]
    
    if manuscript["status"] not in [ManuscriptStatus.DRAFT, ManuscriptStatus.REVISION]:
        raise HTTPException(status_code=400, detail=f"Cannot submit manuscript in {manuscript['status']} status")
    
    checkpoint = create_checkpoint(
        action="submit_manuscript",
        resource_type="manuscript",
        resource_id=manuscript_id,
        reason="Manuscript submission requires human approval"
    )
    
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_required",
            "checkpoint": checkpoint,
            "message": "Human approval required to submit manuscript"
        }
    )


# ═══════════════════════════════════════════════════════════════════════════════
# RESEARCH NOTES ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/notes", response_model=List[ResearchNoteResponse], tags=["Notes"])
async def list_research_notes(
    note_type: Optional[NoteType] = None,
    tag: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200)
):
    """
    List research notes.
    
    ⚠️ R&D Rule #5: Chronological order.
    """
    user_id = get_mock_user_id()
    
    notes = [n for n in _research_notes.values() if n["created_by"] == user_id]
    
    if note_type:
        notes = [n for n in notes if n["note_type"] == note_type]
    if tag:
        notes = [n for n in notes if tag in n.get("tags", [])]
    
    # Chronological (R&D Rule #5)
    notes.sort(key=lambda x: x["updated_at"], reverse=True)
    
    return notes[:limit]


@router.post("/notes", response_model=ResearchNoteResponse, status_code=201, tags=["Notes"])
async def create_research_note(data: ResearchNoteCreate):
    """Create a research note."""
    user_id = get_mock_user_id()
    now = datetime.utcnow()
    
    note = {
        "id": uuid4(),
        **data.dict(),
        "created_by": user_id,
        "created_at": now,
        "updated_at": now
    }
    
    _research_notes[note["id"]] = note
    return note


# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT RESOLUTION
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/checkpoints/{checkpoint_id}/approve", tags=["Checkpoints"])
async def approve_checkpoint(checkpoint_id: UUID):
    """Approve a pending checkpoint."""
    if checkpoint_id not in _pending_checkpoints:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    
    checkpoint = _pending_checkpoints[checkpoint_id]
    
    if checkpoint["status"] != "pending":
        raise HTTPException(status_code=400, detail=f"Checkpoint already {checkpoint['status']}")
    
    action = checkpoint["action"]
    resource_id = checkpoint["resource_id"]
    
    if action == "submit_manuscript":
        if resource_id in _manuscripts:
            _manuscripts[resource_id]["status"] = ManuscriptStatus.SUBMITTED
            _manuscripts[resource_id]["submitted_at"] = datetime.utcnow()
            _manuscripts[resource_id]["updated_at"] = datetime.utcnow()
    
    checkpoint["status"] = "approved"
    checkpoint["resolved_at"] = datetime.utcnow()
    
    return {"message": "Checkpoint approved", "action": action, "executed": True}


@router.post("/checkpoints/{checkpoint_id}/reject", tags=["Checkpoints"])
async def reject_checkpoint(checkpoint_id: UUID):
    """Reject a pending checkpoint."""
    if checkpoint_id not in _pending_checkpoints:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    
    checkpoint = _pending_checkpoints[checkpoint_id]
    
    if checkpoint["status"] != "pending":
        raise HTTPException(status_code=400, detail=f"Checkpoint already {checkpoint['status']}")
    
    checkpoint["status"] = "rejected"
    checkpoint["resolved_at"] = datetime.utcnow()
    
    return {"message": "Checkpoint rejected", "action": checkpoint["action"], "executed": False}
