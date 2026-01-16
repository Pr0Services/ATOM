"""
CHE·NU™ V68 - Education & LMS Tests
Vertical 11: Learning Management System

Comprehensive tests for education functionality.
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from uuid import uuid4

from spheres.education.agents.education_agent import (
    EducationAgent, CourseStatus, EnrollmentStatus, AssignmentType,
    SubmissionStatus, GradeStatus, QuestionType, ContentType,
    CertificateStatus
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def agent():
    """Fresh agent for each test."""
    return EducationAgent()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def create_published_course(agent, instructor_id="instructor_1", user_id="admin_1"):
    """Helper to create and publish a course."""
    course = await agent.create_course(
        code="CS101",
        title="Introduction to Computer Science",
        description="Fundamental CS concepts",
        instructor_id=instructor_id,
        category="Computer Science",
        tags=["programming", "algorithms"],
        user_id=user_id
    )
    await agent.submit_course_for_review(course.id, user_id)
    return await agent.approve_course(course.id, "reviewer_1")


async def create_enrolled_student(agent, course_id, student_id="student_1", student_name="Alice Smith"):
    """Helper to create an enrolled student."""
    return await agent.enroll_student(course_id, student_id, student_name)


async def create_module_with_lessons(agent, course_id, user_id="admin_1"):
    """Helper to create a module with lessons."""
    module = await agent.create_module(
        course_id=course_id,
        title="Module 1: Basics",
        description="Basic concepts",
        order=1,
        user_id=user_id
    )
    lesson = await agent.create_lesson(
        module_id=module.id,
        title="Lesson 1: Introduction",
        content_type=ContentType.VIDEO,
        order=1,
        duration_minutes=30,
        user_id=user_id
    )
    return module, lesson


async def create_assignment_with_submission(agent, course_id, student_id="student_1", user_id="admin_1"):
    """Helper to create an assignment with submission."""
    assignment = await agent.create_assignment(
        course_id=course_id,
        title="Homework 1",
        description="First homework",
        assignment_type=AssignmentType.HOMEWORK,
        points_possible=Decimal("100"),
        user_id=user_id
    )
    submission = await agent.submit_assignment(
        assignment_id=assignment.id,
        student_id=student_id,
        content_text="My answer"
    )
    return assignment, submission


# ============================================================================
# COURSE MANAGEMENT TESTS
# ============================================================================

class TestCourseManagement:
    """Test course CRUD and publishing workflow."""
    
    @pytest.mark.asyncio
    async def test_create_course(self, agent):
        """Test course creation starts as draft."""
        course = await agent.create_course(
            code="CS101",
            title="Intro to CS",
            description="Basic CS",
            instructor_id="instructor_1",
            category="Computer Science",
            user_id="admin_1"
        )
        
        assert course.code == "CS101"
        assert course.status == CourseStatus.DRAFT
        assert course.created_by == "admin_1"
        assert course.id in agent.courses
    
    @pytest.mark.asyncio
    async def test_submit_for_review(self, agent):
        """Test submitting course for review."""
        course = await agent.create_course(
            code="CS101", title="Intro", description="Desc",
            instructor_id="inst_1", category="CS", user_id="admin_1"
        )
        
        reviewed = await agent.submit_course_for_review(course.id, "admin_1")
        assert reviewed.status == CourseStatus.UNDER_REVIEW
    
    @pytest.mark.asyncio
    async def test_approve_course(self, agent):
        """Test course approval and publishing."""
        course = await agent.create_course(
            code="CS101", title="Intro", description="Desc",
            instructor_id="inst_1", category="CS", user_id="admin_1"
        )
        await agent.submit_course_for_review(course.id, "admin_1")
        
        approved = await agent.approve_course(course.id, "reviewer_1")
        assert approved.status == CourseStatus.PUBLISHED
        assert approved.reviewed_by == "reviewer_1"
        assert approved.published_at is not None
    
    @pytest.mark.asyncio
    async def test_cannot_approve_without_review(self, agent):
        """Test that courses must be reviewed before approval."""
        course = await agent.create_course(
            code="CS101", title="Intro", description="Desc",
            instructor_id="inst_1", category="CS", user_id="admin_1"
        )
        
        with pytest.raises(ValueError, match="must be under review"):
            await agent.approve_course(course.id, "reviewer_1")
    
    @pytest.mark.asyncio
    async def test_get_courses_alphabetical(self, agent):
        """Test courses returned alphabetically by title (Rule #5)."""
        await agent.create_course(code="Z001", title="Zoology", description="", instructor_id="i1", category="Science", user_id="a1")
        await agent.create_course(code="A001", title="Anatomy", description="", instructor_id="i1", category="Science", user_id="a1")
        await agent.create_course(code="M001", title="Mathematics", description="", instructor_id="i1", category="Math", user_id="a1")
        
        courses = await agent.get_courses()
        titles = [c.title for c in courses]
        assert titles == ["Anatomy", "Mathematics", "Zoology"]
    
    @pytest.mark.asyncio
    async def test_archive_course(self, agent):
        """Test archiving a course."""
        course = await create_published_course(agent)
        
        archived = await agent.archive_course(course.id, "admin_1")
        assert archived.status == CourseStatus.ARCHIVED


# ============================================================================
# MODULE & LESSON TESTS
# ============================================================================

class TestModulesAndLessons:
    """Test module and lesson management."""
    
    @pytest.mark.asyncio
    async def test_create_module(self, agent):
        """Test creating a module."""
        course = await create_published_course(agent)
        
        module = await agent.create_module(
            course_id=course.id,
            title="Module 1",
            description="First module",
            order=1,
            user_id="admin_1"
        )
        
        assert module.title == "Module 1"
        assert module.course_id == course.id
        assert module.id in agent.modules
    
    @pytest.mark.asyncio
    async def test_get_modules_ordered(self, agent):
        """Test modules returned in order."""
        course = await create_published_course(agent)
        
        await agent.create_module(course.id, "Module 3", "", 3, user_id="a1")
        await agent.create_module(course.id, "Module 1", "", 1, user_id="a1")
        await agent.create_module(course.id, "Module 2", "", 2, user_id="a1")
        
        modules = await agent.get_modules(course.id)
        orders = [m.order for m in modules]
        assert orders == [1, 2, 3]
    
    @pytest.mark.asyncio
    async def test_create_lesson(self, agent):
        """Test creating a lesson."""
        course = await create_published_course(agent)
        module = await agent.create_module(course.id, "Module 1", "", 1, user_id="a1")
        
        lesson = await agent.create_lesson(
            module_id=module.id,
            title="Lesson 1",
            content_type=ContentType.VIDEO,
            order=1,
            duration_minutes=30,
            user_id="admin_1"
        )
        
        assert lesson.title == "Lesson 1"
        assert lesson.content_type == ContentType.VIDEO
        assert lesson.course_id == course.id


# ============================================================================
# ENROLLMENT TESTS
# ============================================================================

class TestEnrollment:
    """Test student enrollment."""
    
    @pytest.mark.asyncio
    async def test_enroll_student(self, agent):
        """Test enrolling a student."""
        course = await create_published_course(agent)
        
        enrollment = await agent.enroll_student(
            course_id=course.id,
            student_id="student_1",
            student_name="Alice Smith"
        )
        
        assert enrollment.status == EnrollmentStatus.ACTIVE
        assert enrollment.progress_percent == Decimal("0")
        assert enrollment.id in agent.enrollments
    
    @pytest.mark.asyncio
    async def test_cannot_enroll_in_unpublished(self, agent):
        """Test cannot enroll in draft course."""
        course = await agent.create_course(
            code="CS101", title="Intro", description="",
            instructor_id="i1", category="CS", user_id="a1"
        )
        
        with pytest.raises(ValueError, match="Cannot enroll in unpublished"):
            await agent.enroll_student(course.id, "student_1", "Alice")
    
    @pytest.mark.asyncio
    async def test_students_alphabetical(self, agent):
        """Test students listed alphabetically (Rule #5)."""
        course = await create_published_course(agent)
        
        await agent.enroll_student(course.id, "s3", "Zara Wilson")
        await agent.enroll_student(course.id, "s1", "Alice Smith")
        await agent.enroll_student(course.id, "s2", "Bob Jones")
        
        students = await agent.get_enrolled_students(course.id)
        names = [s.student_name for s in students]
        assert names == ["Alice Smith", "Bob Jones", "Zara Wilson"]
    
    @pytest.mark.asyncio
    async def test_drop_student(self, agent):
        """Test dropping a student."""
        course = await create_published_course(agent)
        enrollment = await agent.enroll_student(course.id, "s1", "Alice")
        
        dropped = await agent.drop_student(enrollment.id, "admin_1")
        assert dropped.status == EnrollmentStatus.DROPPED


# ============================================================================
# ASSIGNMENT & SUBMISSION TESTS
# ============================================================================

class TestAssignmentsAndSubmissions:
    """Test assignments and submissions."""
    
    @pytest.mark.asyncio
    async def test_create_assignment(self, agent):
        """Test creating an assignment."""
        course = await create_published_course(agent)
        
        assignment = await agent.create_assignment(
            course_id=course.id,
            title="Homework 1",
            description="First assignment",
            assignment_type=AssignmentType.HOMEWORK,
            points_possible=Decimal("100"),
            user_id="admin_1"
        )
        
        assert assignment.title == "Homework 1"
        assert assignment.points_possible == Decimal("100")
        assert assignment.id in agent.assignments
    
    @pytest.mark.asyncio
    async def test_submit_assignment(self, agent):
        """Test submitting an assignment."""
        course = await create_published_course(agent)
        await agent.enroll_student(course.id, "student_1", "Alice")
        assignment = await agent.create_assignment(
            course_id=course.id, title="HW1", description="",
            assignment_type=AssignmentType.HOMEWORK,
            points_possible=Decimal("100"), user_id="a1"
        )
        
        submission = await agent.submit_assignment(
            assignment_id=assignment.id,
            student_id="student_1",
            content_text="My answer"
        )
        
        assert submission.status == SubmissionStatus.SUBMITTED
        assert submission.attempt_number == 1
    
    @pytest.mark.asyncio
    async def test_grade_submission_draft(self, agent):
        """Test grading creates draft (requires approval)."""
        course = await create_published_course(agent)
        await agent.enroll_student(course.id, "student_1", "Alice")
        assignment, submission = await create_assignment_with_submission(
            agent, course.id, "student_1"
        )
        
        graded = await agent.grade_submission(
            submission_id=submission.id,
            score=Decimal("85"),
            feedback="Good work!",
            grader_id="instructor_1"
        )
        
        assert graded.score == Decimal("85")
        assert graded.grade_status == GradeStatus.DRAFT  # Not approved yet!
    
    @pytest.mark.asyncio
    async def test_approve_grade(self, agent):
        """Test approving a grade (GOVERNANCE)."""
        course = await create_published_course(agent)
        await agent.enroll_student(course.id, "student_1", "Alice")
        assignment, submission = await create_assignment_with_submission(
            agent, course.id, "student_1"
        )
        await agent.grade_submission(submission.id, Decimal("85"), "Good!", "inst_1")
        
        approved = await agent.approve_grade(submission.id, "dept_head")
        assert approved.grade_status == GradeStatus.APPROVED


# ============================================================================
# GRADE CHANGE GOVERNANCE TESTS
# ============================================================================

class TestGradeChangeGovernance:
    """Test grade change approval workflow."""
    
    @pytest.mark.asyncio
    async def test_request_grade_change(self, agent):
        """Test requesting a grade change."""
        course = await create_published_course(agent)
        await agent.enroll_student(course.id, "student_1", "Alice")
        assignment, submission = await create_assignment_with_submission(
            agent, course.id, "student_1"
        )
        await agent.grade_submission(submission.id, Decimal("70"), "OK", "inst_1")
        await agent.approve_grade(submission.id, "head_1")
        
        change = await agent.request_grade_change(
            submission_id=submission.id,
            new_score=Decimal("80"),
            reason="Re-evaluated based on rubric",
            requester_id="instructor_1"
        )
        
        assert change.status == GradeStatus.PENDING
        assert change.new_score == Decimal("80")
    
    @pytest.mark.asyncio
    async def test_approve_grade_change(self, agent):
        """Test approving grade change (GOVERNANCE)."""
        course = await create_published_course(agent)
        await agent.enroll_student(course.id, "student_1", "Alice")
        assignment, submission = await create_assignment_with_submission(
            agent, course.id, "student_1"
        )
        await agent.grade_submission(submission.id, Decimal("70"), "OK", "inst_1")
        await agent.approve_grade(submission.id, "head_1")
        change = await agent.request_grade_change(
            submission.id, Decimal("80"), "Re-eval", "inst_1"
        )
        
        approved = await agent.approve_grade_change(change.id, "dept_head")
        
        assert approved.status == GradeStatus.APPROVED
        assert approved.approved_by == "dept_head"
        
        # Verify submission was updated
        updated = agent.submissions.get(submission.id)
        assert updated.score == Decimal("80")
    
    @pytest.mark.asyncio
    async def test_get_pending_grade_changes(self, agent):
        """Test getting pending grade changes."""
        course = await create_published_course(agent)
        await agent.enroll_student(course.id, "student_1", "Alice")
        assignment, submission = await create_assignment_with_submission(
            agent, course.id, "student_1"
        )
        await agent.grade_submission(submission.id, Decimal("70"), "OK", "inst_1")
        await agent.approve_grade(submission.id, "head_1")
        await agent.request_grade_change(submission.id, Decimal("80"), "Re-eval", "inst_1")
        
        pending = await agent.get_pending_grade_changes()
        assert len(pending) == 1


# ============================================================================
# QUIZ TESTS
# ============================================================================

class TestQuizzes:
    """Test quiz functionality."""
    
    @pytest.mark.asyncio
    async def test_create_quiz(self, agent):
        """Test creating a quiz."""
        course = await create_published_course(agent)
        assignment = await agent.create_assignment(
            course.id, "Quiz 1", "", AssignmentType.QUIZ,
            Decimal("50"), user_id="a1"
        )
        
        quiz = await agent.create_quiz(
            course_id=course.id,
            assignment_id=assignment.id,
            title="Quiz 1",
            time_limit_minutes=30,
            user_id="admin_1"
        )
        
        assert quiz.title == "Quiz 1"
        assert quiz.time_limit_minutes == 30
    
    @pytest.mark.asyncio
    async def test_add_question(self, agent):
        """Test adding questions to quiz."""
        course = await create_published_course(agent)
        assignment = await agent.create_assignment(
            course.id, "Quiz 1", "", AssignmentType.QUIZ,
            Decimal("50"), user_id="a1"
        )
        quiz = await agent.create_quiz(course.id, assignment.id, "Quiz 1", user_id="a1")
        
        question = await agent.add_question(
            quiz_id=quiz.id,
            question_type=QuestionType.MULTIPLE_CHOICE,
            question_text="What is 2+2?",
            points=Decimal("10"),
            options=[{"A": "3"}, {"B": "4"}, {"C": "5"}],
            correct_answer="B"
        )
        
        assert len(quiz.questions) == 1
        assert question.correct_answer == "B"
    
    @pytest.mark.asyncio
    async def test_quiz_attempt_workflow(self, agent):
        """Test complete quiz attempt workflow."""
        course = await create_published_course(agent)
        await agent.enroll_student(course.id, "student_1", "Alice")
        assignment = await agent.create_assignment(
            course.id, "Quiz 1", "", AssignmentType.QUIZ,
            Decimal("10"), max_attempts=2, user_id="a1"
        )
        quiz = await agent.create_quiz(course.id, assignment.id, "Quiz 1", user_id="a1")
        q = await agent.add_question(
            quiz.id, QuestionType.MULTIPLE_CHOICE, "2+2?",
            Decimal("10"), correct_answer="4"
        )
        
        # Start attempt
        attempt = await agent.start_quiz_attempt(quiz.id, "student_1")
        assert attempt.attempt_number == 1
        
        # Submit with correct answer
        submitted = await agent.submit_quiz_attempt(
            attempt.id, {str(q.id): "4"}
        )
        assert submitted.score == Decimal("10")
        assert submitted.graded is True


# ============================================================================
# DISCUSSION TESTS
# ============================================================================

class TestDiscussions:
    """Test discussion forums."""
    
    @pytest.mark.asyncio
    async def test_create_discussion(self, agent):
        """Test creating a discussion."""
        course = await create_published_course(agent)
        
        discussion = await agent.create_discussion(
            course_id=course.id,
            title="Week 1 Discussion",
            description="Discuss the readings",
            user_id="admin_1"
        )
        
        assert discussion.title == "Week 1 Discussion"
        assert discussion.id in agent.discussions
    
    @pytest.mark.asyncio
    async def test_create_post(self, agent):
        """Test creating discussion posts."""
        course = await create_published_course(agent)
        discussion = await agent.create_discussion(
            course.id, "Discussion", "", user_id="a1"
        )
        
        post = await agent.create_post(
            discussion_id=discussion.id,
            author_id="student_1",
            author_name="Alice",
            content="My thoughts..."
        )
        
        assert post.content == "My thoughts..."
        assert post.author_name == "Alice"
    
    @pytest.mark.asyncio
    async def test_posts_chronological(self, agent):
        """Test posts returned chronologically."""
        course = await create_published_course(agent)
        discussion = await agent.create_discussion(
            course.id, "Discussion", "", user_id="a1"
        )
        
        await agent.create_post(discussion.id, "s1", "Alice", "First")
        await agent.create_post(discussion.id, "s2", "Bob", "Second")
        
        posts = await agent.get_discussion_posts(discussion.id)
        assert posts[0].content == "First"
        assert posts[1].content == "Second"


# ============================================================================
# RESOURCE TESTS
# ============================================================================

class TestResources:
    """Test course resources."""
    
    @pytest.mark.asyncio
    async def test_add_resource(self, agent):
        """Test adding a resource."""
        course = await create_published_course(agent)
        
        resource = await agent.add_resource(
            course_id=course.id,
            title="Lecture Slides",
            description="Week 1 slides",
            content_type=ContentType.DOCUMENT,
            url="https://example.com/slides.pdf",
            user_id="admin_1"
        )
        
        assert resource.title == "Lecture Slides"
        assert resource.id in agent.resources
    
    @pytest.mark.asyncio
    async def test_resources_alphabetical(self, agent):
        """Test resources returned alphabetically."""
        course = await create_published_course(agent)
        
        await agent.add_resource(course.id, "Zebra Guide", "", ContentType.DOCUMENT, "url", user_id="a1")
        await agent.add_resource(course.id, "Alpha Notes", "", ContentType.DOCUMENT, "url", user_id="a1")
        
        resources = await agent.get_resources(course.id)
        titles = [r.title for r in resources]
        assert titles == ["Alpha Notes", "Zebra Guide"]


# ============================================================================
# ANNOUNCEMENT TESTS
# ============================================================================

class TestAnnouncements:
    """Test course announcements."""
    
    @pytest.mark.asyncio
    async def test_create_announcement(self, agent):
        """Test creating announcement."""
        course = await create_published_course(agent)
        
        announcement = await agent.create_announcement(
            course_id=course.id,
            title="Welcome!",
            content="Welcome to the course",
            author_id="instructor_1"
        )
        
        assert announcement.title == "Welcome!"
    
    @pytest.mark.asyncio
    async def test_pinned_announcements_first(self, agent):
        """Test pinned announcements appear first."""
        course = await create_published_course(agent)
        
        await agent.create_announcement(course.id, "Regular", "Content", "i1", pinned=False)
        await agent.create_announcement(course.id, "Pinned", "Important", "i1", pinned=True)
        
        announcements = await agent.get_announcements(course.id)
        assert announcements[0].pinned is True
        assert announcements[1].pinned is False


# ============================================================================
# CERTIFICATE GOVERNANCE TESTS
# ============================================================================

class TestCertificateGovernance:
    """Test certificate verification workflow."""
    
    @pytest.mark.asyncio
    async def test_request_certificate(self, agent):
        """Test requesting a certificate."""
        course = await create_published_course(agent)
        enrollment = await agent.enroll_student(course.id, "s1", "Alice")
        
        # Mark as completed
        enrollment.status = EnrollmentStatus.COMPLETED
        enrollment.final_grade = Decimal("85")
        
        cert = await agent.request_certificate(
            course_id=course.id,
            student_id="s1",
            student_name="Alice"
        )
        
        assert cert.status == CertificateStatus.PENDING
    
    @pytest.mark.asyncio
    async def test_verify_certificate(self, agent):
        """Test verifying certificate (GOVERNANCE)."""
        course = await create_published_course(agent)
        enrollment = await agent.enroll_student(course.id, "s1", "Alice")
        enrollment.status = EnrollmentStatus.COMPLETED
        enrollment.final_grade = Decimal("85")
        cert = await agent.request_certificate(course.id, "s1", "Alice")
        
        verified = await agent.verify_certificate(cert.id, "verifier_1")
        assert verified.status == CertificateStatus.VERIFIED
        assert verified.verified_by == "verifier_1"
    
    @pytest.mark.asyncio
    async def test_issue_certificate(self, agent):
        """Test issuing certificate after verification."""
        course = await create_published_course(agent)
        enrollment = await agent.enroll_student(course.id, "s1", "Alice")
        enrollment.status = EnrollmentStatus.COMPLETED
        enrollment.final_grade = Decimal("85")
        cert = await agent.request_certificate(course.id, "s1", "Alice")
        await agent.verify_certificate(cert.id, "verifier_1")
        
        issued = await agent.issue_certificate(cert.id, "issuer_1")
        assert issued.status == CertificateStatus.ISSUED
        assert issued.certificate_url is not None
    
    @pytest.mark.asyncio
    async def test_cannot_issue_without_verification(self, agent):
        """Test cannot issue unverified certificate."""
        course = await create_published_course(agent)
        enrollment = await agent.enroll_student(course.id, "s1", "Alice")
        enrollment.status = EnrollmentStatus.COMPLETED
        enrollment.final_grade = Decimal("85")
        cert = await agent.request_certificate(course.id, "s1", "Alice")
        
        with pytest.raises(ValueError, match="must be verified"):
            await agent.issue_certificate(cert.id, "issuer_1")


# ============================================================================
# PROGRESS TRACKING TESTS
# ============================================================================

class TestProgressTracking:
    """Test student progress tracking."""
    
    @pytest.mark.asyncio
    async def test_mark_lesson_complete(self, agent):
        """Test marking lesson as complete."""
        course = await create_published_course(agent)
        await agent.enroll_student(course.id, "s1", "Alice")
        module, lesson = await create_module_with_lessons(agent, course.id)
        
        progress = await agent.mark_lesson_complete(
            lesson_id=lesson.id,
            student_id="s1",
            time_spent_minutes=25
        )
        
        assert lesson.id in progress.lessons_completed
        assert progress.total_time_minutes == 25
    
    @pytest.mark.asyncio
    async def test_module_completes_with_all_lessons(self, agent):
        """Test module marked complete when all lessons done."""
        course = await create_published_course(agent)
        await agent.enroll_student(course.id, "s1", "Alice")
        module = await agent.create_module(course.id, "M1", "", 1, user_id="a1")
        lesson1 = await agent.create_lesson(module.id, "L1", ContentType.VIDEO, 1, user_id="a1")
        lesson2 = await agent.create_lesson(module.id, "L2", ContentType.VIDEO, 2, user_id="a1")
        
        await agent.mark_lesson_complete(lesson1.id, "s1")
        progress = await agent.mark_lesson_complete(lesson2.id, "s1")
        
        assert module.id in progress.modules_completed


# ============================================================================
# LEARNING PATH TESTS
# ============================================================================

class TestLearningPaths:
    """Test learning paths."""
    
    @pytest.mark.asyncio
    async def test_create_learning_path(self, agent):
        """Test creating a learning path."""
        course1 = await create_published_course(agent)
        course2 = await agent.create_course(
            "CS102", "Advanced CS", "", "i1", "CS", user_id="a1"
        )
        
        path = await agent.create_learning_path(
            title="CS Track",
            description="Complete CS curriculum",
            course_ids=[course1.id, course2.id],
            user_id="admin_1"
        )
        
        assert path.title == "CS Track"
        assert len(path.course_ids) == 2
    
    @pytest.mark.asyncio
    async def test_learning_paths_alphabetical(self, agent):
        """Test learning paths returned alphabetically."""
        c1 = await create_published_course(agent)
        
        await agent.create_learning_path("Zebra Path", "", [c1.id], "a1")
        await agent.create_learning_path("Alpha Path", "", [c1.id], "a1")
        
        paths = await agent.get_learning_paths()
        titles = [p.title for p in paths]
        assert titles == ["Alpha Path", "Zebra Path"]


# ============================================================================
# GRADEBOOK TESTS
# ============================================================================

class TestGradebook:
    """Test gradebook functionality."""
    
    @pytest.mark.asyncio
    async def test_gradebook_students_alphabetical(self, agent):
        """Test gradebook lists students alphabetically (Rule #5)."""
        course = await create_published_course(agent)
        await agent.enroll_student(course.id, "s3", "Zara Wilson")
        await agent.enroll_student(course.id, "s1", "Alice Smith")
        await agent.enroll_student(course.id, "s2", "Bob Jones")
        
        gradebook = await agent.get_gradebook(course.id)
        
        names = [s["student_name"] for s in gradebook["students"]]
        assert names == ["Alice Smith", "Bob Jones", "Zara Wilson"]
        assert gradebook["sort_order"] == "alphabetical_by_name"


# ============================================================================
# ANALYTICS TESTS
# ============================================================================

class TestAnalytics:
    """Test course analytics."""
    
    @pytest.mark.asyncio
    async def test_course_analytics(self, agent):
        """Test course analytics."""
        course = await create_published_course(agent)
        await agent.enroll_student(course.id, "s1", "Alice")
        await agent.enroll_student(course.id, "s2", "Bob")
        module, lesson = await create_module_with_lessons(agent, course.id)
        
        analytics = await agent.get_course_analytics(course.id)
        
        assert analytics["enrollment"]["active"] == 2
        assert analytics["modules_count"] == 1
        assert analytics["lessons_count"] == 1


# ============================================================================
# HEALTH CHECK TESTS
# ============================================================================

class TestHealthCheck:
    """Test health check."""
    
    @pytest.mark.asyncio
    async def test_health_check(self, agent):
        """Test health check returns stats."""
        health = await agent.get_health()
        
        assert health["status"] == "healthy"
        assert health["service"] == "education_agent"
        assert "stats" in health


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
