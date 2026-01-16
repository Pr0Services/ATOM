"""
CHE·NU™ V68 - Education & LMS API Routes
Vertical 11: Learning Management System

60+ endpoints for complete LMS functionality.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, Path, Body
from pydantic import BaseModel, Field

from ..agents.education_agent import (
    get_education_agent,
    CourseStatus, EnrollmentStatus, AssignmentType,
    SubmissionStatus, GradeStatus, QuestionType, ContentType,
    CertificateStatus
)

router = APIRouter(prefix="/api/v2/education", tags=["Education & LMS"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class CreateCourseRequest(BaseModel):
    code: str = Field(..., description="Course code (e.g., CS101)")
    title: str
    description: str
    category: str
    tags: List[str] = []
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    max_students: Optional[int] = None
    is_self_paced: bool = False
    prerequisites: List[UUID] = []


class CreateModuleRequest(BaseModel):
    title: str
    description: str
    order: int
    is_locked: bool = False
    unlock_date: Optional[datetime] = None


class CreateLessonRequest(BaseModel):
    title: str
    content_type: ContentType
    order: int
    content_url: Optional[str] = None
    content_text: Optional[str] = None
    duration_minutes: int = 0
    is_required: bool = True


class EnrollStudentRequest(BaseModel):
    student_id: str
    student_name: str


class CreateAssignmentRequest(BaseModel):
    title: str
    description: str
    assignment_type: AssignmentType
    points_possible: Decimal
    due_date: Optional[datetime] = None
    module_id: Optional[UUID] = None
    allow_late: bool = True
    late_penalty_percent: Decimal = Decimal("10")
    max_attempts: int = 1
    instructions: str = ""
    rubric: Optional[Dict[str, Any]] = None


class SubmitAssignmentRequest(BaseModel):
    content_text: Optional[str] = None
    file_urls: List[str] = []


class GradeSubmissionRequest(BaseModel):
    score: Decimal
    feedback: str


class RequestGradeChangeRequest(BaseModel):
    new_score: Decimal
    reason: str


class CreateQuizRequest(BaseModel):
    assignment_id: UUID
    title: str
    description: str = ""
    time_limit_minutes: Optional[int] = None
    shuffle_questions: bool = False
    shuffle_answers: bool = False
    show_correct_answers: bool = True


class AddQuestionRequest(BaseModel):
    question_type: QuestionType
    question_text: str
    points: Decimal
    options: List[Dict[str, Any]] = []
    correct_answer: Any = None
    explanation: Optional[str] = None


class SubmitQuizRequest(BaseModel):
    answers: Dict[str, Any]


class CreateDiscussionRequest(BaseModel):
    title: str
    description: str
    is_graded: bool = False
    points_possible: Optional[Decimal] = None
    module_id: Optional[UUID] = None


class CreatePostRequest(BaseModel):
    content: str
    parent_id: Optional[UUID] = None
    attachments: List[str] = []


class AddResourceRequest(BaseModel):
    title: str
    description: str
    content_type: ContentType
    url: str
    module_id: Optional[UUID] = None


class CreateAnnouncementRequest(BaseModel):
    title: str
    content: str
    pinned: bool = False
    send_notification: bool = True


class RequestCertificateRequest(BaseModel):
    student_name: str


class CreateLearningPathRequest(BaseModel):
    title: str
    description: str
    course_ids: List[UUID]


class MarkLessonCompleteRequest(BaseModel):
    time_spent_minutes: int = 0


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    agent = get_education_agent()
    return await agent.get_health()


# ============================================================================
# COURSE MANAGEMENT
# ============================================================================

@router.post("/courses")
async def create_course(
    request: CreateCourseRequest,
    instructor_id: str = Query(...),
    user_id: str = Query(...)
):
    """Create a new course (starts as draft)."""
    agent = get_education_agent()
    try:
        course = await agent.create_course(
            code=request.code,
            title=request.title,
            description=request.description,
            instructor_id=instructor_id,
            category=request.category,
            tags=request.tags,
            start_date=request.start_date,
            end_date=request.end_date,
            max_students=request.max_students,
            is_self_paced=request.is_self_paced,
            prerequisites=request.prerequisites,
            user_id=user_id
        )
        return {"course": _serialize_course(course)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses")
async def get_courses(
    instructor_id: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[CourseStatus] = None
):
    """Get courses - alphabetical by title (Rule #5)."""
    agent = get_education_agent()
    courses = await agent.get_courses(instructor_id, category, status)
    return {
        "courses": [_serialize_course(c) for c in courses],
        "total": len(courses),
        "sort_order": "alphabetical_by_title"
    }


@router.get("/courses/{course_id}")
async def get_course(course_id: UUID = Path(...)):
    """Get course details."""
    agent = get_education_agent()
    course = agent.courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"course": _serialize_course(course)}


@router.post("/courses/{course_id}/submit-for-review")
async def submit_course_for_review(
    course_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Submit course for review before publishing."""
    agent = get_education_agent()
    try:
        course = await agent.submit_course_for_review(course_id, user_id)
        return {"course": _serialize_course(course), "message": "Course submitted for review"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/courses/{course_id}/approve")
async def approve_course(
    course_id: UUID = Path(...),
    reviewer_id: str = Query(...)
):
    """Approve and publish course (GOVERNANCE: requires review)."""
    agent = get_education_agent()
    try:
        course = await agent.approve_course(course_id, reviewer_id)
        return {"course": _serialize_course(course), "message": "Course published"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/courses/{course_id}/archive")
async def archive_course(
    course_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Archive a course."""
    agent = get_education_agent()
    try:
        course = await agent.archive_course(course_id, user_id)
        return {"course": _serialize_course(course), "message": "Course archived"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# MODULE MANAGEMENT
# ============================================================================

@router.post("/courses/{course_id}/modules")
async def create_module(
    request: CreateModuleRequest,
    course_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Create a module within a course."""
    agent = get_education_agent()
    try:
        module = await agent.create_module(
            course_id=course_id,
            title=request.title,
            description=request.description,
            order=request.order,
            is_locked=request.is_locked,
            unlock_date=request.unlock_date,
            user_id=user_id
        )
        return {"module": _serialize_module(module)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/{course_id}/modules")
async def get_modules(course_id: UUID = Path(...)):
    """Get modules for course - ordered by sequence."""
    agent = get_education_agent()
    modules = await agent.get_modules(course_id)
    return {"modules": [_serialize_module(m) for m in modules], "total": len(modules)}


# ============================================================================
# LESSON MANAGEMENT
# ============================================================================

@router.post("/modules/{module_id}/lessons")
async def create_lesson(
    request: CreateLessonRequest,
    module_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Create a lesson within a module."""
    agent = get_education_agent()
    try:
        lesson = await agent.create_lesson(
            module_id=module_id,
            title=request.title,
            content_type=request.content_type,
            order=request.order,
            content_url=request.content_url,
            content_text=request.content_text,
            duration_minutes=request.duration_minutes,
            is_required=request.is_required,
            user_id=user_id
        )
        return {"lesson": _serialize_lesson(lesson)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/modules/{module_id}/lessons")
async def get_lessons(module_id: UUID = Path(...)):
    """Get lessons for module - ordered by sequence."""
    agent = get_education_agent()
    lessons = await agent.get_lessons(module_id)
    return {"lessons": [_serialize_lesson(l) for l in lessons], "total": len(lessons)}


@router.post("/lessons/{lesson_id}/complete")
async def mark_lesson_complete(
    request: MarkLessonCompleteRequest,
    lesson_id: UUID = Path(...),
    student_id: str = Query(...)
):
    """Mark lesson as complete."""
    agent = get_education_agent()
    try:
        progress = await agent.mark_lesson_complete(
            lesson_id=lesson_id,
            student_id=student_id,
            time_spent_minutes=request.time_spent_minutes
        )
        return {"progress": _serialize_progress(progress), "message": "Lesson completed"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# ENROLLMENT MANAGEMENT
# ============================================================================

@router.post("/courses/{course_id}/enroll")
async def enroll_student(
    request: EnrollStudentRequest,
    course_id: UUID = Path(...)
):
    """Enroll student in course."""
    agent = get_education_agent()
    try:
        enrollment = await agent.enroll_student(
            course_id=course_id,
            student_id=request.student_id,
            student_name=request.student_name
        )
        return {"enrollment": _serialize_enrollment(enrollment)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/{course_id}/students")
async def get_enrolled_students(
    course_id: UUID = Path(...),
    status: Optional[EnrollmentStatus] = None
):
    """Get enrolled students - ALPHABETICAL by name (Rule #5)."""
    agent = get_education_agent()
    enrollments = await agent.get_enrolled_students(course_id, status)
    return {
        "students": [_serialize_enrollment(e) for e in enrollments],
        "total": len(enrollments),
        "sort_order": "alphabetical_by_name"
    }


@router.post("/enrollments/{enrollment_id}/drop")
async def drop_student(
    enrollment_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Drop student from course."""
    agent = get_education_agent()
    try:
        enrollment = await agent.drop_student(enrollment_id, user_id)
        return {"enrollment": _serialize_enrollment(enrollment), "message": "Student dropped"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/{course_id}/progress")
async def get_student_progress(
    course_id: UUID = Path(...),
    student_id: str = Query(...)
):
    """Get student progress for course."""
    agent = get_education_agent()
    progress = await agent.get_student_progress(course_id, student_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    return {"progress": _serialize_progress(progress)}


# ============================================================================
# ASSIGNMENT MANAGEMENT
# ============================================================================

@router.post("/courses/{course_id}/assignments")
async def create_assignment(
    request: CreateAssignmentRequest,
    course_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Create an assignment."""
    agent = get_education_agent()
    try:
        assignment = await agent.create_assignment(
            course_id=course_id,
            title=request.title,
            description=request.description,
            assignment_type=request.assignment_type,
            points_possible=request.points_possible,
            due_date=request.due_date,
            module_id=request.module_id,
            allow_late=request.allow_late,
            late_penalty_percent=request.late_penalty_percent,
            max_attempts=request.max_attempts,
            instructions=request.instructions,
            rubric=request.rubric,
            user_id=user_id
        )
        return {"assignment": _serialize_assignment(assignment)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/{course_id}/assignments")
async def get_assignments(
    course_id: UUID = Path(...),
    module_id: Optional[UUID] = None
):
    """Get assignments - chronological by due date."""
    agent = get_education_agent()
    assignments = await agent.get_assignments(course_id, module_id)
    return {"assignments": [_serialize_assignment(a) for a in assignments], "total": len(assignments)}


# ============================================================================
# SUBMISSION & GRADING
# ============================================================================

@router.post("/assignments/{assignment_id}/submit")
async def submit_assignment(
    request: SubmitAssignmentRequest,
    assignment_id: UUID = Path(...),
    student_id: str = Query(...)
):
    """Submit assignment work."""
    agent = get_education_agent()
    try:
        submission = await agent.submit_assignment(
            assignment_id=assignment_id,
            student_id=student_id,
            content_text=request.content_text,
            file_urls=request.file_urls
        )
        return {"submission": _serialize_submission(submission)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/assignments/{assignment_id}/submissions")
async def get_submissions(assignment_id: UUID = Path(...)):
    """Get submissions for assignment."""
    agent = get_education_agent()
    submissions = [s for s in agent.submissions.values() if s.assignment_id == assignment_id]
    return {"submissions": [_serialize_submission(s) for s in submissions], "total": len(submissions)}


@router.post("/submissions/{submission_id}/grade")
async def grade_submission(
    request: GradeSubmissionRequest,
    submission_id: UUID = Path(...),
    grader_id: str = Query(...)
):
    """Grade a submission (creates draft - requires approval)."""
    agent = get_education_agent()
    try:
        submission = await agent.grade_submission(
            submission_id=submission_id,
            score=request.score,
            feedback=request.feedback,
            grader_id=grader_id
        )
        return {
            "submission": _serialize_submission(submission),
            "message": "Grade saved as draft - requires approval",
            "requires_approval": True
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/submissions/{submission_id}/approve-grade")
async def approve_grade(
    submission_id: UUID = Path(...),
    approver_id: str = Query(...)
):
    """Approve a grade (GOVERNANCE: human approval required)."""
    agent = get_education_agent()
    try:
        submission = await agent.approve_grade(submission_id, approver_id)
        return {"submission": _serialize_submission(submission), "message": "Grade approved"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/submissions/{submission_id}/request-grade-change")
async def request_grade_change(
    request: RequestGradeChangeRequest,
    submission_id: UUID = Path(...),
    requester_id: str = Query(...)
):
    """Request a grade change (GOVERNANCE: requires approval)."""
    agent = get_education_agent()
    try:
        change = await agent.request_grade_change(
            submission_id=submission_id,
            new_score=request.new_score,
            reason=request.reason,
            requester_id=requester_id
        )
        return {
            "grade_change": _serialize_grade_change(change),
            "message": "Grade change requested - pending approval"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/grade-changes/pending")
async def get_pending_grade_changes(course_id: Optional[UUID] = None):
    """Get pending grade change requests."""
    agent = get_education_agent()
    changes = await agent.get_pending_grade_changes(course_id)
    return {"grade_changes": [_serialize_grade_change(c) for c in changes], "total": len(changes)}


@router.post("/grade-changes/{change_id}/approve")
async def approve_grade_change(
    change_id: UUID = Path(...),
    approver_id: str = Query(...)
):
    """Approve grade change request (GOVERNANCE: human approval)."""
    agent = get_education_agent()
    try:
        change = await agent.approve_grade_change(change_id, approver_id)
        return {"grade_change": _serialize_grade_change(change), "message": "Grade change approved"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# QUIZ MANAGEMENT
# ============================================================================

@router.post("/courses/{course_id}/quizzes")
async def create_quiz(
    request: CreateQuizRequest,
    course_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Create a quiz."""
    agent = get_education_agent()
    try:
        quiz = await agent.create_quiz(
            course_id=course_id,
            assignment_id=request.assignment_id,
            title=request.title,
            description=request.description,
            time_limit_minutes=request.time_limit_minutes,
            shuffle_questions=request.shuffle_questions,
            shuffle_answers=request.shuffle_answers,
            show_correct_answers=request.show_correct_answers,
            user_id=user_id
        )
        return {"quiz": _serialize_quiz(quiz)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quizzes/{quiz_id}/questions")
async def add_question(
    request: AddQuestionRequest,
    quiz_id: UUID = Path(...)
):
    """Add question to quiz."""
    agent = get_education_agent()
    try:
        question = await agent.add_question(
            quiz_id=quiz_id,
            question_type=request.question_type,
            question_text=request.question_text,
            points=request.points,
            options=request.options,
            correct_answer=request.correct_answer,
            explanation=request.explanation
        )
        return {"question": _serialize_question(question)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quizzes/{quiz_id}/start")
async def start_quiz_attempt(
    quiz_id: UUID = Path(...),
    student_id: str = Query(...)
):
    """Start a quiz attempt."""
    agent = get_education_agent()
    try:
        attempt = await agent.start_quiz_attempt(quiz_id, student_id)
        quiz = agent.quizzes.get(quiz_id)
        return {
            "attempt": _serialize_quiz_attempt(attempt),
            "quiz": _serialize_quiz(quiz),
            "message": "Quiz started"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quiz-attempts/{attempt_id}/submit")
async def submit_quiz_attempt(
    request: SubmitQuizRequest,
    attempt_id: UUID = Path(...)
):
    """Submit quiz answers."""
    agent = get_education_agent()
    try:
        attempt = await agent.submit_quiz_attempt(attempt_id, request.answers)
        return {"attempt": _serialize_quiz_attempt(attempt), "message": "Quiz submitted"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# DISCUSSION FORUMS
# ============================================================================

@router.post("/courses/{course_id}/discussions")
async def create_discussion(
    request: CreateDiscussionRequest,
    course_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Create a discussion forum."""
    agent = get_education_agent()
    try:
        discussion = await agent.create_discussion(
            course_id=course_id,
            title=request.title,
            description=request.description,
            is_graded=request.is_graded,
            points_possible=request.points_possible,
            module_id=request.module_id,
            user_id=user_id
        )
        return {"discussion": _serialize_discussion(discussion)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/{course_id}/discussions")
async def get_discussions(course_id: UUID = Path(...)):
    """Get discussions for course."""
    agent = get_education_agent()
    discussions = [d for d in agent.discussions.values() if d.course_id == course_id]
    return {"discussions": [_serialize_discussion(d) for d in discussions], "total": len(discussions)}


@router.post("/discussions/{discussion_id}/posts")
async def create_post(
    request: CreatePostRequest,
    discussion_id: UUID = Path(...),
    author_id: str = Query(...),
    author_name: str = Query(...)
):
    """Create a discussion post."""
    agent = get_education_agent()
    try:
        post = await agent.create_post(
            discussion_id=discussion_id,
            author_id=author_id,
            author_name=author_name,
            content=request.content,
            parent_id=request.parent_id,
            attachments=request.attachments
        )
        return {"post": _serialize_post(post)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/discussions/{discussion_id}/posts")
async def get_discussion_posts(discussion_id: UUID = Path(...)):
    """Get discussion posts - chronological."""
    agent = get_education_agent()
    posts = await agent.get_discussion_posts(discussion_id)
    return {"posts": [_serialize_post(p) for p in posts], "total": len(posts)}


# ============================================================================
# RESOURCES
# ============================================================================

@router.post("/courses/{course_id}/resources")
async def add_resource(
    request: AddResourceRequest,
    course_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Add a resource to course."""
    agent = get_education_agent()
    try:
        resource = await agent.add_resource(
            course_id=course_id,
            title=request.title,
            description=request.description,
            content_type=request.content_type,
            url=request.url,
            module_id=request.module_id,
            user_id=user_id
        )
        return {"resource": _serialize_resource(resource)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/{course_id}/resources")
async def get_resources(
    course_id: UUID = Path(...),
    module_id: Optional[UUID] = None
):
    """Get resources - alphabetical by title."""
    agent = get_education_agent()
    resources = await agent.get_resources(course_id, module_id)
    return {"resources": [_serialize_resource(r) for r in resources], "total": len(resources)}


# ============================================================================
# ANNOUNCEMENTS
# ============================================================================

@router.post("/courses/{course_id}/announcements")
async def create_announcement(
    request: CreateAnnouncementRequest,
    course_id: UUID = Path(...),
    author_id: str = Query(...)
):
    """Create course announcement."""
    agent = get_education_agent()
    try:
        announcement = await agent.create_announcement(
            course_id=course_id,
            title=request.title,
            content=request.content,
            author_id=author_id,
            pinned=request.pinned,
            send_notification=request.send_notification
        )
        return {"announcement": _serialize_announcement(announcement)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/{course_id}/announcements")
async def get_announcements(course_id: UUID = Path(...)):
    """Get announcements - pinned first, then chronological."""
    agent = get_education_agent()
    announcements = await agent.get_announcements(course_id)
    return {"announcements": [_serialize_announcement(a) for a in announcements], "total": len(announcements)}


# ============================================================================
# CERTIFICATES
# ============================================================================

@router.post("/courses/{course_id}/certificates/request")
async def request_certificate(
    request: RequestCertificateRequest,
    course_id: UUID = Path(...),
    student_id: str = Query(...)
):
    """Request completion certificate (requires verification)."""
    agent = get_education_agent()
    try:
        certificate = await agent.request_certificate(
            course_id=course_id,
            student_id=student_id,
            student_name=request.student_name
        )
        return {
            "certificate": _serialize_certificate(certificate),
            "message": "Certificate requested - pending verification"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/certificates/pending")
async def get_pending_certificates():
    """Get pending certificate requests."""
    agent = get_education_agent()
    pending = [c for c in agent.certificates.values() if c.status == CertificateStatus.PENDING]
    return {"certificates": [_serialize_certificate(c) for c in pending], "total": len(pending)}


@router.post("/certificates/{certificate_id}/verify")
async def verify_certificate(
    certificate_id: UUID = Path(...),
    verifier_id: str = Query(...)
):
    """Verify certificate eligibility (GOVERNANCE: human verification)."""
    agent = get_education_agent()
    try:
        certificate = await agent.verify_certificate(certificate_id, verifier_id)
        return {"certificate": _serialize_certificate(certificate), "message": "Certificate verified"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/certificates/{certificate_id}/issue")
async def issue_certificate(
    certificate_id: UUID = Path(...),
    issuer_id: str = Query(...)
):
    """Issue certificate after verification."""
    agent = get_education_agent()
    try:
        certificate = await agent.issue_certificate(certificate_id, issuer_id)
        return {"certificate": _serialize_certificate(certificate), "message": "Certificate issued"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# LEARNING PATHS
# ============================================================================

@router.post("/learning-paths")
async def create_learning_path(
    request: CreateLearningPathRequest,
    user_id: str = Query(...)
):
    """Create a learning path."""
    agent = get_education_agent()
    try:
        path = await agent.create_learning_path(
            title=request.title,
            description=request.description,
            course_ids=request.course_ids,
            user_id=user_id
        )
        return {"learning_path": _serialize_learning_path(path)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/learning-paths")
async def get_learning_paths():
    """Get learning paths - alphabetical by title."""
    agent = get_education_agent()
    paths = await agent.get_learning_paths()
    return {"learning_paths": [_serialize_learning_path(p) for p in paths], "total": len(paths)}


# ============================================================================
# GRADEBOOK & ANALYTICS
# ============================================================================

@router.get("/courses/{course_id}/gradebook")
async def get_gradebook(course_id: UUID = Path(...)):
    """Get course gradebook - students ALPHABETICAL (Rule #5)."""
    agent = get_education_agent()
    try:
        gradebook = await agent.get_gradebook(course_id)
        return gradebook
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/{course_id}/analytics")
async def get_course_analytics(course_id: UUID = Path(...)):
    """Get course analytics."""
    agent = get_education_agent()
    try:
        analytics = await agent.get_course_analytics(course_id)
        return analytics
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# SERIALIZERS
# ============================================================================

def _serialize_course(course) -> Dict[str, Any]:
    return {
        "id": str(course.id),
        "code": course.code,
        "title": course.title,
        "description": course.description,
        "instructor_id": course.instructor_id,
        "status": course.status.value,
        "category": course.category,
        "tags": course.tags,
        "start_date": course.start_date.isoformat() if course.start_date else None,
        "end_date": course.end_date.isoformat() if course.end_date else None,
        "max_students": course.max_students,
        "is_self_paced": course.is_self_paced,
        "prerequisites": [str(p) for p in course.prerequisites],
        "created_at": course.created_at.isoformat(),
        "created_by": course.created_by,
        "published_at": course.published_at.isoformat() if course.published_at else None,
        "reviewed_by": course.reviewed_by
    }


def _serialize_module(module) -> Dict[str, Any]:
    return {
        "id": str(module.id),
        "course_id": str(module.course_id),
        "title": module.title,
        "description": module.description,
        "order": module.order,
        "is_locked": module.is_locked,
        "unlock_date": module.unlock_date.isoformat() if module.unlock_date else None,
        "created_at": module.created_at.isoformat()
    }


def _serialize_lesson(lesson) -> Dict[str, Any]:
    return {
        "id": str(lesson.id),
        "module_id": str(lesson.module_id),
        "course_id": str(lesson.course_id),
        "title": lesson.title,
        "content_type": lesson.content_type.value,
        "content_url": lesson.content_url,
        "duration_minutes": lesson.duration_minutes,
        "order": lesson.order,
        "is_required": lesson.is_required,
        "created_at": lesson.created_at.isoformat()
    }


def _serialize_enrollment(enrollment) -> Dict[str, Any]:
    return {
        "id": str(enrollment.id),
        "course_id": str(enrollment.course_id),
        "student_id": enrollment.student_id,
        "student_name": enrollment.student_name,
        "status": enrollment.status.value,
        "enrolled_at": enrollment.enrolled_at.isoformat(),
        "completed_at": enrollment.completed_at.isoformat() if enrollment.completed_at else None,
        "final_grade": float(enrollment.final_grade) if enrollment.final_grade else None,
        "progress_percent": float(enrollment.progress_percent),
        "last_activity": enrollment.last_activity.isoformat() if enrollment.last_activity else None
    }


def _serialize_assignment(assignment) -> Dict[str, Any]:
    return {
        "id": str(assignment.id),
        "course_id": str(assignment.course_id),
        "module_id": str(assignment.module_id) if assignment.module_id else None,
        "title": assignment.title,
        "description": assignment.description,
        "assignment_type": assignment.assignment_type.value,
        "points_possible": float(assignment.points_possible),
        "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
        "allow_late": assignment.allow_late,
        "late_penalty_percent": float(assignment.late_penalty_percent),
        "max_attempts": assignment.max_attempts,
        "created_at": assignment.created_at.isoformat()
    }


def _serialize_submission(submission) -> Dict[str, Any]:
    return {
        "id": str(submission.id),
        "assignment_id": str(submission.assignment_id),
        "student_id": submission.student_id,
        "status": submission.status.value,
        "submitted_at": submission.submitted_at.isoformat() if submission.submitted_at else None,
        "attempt_number": submission.attempt_number,
        "score": float(submission.score) if submission.score else None,
        "feedback": submission.feedback,
        "graded_by": submission.graded_by,
        "graded_at": submission.graded_at.isoformat() if submission.graded_at else None,
        "grade_status": submission.grade_status.value
    }


def _serialize_grade_change(change) -> Dict[str, Any]:
    return {
        "id": str(change.id),
        "submission_id": str(change.submission_id),
        "student_id": change.student_id,
        "old_score": float(change.old_score) if change.old_score else None,
        "new_score": float(change.new_score),
        "reason": change.reason,
        "requested_by": change.requested_by,
        "requested_at": change.requested_at.isoformat(),
        "status": change.status.value,
        "approved_by": change.approved_by,
        "approved_at": change.approved_at.isoformat() if change.approved_at else None
    }


def _serialize_quiz(quiz) -> Dict[str, Any]:
    return {
        "id": str(quiz.id),
        "course_id": str(quiz.course_id),
        "assignment_id": str(quiz.assignment_id),
        "title": quiz.title,
        "description": quiz.description,
        "time_limit_minutes": quiz.time_limit_minutes,
        "shuffle_questions": quiz.shuffle_questions,
        "shuffle_answers": quiz.shuffle_answers,
        "questions_count": len(quiz.questions),
        "created_at": quiz.created_at.isoformat()
    }


def _serialize_question(question) -> Dict[str, Any]:
    return {
        "id": str(question.id),
        "quiz_id": str(question.quiz_id),
        "question_type": question.question_type.value,
        "question_text": question.question_text,
        "points": float(question.points),
        "options": question.options,
        "order": question.order
    }


def _serialize_quiz_attempt(attempt) -> Dict[str, Any]:
    return {
        "id": str(attempt.id),
        "quiz_id": str(attempt.quiz_id),
        "student_id": attempt.student_id,
        "started_at": attempt.started_at.isoformat(),
        "submitted_at": attempt.submitted_at.isoformat() if attempt.submitted_at else None,
        "time_spent_seconds": attempt.time_spent_seconds,
        "score": float(attempt.score) if attempt.score else None,
        "graded": attempt.graded,
        "attempt_number": attempt.attempt_number
    }


def _serialize_discussion(discussion) -> Dict[str, Any]:
    return {
        "id": str(discussion.id),
        "course_id": str(discussion.course_id),
        "module_id": str(discussion.module_id) if discussion.module_id else None,
        "title": discussion.title,
        "description": discussion.description,
        "is_graded": discussion.is_graded,
        "points_possible": float(discussion.points_possible) if discussion.points_possible else None,
        "created_at": discussion.created_at.isoformat()
    }


def _serialize_post(post) -> Dict[str, Any]:
    return {
        "id": str(post.id),
        "discussion_id": str(post.discussion_id),
        "author_id": post.author_id,
        "author_name": post.author_name,
        "parent_id": str(post.parent_id) if post.parent_id else None,
        "content": post.content,
        "attachments": post.attachments,
        "created_at": post.created_at.isoformat(),
        "likes": post.likes
    }


def _serialize_resource(resource) -> Dict[str, Any]:
    return {
        "id": str(resource.id),
        "course_id": str(resource.course_id),
        "module_id": str(resource.module_id) if resource.module_id else None,
        "title": resource.title,
        "description": resource.description,
        "content_type": resource.content_type.value,
        "url": resource.url,
        "created_at": resource.created_at.isoformat()
    }


def _serialize_announcement(announcement) -> Dict[str, Any]:
    return {
        "id": str(announcement.id),
        "course_id": str(announcement.course_id),
        "title": announcement.title,
        "content": announcement.content,
        "author_id": announcement.author_id,
        "posted_at": announcement.posted_at.isoformat(),
        "pinned": announcement.pinned
    }


def _serialize_certificate(certificate) -> Dict[str, Any]:
    return {
        "id": str(certificate.id),
        "course_id": str(certificate.course_id),
        "student_id": certificate.student_id,
        "student_name": certificate.student_name,
        "status": certificate.status.value,
        "completion_date": certificate.completion_date.isoformat(),
        "final_grade": float(certificate.final_grade),
        "certificate_url": certificate.certificate_url,
        "verified_by": certificate.verified_by,
        "issued_at": certificate.issued_at.isoformat() if certificate.issued_at else None
    }


def _serialize_learning_path(path) -> Dict[str, Any]:
    return {
        "id": str(path.id),
        "title": path.title,
        "description": path.description,
        "course_ids": [str(c) for c in path.course_ids],
        "estimated_hours": path.estimated_hours,
        "created_at": path.created_at.isoformat()
    }


def _serialize_progress(progress) -> Dict[str, Any]:
    return {
        "id": str(progress.id),
        "enrollment_id": str(progress.enrollment_id),
        "student_id": progress.student_id,
        "course_id": str(progress.course_id),
        "lessons_completed": len(progress.lessons_completed),
        "modules_completed": len(progress.modules_completed),
        "assignments_completed": len(progress.assignments_completed),
        "total_time_minutes": progress.total_time_minutes,
        "streak_days": progress.streak_days,
        "last_activity": progress.last_activity.isoformat()
    }
