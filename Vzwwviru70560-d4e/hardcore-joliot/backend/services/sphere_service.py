"""
CHE·NU™ Sphere Service

Complete sphere management service with:
- Sphere initialization (9 spheres per user)
- Bureau section management
- Quick capture
- Statistics
- Identity boundary enforcement
"""

from datetime import datetime, timedelta
from typing import Optional, List
from uuid import uuid4
import logging

from sqlalchemy import select, update, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.core.exceptions import (
    NotFoundError,
    SphereNotFoundError,
    IdentityBoundaryError,
    ValidationError,
)
from backend.models.sphere import (
    Sphere,
    BureauSection,
    QuickCapture,
    SphereType,
    BureauSectionType,
    QuickCaptureType,
    QuickCaptureStatus,
    SPHERE_METADATA,
    BUREAU_SECTION_METADATA,
)
from backend.schemas.sphere_schemas import (
    SphereSummary,
    SphereDetail,
    SphereUpdate,
    SphereStats,
    BureauSectionResponse,
    QuickCaptureRequest,
    QuickCaptureResponse,
)

logger = logging.getLogger(__name__)


class SphereService:
    """
    Sphere management service.
    
    Handles all sphere operations with identity boundary enforcement.
    """
    
    def __init__(self, db: AsyncSession, identity_id: str):
        self.db = db
        self.identity_id = identity_id
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SPHERE INITIALIZATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def initialize_spheres_for_user(self) -> List[Sphere]:
        """
        Create all 9 spheres for a new user.
        
        Called during user registration.
        Each sphere gets 6 bureau sections.
        """
        spheres = []
        
        for idx, sphere_type in enumerate(SphereType):
            metadata = SPHERE_METADATA[sphere_type]
            
            sphere = Sphere(
                id=str(uuid4()),
                identity_id=self.identity_id,
                sphere_type=sphere_type,
                name=metadata["name"],
                slug=sphere_type.value,
                icon=metadata["icon"],
                color=metadata["color"],
                description=metadata["description"],
                display_order=idx,
                is_active=True,
            )
            
            self.db.add(sphere)
            await self.db.flush()
            
            # Create bureau sections for this sphere
            await self._create_bureau_sections(sphere.id)
            
            spheres.append(sphere)
        
        await self.db.commit()
        
        logger.info(f"Initialized 9 spheres for identity: {self.identity_id}")
        
        return spheres
    
    async def _create_bureau_sections(self, sphere_id: str) -> List[BureauSection]:
        """Create all 6 bureau sections for a sphere."""
        sections = []
        
        for idx, section_type in enumerate(BureauSectionType):
            metadata = BUREAU_SECTION_METADATA[section_type]
            
            section = BureauSection(
                id=str(uuid4()),
                sphere_id=sphere_id,
                section_type=section_type,
                name=metadata["name"],
                icon=metadata["icon"],
                display_order=idx,
                is_active=True,
            )
            
            self.db.add(section)
            sections.append(section)
        
        return sections
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SPHERE RETRIEVAL
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def list_spheres(self) -> List[SphereSummary]:
        """
        List all spheres for current identity.
        
        Returns spheres ordered by display_order.
        """
        result = await self.db.execute(
            select(Sphere)
            .where(Sphere.identity_id == self.identity_id)
            .order_by(Sphere.display_order)
        )
        
        spheres = result.scalars().all()
        
        return [
            SphereSummary(
                id=s.id,
                type=s.sphere_type,
                name=s.name,
                slug=s.slug,
                icon=s.icon,
                color=s.color,
                description=s.description,
                is_active=s.is_active,
                is_pinned=s.is_pinned,
                thread_count=s.thread_count,
                active_agent_count=s.active_agent_count,
                last_activity_at=s.last_activity_at,
            )
            for s in spheres
        ]
    
    async def get_sphere(self, sphere_id: str) -> SphereDetail:
        """
        Get sphere details with bureau sections.
        
        Args:
            sphere_id: Sphere ID
            
        Returns:
            SphereDetail with bureau sections
            
        Raises:
            SphereNotFoundError: If sphere not found
            IdentityBoundaryError: If sphere belongs to different identity
        """
        result = await self.db.execute(
            select(Sphere)
            .options(selectinload(Sphere.bureau_sections))
            .where(Sphere.id == sphere_id)
        )
        
        sphere = result.scalar_one_or_none()
        
        if not sphere:
            raise SphereNotFoundError(sphere_id=sphere_id)
        
        # Identity boundary check
        if sphere.identity_id != self.identity_id:
            raise IdentityBoundaryError(
                requested_identity=self.identity_id,
                resource_identity=sphere.identity_id,
                resource_type="Sphere",
            )
        
        # Get bureau sections
        bureau_sections = [
            BureauSectionResponse(
                id=s.id,
                type=s.section_type,
                name=s.name,
                icon=s.icon,
                is_active=s.is_active,
                display_order=s.display_order,
                item_count=s.item_count,
                unread_count=s.unread_count,
                has_unread=s.unread_count > 0,
            )
            for s in sorted(sphere.bureau_sections, key=lambda x: x.display_order)
        ]
        
        return SphereDetail(
            id=sphere.id,
            identity_id=sphere.identity_id,
            type=sphere.sphere_type,
            name=sphere.name,
            slug=sphere.slug,
            icon=sphere.icon,
            color=sphere.color,
            description=sphere.description,
            is_active=sphere.is_active,
            is_pinned=sphere.is_pinned,
            display_order=sphere.display_order,
            thread_count=sphere.thread_count,
            active_agent_count=sphere.active_agent_count,
            settings=sphere.settings,
            bureau_sections=bureau_sections,
            recent_threads=[],  # TODO: Fetch from Thread service
            created_at=sphere.created_at,
            updated_at=sphere.updated_at,
            last_activity_at=sphere.last_activity_at,
        )
    
    async def get_sphere_by_type(self, sphere_type: SphereType) -> SphereDetail:
        """Get sphere by type for current identity."""
        result = await self.db.execute(
            select(Sphere)
            .options(selectinload(Sphere.bureau_sections))
            .where(
                and_(
                    Sphere.identity_id == self.identity_id,
                    Sphere.sphere_type == sphere_type,
                )
            )
        )
        
        sphere = result.scalar_one_or_none()
        
        if not sphere:
            raise SphereNotFoundError(sphere_type=sphere_type.value)
        
        return await self.get_sphere(sphere.id)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SPHERE UPDATE
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def update_sphere(
        self,
        sphere_id: str,
        update_data: SphereUpdate,
    ) -> SphereDetail:
        """
        Update sphere settings.
        
        Note: sphere_type cannot be changed (FROZEN).
        """
        sphere = await self._get_sphere_with_check(sphere_id)
        
        # Update allowed fields
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            if value is not None:
                setattr(sphere, field, value)
        
        sphere.updated_at = datetime.utcnow()
        await self.db.commit()
        
        logger.info(f"Sphere updated: {sphere_id}")
        
        return await self.get_sphere(sphere_id)
    
    async def reorder_spheres(self, sphere_order: List[str]) -> List[SphereSummary]:
        """
        Reorder spheres by ID list.
        
        Args:
            sphere_order: List of sphere IDs in desired order
        """
        for idx, sphere_id in enumerate(sphere_order):
            await self.db.execute(
                update(Sphere)
                .where(
                    and_(
                        Sphere.id == sphere_id,
                        Sphere.identity_id == self.identity_id,
                    )
                )
                .values(display_order=idx)
            )
        
        await self.db.commit()
        
        return await self.list_spheres()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BUREAU SECTIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def get_bureau_sections(self, sphere_id: str) -> List[BureauSectionResponse]:
        """Get all bureau sections for a sphere."""
        await self._get_sphere_with_check(sphere_id)
        
        result = await self.db.execute(
            select(BureauSection)
            .where(BureauSection.sphere_id == sphere_id)
            .order_by(BureauSection.display_order)
        )
        
        sections = result.scalars().all()
        
        return [
            BureauSectionResponse(
                id=s.id,
                type=s.section_type,
                name=s.name,
                icon=s.icon,
                is_active=s.is_active,
                display_order=s.display_order,
                item_count=s.item_count,
                unread_count=s.unread_count,
                has_unread=s.unread_count > 0,
            )
            for s in sections
        ]
    
    async def get_bureau_section_content(
        self,
        sphere_id: str,
        section_type: BureauSectionType,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """
        Get content for a bureau section.
        
        Returns different content based on section type:
        - quick_capture: QuickCapture items
        - threads: Thread summaries
        - active_agents: Running agents
        - etc.
        """
        await self._get_sphere_with_check(sphere_id)
        
        if section_type == BureauSectionType.QUICK_CAPTURE:
            return await self._get_quick_capture_content(sphere_id, page, page_size)
        
        elif section_type == BureauSectionType.THREADS:
            # TODO: Integrate with Thread service
            return {"items": [], "total": 0}
        
        elif section_type == BureauSectionType.ACTIVE_AGENTS:
            # TODO: Integrate with Agent service
            return {"items": [], "total": 0}
        
        elif section_type == BureauSectionType.DATA_FILES:
            # TODO: Integrate with Storage service
            return {"items": [], "total": 0}
        
        elif section_type == BureauSectionType.MEETINGS:
            # TODO: Integrate with Calendar service
            return {"items": [], "total": 0}
        
        elif section_type == BureauSectionType.RESUME_WORKSPACE:
            # TODO: Integrate with Thread + Agent services
            return {"items": [], "total": 0}
        
        return {"items": [], "total": 0}
    
    # ═══════════════════════════════════════════════════════════════════════════
    # QUICK CAPTURE
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def create_quick_capture(
        self,
        sphere_id: str,
        request: QuickCaptureRequest,
        user_id: str,
    ) -> QuickCaptureResponse:
        """
        Create a quick capture in sphere inbox.
        
        Quick captures can be:
        - Notes
        - Tasks
        - Ideas
        - Links
        """
        await self._get_sphere_with_check(sphere_id)
        
        capture = QuickCapture(
            id=str(uuid4()),
            identity_id=self.identity_id,
            sphere_id=sphere_id,
            content=request.content,
            capture_type=QuickCaptureType(request.type.value),
            status=QuickCaptureStatus.CAPTURED,
            tags=request.tags,
            target_thread_id=request.target_thread_id,
            source="api",
            created_by=user_id,
        )
        
        self.db.add(capture)
        
        # Update section item count
        await self._increment_section_count(
            sphere_id,
            BureauSectionType.QUICK_CAPTURE,
        )
        
        # Update sphere activity
        await self._update_sphere_activity(sphere_id)
        
        await self.db.commit()
        
        logger.info(f"Quick capture created: {capture.id} in sphere {sphere_id}")
        
        return QuickCaptureResponse.model_validate(capture)
    
    async def _get_quick_capture_content(
        self,
        sphere_id: str,
        page: int,
        page_size: int,
    ) -> dict:
        """Get quick captures for a sphere."""
        offset = (page - 1) * page_size
        
        # Count total
        count_result = await self.db.execute(
            select(func.count(QuickCapture.id))
            .where(
                and_(
                    QuickCapture.sphere_id == sphere_id,
                    QuickCapture.identity_id == self.identity_id,
                    QuickCapture.status != QuickCaptureStatus.ARCHIVED,
                )
            )
        )
        total = count_result.scalar() or 0
        
        # Get items
        result = await self.db.execute(
            select(QuickCapture)
            .where(
                and_(
                    QuickCapture.sphere_id == sphere_id,
                    QuickCapture.identity_id == self.identity_id,
                    QuickCapture.status != QuickCaptureStatus.ARCHIVED,
                )
            )
            .order_by(QuickCapture.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        
        items = [
            QuickCaptureResponse.model_validate(c).model_dump()
            for c in result.scalars().all()
        ]
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STATISTICS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def get_sphere_stats(
        self,
        sphere_id: str,
        period: str = "week",
    ) -> SphereStats:
        """
        Get sphere statistics for a time period.
        
        Args:
            sphere_id: Sphere ID
            period: day, week, month, year
        """
        await self._get_sphere_with_check(sphere_id)
        
        # Calculate date range
        now = datetime.utcnow()
        if period == "day":
            start_date = now - timedelta(days=1)
        elif period == "week":
            start_date = now - timedelta(weeks=1)
        elif period == "month":
            start_date = now - timedelta(days=30)
        elif period == "year":
            start_date = now - timedelta(days=365)
        else:
            start_date = now - timedelta(weeks=1)
        
        # TODO: Integrate with Thread and Agent services for real stats
        # For now, return placeholder data
        
        return SphereStats(
            sphere_id=sphere_id,
            period=period,
            thread_count=0,
            new_threads=0,
            total_events=0,
            agent_executions=0,
            tokens_used=0,
            decision_points=0,
            checkpoints_resolved=0,
        )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PRIVATE HELPERS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def _get_sphere_with_check(self, sphere_id: str) -> Sphere:
        """Get sphere and verify identity boundary."""
        result = await self.db.execute(
            select(Sphere).where(Sphere.id == sphere_id)
        )
        
        sphere = result.scalar_one_or_none()
        
        if not sphere:
            raise SphereNotFoundError(sphere_id=sphere_id)
        
        if sphere.identity_id != self.identity_id:
            raise IdentityBoundaryError(
                requested_identity=self.identity_id,
                resource_identity=sphere.identity_id,
                resource_type="Sphere",
            )
        
        return sphere
    
    async def _increment_section_count(
        self,
        sphere_id: str,
        section_type: BureauSectionType,
        amount: int = 1,
    ) -> None:
        """Increment item count for a bureau section."""
        await self.db.execute(
            update(BureauSection)
            .where(
                and_(
                    BureauSection.sphere_id == sphere_id,
                    BureauSection.section_type == section_type,
                )
            )
            .values(
                item_count=BureauSection.item_count + amount,
                unread_count=BureauSection.unread_count + amount,
            )
        )
    
    async def _update_sphere_activity(self, sphere_id: str) -> None:
        """Update sphere last activity timestamp."""
        await self.db.execute(
            update(Sphere)
            .where(Sphere.id == sphere_id)
            .values(last_activity_at=datetime.utcnow())
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

def get_sphere_service(db: AsyncSession, identity_id: str) -> SphereService:
    """Factory function for SphereService."""
    return SphereService(db, identity_id)
