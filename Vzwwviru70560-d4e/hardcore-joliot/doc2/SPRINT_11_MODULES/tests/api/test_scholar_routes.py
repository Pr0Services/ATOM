"""
CHE·NU™ - Scholar Routes Tests
Tests for Scholar Sphere (Academic/Research)
"""
import pytest
from datetime import datetime, timedelta


class TestScholarReferences:
    """Test suite for bibliographic references"""
    
    def test_create_reference(self, client, auth_headers):
        """Test creating a bibliographic reference"""
        ref_data = {
            "title": "Artificial Intelligence: A Modern Approach",
            "authors": ["Stuart Russell", "Peter Norvig"],
            "year": 2020,
            "type": "book",
            "publisher": "Pearson",
            "isbn": "978-0134610993",
            "tags": ["ai", "textbook", "computer-science"]
        }
        response = client.post(
            "/api/v1/scholar/references",
            json=ref_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == ref_data["title"]
        assert len(data["authors"]) == 2
        assert "id" in data
    
    def test_create_reference_article(self, client, auth_headers):
        """Test creating a journal article reference"""
        ref_data = {
            "title": "Attention Is All You Need",
            "authors": ["Vaswani et al."],
            "year": 2017,
            "type": "article",
            "journal": "NeurIPS",
            "doi": "10.48550/arXiv.1706.03762",
            "url": "https://arxiv.org/abs/1706.03762"
        }
        response = client.post(
            "/api/v1/scholar/references",
            json=ref_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "article"
        assert data["doi"] is not None
    
    def test_list_references(self, client, auth_headers, multiple_references):
        """Test listing references"""
        response = client.get("/api/v1/scholar/references", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) > 0
    
    def test_search_references(self, client, auth_headers, multiple_references):
        """Test searching references"""
        response = client.get(
            "/api/v1/scholar/references?search=artificial",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] > 0
    
    def test_filter_references_by_type(self, client, auth_headers, multiple_references):
        """Test filtering references by type"""
        response = client.get(
            "/api/v1/scholar/references?type=book",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        for ref in data["items"]:
            assert ref["type"] == "book"
    
    def test_update_reference(self, client, auth_headers, sample_reference):
        """Test updating a reference"""
        ref_id = sample_reference["id"]
        update_data = {
            "notes": "Classic AI textbook, comprehensive coverage",
            "rating": 5
        }
        response = client.put(
            f"/api/v1/scholar/references/{ref_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["notes"] == update_data["notes"]
        assert data["rating"] == 5
    
    def test_delete_reference(self, client, auth_headers, sample_reference):
        """Test deleting a reference"""
        ref_id = sample_reference["id"]
        response = client.delete(
            f"/api/v1/scholar/references/{ref_id}",
            headers=auth_headers
        )
        assert response.status_code == 204
    
    def test_generate_citation(self, client, auth_headers, sample_reference):
        """Test generating citation formats"""
        ref_id = sample_reference["id"]
        formats = ["apa", "mla", "chicago", "bibtex"]
        
        for fmt in formats:
            response = client.get(
                f"/api/v1/scholar/references/{ref_id}/citation?format={fmt}",
                headers=auth_headers
            )
            assert response.status_code == 200
            data = response.json()
            assert "citation" in data
            assert len(data["citation"]) > 0


class TestScholarFlashcards:
    """Test suite for flashcards and spaced repetition"""
    
    def test_create_flashcard(self, client, auth_headers):
        """Test creating a flashcard"""
        card_data = {
            "front": "What is the time complexity of binary search?",
            "back": "O(log n)",
            "deck": "Algorithms",
            "tags": ["algorithms", "complexity", "search"]
        }
        response = client.post(
            "/api/v1/scholar/flashcards",
            json=card_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["front"] == card_data["front"]
        assert data["back"] == card_data["back"]
        assert "id" in data
        assert "next_review" in data
    
    def test_create_flashcard_with_image(self, client, auth_headers):
        """Test creating flashcard with image"""
        card_data = {
            "front": "Identify this data structure",
            "back": "Binary Tree",
            "image_url": "https://example.com/binary-tree.png",
            "deck": "Data Structures"
        }
        response = client.post(
            "/api/v1/scholar/flashcards",
            json=card_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["image_url"] is not None
    
    def test_review_flashcard_correct(self, client, auth_headers, sample_flashcard):
        """Test reviewing flashcard - correct answer"""
        card_id = sample_flashcard["id"]
        review_data = {
            "quality": 5,  # Perfect recall
            "time_spent": 3.5
        }
        response = client.post(
            f"/api/v1/scholar/flashcards/{card_id}/review",
            json=review_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "next_review" in data
        assert "interval" in data
        assert data["easiness_factor"] >= sample_flashcard.get("easiness_factor", 2.5)
    
    def test_review_flashcard_incorrect(self, client, auth_headers, sample_flashcard):
        """Test reviewing flashcard - incorrect answer"""
        card_id = sample_flashcard["id"]
        review_data = {
            "quality": 0,  # Complete blackout
            "time_spent": 10.0
        }
        response = client.post(
            f"/api/v1/scholar/flashcards/{card_id}/review",
            json=review_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        # Should reset interval for incorrect answer
        assert data["interval"] <= 1
    
    def test_sm2_algorithm_progression(self, client, auth_headers, sample_flashcard):
        """Test SM-2 algorithm progression over multiple reviews"""
        card_id = sample_flashcard["id"]
        
        # Simulate 5 perfect reviews
        qualities = [5, 5, 5, 4, 5]
        intervals = []
        
        for quality in qualities:
            review_data = {"quality": quality, "time_spent": 2.0}
            response = client.post(
                f"/api/v1/scholar/flashcards/{card_id}/review",
                json=review_data,
                headers=auth_headers
            )
            assert response.status_code == 200
            data = response.json()
            intervals.append(data["interval"])
        
        # Intervals should increase
        assert intervals[-1] > intervals[0]
    
    def test_get_due_flashcards(self, client, auth_headers, multiple_flashcards):
        """Test getting flashcards due for review"""
        response = client.get(
            "/api/v1/scholar/flashcards/due",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        # All returned cards should be due
        now = datetime.now()
        for card in data["items"]:
            next_review = datetime.fromisoformat(card["next_review"])
            assert next_review <= now
    
    def test_get_flashcards_by_deck(self, client, auth_headers, multiple_flashcards):
        """Test filtering flashcards by deck"""
        response = client.get(
            "/api/v1/scholar/flashcards?deck=Algorithms",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        for card in data["items"]:
            assert card["deck"] == "Algorithms"
    
    def test_flashcard_statistics(self, client, auth_headers, sample_flashcard):
        """Test getting flashcard review statistics"""
        card_id = sample_flashcard["id"]
        response = client.get(
            f"/api/v1/scholar/flashcards/{card_id}/stats",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_reviews" in data
        assert "average_quality" in data
        assert "retention_rate" in data


class TestScholarStudyPlans:
    """Test suite for study plans and schedules"""
    
    def test_create_study_plan(self, client, auth_headers):
        """Test creating a study plan"""
        plan_data = {
            "title": "Machine Learning Fundamentals",
            "description": "Master ML basics in 8 weeks",
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(weeks=8)).isoformat(),
            "topics": [
                "Linear Regression",
                "Logistic Regression",
                "Neural Networks",
                "Deep Learning"
            ],
            "daily_goal_minutes": 60
        }
        response = client.post(
            "/api/v1/scholar/study-plans",
            json=plan_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == plan_data["title"]
        assert len(data["topics"]) == 4
        assert "id" in data
    
    def test_add_milestone_to_plan(self, client, auth_headers, sample_study_plan):
        """Test adding milestone to study plan"""
        plan_id = sample_study_plan["id"]
        milestone_data = {
            "title": "Complete Chapter 1",
            "due_date": (datetime.now() + timedelta(weeks=1)).isoformat(),
            "description": "Finish all exercises in Chapter 1"
        }
        response = client.post(
            f"/api/v1/scholar/study-plans/{plan_id}/milestones",
            json=milestone_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == milestone_data["title"]
    
    def test_complete_milestone(self, client, auth_headers, sample_study_plan, sample_milestone):
        """Test marking milestone as complete"""
        plan_id = sample_study_plan["id"]
        milestone_id = sample_milestone["id"]
        
        response = client.post(
            f"/api/v1/scholar/study-plans/{plan_id}/milestones/{milestone_id}/complete",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True
        assert "completed_at" in data
    
    def test_track_study_session(self, client, auth_headers, sample_study_plan):
        """Test tracking a study session"""
        plan_id = sample_study_plan["id"]
        session_data = {
            "duration_minutes": 45,
            "topics_covered": ["Linear Regression"],
            "notes": "Covered gradient descent basics",
            "completed_at": datetime.now().isoformat()
        }
        response = client.post(
            f"/api/v1/scholar/study-plans/{plan_id}/sessions",
            json=session_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["duration_minutes"] == 45
    
    def test_get_study_plan_progress(self, client, auth_headers, sample_study_plan):
        """Test getting study plan progress"""
        plan_id = sample_study_plan["id"]
        response = client.get(
            f"/api/v1/scholar/study-plans/{plan_id}/progress",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "completion_percentage" in data
        assert "total_study_time" in data
        assert "milestones_completed" in data
        assert "milestones_total" in data
    
    def test_list_active_study_plans(self, client, auth_headers, multiple_study_plans):
        """Test listing active study plans"""
        response = client.get(
            "/api/v1/scholar/study-plans?status=active",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        for plan in data["items"]:
            assert plan["status"] == "active"


class TestScholarIntegration:
    """Integration tests for Scholar workflows"""
    
    def test_research_workflow(self, client, auth_headers):
        """Test complete research workflow"""
        # 1. Create reference
        ref_data = {
            "title": "Deep Learning",
            "authors": ["Ian Goodfellow", "Yoshua Bengio"],
            "year": 2016,
            "type": "book"
        }
        ref_resp = client.post(
            "/api/v1/scholar/references",
            json=ref_data,
            headers=auth_headers
        )
        assert ref_resp.status_code == 201
        
        # 2. Create flashcards from reference
        card_data = {
            "front": "Who wrote Deep Learning (2016)?",
            "back": "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
            "deck": "ML Literature",
            "reference_id": ref_resp.json()["id"]
        }
        card_resp = client.post(
            "/api/v1/scholar/flashcards",
            json=card_data,
            headers=auth_headers
        )
        assert card_resp.status_code == 201
        
        # 3. Create study plan
        plan_data = {
            "title": "Deep Learning Study",
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(weeks=12)).isoformat(),
            "topics": ["Neural Networks", "CNNs", "RNNs"]
        }
        plan_resp = client.post(
            "/api/v1/scholar/study-plans",
            json=plan_data,
            headers=auth_headers
        )
        assert plan_resp.status_code == 201
        
        # 4. Add milestone
        milestone_data = {
            "title": "Finish Part I",
            "due_date": (datetime.now() + timedelta(weeks=4)).isoformat()
        }
        milestone_resp = client.post(
            f"/api/v1/scholar/study-plans/{plan_resp.json()['id']}/milestones",
            json=milestone_data,
            headers=auth_headers
        )
        assert milestone_resp.status_code == 201


# Fixtures
@pytest.fixture
def sample_reference(client, auth_headers):
    """Create sample reference"""
    ref_data = {
        "title": "Introduction to Algorithms",
        "authors": ["Cormen", "Leiserson", "Rivest", "Stein"],
        "year": 2009,
        "type": "book"
    }
    response = client.post(
        "/api/v1/scholar/references",
        json=ref_data,
        headers=auth_headers
    )
    return response.json()


@pytest.fixture
def sample_flashcard(client, auth_headers):
    """Create sample flashcard"""
    card_data = {
        "front": "Test Question",
        "back": "Test Answer",
        "deck": "Test Deck"
    }
    response = client.post(
        "/api/v1/scholar/flashcards",
        json=card_data,
        headers=auth_headers
    )
    return response.json()


@pytest.fixture
def sample_study_plan(client, auth_headers):
    """Create sample study plan"""
    plan_data = {
        "title": "Test Study Plan",
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(weeks=4)).isoformat()
    }
    response = client.post(
        "/api/v1/scholar/study-plans",
        json=plan_data,
        headers=auth_headers
    )
    return response.json()


@pytest.fixture
def sample_milestone(client, auth_headers, sample_study_plan):
    """Create sample milestone"""
    plan_id = sample_study_plan["id"]
    milestone_data = {
        "title": "Test Milestone",
        "due_date": (datetime.now() + timedelta(weeks=1)).isoformat()
    }
    response = client.post(
        f"/api/v1/scholar/study-plans/{plan_id}/milestones",
        json=milestone_data,
        headers=auth_headers
    )
    return response.json()


@pytest.fixture
def multiple_references(client, auth_headers):
    """Create multiple references"""
    refs = []
    types = ["book", "article", "paper"]
    for i, ref_type in enumerate(types):
        ref_data = {
            "title": f"Test Reference {i}",
            "authors": ["Author Test"],
            "year": 2020 + i,
            "type": ref_type
        }
        response = client.post(
            "/api/v1/scholar/references",
            json=ref_data,
            headers=auth_headers
        )
        refs.append(response.json())
    return refs


@pytest.fixture
def multiple_flashcards(client, auth_headers):
    """Create multiple flashcards"""
    cards = []
    for i in range(5):
        card_data = {
            "front": f"Question {i}",
            "back": f"Answer {i}",
            "deck": "Algorithms" if i % 2 == 0 else "Data Structures"
        }
        response = client.post(
            "/api/v1/scholar/flashcards",
            json=card_data,
            headers=auth_headers
        )
        cards.append(response.json())
    return cards


@pytest.fixture
def multiple_study_plans(client, auth_headers):
    """Create multiple study plans"""
    plans = []
    for i in range(3):
        plan_data = {
            "title": f"Study Plan {i}",
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(weeks=4+i)).isoformat(),
            "status": "active" if i < 2 else "completed"
        }
        response = client.post(
            "/api/v1/scholar/study-plans",
            json=plan_data,
            headers=auth_headers
        )
        plans.append(response.json())
    return plans
