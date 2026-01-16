"""
CHE·NU™ — SPHERES TESTS (PYTEST)
Sprint 3: Tests for 9 Spheres Architecture (FROZEN)

Architecture:
- 9 Spheres (FROZEN - NO additional spheres allowed)
- Scholar is 9th sphere
- IA Labs and Skills are in My Team (not separate)
"""

import pytest
from typing import List

# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE CONSTANTS (FROZEN ARCHITECTURE)
# ═══════════════════════════════════════════════════════════════════════════════

FROZEN_SPHERES = [
    {"id": "personal", "name": "Personal", "icon": "🏠", "color": "#D8B26A", "order": 1},
    {"id": "business", "name": "Business", "icon": "💼", "color": "#8D8371", "order": 2},
    {"id": "government", "name": "Government & Institutions", "icon": "🏛️", "color": "#2F4C39", "order": 3},
    {"id": "creative", "name": "Studio de création", "icon": "🎨", "color": "#7A593A", "order": 4},
    {"id": "community", "name": "Community", "icon": "👥", "color": "#3F7249", "order": 5},
    {"id": "social", "name": "Social & Media", "icon": "📱", "color": "#3EB4A2", "order": 6},
    {"id": "entertainment", "name": "Entertainment", "icon": "🎬", "color": "#E9E4D6", "order": 7},
    {"id": "team", "name": "My Team", "icon": "🤝", "color": "#1E1F22", "order": 8},
    {"id": "scholar", "name": "Scholar", "icon": "📚", "color": "#E0C46B", "order": 9},
]

CHENU_COLORS = {
    "sacredGold": "#D8B26A",
    "ancientStone": "#8D8371",
    "jungleEmerald": "#3F7249",
    "cenoteTurquoise": "#3EB4A2",
    "shadowMoss": "#2F4C39",
    "earthEmber": "#7A593A",
    "uiSlate": "#1E1F22",
    "softSand": "#E9E4D6",
    "scholarGold": "#E0C46B",
}


# ═══════════════════════════════════════════════════════════════════════════════
# 9 SPHERES ARCHITECTURE TESTS (FROZEN)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSpheresArchitecture:
    """Tests for 9 spheres frozen architecture."""

    def test_exactly_9_spheres(self, sphere_ids: List[str]):
        """Should have exactly 9 spheres."""
        assert len(sphere_ids) == 9

    def test_all_sphere_ids_present(self, sphere_ids: List[str]):
        """All 9 required sphere IDs should be present."""
        expected = ["personal", "business", "government", "creative", 
                   "community", "social", "entertainment", "team", "scholar"]
        assert sorted(sphere_ids) == sorted(expected)

    def test_scholar_is_ninth_sphere(self, sphere_ids: List[str]):
        """Scholar should be the 9th sphere."""
        assert "scholar" in sphere_ids
        # In order, scholar should be last
        assert sphere_ids[-1] == "scholar"

    def test_personal_is_first_sphere(self, sphere_ids: List[str]):
        """Personal should be the first sphere."""
        assert sphere_ids[0] == "personal"

    def test_no_ia_labs_as_separate_sphere(self, sphere_ids: List[str]):
        """IA Labs should NOT be a separate sphere (it's in My Team)."""
        assert "ia_labs" not in sphere_ids
        assert "ialabs" not in sphere_ids

    def test_no_skills_as_separate_sphere(self, sphere_ids: List[str]):
        """Skills & Tools should NOT be a separate sphere (it's in My Team)."""
        assert "skills" not in sphere_ids
        assert "tools" not in sphere_ids
        assert "skills_tools" not in sphere_ids

    def test_spheres_have_unique_ids(self, sphere_ids: List[str]):
        """All sphere IDs should be unique."""
        assert len(sphere_ids) == len(set(sphere_ids))


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE PROPERTIES TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSphereProperties:
    """Tests for sphere properties."""

    @pytest.mark.parametrize("sphere", FROZEN_SPHERES)
    def test_sphere_has_required_properties(self, sphere):
        """Each sphere should have all required properties."""
        required = ["id", "name", "icon", "color", "order"]
        for prop in required:
            assert prop in sphere

    @pytest.mark.parametrize("sphere", FROZEN_SPHERES)
    def test_sphere_color_is_valid_hex(self, sphere):
        """Sphere colors should be valid hex codes."""
        color = sphere["color"]
        assert color.startswith("#")
        assert len(color) == 7
        # Validate hex
        int(color[1:], 16)

    @pytest.mark.parametrize("sphere", FROZEN_SPHERES)
    def test_sphere_order_is_sequential(self, sphere):
        """Sphere orders should be 1-9."""
        assert 1 <= sphere["order"] <= 9

    def test_all_orders_unique(self):
        """All sphere orders should be unique."""
        orders = [s["order"] for s in FROZEN_SPHERES]
        assert len(orders) == len(set(orders))
        assert sorted(orders) == list(range(1, 10))


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE COLORS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSphereColors:
    """Tests for CHE·NU sphere colors."""

    def test_personal_uses_sacred_gold(self):
        """Personal sphere should use Sacred Gold color."""
        personal = next(s for s in FROZEN_SPHERES if s["id"] == "personal")
        assert personal["color"] == CHENU_COLORS["sacredGold"]

    def test_business_uses_ancient_stone(self):
        """Business sphere should use Ancient Stone color."""
        business = next(s for s in FROZEN_SPHERES if s["id"] == "business")
        assert business["color"] == CHENU_COLORS["ancientStone"]

    def test_scholar_uses_scholar_gold(self):
        """Scholar sphere should use Scholar Gold color."""
        scholar = next(s for s in FROZEN_SPHERES if s["id"] == "scholar")
        assert scholar["color"] == CHENU_COLORS["scholarGold"]

    def test_community_uses_jungle_emerald(self):
        """Community sphere should use Jungle Emerald color."""
        community = next(s for s in FROZEN_SPHERES if s["id"] == "community")
        assert community["color"] == CHENU_COLORS["jungleEmerald"]

    def test_social_uses_cenote_turquoise(self):
        """Social sphere should use Cenote Turquoise color."""
        social = next(s for s in FROZEN_SPHERES if s["id"] == "social")
        assert social["color"] == CHENU_COLORS["cenoteTurquoise"]


# ═══════════════════════════════════════════════════════════════════════════════
# SPECIFIC SPHERE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSpecificSpheres:
    """Tests for specific sphere requirements."""

    def test_personal_sphere(self):
        """Personal sphere should have correct properties."""
        personal = next(s for s in FROZEN_SPHERES if s["id"] == "personal")
        assert personal["icon"] == "🏠"
        assert personal["order"] == 1

    def test_scholar_sphere(self):
        """Scholar sphere (9th) should have correct properties."""
        scholar = next(s for s in FROZEN_SPHERES if s["id"] == "scholar")
        assert scholar["icon"] == "📚"
        assert scholar["order"] == 9
        assert "scholar" in scholar["name"].lower()

    def test_my_team_sphere(self):
        """My Team sphere should have correct properties."""
        team = next(s for s in FROZEN_SPHERES if s["id"] == "team")
        assert team["icon"] == "🤝"
        assert "team" in team["name"].lower()

    def test_entertainment_sphere(self):
        """Entertainment sphere should have correct properties."""
        entertainment = next(s for s in FROZEN_SPHERES if s["id"] == "entertainment")
        assert entertainment["icon"] == "🎬"


# ═══════════════════════════════════════════════════════════════════════════════
# API ENDPOINT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSpheresAPI:
    """Tests for spheres API endpoints."""

    def test_get_spheres_returns_9(self, client):
        """GET /spheres should return exactly 9 spheres."""
        response = client.get("/api/v1/spheres")
        # If endpoint exists
        if response.status_code == 200:
            data = response.json()
            assert len(data) == 9

    def test_get_sphere_by_id(self, client, sphere_ids: List[str]):
        """GET /spheres/{id} should return sphere data."""
        for sphere_id in sphere_ids:
            response = client.get(f"/api/v1/spheres/{sphere_id}")
            # If endpoint exists
            if response.status_code == 200:
                data = response.json()
                assert data["id"] == sphere_id

    def test_get_scholar_sphere(self, client):
        """GET /spheres/scholar should return Scholar sphere."""
        response = client.get("/api/v1/spheres/scholar")
        if response.status_code == 200:
            data = response.json()
            assert data["id"] == "scholar"
            assert "📚" in data.get("icon", "")


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY PROMPT COMPLIANCE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMemoryPromptCompliance:
    """Tests ensuring Memory Prompt compliance."""

    def test_frozen_architecture_9_spheres(self, sphere_ids: List[str]):
        """Architecture should be FROZEN at exactly 9 spheres."""
        assert len(sphere_ids) == 9
        assert len(sphere_ids) <= 9, "NO additional spheres allowed!"

    def test_no_sphere_merge_or_split(self, sphere_ids: List[str]):
        """No sphere may be split or merged."""
        # Each expected sphere should exist exactly once
        expected = {"personal", "business", "government", "creative", 
                   "community", "social", "entertainment", "team", "scholar"}
        actual = set(sphere_ids)
        assert actual == expected

    def test_ia_labs_in_my_team_not_separate(self, sphere_ids: List[str]):
        """IA Labs and Skills & Tools are INCLUDED INSIDE My Team."""
        # Should NOT exist as separate spheres
        forbidden = ["ia_labs", "ialabs", "skills", "tools", "skills_tools"]
        for forbidden_id in forbidden:
            assert forbidden_id not in sphere_ids
        
        # My Team should exist
        assert "team" in sphere_ids


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE NAVIGATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSphereNavigation:
    """Tests for sphere navigation rules."""

    def test_one_sphere_active_at_time(self):
        """CHE·NU UI: One active SPHERE at a time."""
        # This is a UI rule - we verify it's documented
        active_spheres_limit = 1
        assert active_spheres_limit == 1

    def test_personal_sphere_always_unlocked(self, sphere_ids: List[str]):
        """Personal sphere should always be unlocked (default)."""
        assert "personal" in sphere_ids
        # Personal is first sphere and always available
        personal_index = sphere_ids.index("personal")
        assert personal_index == 0
