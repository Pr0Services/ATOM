"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                 CHE·NU™ PERSONAL PRODUCTIVITY — NOTE ASSISTANT               ║
║                                                                              ║
║  AI-powered note-taking with intelligent organization.                       ║
║                                                                              ║
║  Features:                                                                   ║
║  - Auto-title generation                                                     ║
║  - Smart tag extraction                                                      ║
║  - Summary creation                                                          ║
║  - Folder suggestions                                                        ║
║  - Related notes linking                                                     ║
║                                                                              ║
║  COS: 93/100 — Notion Competitor                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import uuid
import asyncio
import logging
import httpx
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class NoteType(str, Enum):
    NOTE = "note"
    MEETING = "meeting"
    JOURNAL = "journal"
    IDEA = "idea"
    REFERENCE = "reference"
    TODO = "todo"


class NoteStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    PINNED = "pinned"


@dataclass
class Note:
    """A note object."""
    id: str
    title: str
    content: str
    type: NoteType
    status: NoteStatus
    tags: List[str]
    folder: Optional[str]
    summary: Optional[str]
    created_at: datetime
    updated_at: datetime
    user_id: str
    identity_id: str
    word_count: int
    ai_enhanced: bool = False
    related_notes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NoteEnhancement:
    """AI enhancement result for a note."""
    suggested_title: str
    extracted_tags: List[str]
    summary: str
    suggested_folder: str
    note_type: NoteType
    key_points: List[str]
    action_items: List[str]
    related_topics: List[str]


# ═══════════════════════════════════════════════════════════════════════════════
# AI ENHANCEMENT ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class NoteAIEngine:
    """AI engine for note enhancement using Claude/OpenAI."""
    
    def __init__(self):
        self.anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self.openai_key = os.environ.get("OPENAI_API_KEY", "")
        self.provider = "anthropic" if self.anthropic_key else "openai"
    
    async def enhance_note(self, content: str) -> NoteEnhancement:
        """Enhance a note with AI-generated metadata."""
        
        if self.provider == "anthropic" and self.anthropic_key:
            return await self._enhance_with_claude(content)
        elif self.openai_key:
            return await self._enhance_with_openai(content)
        else:
            return self._local_enhancement(content)
    
    async def _enhance_with_claude(self, content: str) -> NoteEnhancement:
        """Enhance note using Claude."""
        
        prompt = f"""Analyze this note and provide structured metadata in JSON format:

NOTE CONTENT:
{content[:3000]}

Respond ONLY with valid JSON in this exact format:
{{
    "suggested_title": "concise title (max 60 chars)",
    "extracted_tags": ["tag1", "tag2", "tag3"],
    "summary": "2-3 sentence summary",
    "suggested_folder": "category like Work, Personal, Learning, Projects",
    "note_type": "note|meeting|journal|idea|reference|todo",
    "key_points": ["point 1", "point 2"],
    "action_items": ["action 1 if any"],
    "related_topics": ["topic 1", "topic 2"]
}}"""

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.anthropic_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 1024,
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    text = data["content"][0]["text"]
                    
                    # Parse JSON from response
                    json_start = text.find("{")
                    json_end = text.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        result = json.loads(text[json_start:json_end])
                        return NoteEnhancement(
                            suggested_title=result.get("suggested_title", "Untitled Note"),
                            extracted_tags=result.get("extracted_tags", [])[:5],
                            summary=result.get("summary", ""),
                            suggested_folder=result.get("suggested_folder", "General"),
                            note_type=NoteType(result.get("note_type", "note")),
                            key_points=result.get("key_points", []),
                            action_items=result.get("action_items", []),
                            related_topics=result.get("related_topics", []),
                        )
            except Exception as e:
                logger.error(f"Claude enhancement failed: {e}")
        
        return self._local_enhancement(content)
    
    async def _enhance_with_openai(self, content: str) -> NoteEnhancement:
        """Enhance note using OpenAI."""
        
        prompt = f"""Analyze this note and provide structured metadata.

NOTE:
{content[:3000]}

Respond with JSON only:
{{"suggested_title": "...", "extracted_tags": [...], "summary": "...", "suggested_folder": "...", "note_type": "note|meeting|journal|idea|reference|todo", "key_points": [...], "action_items": [...], "related_topics": [...]}}"""

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openai_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 1024,
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    text = data["choices"][0]["message"]["content"]
                    
                    json_start = text.find("{")
                    json_end = text.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        result = json.loads(text[json_start:json_end])
                        return NoteEnhancement(
                            suggested_title=result.get("suggested_title", "Untitled Note"),
                            extracted_tags=result.get("extracted_tags", [])[:5],
                            summary=result.get("summary", ""),
                            suggested_folder=result.get("suggested_folder", "General"),
                            note_type=NoteType(result.get("note_type", "note")),
                            key_points=result.get("key_points", []),
                            action_items=result.get("action_items", []),
                            related_topics=result.get("related_topics", []),
                        )
            except Exception as e:
                logger.error(f"OpenAI enhancement failed: {e}")
        
        return self._local_enhancement(content)
    
    def _local_enhancement(self, content: str) -> NoteEnhancement:
        """Local fallback enhancement without API."""
        
        words = content.split()
        
        # Extract title from first line or first few words
        first_line = content.split('\n')[0].strip()
        title = first_line[:60] if first_line else " ".join(words[:6])
        
        # Extract potential tags (capitalized words, hashtags)
        tags = []
        for word in words:
            if word.startswith('#'):
                tags.append(word[1:].lower())
            elif word[0].isupper() and len(word) > 3 and word.isalpha():
                tags.append(word.lower())
        tags = list(set(tags))[:5]
        
        # Simple summary
        sentences = content.replace('\n', ' ').split('.')
        summary = '. '.join(sentences[:2]).strip() + '.' if sentences else ""
        
        # Detect type
        content_lower = content.lower()
        if 'meeting' in content_lower or 'attendees' in content_lower:
            note_type = NoteType.MEETING
        elif 'todo' in content_lower or '[ ]' in content or '- [ ]' in content:
            note_type = NoteType.TODO
        elif 'idea' in content_lower or 'brainstorm' in content_lower:
            note_type = NoteType.IDEA
        elif 'dear diary' in content_lower or 'today i' in content_lower:
            note_type = NoteType.JOURNAL
        else:
            note_type = NoteType.NOTE
        
        return NoteEnhancement(
            suggested_title=title,
            extracted_tags=tags,
            summary=summary[:200],
            suggested_folder="General",
            note_type=note_type,
            key_points=[],
            action_items=[],
            related_topics=tags[:3],
        )


# ═══════════════════════════════════════════════════════════════════════════════
# NOTE ASSISTANT AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class NoteAssistantAgent:
    """
    CHE·NU Personal Productivity Note Assistant Agent.
    
    Features:
    - CRUD operations for notes
    - AI-powered enhancement
    - Smart organization
    - Search and filtering
    - Related notes linking
    """
    
    def __init__(self):
        self.ai_engine = NoteAIEngine()
        
        # In-memory storage (replace with DB in production)
        self._notes: Dict[str, Dict[str, Note]] = {}  # user_id -> note_id -> Note
        self._folders: Dict[str, List[str]] = {}  # user_id -> folder names
        self._tags: Dict[str, Dict[str, int]] = {}  # user_id -> tag -> count
        
        logger.info("NoteAssistantAgent initialized")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CRUD OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def create_note(
        self,
        content: str,
        user_id: str,
        identity_id: str = "",
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        folder: Optional[str] = None,
        note_type: Optional[NoteType] = None,
        auto_enhance: bool = True,
    ) -> Note:
        """Create a new note with optional AI enhancement."""
        
        enhancement = None
        if auto_enhance:
            enhancement = await self.ai_engine.enhance_note(content)
        
        now = datetime.now(timezone.utc)
        
        note = Note(
            id=str(uuid.uuid4()),
            title=title or (enhancement.suggested_title if enhancement else content[:50]),
            content=content,
            type=note_type or (enhancement.note_type if enhancement else NoteType.NOTE),
            status=NoteStatus.ACTIVE,
            tags=tags or (enhancement.extracted_tags if enhancement else []),
            folder=folder or (enhancement.suggested_folder if enhancement else "General"),
            summary=enhancement.summary if enhancement else None,
            created_at=now,
            updated_at=now,
            user_id=user_id,
            identity_id=identity_id,
            word_count=len(content.split()),
            ai_enhanced=auto_enhance and enhancement is not None,
            metadata={
                "key_points": enhancement.key_points if enhancement else [],
                "action_items": enhancement.action_items if enhancement else [],
            }
        )
        
        # Store note
        if user_id not in self._notes:
            self._notes[user_id] = {}
        self._notes[user_id][note.id] = note
        
        # Update folders
        if user_id not in self._folders:
            self._folders[user_id] = []
        if note.folder and note.folder not in self._folders[user_id]:
            self._folders[user_id].append(note.folder)
        
        # Update tag counts
        if user_id not in self._tags:
            self._tags[user_id] = {}
        for tag in note.tags:
            self._tags[user_id][tag] = self._tags[user_id].get(tag, 0) + 1
        
        logger.info(f"Created note {note.id} for user {user_id}")
        return note
    
    def get_note(self, note_id: str, user_id: str) -> Optional[Note]:
        """Get a note by ID."""
        return self._notes.get(user_id, {}).get(note_id)
    
    async def update_note(
        self,
        note_id: str,
        user_id: str,
        content: Optional[str] = None,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        folder: Optional[str] = None,
        status: Optional[NoteStatus] = None,
        auto_enhance: bool = False,
    ) -> Optional[Note]:
        """Update an existing note."""
        
        note = self.get_note(note_id, user_id)
        if not note:
            return None
        
        # Update old tag counts
        for tag in note.tags:
            if tag in self._tags.get(user_id, {}):
                self._tags[user_id][tag] -= 1
        
        # Apply updates
        if content is not None:
            note.content = content
            note.word_count = len(content.split())
            
            if auto_enhance:
                enhancement = await self.ai_engine.enhance_note(content)
                if not title:
                    note.title = enhancement.suggested_title
                if not tags:
                    note.tags = enhancement.extracted_tags
                if not folder:
                    note.folder = enhancement.suggested_folder
                note.summary = enhancement.summary
                note.ai_enhanced = True
        
        if title is not None:
            note.title = title
        if tags is not None:
            note.tags = tags
        if folder is not None:
            note.folder = folder
            if folder not in self._folders.get(user_id, []):
                self._folders[user_id].append(folder)
        if status is not None:
            note.status = status
        
        note.updated_at = datetime.now(timezone.utc)
        
        # Update new tag counts
        for tag in note.tags:
            self._tags[user_id][tag] = self._tags[user_id].get(tag, 0) + 1
        
        logger.info(f"Updated note {note_id}")
        return note
    
    def delete_note(self, note_id: str, user_id: str) -> bool:
        """Delete a note."""
        note = self.get_note(note_id, user_id)
        if not note:
            return False
        
        # Update tag counts
        for tag in note.tags:
            if tag in self._tags.get(user_id, {}):
                self._tags[user_id][tag] -= 1
        
        del self._notes[user_id][note_id]
        logger.info(f"Deleted note {note_id}")
        return True
    
    # ═══════════════════════════════════════════════════════════════════════════
    # QUERIES
    # ═══════════════════════════════════════════════════════════════════════════
    
    def list_notes(
        self,
        user_id: str,
        folder: Optional[str] = None,
        tag: Optional[str] = None,
        note_type: Optional[NoteType] = None,
        status: Optional[NoteStatus] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Note]:
        """List notes with filtering."""
        
        notes = list(self._notes.get(user_id, {}).values())
        
        # Apply filters
        if folder:
            notes = [n for n in notes if n.folder == folder]
        if tag:
            notes = [n for n in notes if tag in n.tags]
        if note_type:
            notes = [n for n in notes if n.type == note_type]
        if status:
            notes = [n for n in notes if n.status == status]
        if search:
            search_lower = search.lower()
            notes = [n for n in notes if 
                     search_lower in n.title.lower() or 
                     search_lower in n.content.lower()]
        
        # Sort by updated_at desc
        notes = sorted(notes, key=lambda n: n.updated_at, reverse=True)
        
        return notes[offset:offset + limit]
    
    def get_folders(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all folders with note counts."""
        folders = self._folders.get(user_id, [])
        notes = self._notes.get(user_id, {}).values()
        
        result = []
        for folder in folders:
            count = sum(1 for n in notes if n.folder == folder)
            result.append({"name": folder, "count": count})
        
        return sorted(result, key=lambda f: f["count"], reverse=True)
    
    def get_tags(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get all tags with counts."""
        tags = self._tags.get(user_id, {})
        
        result = [
            {"name": tag, "count": count}
            for tag, count in tags.items()
            if count > 0
        ]
        
        return sorted(result, key=lambda t: t["count"], reverse=True)[:limit]
    
    def get_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user's note statistics."""
        notes = list(self._notes.get(user_id, {}).values())
        
        if not notes:
            return {
                "total_notes": 0,
                "total_words": 0,
                "by_type": {},
                "by_status": {},
                "folders_count": 0,
                "tags_count": 0,
            }
        
        by_type = {}
        by_status = {}
        total_words = 0
        
        for note in notes:
            by_type[note.type.value] = by_type.get(note.type.value, 0) + 1
            by_status[note.status.value] = by_status.get(note.status.value, 0) + 1
            total_words += note.word_count
        
        return {
            "total_notes": len(notes),
            "total_words": total_words,
            "by_type": by_type,
            "by_status": by_status,
            "folders_count": len(self._folders.get(user_id, [])),
            "tags_count": len([t for t, c in self._tags.get(user_id, {}).items() if c > 0]),
        }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # AI FEATURES
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def enhance_note(self, note_id: str, user_id: str) -> Optional[Note]:
        """Enhance an existing note with AI."""
        note = self.get_note(note_id, user_id)
        if not note:
            return None
        
        enhancement = await self.ai_engine.enhance_note(note.content)
        
        note.title = enhancement.suggested_title
        note.tags = enhancement.extracted_tags
        note.folder = enhancement.suggested_folder
        note.summary = enhancement.summary
        note.type = enhancement.note_type
        note.ai_enhanced = True
        note.metadata["key_points"] = enhancement.key_points
        note.metadata["action_items"] = enhancement.action_items
        note.updated_at = datetime.now(timezone.utc)
        
        return note
    
    async def suggest_related(self, note_id: str, user_id: str, limit: int = 5) -> List[Note]:
        """Suggest related notes based on content similarity."""
        note = self.get_note(note_id, user_id)
        if not note:
            return []
        
        all_notes = [n for n in self._notes.get(user_id, {}).values() if n.id != note_id]
        
        # Simple tag-based similarity
        scored = []
        for other in all_notes:
            common_tags = set(note.tags) & set(other.tags)
            score = len(common_tags)
            
            # Boost same folder
            if note.folder == other.folder:
                score += 0.5
            
            # Boost same type
            if note.type == other.type:
                score += 0.3
            
            if score > 0:
                scored.append((score, other))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [n for _, n in scored[:limit]]


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════════════════════

_note_assistant: Optional[NoteAssistantAgent] = None


def get_note_assistant() -> NoteAssistantAgent:
    """Get or create the note assistant agent."""
    global _note_assistant
    if _note_assistant is None:
        _note_assistant = NoteAssistantAgent()
    return _note_assistant


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import asyncio
    
    print("📝 CHE·NU Personal Productivity - Note Assistant")
    print("=" * 60)
    
    agent = get_note_assistant()
    
    async def test():
        # Create a test note
        note = await agent.create_note(
            content="""Meeting Notes - Q1 Planning
            
Attendees: John, Sarah, Mike
Date: January 5, 2026

Key Discussion Points:
1. Budget allocation for new features
2. Hiring timeline - need 2 engineers by March
3. Product roadmap review

Action Items:
- [ ] John to prepare budget proposal
- [ ] Sarah to post job listings
- [ ] Mike to update roadmap document

Next meeting: January 12, 2026""",
            user_id="test_user",
            auto_enhance=False,  # Skip API call for test
        )
        
        print(f"\n✅ Created note: {note.id}")
        print(f"   Title: {note.title}")
        print(f"   Type: {note.type.value}")
        print(f"   Words: {note.word_count}")
        
        # Get stats
        stats = agent.get_stats("test_user")
        print(f"\n📊 Stats: {stats['total_notes']} notes, {stats['total_words']} words")
    
    asyncio.run(test())
    
    print("\n✅ Note Assistant Agent ready!")
