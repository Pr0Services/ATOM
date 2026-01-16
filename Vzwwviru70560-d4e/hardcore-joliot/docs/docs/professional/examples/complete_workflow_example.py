"""
CHE·NU Cross-Sphere Integration — Complete Example
Version: 1.0 CANONICAL

This example demonstrates a complete end-to-end workflow:
1. Create Community group
2. Propose social page
3. Approve and create page
4. Create event
5. Stage event for social sharing
6. Review and publish
7. Undo if needed

This is a CANONICAL implementation showing all validation gates.
"""

import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

# Imports (assuming proper structure)
from backend.community_canonical_models import (
    CommunityGroupDB,
    CommunityEventDB,
    CommunityGroupType,
    EventVisibility,
    prepare_event_social_content
)
from backend.cross_sphere_canonical_models import (
    CrossSphereRequestDB,
    StagedCrossSphereContentDB,
    CrossSphereActionDB,
    Sphere,
    ConnectionType,
    RequestStatus,
    ContentStatus,
    generate_undo_patch,
    log_audit_event
)


# ═══════════════════════════════════════════════════════════════════════
# EXAMPLE 1: Complete Community → Social Workflow
# ═══════════════════════════════════════════════════════════════════════

async def example_community_to_social_complete():
    """
    Complete example: Community group creates social page and shares event.
    
    This demonstrates ALL validation gates and audit trails.
    """
    
    print("=" * 80)
    print("EXAMPLE: Community Group → Social Page")
    print("=" * 80)
    
    # Simulate user
    user_id = uuid4()
    print(f"\n👤 User ID: {user_id}")
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 1: Create Community Group
    # ═════════════════════════════════════════════════════════════════
    
    print("\n📝 STEP 1: Create Community Group")
    print("-" * 80)
    
    group = CommunityGroupDB(
        id=uuid4(),
        name="Vélo MTL",
        description="Club de cyclisme à Montréal - sorties hebdomadaires",
        type=CommunityGroupType.CLUB,
        creator_id=user_id,
        admins=[str(user_id)],
        members=[str(user_id)],
        member_count=1,
        is_private=False,
        requires_approval_to_join=True,
        has_social_page=False,  # Not yet
        created_at=datetime.utcnow()
    )
    
    print(f"✅ Group created: {group.name}")
    print(f"   ID: {group.id}")
    print(f"   Type: {group.type}")
    print(f"   Has social page: {group.has_social_page}")
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 2: Propose Social Page Creation (HUMAN DECISION)
    # ═════════════════════════════════════════════════════════════════
    
    print("\n📢 STEP 2: Propose Social Page Creation")
    print("-" * 80)
    
    # UI shows dialog: "Create public social page?"
    print("🎯 UI Dialog shown to user:")
    print("   'Create public social page for Vélo MTL?'")
    print("   - Preview: Page name, description, settings")
    print("   - Explanation: What will be shared, who can see")
    print("   - Undo option: Explained")
    
    # User clicks "Create Social Page" (EXPLICIT ACTION)
    print("\n👆 User clicks: 'Create Social Page'")
    print("   (This is HUMAN APPROVAL — explicit click)")
    
    # Create Cross-Sphere Request
    request = CrossSphereRequestDB(
        id=uuid4(),
        connection_type=ConnectionType.REQUEST,
        source_sphere=Sphere.COMMUNITY,
        source_entity_id=str(group.id),
        source_entity_type="community_group",
        target_sphere=Sphere.SOCIAL_MEDIA,
        target_entity_type="social_page",
        action_type="create_social_page",
        action_details={
            "page_name": "Vélo MTL",
            "page_description": "Club de cyclisme à Montréal",
            "page_category": "Sports & Recreation",
            "page_visibility": "public"
        },
        status=RequestStatus.PENDING,
        requires_human_validation=True,
        requested_by=user_id,
        requested_at=datetime.utcnow(),
        request_reasoning="Want to reach more cyclists in Montreal and grow our community",
        audit_trail=[
            log_audit_event(
                performed_by=str(user_id),
                action_type="create_request",
                source_sphere=Sphere.COMMUNITY,
                target_sphere=Sphere.SOCIAL_MEDIA,
                details={
                    "method": "explicit_click",
                    "ui_component": "CreateSocialPageDialog"
                }
            )
        ]
    )
    
    print(f"\n✅ Cross-Sphere Request created:")
    print(f"   Request ID: {request.id}")
    print(f"   Connection Type: {request.connection_type}")
    print(f"   Status: {request.status}")
    print(f"   Source: {request.source_sphere}")
    print(f"   Target: {request.target_sphere}")
    print(f"   Reasoning: {request.request_reasoning}")
    
    # Update group
    group.social_page_request_id = request.id
    group.social_page_creation_proposed = True
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 3: Validation Gate — Human Approves
    # ═════════════════════════════════════════════════════════════════
    
    print("\n✅ STEP 3: Validation Gate")
    print("-" * 80)
    
    # For own groups, approval can be immediate
    # For organizational groups, may require admin review
    
    print("🎯 Validation process:")
    print("   - Request visible in 'Pending Requests' UI")
    print("   - User reviews: action type, source, target")
    print("   - User clicks 'Approve' button")
    
    # Simulate approval
    print("\n👆 User clicks: 'Approve Request'")
    print("   (HUMAN VALIDATION GATE — explicit approval)")
    
    request.status = RequestStatus.APPROVED
    request.reviewed_by = user_id
    request.reviewed_at = datetime.utcnow()
    request.approved_by = user_id
    request.approved_at = datetime.utcnow()
    
    request.audit_trail.append(
        log_audit_event(
            performed_by=str(user_id),
            action_type="approve_request",
            source_sphere=request.source_sphere,
            target_sphere=request.target_sphere,
            details={
                "method": "explicit_click",
                "ui_component": "ApproveButton"
            }
        )
    )
    
    print(f"\n✅ Request approved:")
    print(f"   Approved by: {request.approved_by}")
    print(f"   Approved at: {request.approved_at}")
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 4: Execute — Create Social Page
    # ═════════════════════════════════════════════════════════════════
    
    print("\n🚀 STEP 4: Execute Request — Create Social Page")
    print("-" * 80)
    
    # Create social page in Social Sphere
    social_page_id = f"page_{uuid4()}"
    
    # Generate undo patch
    undo_patch = generate_undo_patch(
        action_type="create_social_page",
        original_data={
            "group_id": str(group.id),
            "group_had_social_page": False
        },
        created_ids=[social_page_id]
    )
    
    # Update request
    request.status = RequestStatus.EXECUTED
    request.executed_at = datetime.utcnow()
    request.execution_result = {
        "social_page_id": social_page_id,
        "page_url": f"https://chenu.ai/social/pages/{social_page_id}"
    }
    request.target_entity_id = social_page_id
    request.undo_patch = undo_patch
    
    # Update group
    group.has_social_page = True
    group.social_page_id = social_page_id
    group.social_page_creation_approved_by = user_id
    group.social_page_creation_approved_at = datetime.utcnow()
    
    # Log action in audit trail
    action = CrossSphereActionDB(
        id=uuid4(),
        performed_by=user_id,
        action_type="create_social_page",
        source_sphere=request.source_sphere,
        source_entity_id=request.source_entity_id,
        target_sphere=request.target_sphere,
        target_entity_id=social_page_id,
        timestamp=datetime.utcnow(),
        reasoning="Approved social page creation for community outreach",
        method="explicit_click",
        request_id=request.id,
        required_validation=True,
        validated_by=user_id,
        validated_at=datetime.utcnow(),
        validation_decision="approve",
        is_reversible=True,
        undo_patch=undo_patch
    )
    
    print(f"✅ Social page created:")
    print(f"   Page ID: {social_page_id}")
    print(f"   Page URL: {request.execution_result['page_url']}")
    print(f"   Reversible: {action.is_reversible}")
    print(f"   Undo patch: Generated ✓")
    
    print(f"\n📊 Audit trail:")
    print(f"   Action ID: {action.id}")
    print(f"   Performed by: {action.performed_by}")
    print(f"   Timestamp: {action.timestamp}")
    print(f"   Logged in: cross_sphere_actions table")
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 5: Create Community Event
    # ═════════════════════════════════════════════════════════════════
    
    print("\n🎉 STEP 5: Create Community Event")
    print("-" * 80)
    
    event = CommunityEventDB(
        id=uuid4(),
        group_id=group.id,
        name="Sortie vélo dimanche — Mont-Royal",
        description="Rendez-vous 10h au pied du Mont-Royal. Environ 20km, niveau intermédiaire.",
        event_date=datetime.utcnow() + timedelta(days=7),
        location="Mont-Royal, Montréal",
        is_online=False,
        max_participants=15,
        created_by=user_id,
        organizers=[str(user_id)],
        visibility=EventVisibility.PUBLIC,
        visible_to_non_members=False,
        share_on_social_proposed=False,
        share_on_social_status="not_proposed",
        created_at=datetime.utcnow()
    )
    
    print(f"✅ Event created:")
    print(f"   Event ID: {event.id}")
    print(f"   Name: {event.name}")
    print(f"   Date: {event.event_date}")
    print(f"   Location: {event.location}")
    print(f"   Share status: {event.share_on_social_status}")
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 6: Propose Sharing Event on Social Page (STAGING)
    # ═════════════════════════════════════════════════════════════════
    
    print("\n📤 STEP 6: Propose Sharing Event on Social Page")
    print("-" * 80)
    
    # System prepares content
    prepared_content = prepare_event_social_content(event)
    
    print("🎯 System prepares content (STAGING):")
    print(f"   Title: {prepared_content['title']}")
    print(f"   Description: {prepared_content['description'][:50]}...")
    print(f"   Date: {prepared_content['date']}")
    print(f"   Location: {prepared_content['location']}")
    
    # Create staged content (QUARANTINED)
    staged = StagedCrossSphereContentDB(
        id=uuid4(),
        status=ContentStatus.QUARANTINED,
        source_sphere=Sphere.COMMUNITY,
        source_entity_id=str(group.id),
        source_entity_type="community_group",
        source_content_id=str(event.id),
        target_sphere=Sphere.SOCIAL_MEDIA,
        target_page_id=group.social_page_id,
        target_page_type="social_page",
        content_type="event",
        prepared_content=prepared_content,
        requires_validation=True,
        prepared_by=user_id,
        prepared_at=datetime.utcnow()
    )
    
    # Update event
    event.staged_content_id = staged.id
    event.share_on_social_proposed = True
    event.share_on_social_status = "staged"
    
    print(f"\n✅ Content staged:")
    print(f"   Staged ID: {staged.id}")
    print(f"   Status: {staged.status} (QUARANTINED)")
    print(f"   Requires validation: {staged.requires_validation}")
    
    print("\n🎯 UI shows proposal:")
    print("   'Share this event on social page?'")
    print("   - Shows prepared post preview")
    print("   - User can edit before sharing")
    print("   - User can schedule publication")
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 7: Human Reviews & Approves (VALIDATION GATE)
    # ═════════════════════════════════════════════════════════════════
    
    print("\n✅ STEP 7: Human Reviews & Approves")
    print("-" * 80)
    
    print("👁️  User reviews prepared content:")
    print("   - Sees exact preview as it will appear")
    print("   - Checks title, description, date, location")
    print("   - Verifies visibility settings")
    
    print("\n👆 User clicks: 'Publish Now'")
    print("   (HUMAN VALIDATION GATE — explicit publish)")
    
    # Validate
    staged.status = ContentStatus.VALIDATED
    staged.validated_by = user_id
    staged.validated_at = datetime.utcnow()
    staged.validation_decision = "approve"
    staged.validation_notes = "Event details verified, ready to publish"
    
    # Publish to Social Sphere
    social_post_id = f"post_{uuid4()}"
    
    # Generate undo patch
    post_undo_patch = generate_undo_patch(
        action_type="publish_content",
        original_data={"staged_id": str(staged.id)},
        created_ids=[social_post_id]
    )
    
    staged.published = True
    staged.published_by = user_id
    staged.published_at = datetime.utcnow()
    staged.published_post_id = social_post_id
    staged.status = ContentStatus.PUBLISHED
    staged.undo_patch = post_undo_patch
    
    # Update event
    event.share_on_social_status = "published"
    event.social_post_id = social_post_id
    event.social_post_undo_patch = post_undo_patch
    event.share_approved_by = user_id
    event.share_approved_at = datetime.utcnow()
    
    # Log action
    publish_action = CrossSphereActionDB(
        id=uuid4(),
        performed_by=user_id,
        action_type="publish_content",
        source_sphere=Sphere.COMMUNITY,
        source_entity_id=str(event.id),
        target_sphere=Sphere.SOCIAL_MEDIA,
        target_entity_id=social_post_id,
        timestamp=datetime.utcnow(),
        reasoning="Event shared for public visibility and community growth",
        method="explicit_click",
        staged_content_id=staged.id,
        required_validation=True,
        validated_by=user_id,
        validated_at=datetime.utcnow(),
        validation_decision="approve",
        is_reversible=True,
        undo_patch=post_undo_patch
    )
    
    print(f"\n✅ Content published:")
    print(f"   Post ID: {social_post_id}")
    print(f"   Post URL: https://chenu.ai/social/posts/{social_post_id}")
    print(f"   Published by: {staged.published_by}")
    print(f"   Published at: {staged.published_at}")
    print(f"   Reversible: {publish_action.is_reversible}")
    
    print(f"\n📊 Audit trail:")
    print(f"   Action ID: {publish_action.id}")
    print(f"   Type: {publish_action.action_type}")
    print(f"   Route: {publish_action.source_sphere} → {publish_action.target_sphere}")
    print(f"   Timestamp: {publish_action.timestamp}")
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 8: Undo (REVERSIBILITY)
    # ═════════════════════════════════════════════════════════════════
    
    print("\n↩️  STEP 8: Undo Example (Optional)")
    print("-" * 80)
    
    print("🎯 UI shows undo button:")
    print("   'Undo share ↩' (available)")
    
    print("\n💡 If user clicks undo:")
    print("   1. User must provide reasoning (required)")
    print("   2. Confirmation dialog shown")
    print("   3. Undo patch applied:")
    print(f"      - Delete post: {social_post_id}")
    print(f"      - Update event: share_status → 'undone'")
    print(f"      - Update staged: status → 'undone'")
    print("   4. Action logged:")
    print("      - undo_performed = True")
    print("      - undo_by = user_id")
    print("      - undo_reasoning = '...'")
    
    # ═════════════════════════════════════════════════════════════════
    # SUMMARY
    # ═════════════════════════════════════════════════════════════════
    
    print("\n" + "=" * 80)
    print("📊 WORKFLOW SUMMARY")
    print("=" * 80)
    
    print("\n✅ Actions performed:")
    print("   1. Created Community group")
    print("   2. Proposed social page (HUMAN DECISION)")
    print("   3. Approved request (VALIDATION GATE)")
    print("   4. Created social page with audit trail")
    print("   5. Created community event")
    print("   6. Staged event for sharing (QUARANTINE)")
    print("   7. Reviewed and published (VALIDATION GATE)")
    print("   8. Full reversibility available")
    
    print("\n✅ Guarantees:")
    print("   ✓ Human sovereignty — Every action approved")
    print("   ✓ No silent action — All staging → validation → publish")
    print("   ✓ Reversibility — Undo patches generated")
    print("   ✓ Auditability — Complete trail in cross_sphere_actions")
    print("   ✓ Connection type — REQUEST (canonical)")
    
    print("\n📊 Database records created:")
    print(f"   cross_sphere_requests: 1 (create page)")
    print(f"   staged_cross_sphere_content: 1 (event share)")
    print(f"   cross_sphere_actions: 2 (page creation + publish)")
    print(f"   community_groups: 1")
    print(f"   community_events: 1")
    
    print("\n" + "=" * 80)
    print("✅ CANONICAL WORKFLOW COMPLETE")
    print("=" * 80)


# ═══════════════════════════════════════════════════════════════════════
# RUN EXAMPLE
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Run complete example
    asyncio.run(example_community_to_social_complete())
    
    print("\n\n💡 Key Takeaways:")
    print("   1. NO auto-publishing — everything requires human approval")
    print("   2. Staging area (quarantine) before validation")
    print("   3. Per-action approval (not batch)")
    print("   4. Full audit trail with who/what/when/why/how")
    print("   5. Complete reversibility with undo patches")
    print("   6. Connection type: REQUEST (one of 4 allowed)")
    
    print("\n🎯 This is the CANONICAL way.")
    print("   Safe. Traceable. Human-controlled.")
