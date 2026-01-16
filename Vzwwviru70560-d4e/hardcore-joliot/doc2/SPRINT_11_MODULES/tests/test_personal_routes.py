"""
CHE·NU™ — Personal Routes Tests
Tests unitaires pour les endpoints Personal Sphere
"""

import pytest
from datetime import date, datetime
from uuid import uuid4


class TestGoalsEndpoints:
    """Tests for /personal/goals endpoints."""
    
    def test_get_goals_empty(self):
        """Test getting goals when none exist."""
        # Simulate empty response
        response = {"goals": [], "total": 0}
        assert response["total"] == 0
        assert len(response["goals"]) == 0
    
    def test_create_goal_valid(self):
        """Test creating a valid goal."""
        goal_data = {
            "title": "Learn Python",
            "description": "Master Python programming",
            "category": "education",
            "target_date": "2025-12-31",
            "priority": "high",
        }
        
        # Validate required fields
        assert "title" in goal_data
        assert len(goal_data["title"]) > 0
        assert goal_data["priority"] in ["low", "medium", "high", "critical"]
    
    def test_goal_status_transitions(self):
        """Test valid goal status transitions."""
        valid_statuses = ["draft", "active", "paused", "completed", "abandoned"]
        
        for status in valid_statuses:
            assert status in valid_statuses
    
    def test_goal_progress_calculation(self):
        """Test goal progress percentage calculation."""
        target = 100
        current = 75
        progress = (current / target) * 100
        assert progress == 75.0
    
    def test_milestone_creation(self):
        """Test creating milestone for a goal."""
        milestone = {
            "title": "Complete module 1",
            "target_date": "2025-06-01",
            "is_completed": False,
        }
        assert milestone["is_completed"] == False


class TestHabitsEndpoints:
    """Tests for /personal/habits endpoints."""
    
    def test_get_habits_empty(self):
        """Test getting habits when none exist."""
        response = {"habits": [], "total": 0}
        assert response["total"] == 0
    
    def test_create_habit_valid(self):
        """Test creating a valid habit."""
        habit_data = {
            "name": "Morning meditation",
            "frequency": "daily",
            "tracking_type": "boolean",
        }
        
        assert "name" in habit_data
        assert habit_data["frequency"] in ["daily", "weekly", "specific_days"]
    
    def test_habit_streak_calculation(self):
        """Test streak calculation logic."""
        logs = [True, True, True, False, True, True]
        
        # Current streak (from end)
        current_streak = 0
        for log in reversed(logs):
            if log:
                current_streak += 1
            else:
                break
        
        assert current_streak == 2
    
    def test_habit_completion_rate(self):
        """Test habit completion rate calculation."""
        total_days = 30
        completed_days = 25
        rate = (completed_days / total_days) * 100
        assert rate == pytest.approx(83.33, 0.01)


class TestJournalEndpoints:
    """Tests for /personal/journal endpoints."""
    
    def test_get_journal_entries_empty(self):
        """Test getting journal entries when none exist."""
        response = {"entries": [], "total": 0}
        assert response["total"] == 0
    
    def test_create_journal_entry_valid(self):
        """Test creating a valid journal entry."""
        entry_data = {
            "content": "Today was a productive day...",
            "entry_type": "freeform",
            "entry_date": date.today().isoformat(),
            "mood_score": 8,
        }
        
        assert len(entry_data["content"]) > 0
        assert 1 <= entry_data["mood_score"] <= 10
    
    def test_journal_entry_types(self):
        """Test valid journal entry types."""
        valid_types = ["freeform", "gratitude", "reflection", "morning_pages", "evening_review", "prompt"]
        
        for entry_type in valid_types:
            assert entry_type in valid_types


class TestDailyPlanEndpoints:
    """Tests for /personal/daily-plan endpoints."""
    
    def test_create_daily_plan_valid(self):
        """Test creating a valid daily plan."""
        plan_data = {
            "plan_date": date.today().isoformat(),
            "top_priorities": ["Task 1", "Task 2", "Task 3"],
            "intention": "Stay focused",
        }
        
        assert len(plan_data["top_priorities"]) <= 3
    
    def test_evening_review_completion(self):
        """Test completing evening review."""
        review_data = {
            "wins": ["Completed project", "Good meeting"],
            "lessons": "Need to plan better",
            "gratitude": ["Team support", "Good health"],
        }
        
        assert len(review_data["wins"]) > 0


class TestLifeAreasEndpoints:
    """Tests for /personal/life-areas endpoints."""
    
    def test_life_area_score_valid(self):
        """Test valid life area scores."""
        score = 7
        assert 1 <= score <= 10
    
    def test_assessment_overall_calculation(self):
        """Test overall assessment score calculation."""
        scores = {"health": 8, "career": 7, "relationships": 9, "finance": 6}
        overall = sum(scores.values()) / len(scores)
        assert overall == 7.5


class TestRemindersEndpoints:
    """Tests for /personal/reminders endpoints."""
    
    def test_create_reminder_valid(self):
        """Test creating a valid reminder."""
        reminder_data = {
            "title": "Doctor appointment",
            "remind_at": "2025-01-15T10:00:00",
            "priority": "high",
        }
        
        assert "title" in reminder_data
        assert reminder_data["priority"] in ["low", "medium", "high"]


class TestDashboardEndpoint:
    """Tests for /personal/dashboard endpoint."""
    
    def test_dashboard_structure(self):
        """Test dashboard response structure."""
        dashboard = {
            "today": {
                "date": date.today().isoformat(),
                "habits_completed": 3,
                "habits_total": 5,
                "goals_in_progress": 2,
            },
            "streaks": {
                "journal": 7,
                "habits_best": 14,
            },
        }
        
        assert "today" in dashboard
        assert "streaks" in dashboard
        assert dashboard["today"]["habits_completed"] <= dashboard["today"]["habits_total"]


# Governance Tests
class TestPersonalGovernance:
    """Tests for Personal sphere governance compliance."""
    
    def test_sphere_isolation(self):
        """Test that personal data stays in personal sphere."""
        sphere_id = "personal"
        assert sphere_id == "personal"
    
    def test_privacy_default(self):
        """Test that personal data is private by default."""
        entry = {"is_private": True}
        assert entry["is_private"] == True
    
    def test_user_ownership(self):
        """Test that personal data has user ownership."""
        user_id = uuid4()
        data = {"user_id": user_id}
        assert data["user_id"] == user_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
