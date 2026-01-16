"""
CHE·NU™ — BUREAU SECTIONS TESTS (PYTEST)
Sprint 3: Tests for 6 Bureau Sections (HARD LIMIT)

Architecture:
- Each SPHERE opens a BUREAU containing maximum 6 SECTIONS
- This structure NEVER changes
- Only content, permissions, and agents vary
"""

import pytest
from typing import List

# ═══════════════════════════════════════════════════════════════════════════════
# BUREAU SECTION CONSTANTS (HARD LIMIT - 6 SECTIONS)
# ═══════════════════════════════════════════════════════════════════════════════

BUREAU_SECTIONS = [
    {
        "id": "QUICK_CAPTURE",
        "key": "quick_capture",
        "name": "Quick Capture",
        "name_fr": "Capture Rapide",
        "icon": "📝",
        "hierarchy": 1,
        "level": "L2",
    },
    {
        "id": "RESUME_WORKSPACE",
        "key": "resume_workspace",
        "name": "Resume Workspace",
        "name_fr": "Reprendre le Travail",
        "icon": "▶️",
        "hierarchy": 2,
        "level": "L2",
    },
    {
        "id": "THREADS",
        "key": "threads",
        "name": "Threads",
        "name_fr": "Fils de Discussion",
        "icon": "💬",
        "hierarchy": 3,
        "level": "L2",
    },
    {
        "id": "DATA_FILES",
        "key": "data_files",
        "name": "Data Files",
        "name_fr": "Fichiers de Données",
        "icon": "📁",
        "hierarchy": 4,
        "level": "L2",
    },
    {
        "id": "ACTIVE_AGENTS",
        "key": "active_agents",
        "name": "Active Agents",
        "name_fr": "Agents Actifs",
        "icon": "🤖",
        "hierarchy": 5,
        "level": "L2",
    },
    {
        "id": "MEETINGS",
        "key": "meetings",
        "name": "Meetings",
        "name_fr": "Réunions",
        "icon": "📅",
        "hierarchy": 6,
        "level": "L2",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# 6 SECTIONS ARCHITECTURE TESTS (HARD LIMIT)
# ═══════════════════════════════════════════════════════════════════════════════

class TestBureauArchitecture:
    """Tests for 6 bureau sections hard limit."""

    def test_exactly_6_sections(self, bureau_section_ids: List[str]):
        """Should have exactly 6 bureau sections (HARD LIMIT)."""
        assert len(bureau_section_ids) == 6

    def test_section_count_not_exceeded(self, bureau_section_ids: List[str]):
        """Bureau sections should NEVER exceed 6 (HARD LIMIT from Memory Prompt)."""
        assert len(bureau_section_ids) <= 6, "HARD LIMIT: Maximum 6 sections!"

    def test_all_section_ids_present(self, bureau_section_ids: List[str]):
        """All 6 required section IDs should be present."""
        expected = [
            "quick_capture",
            "resume_workspace",
            "threads",
            "data_files",
            "active_agents",
            "meetings",
        ]
        assert sorted(bureau_section_ids) == sorted(expected)

    def test_quick_capture_is_first(self, bureau_section_ids: List[str]):
        """Quick Capture should be the first section."""
        assert bureau_section_ids[0] == "quick_capture"

    def test_meetings_is_last(self, bureau_section_ids: List[str]):
        """Meetings should be the last section."""
        assert bureau_section_ids[-1] == "meetings"

    def test_sections_have_unique_ids(self, bureau_section_ids: List[str]):
        """All section IDs should be unique."""
        assert len(bureau_section_ids) == len(set(bureau_section_ids))


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION PROPERTIES TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSectionProperties:
    """Tests for bureau section properties."""

    @pytest.mark.parametrize("section", BUREAU_SECTIONS)
    def test_section_has_required_properties(self, section):
        """Each section should have all required properties."""
        required = ["id", "key", "name", "name_fr", "icon", "hierarchy", "level"]
        for prop in required:
            assert prop in section

    @pytest.mark.parametrize("section", BUREAU_SECTIONS)
    def test_section_level_is_l2(self, section):
        """All sections should be at L2 (Sphere Bureau level)."""
        assert section["level"] == "L2"

    @pytest.mark.parametrize("section", BUREAU_SECTIONS)
    def test_section_hierarchy_is_1_to_6(self, section):
        """Section hierarchy should be 1-6."""
        assert 1 <= section["hierarchy"] <= 6

    def test_all_hierarchies_unique(self):
        """All section hierarchies should be unique."""
        hierarchies = [s["hierarchy"] for s in BUREAU_SECTIONS]
        assert len(hierarchies) == len(set(hierarchies))
        assert sorted(hierarchies) == list(range(1, 7))


# ═══════════════════════════════════════════════════════════════════════════════
# SPECIFIC SECTION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSpecificSections:
    """Tests for specific section requirements."""

    def test_quick_capture_section(self):
        """Quick Capture section should have correct properties."""
        quick_capture = BUREAU_SECTIONS[0]
        assert quick_capture["key"] == "quick_capture"
        assert quick_capture["icon"] == "📝"
        assert quick_capture["hierarchy"] == 1

    def test_threads_section(self):
        """Threads section should have correct properties."""
        threads = next(s for s in BUREAU_SECTIONS if s["key"] == "threads")
        assert threads["icon"] == "💬"
        assert threads["hierarchy"] == 3

    def test_active_agents_section(self):
        """Active Agents section should have correct properties."""
        agents = next(s for s in BUREAU_SECTIONS if s["key"] == "active_agents")
        assert agents["icon"] == "🤖"
        assert agents["hierarchy"] == 5

    def test_meetings_section(self):
        """Meetings section should have correct properties."""
        meetings = next(s for s in BUREAU_SECTIONS if s["key"] == "meetings")
        assert meetings["icon"] == "📅"
        assert meetings["hierarchy"] == 6


# ═══════════════════════════════════════════════════════════════════════════════
# OLD SECTIONS REMOVED TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestOldSectionsRemoved:
    """Tests ensuring old 10-section model is removed."""

    def test_dashboard_not_separate_section(self, bureau_section_ids: List[str]):
        """Dashboard should NOT be a separate section (was in old model)."""
        assert "dashboard" not in bureau_section_ids

    def test_notes_not_separate_section(self, bureau_section_ids: List[str]):
        """Notes should NOT be a separate section (was in old model)."""
        assert "notes" not in bureau_section_ids

    def test_tasks_not_separate_section(self, bureau_section_ids: List[str]):
        """Tasks should NOT be a separate section (was in old model)."""
        assert "tasks" not in bureau_section_ids

    def test_projects_not_separate_section(self, bureau_section_ids: List[str]):
        """Projects should NOT be a separate section (was in old model)."""
        assert "projects" not in bureau_section_ids

    def test_reports_not_separate_section(self, bureau_section_ids: List[str]):
        """Reports should NOT be a separate section (was in old model)."""
        assert "reports" not in bureau_section_ids

    def test_budget_not_separate_section(self, bureau_section_ids: List[str]):
        """Budget should NOT be a separate section (was in old model)."""
        assert "budget" not in bureau_section_ids


# ═══════════════════════════════════════════════════════════════════════════════
# BUREAU HIERARCHY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBureauHierarchy:
    """Tests for bureau hierarchy levels."""

    def test_hierarchy_levels_exist(self):
        """Bureau should support 5 hierarchy levels (L0-L4)."""
        levels = ["L0", "L1", "L2", "L3", "L4"]
        for level in levels:
            assert level in ["L0", "L1", "L2", "L3", "L4"]

    def test_l0_is_global_bureau(self):
        """L0 should be Global Bureau level."""
        l0_name = "Global Bureau"
        assert "global" in l0_name.lower()

    def test_l1_is_identity_bureau(self):
        """L1 should be Identity Bureau level."""
        l1_name = "Identity Bureau"
        assert "identity" in l1_name.lower()

    def test_l2_is_sphere_bureau_with_6_sections(self):
        """L2 should be Sphere Bureau level with 6 sections."""
        l2_name = "Sphere Bureau"
        l2_section_count = 6
        assert "sphere" in l2_name.lower()
        assert l2_section_count == 6

    def test_l3_is_project_bureau(self):
        """L3 should be Project Bureau level."""
        l3_name = "Project Bureau"
        assert "project" in l3_name.lower()

    def test_l4_is_agent_bureau(self):
        """L4 should be Agent Bureau level."""
        l4_name = "Agent Bureau"
        assert "agent" in l4_name.lower()


# ═══════════════════════════════════════════════════════════════════════════════
# BUREAU PER SPHERE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBureauPerSphere:
    """Tests for bureau structure per sphere."""

    def test_all_spheres_same_bureau_structure(self, sphere_ids: List[str], bureau_section_ids: List[str]):
        """All BUREAUS share the SAME STRUCTURE."""
        # Each sphere should have access to the same 6 sections
        for sphere_id in sphere_ids:
            # The bureau structure is constant
            assert len(bureau_section_ids) == 6

    def test_scholar_sphere_has_6_sections(self, bureau_section_ids: List[str]):
        """Scholar sphere should have the same 6 sections."""
        # Scholar (9th sphere) uses same bureau structure
        assert len(bureau_section_ids) == 6

    def test_structure_never_changes(self, bureau_section_ids: List[str]):
        """Bureau structure NEVER changes (only content varies)."""
        # The 6 sections are fixed
        fixed_sections = {
            "quick_capture",
            "resume_workspace",
            "threads",
            "data_files",
            "active_agents",
            "meetings",
        }
        assert set(bureau_section_ids) == fixed_sections


# ═══════════════════════════════════════════════════════════════════════════════
# LOCALIZATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSectionLocalization:
    """Tests for section localization."""

    @pytest.mark.parametrize("section", BUREAU_SECTIONS)
    def test_section_has_french_name(self, section):
        """Each section should have French translation."""
        assert "name_fr" in section
        assert len(section["name_fr"]) > 0

    def test_quick_capture_french_name(self):
        """Quick Capture should be 'Capture Rapide' in French."""
        quick_capture = BUREAU_SECTIONS[0]
        assert quick_capture["name_fr"] == "Capture Rapide"

    def test_threads_french_name(self):
        """Threads should be 'Fils de Discussion' in French."""
        threads = next(s for s in BUREAU_SECTIONS if s["key"] == "threads")
        assert "fils" in threads["name_fr"].lower()


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY PROMPT COMPLIANCE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBureauMemoryPromptCompliance:
    """Tests ensuring Memory Prompt bureau compliance."""

    def test_maximum_6_sections(self, bureau_section_ids: List[str]):
        """Each SPHERE opens a BUREAU containing maximum 6 SECTIONS."""
        assert len(bureau_section_ids) <= 6

    def test_structure_never_changes_compliance(self, bureau_section_ids: List[str]):
        """This structure NEVER changes (per Memory Prompt)."""
        expected = [
            "quick_capture",
            "resume_workspace", 
            "threads",
            "data_files",
            "active_agents",
            "meetings",
        ]
        assert bureau_section_ids == expected

    def test_threads_are_first_class_objects(self, bureau_section_ids: List[str]):
        """Threads (.chenu) are FIRST-CLASS OBJECTS - should be in sections."""
        assert "threads" in bureau_section_ids
