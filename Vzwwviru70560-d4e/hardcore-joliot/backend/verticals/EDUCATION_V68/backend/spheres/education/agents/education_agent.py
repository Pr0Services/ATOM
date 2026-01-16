"""
CHE·NU™ V68 - Education & LMS Agent
Vertical 11: Learning Management System (Canvas/Blackboard Killer)

GOVERNANCE:
- Grade changes require human approval
- Certificate generation requires completion verification
- Content publishing requires review workflow

RULE #5 COMPLIANCE:
- Students listed ALPHABETICALLY (NO grade ranking)
- Courses listed ALPHABETICALLY or CHRONOLOGICALLY (NO popularity ranking)
- NO engagement-based recommendations
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Any, Set
from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class CourseStatus(Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class EnrollmentStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"
    SUSPENDED = "suspended"


class AssignmentType(Enum):
    HOMEWORK = "homework"
    QUIZ = "quiz"
    EXAM = "exam"
    PROJECT = "project"
    DISCUSSION = "discussion"
    LAB = "lab"
    ESSAY = "essay"


class SubmissionStatus(Enum):
    NOT_SUBMITTED = "not_submitted"
    SUBMITTED = "submitted"
    LATE = "late"
    GRADED = "graded"
    RETURNED = "returned"
    RESUBMIT_REQUESTED = "resubmit_requested"


class GradeStatus(Enum):
    PENDING = "pending"
    DRAFT = "draft"
    APPROVED = "approved"
    DISPUTED = "disputed"


class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    MATCHING = "matching"
    FILL_BLANK = "fill_blank"
    NUMERIC = "numeric"


class ContentType(Enum):
    VIDEO = "video"
    DOCUMENT = "document"
    LINK = "link"
    AUDIO = "audio"
    IMAGE = "image"
    EMBED = "embed"
    SCORM = "scorm"


class CertificateStatus(Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    ISSUED = "issued"
    REVOKED = "revoked"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Course:
    """Course model."""
    id: UUID
    code: str  # e.g., "CS101"
    title: str
    description: str
    instructor_id: str
    status: CourseStatus
    category: str
    tags: List[str]
    start_date: Optional[date]
    end_date: Optional[date]
    max_students: Optional[int]
    is_self_paced: bool
    prerequisites: List[UUID]  # Course IDs
    created_at: datetime
    created_by: str
    updated_at: datetime
    published_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None


@dataclass
class Module:
    """Course module/unit."""
    id: UUID
    course_id: UUID
    title: str
    description: str
    order: int
    is_locked: bool  # Requires previous module completion
    unlock_date: Optional[datetime]
    created_at: datetime
    created_by: str


@dataclass
class Lesson:
    """Lesson within a module."""
    id: UUID
    module_id: UUID
    course_id: UUID
    title: str
    content_type: ContentType
    content_url: Optional[str]
    content_text: Optional[str]
    duration_minutes: int
    order: int
    is_required: bool
    created_at: datetime
    created_by: str


@dataclass
class Assignment:
    """Assignment model."""
    id: UUID
    course_id: UUID
    module_id: Optional[UUID]
    title: str
    description: str
    assignment_type: AssignmentType
    points_possible: Decimal
    due_date: Optional[datetime]
    available_from: Optional[datetime]
    available_until: Optional[datetime]
    allow_late: bool
    late_penalty_percent: Decimal
    submission_types: List[str]  # file, text, url, etc.
    max_attempts: int
    instructions: str
    rubric: Optional[Dict[str, Any]]
    created_at: datetime
    created_by: str


@dataclass
class Quiz:
    """Quiz/exam model."""
    id: UUID
    course_id: UUID
    assignment_id: UUID  # Linked to assignment for grading
    title: str
    description: str
    time_limit_minutes: Optional[int]
    shuffle_questions: bool
    shuffle_answers: bool
    show_correct_answers: bool
    show_correct_after: Optional[datetime]
    one_question_at_a_time: bool
    cant_go_back: bool
    questions: List["QuizQuestion"]
    created_at: datetime
    created_by: str


@dataclass
class QuizQuestion:
    """Quiz question."""
    id: UUID
    quiz_id: UUID
    question_type: QuestionType
    question_text: str
    points: Decimal
    options: List[Dict[str, Any]]  # For MC, matching, etc.
    correct_answer: Any
    explanation: Optional[str]
    order: int


@dataclass
class Enrollment:
    """Student enrollment."""
    id: UUID
    course_id: UUID
    student_id: str
    student_name: str  # For alphabetical sorting
    status: EnrollmentStatus
    enrolled_at: datetime
    completed_at: Optional[datetime]
    final_grade: Optional[Decimal]
    grade_status: GradeStatus
    progress_percent: Decimal
    last_activity: Optional[datetime]


@dataclass
class Submission:
    """Assignment submission."""
    id: UUID
    assignment_id: UUID
    student_id: str
    course_id: UUID
    status: SubmissionStatus
    submitted_at: Optional[datetime]
    content_text: Optional[str]
    file_urls: List[str]
    attempt_number: int
    score: Optional[Decimal]
    feedback: Optional[str]
    graded_by: Optional[str]
    graded_at: Optional[datetime]
    grade_status: GradeStatus
    created_at: datetime


@dataclass
class QuizAttempt:
    """Quiz attempt by student."""
    id: UUID
    quiz_id: UUID
    student_id: str
    started_at: datetime
    submitted_at: Optional[datetime]
    time_spent_seconds: int
    answers: Dict[str, Any]  # question_id -> answer
    score: Optional[Decimal]
    graded: bool
    attempt_number: int


@dataclass
class Discussion:
    """Discussion forum."""
    id: UUID
    course_id: UUID
    module_id: Optional[UUID]
    title: str
    description: str
    is_graded: bool
    points_possible: Optional[Decimal]
    require_initial_post: bool
    allow_attachments: bool
    close_date: Optional[datetime]
    created_at: datetime
    created_by: str


@dataclass
class DiscussionPost:
    """Discussion post."""
    id: UUID
    discussion_id: UUID
    author_id: str
    author_name: str
    parent_id: Optional[UUID]  # For replies
    content: str
    attachments: List[str]
    created_at: datetime
    edited_at: Optional[datetime]
    likes: int


@dataclass 
class Resource:
    """Course resource/material."""
    id: UUID
    course_id: UUID
    module_id: Optional[UUID]
    title: str
    description: str
    content_type: ContentType
    url: str
    file_size_bytes: Optional[int]
    created_at: datetime
    created_by: str


@dataclass
class Announcement:
    """Course announcement."""
    id: UUID
    course_id: UUID
    title: str
    content: str
    author_id: str
    posted_at: datetime
    pinned: bool
    send_notification: bool


@dataclass
class Certificate:
    """Completion certificate."""
    id: UUID
    course_id: UUID
    student_id: str
    student_name: str
    status: CertificateStatus
    completion_date: date
    final_grade: Decimal
    certificate_url: Optional[str]
    verified_by: Optional[str]
    verified_at: Optional[datetime]
    issued_at: Optional[datetime]
    created_at: datetime


@dataclass
class LearningPath:
    """Sequence of courses."""
    id: UUID
    title: str
    description: str
    course_ids: List[UUID]  # Ordered sequence
    estimated_hours: int
    created_at: datetime
    created_by: str


@dataclass
class StudentProgress:
    """Track student progress through course."""
    id: UUID
    enrollment_id: UUID
    student_id: str
    course_id: UUID
    lessons_completed: Set[UUID]
    modules_completed: Set[UUID]
    assignments_completed: Set[UUID]
    total_time_minutes: int
    last_lesson_id: Optional[UUID]
    streak_days: int
    last_activity: datetime


@dataclass
class GradeChange:
    """Grade change request (GOVERNANCE)."""
    id: UUID
    submission_id: UUID
    student_id: str
    course_id: UUID
    old_score: Optional[Decimal]
    new_score: Decimal
    reason: str
    requested_by: str
    requested_at: datetime
    status: GradeStatus  # PENDING -> APPROVED
    approved_by: Optional[str]
    approved_at: Optional[datetime]


# ============================================================================
# EDUCATION AGENT
# ============================================================================

class EducationAgent:
    """
    Education & LMS Agent for CHE·NU V68.
    
    Competes with: Canvas, Blackboard, Moodle, Teachable
    
    GOVERNANCE:
    - Grade changes require approval
    - Certificates require verification
    - Course publishing requires review
    
    RULE #5:
    - Students listed alphabetically (NO grade ranking)
    - Courses listed alphabetically/chronologically (NO popularity)
    """
    
    def __init__(self):
        self.courses: Dict[UUID, Course] = {}
        self.modules: Dict[UUID, Module] = {}
        self.lessons: Dict[UUID, Lesson] = {}
        self.assignments: Dict[UUID, Assignment] = {}
        self.quizzes: Dict[UUID, Quiz] = {}
        self.enrollments: Dict[UUID, Enrollment] = {}
        self.submissions: Dict[UUID, Submission] = {}
        self.quiz_attempts: Dict[UUID, QuizAttempt] = {}
        self.discussions: Dict[UUID, Discussion] = {}
        self.discussion_posts: Dict[UUID, DiscussionPost] = {}
        self.resources: Dict[UUID, Resource] = {}
        self.announcements: Dict[UUID, Announcement] = {}
        self.certificates: Dict[UUID, Certificate] = {}
        self.learning_paths: Dict[UUID, LearningPath] = {}
        self.progress: Dict[UUID, StudentProgress] = {}
        self.grade_changes: Dict[UUID, GradeChange] = {}
    
    # ========================================================================
    # COURSE MANAGEMENT
    # ========================================================================
    
    async def create_course(
        self,
        code: str,
        title: str,
        description: str,
        instructor_id: str,
        category: str,
        tags: List[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        max_students: Optional[int] = None,
        is_self_paced: bool = False,
        prerequisites: List[UUID] = None,
        user_id: str = None
    ) -> Course:
        """
        Create a new course (starts as DRAFT).
        
        GOVERNANCE: Courses start as draft, require review to publish.
        """
        course = Course(
            id=uuid4(),
            code=code.upper(),
            title=title,
            description=description,
            instructor_id=instructor_id,
            status=CourseStatus.DRAFT,
            category=category,
            tags=sorted(tags or []),  # Alphabetical
            start_date=start_date,
            end_date=end_date,
            max_students=max_students,
            is_self_paced=is_self_paced,
            prerequisites=prerequisites or [],
            created_at=datetime.utcnow(),
            created_by=user_id or instructor_id,
            updated_at=datetime.utcnow()
        )
        
        self.courses[course.id] = course
        logger.info(f"Course created: {course.code} - {course.title}")
        return course
    
    async def submit_course_for_review(
        self,
        course_id: UUID,
        user_id: str
    ) -> Course:
        """Submit course for review before publishing."""
        course = self.courses.get(course_id)
        if not course:
            raise ValueError(f"Course {course_id} not found")
        
        if course.status != CourseStatus.DRAFT:
            raise ValueError(f"Course must be in draft status to submit for review")
        
        course.status = CourseStatus.UNDER_REVIEW
        course.updated_at = datetime.utcnow()
        
        return course
    
    async def approve_course(
        self,
        course_id: UUID,
        reviewer_id: str
    ) -> Course:
        """
        Approve and publish course.
        
        GOVERNANCE: Only reviewed courses can be published.
        """
        course = self.courses.get(course_id)
        if not course:
            raise ValueError(f"Course {course_id} not found")
        
        if course.status != CourseStatus.UNDER_REVIEW:
            raise ValueError("Course must be under review to approve")
        
        course.status = CourseStatus.PUBLISHED
        course.reviewed_by = reviewer_id
        course.published_at = datetime.utcnow()
        course.updated_at = datetime.utcnow()
        
        logger.info(f"Course published: {course.code} by {reviewer_id}")
        return course
    
    async def archive_course(
        self,
        course_id: UUID,
        user_id: str
    ) -> Course:
        """Archive a course."""
        course = self.courses.get(course_id)
        if not course:
            raise ValueError(f"Course {course_id} not found")
        
        course.status = CourseStatus.ARCHIVED
        course.updated_at = datetime.utcnow()
        
        return course
    
    async def get_courses(
        self,
        instructor_id: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[CourseStatus] = None
    ) -> List[Course]:
        """
        Get courses - ALPHABETICAL by title.
        
        RULE #5: NO popularity ranking.
        """
        courses = list(self.courses.values())
        
        if instructor_id:
            courses = [c for c in courses if c.instructor_id == instructor_id]
        if category:
            courses = [c for c in courses if c.category == category]
        if status:
            courses = [c for c in courses if c.status == status]
        
        # RULE #5: ALPHABETICAL by title
        return sorted(courses, key=lambda c: c.title.lower())
    
    # ========================================================================
    # MODULE & LESSON MANAGEMENT
    # ========================================================================
    
    async def create_module(
        self,
        course_id: UUID,
        title: str,
        description: str,
        order: int,
        is_locked: bool = False,
        unlock_date: Optional[datetime] = None,
        user_id: str = None
    ) -> Module:
        """Create a module within a course."""
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found")
        
        module = Module(
            id=uuid4(),
            course_id=course_id,
            title=title,
            description=description,
            order=order,
            is_locked=is_locked,
            unlock_date=unlock_date,
            created_at=datetime.utcnow(),
            created_by=user_id
        )
        
        self.modules[module.id] = module
        return module
    
    async def get_modules(self, course_id: UUID) -> List[Module]:
        """Get modules for course - ordered by sequence."""
        modules = [m for m in self.modules.values() if m.course_id == course_id]
        return sorted(modules, key=lambda m: m.order)
    
    async def create_lesson(
        self,
        module_id: UUID,
        title: str,
        content_type: ContentType,
        order: int,
        content_url: Optional[str] = None,
        content_text: Optional[str] = None,
        duration_minutes: int = 0,
        is_required: bool = True,
        user_id: str = None
    ) -> Lesson:
        """Create a lesson within a module."""
        module = self.modules.get(module_id)
        if not module:
            raise ValueError(f"Module {module_id} not found")
        
        lesson = Lesson(
            id=uuid4(),
            module_id=module_id,
            course_id=module.course_id,
            title=title,
            content_type=content_type,
            content_url=content_url,
            content_text=content_text,
            duration_minutes=duration_minutes,
            order=order,
            is_required=is_required,
            created_at=datetime.utcnow(),
            created_by=user_id
        )
        
        self.lessons[lesson.id] = lesson
        return lesson
    
    async def get_lessons(self, module_id: UUID) -> List[Lesson]:
        """Get lessons for module - ordered by sequence."""
        lessons = [l for l in self.lessons.values() if l.module_id == module_id]
        return sorted(lessons, key=lambda l: l.order)
    
    # ========================================================================
    # ENROLLMENT MANAGEMENT
    # ========================================================================
    
    async def enroll_student(
        self,
        course_id: UUID,
        student_id: str,
        student_name: str
    ) -> Enrollment:
        """Enroll student in course."""
        course = self.courses.get(course_id)
        if not course:
            raise ValueError(f"Course {course_id} not found")
        
        if course.status != CourseStatus.PUBLISHED:
            raise ValueError("Cannot enroll in unpublished course")
        
        # Check if already enrolled
        existing = [e for e in self.enrollments.values() 
                   if e.course_id == course_id and e.student_id == student_id
                   and e.status not in [EnrollmentStatus.DROPPED]]
        if existing:
            raise ValueError("Student already enrolled")
        
        # Check max students
        if course.max_students:
            active = len([e for e in self.enrollments.values()
                         if e.course_id == course_id 
                         and e.status == EnrollmentStatus.ACTIVE])
            if active >= course.max_students:
                raise ValueError("Course is full")
        
        enrollment = Enrollment(
            id=uuid4(),
            course_id=course_id,
            student_id=student_id,
            student_name=student_name,
            status=EnrollmentStatus.ACTIVE,
            enrolled_at=datetime.utcnow(),
            completed_at=None,
            final_grade=None,
            grade_status=GradeStatus.PENDING,
            progress_percent=Decimal("0"),
            last_activity=datetime.utcnow()
        )
        
        self.enrollments[enrollment.id] = enrollment
        
        # Initialize progress tracking
        progress = StudentProgress(
            id=uuid4(),
            enrollment_id=enrollment.id,
            student_id=student_id,
            course_id=course_id,
            lessons_completed=set(),
            modules_completed=set(),
            assignments_completed=set(),
            total_time_minutes=0,
            last_lesson_id=None,
            streak_days=0,
            last_activity=datetime.utcnow()
        )
        self.progress[progress.id] = progress
        
        return enrollment
    
    async def get_enrolled_students(
        self,
        course_id: UUID,
        status: Optional[EnrollmentStatus] = None
    ) -> List[Enrollment]:
        """
        Get enrolled students - ALPHABETICAL by name.
        
        RULE #5: NO grade ranking. Students listed alphabetically.
        """
        enrollments = [e for e in self.enrollments.values() 
                      if e.course_id == course_id]
        
        if status:
            enrollments = [e for e in enrollments if e.status == status]
        
        # RULE #5: ALPHABETICAL by student name (NOT by grade)
        return sorted(enrollments, key=lambda e: e.student_name.lower())
    
    async def drop_student(
        self,
        enrollment_id: UUID,
        user_id: str
    ) -> Enrollment:
        """Drop student from course."""
        enrollment = self.enrollments.get(enrollment_id)
        if not enrollment:
            raise ValueError(f"Enrollment {enrollment_id} not found")
        
        enrollment.status = EnrollmentStatus.DROPPED
        return enrollment
    
    # ========================================================================
    # ASSIGNMENT MANAGEMENT
    # ========================================================================
    
    async def create_assignment(
        self,
        course_id: UUID,
        title: str,
        description: str,
        assignment_type: AssignmentType,
        points_possible: Decimal,
        due_date: Optional[datetime] = None,
        module_id: Optional[UUID] = None,
        allow_late: bool = True,
        late_penalty_percent: Decimal = Decimal("10"),
        max_attempts: int = 1,
        instructions: str = "",
        rubric: Optional[Dict[str, Any]] = None,
        user_id: str = None
    ) -> Assignment:
        """Create an assignment."""
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found")
        
        assignment = Assignment(
            id=uuid4(),
            course_id=course_id,
            module_id=module_id,
            title=title,
            description=description,
            assignment_type=assignment_type,
            points_possible=points_possible,
            due_date=due_date,
            available_from=datetime.utcnow(),
            available_until=None,
            allow_late=allow_late,
            late_penalty_percent=late_penalty_percent,
            submission_types=["file", "text"],
            max_attempts=max_attempts,
            instructions=instructions,
            rubric=rubric,
            created_at=datetime.utcnow(),
            created_by=user_id
        )
        
        self.assignments[assignment.id] = assignment
        return assignment
    
    async def get_assignments(
        self,
        course_id: UUID,
        module_id: Optional[UUID] = None
    ) -> List[Assignment]:
        """Get assignments - chronological by due date."""
        assignments = [a for a in self.assignments.values()
                      if a.course_id == course_id]
        
        if module_id:
            assignments = [a for a in assignments if a.module_id == module_id]
        
        # Chronological by due date
        return sorted(assignments, key=lambda a: (a.due_date or datetime.max, a.title))
    
    # ========================================================================
    # SUBMISSION & GRADING
    # ========================================================================
    
    async def submit_assignment(
        self,
        assignment_id: UUID,
        student_id: str,
        content_text: Optional[str] = None,
        file_urls: List[str] = None
    ) -> Submission:
        """Submit assignment work."""
        assignment = self.assignments.get(assignment_id)
        if not assignment:
            raise ValueError(f"Assignment {assignment_id} not found")
        
        # Check enrollment
        enrolled = any(e.student_id == student_id 
                      and e.course_id == assignment.course_id
                      and e.status == EnrollmentStatus.ACTIVE
                      for e in self.enrollments.values())
        if not enrolled:
            raise ValueError("Student not enrolled in course")
        
        # Count previous attempts
        prev_attempts = len([s for s in self.submissions.values()
                           if s.assignment_id == assignment_id 
                           and s.student_id == student_id])
        
        if prev_attempts >= assignment.max_attempts:
            raise ValueError(f"Maximum attempts ({assignment.max_attempts}) reached")
        
        # Determine if late
        is_late = False
        if assignment.due_date and datetime.utcnow() > assignment.due_date:
            if not assignment.allow_late:
                raise ValueError("Late submissions not allowed")
            is_late = True
        
        submission = Submission(
            id=uuid4(),
            assignment_id=assignment_id,
            student_id=student_id,
            course_id=assignment.course_id,
            status=SubmissionStatus.LATE if is_late else SubmissionStatus.SUBMITTED,
            submitted_at=datetime.utcnow(),
            content_text=content_text,
            file_urls=file_urls or [],
            attempt_number=prev_attempts + 1,
            score=None,
            feedback=None,
            graded_by=None,
            graded_at=None,
            grade_status=GradeStatus.PENDING,
            created_at=datetime.utcnow()
        )
        
        self.submissions[submission.id] = submission
        return submission
    
    async def grade_submission(
        self,
        submission_id: UUID,
        score: Decimal,
        feedback: str,
        grader_id: str
    ) -> Submission:
        """
        Grade a submission (DRAFT status - requires approval).
        
        GOVERNANCE: Grades start as draft, require approval.
        """
        submission = self.submissions.get(submission_id)
        if not submission:
            raise ValueError(f"Submission {submission_id} not found")
        
        assignment = self.assignments.get(submission.assignment_id)
        if score > assignment.points_possible:
            raise ValueError(f"Score cannot exceed {assignment.points_possible}")
        
        # Apply late penalty if applicable
        if submission.status == SubmissionStatus.LATE:
            penalty = assignment.late_penalty_percent / 100
            score = score * (1 - penalty)
        
        submission.score = score
        submission.feedback = feedback
        submission.graded_by = grader_id
        submission.graded_at = datetime.utcnow()
        submission.grade_status = GradeStatus.DRAFT  # Requires approval
        submission.status = SubmissionStatus.GRADED
        
        return submission
    
    async def approve_grade(
        self,
        submission_id: UUID,
        approver_id: str
    ) -> Submission:
        """
        Approve a grade.
        
        GOVERNANCE: Grades require human approval before finalization.
        """
        submission = self.submissions.get(submission_id)
        if not submission:
            raise ValueError(f"Submission {submission_id} not found")
        
        if submission.grade_status != GradeStatus.DRAFT:
            raise ValueError("Grade must be in draft status to approve")
        
        submission.grade_status = GradeStatus.APPROVED
        
        # Update student progress
        self._update_progress_for_assignment(submission)
        
        logger.info(f"Grade approved: submission {submission_id} by {approver_id}")
        return submission
    
    def _update_progress_for_assignment(self, submission: Submission):
        """Update progress when assignment completed."""
        for progress in self.progress.values():
            if (progress.student_id == submission.student_id 
                and progress.course_id == submission.course_id):
                progress.assignments_completed.add(submission.assignment_id)
                progress.last_activity = datetime.utcnow()
                break
    
    async def request_grade_change(
        self,
        submission_id: UUID,
        new_score: Decimal,
        reason: str,
        requester_id: str
    ) -> GradeChange:
        """
        Request a grade change.
        
        GOVERNANCE: Grade changes require approval workflow.
        """
        submission = self.submissions.get(submission_id)
        if not submission:
            raise ValueError(f"Submission {submission_id} not found")
        
        change = GradeChange(
            id=uuid4(),
            submission_id=submission_id,
            student_id=submission.student_id,
            course_id=submission.course_id,
            old_score=submission.score,
            new_score=new_score,
            reason=reason,
            requested_by=requester_id,
            requested_at=datetime.utcnow(),
            status=GradeStatus.PENDING,
            approved_by=None,
            approved_at=None
        )
        
        self.grade_changes[change.id] = change
        return change
    
    async def approve_grade_change(
        self,
        change_id: UUID,
        approver_id: str
    ) -> GradeChange:
        """
        Approve a grade change request.
        
        GOVERNANCE: Human approval required.
        """
        change = self.grade_changes.get(change_id)
        if not change:
            raise ValueError(f"Grade change {change_id} not found")
        
        if change.status != GradeStatus.PENDING:
            raise ValueError("Grade change already processed")
        
        # Apply the change
        submission = self.submissions.get(change.submission_id)
        submission.score = change.new_score
        
        change.status = GradeStatus.APPROVED
        change.approved_by = approver_id
        change.approved_at = datetime.utcnow()
        
        logger.info(f"Grade change approved: {change_id} by {approver_id}")
        return change
    
    async def get_pending_grade_changes(
        self,
        course_id: Optional[UUID] = None
    ) -> List[GradeChange]:
        """Get pending grade change requests - chronological."""
        changes = [c for c in self.grade_changes.values()
                  if c.status == GradeStatus.PENDING]
        
        if course_id:
            changes = [c for c in changes if c.course_id == course_id]
        
        return sorted(changes, key=lambda c: c.requested_at)
    
    # ========================================================================
    # QUIZ MANAGEMENT
    # ========================================================================
    
    async def create_quiz(
        self,
        course_id: UUID,
        assignment_id: UUID,
        title: str,
        description: str = "",
        time_limit_minutes: Optional[int] = None,
        shuffle_questions: bool = False,
        shuffle_answers: bool = False,
        show_correct_answers: bool = True,
        user_id: str = None
    ) -> Quiz:
        """Create a quiz."""
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found")
        
        quiz = Quiz(
            id=uuid4(),
            course_id=course_id,
            assignment_id=assignment_id,
            title=title,
            description=description,
            time_limit_minutes=time_limit_minutes,
            shuffle_questions=shuffle_questions,
            shuffle_answers=shuffle_answers,
            show_correct_answers=show_correct_answers,
            show_correct_after=None,
            one_question_at_a_time=False,
            cant_go_back=False,
            questions=[],
            created_at=datetime.utcnow(),
            created_by=user_id
        )
        
        self.quizzes[quiz.id] = quiz
        return quiz
    
    async def add_question(
        self,
        quiz_id: UUID,
        question_type: QuestionType,
        question_text: str,
        points: Decimal,
        options: List[Dict[str, Any]] = None,
        correct_answer: Any = None,
        explanation: Optional[str] = None
    ) -> QuizQuestion:
        """Add question to quiz."""
        quiz = self.quizzes.get(quiz_id)
        if not quiz:
            raise ValueError(f"Quiz {quiz_id} not found")
        
        question = QuizQuestion(
            id=uuid4(),
            quiz_id=quiz_id,
            question_type=question_type,
            question_text=question_text,
            points=points,
            options=options or [],
            correct_answer=correct_answer,
            explanation=explanation,
            order=len(quiz.questions) + 1
        )
        
        quiz.questions.append(question)
        return question
    
    async def start_quiz_attempt(
        self,
        quiz_id: UUID,
        student_id: str
    ) -> QuizAttempt:
        """Start a quiz attempt."""
        quiz = self.quizzes.get(quiz_id)
        if not quiz:
            raise ValueError(f"Quiz {quiz_id} not found")
        
        # Check max attempts via assignment
        assignment = self.assignments.get(quiz.assignment_id)
        prev_attempts = len([a for a in self.quiz_attempts.values()
                           if a.quiz_id == quiz_id and a.student_id == student_id])
        
        if prev_attempts >= assignment.max_attempts:
            raise ValueError("Maximum quiz attempts reached")
        
        attempt = QuizAttempt(
            id=uuid4(),
            quiz_id=quiz_id,
            student_id=student_id,
            started_at=datetime.utcnow(),
            submitted_at=None,
            time_spent_seconds=0,
            answers={},
            score=None,
            graded=False,
            attempt_number=prev_attempts + 1
        )
        
        self.quiz_attempts[attempt.id] = attempt
        return attempt
    
    async def submit_quiz_attempt(
        self,
        attempt_id: UUID,
        answers: Dict[str, Any]
    ) -> QuizAttempt:
        """Submit quiz answers."""
        attempt = self.quiz_attempts.get(attempt_id)
        if not attempt:
            raise ValueError(f"Attempt {attempt_id} not found")
        
        if attempt.submitted_at:
            raise ValueError("Quiz already submitted")
        
        quiz = self.quizzes.get(attempt.quiz_id)
        
        # Check time limit
        if quiz.time_limit_minutes:
            elapsed = (datetime.utcnow() - attempt.started_at).total_seconds()
            if elapsed > quiz.time_limit_minutes * 60:
                raise ValueError("Time limit exceeded")
        
        attempt.answers = answers
        attempt.submitted_at = datetime.utcnow()
        attempt.time_spent_seconds = int(
            (attempt.submitted_at - attempt.started_at).total_seconds()
        )
        
        # Auto-grade objective questions
        score = Decimal("0")
        for question in quiz.questions:
            q_id = str(question.id)
            if q_id in answers:
                if question.question_type in [
                    QuestionType.MULTIPLE_CHOICE,
                    QuestionType.TRUE_FALSE,
                    QuestionType.NUMERIC
                ]:
                    if answers[q_id] == question.correct_answer:
                        score += question.points
        
        attempt.score = score
        attempt.graded = True  # For auto-graded questions
        
        return attempt
    
    # ========================================================================
    # DISCUSSION FORUMS
    # ========================================================================
    
    async def create_discussion(
        self,
        course_id: UUID,
        title: str,
        description: str,
        is_graded: bool = False,
        points_possible: Optional[Decimal] = None,
        module_id: Optional[UUID] = None,
        user_id: str = None
    ) -> Discussion:
        """Create a discussion forum."""
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found")
        
        discussion = Discussion(
            id=uuid4(),
            course_id=course_id,
            module_id=module_id,
            title=title,
            description=description,
            is_graded=is_graded,
            points_possible=points_possible,
            require_initial_post=False,
            allow_attachments=True,
            close_date=None,
            created_at=datetime.utcnow(),
            created_by=user_id
        )
        
        self.discussions[discussion.id] = discussion
        return discussion
    
    async def create_post(
        self,
        discussion_id: UUID,
        author_id: str,
        author_name: str,
        content: str,
        parent_id: Optional[UUID] = None,
        attachments: List[str] = None
    ) -> DiscussionPost:
        """Create a discussion post."""
        if discussion_id not in self.discussions:
            raise ValueError(f"Discussion {discussion_id} not found")
        
        post = DiscussionPost(
            id=uuid4(),
            discussion_id=discussion_id,
            author_id=author_id,
            author_name=author_name,
            parent_id=parent_id,
            content=content,
            attachments=attachments or [],
            created_at=datetime.utcnow(),
            edited_at=None,
            likes=0
        )
        
        self.discussion_posts[post.id] = post
        return post
    
    async def get_discussion_posts(
        self,
        discussion_id: UUID
    ) -> List[DiscussionPost]:
        """Get discussion posts - chronological."""
        posts = [p for p in self.discussion_posts.values()
                if p.discussion_id == discussion_id]
        
        return sorted(posts, key=lambda p: p.created_at)
    
    # ========================================================================
    # RESOURCE MANAGEMENT
    # ========================================================================
    
    async def add_resource(
        self,
        course_id: UUID,
        title: str,
        description: str,
        content_type: ContentType,
        url: str,
        module_id: Optional[UUID] = None,
        user_id: str = None
    ) -> Resource:
        """Add a resource to course."""
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found")
        
        resource = Resource(
            id=uuid4(),
            course_id=course_id,
            module_id=module_id,
            title=title,
            description=description,
            content_type=content_type,
            url=url,
            file_size_bytes=None,
            created_at=datetime.utcnow(),
            created_by=user_id
        )
        
        self.resources[resource.id] = resource
        return resource
    
    async def get_resources(
        self,
        course_id: UUID,
        module_id: Optional[UUID] = None
    ) -> List[Resource]:
        """Get resources - alphabetical by title."""
        resources = [r for r in self.resources.values()
                    if r.course_id == course_id]
        
        if module_id:
            resources = [r for r in resources if r.module_id == module_id]
        
        # Alphabetical
        return sorted(resources, key=lambda r: r.title.lower())
    
    # ========================================================================
    # ANNOUNCEMENTS
    # ========================================================================
    
    async def create_announcement(
        self,
        course_id: UUID,
        title: str,
        content: str,
        author_id: str,
        pinned: bool = False,
        send_notification: bool = True
    ) -> Announcement:
        """Create course announcement."""
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found")
        
        announcement = Announcement(
            id=uuid4(),
            course_id=course_id,
            title=title,
            content=content,
            author_id=author_id,
            posted_at=datetime.utcnow(),
            pinned=pinned,
            send_notification=send_notification
        )
        
        self.announcements[announcement.id] = announcement
        return announcement
    
    async def get_announcements(self, course_id: UUID) -> List[Announcement]:
        """Get announcements - pinned first, then chronological."""
        announcements = [a for a in self.announcements.values()
                        if a.course_id == course_id]
        
        # Pinned first, then by date (newest first)
        return sorted(announcements, 
                     key=lambda a: (not a.pinned, -a.posted_at.timestamp()))
    
    # ========================================================================
    # CERTIFICATES
    # ========================================================================
    
    async def request_certificate(
        self,
        course_id: UUID,
        student_id: str,
        student_name: str
    ) -> Certificate:
        """
        Request completion certificate.
        
        GOVERNANCE: Requires verification before issuance.
        """
        course = self.courses.get(course_id)
        if not course:
            raise ValueError(f"Course {course_id} not found")
        
        # Find enrollment
        enrollment = None
        for e in self.enrollments.values():
            if e.course_id == course_id and e.student_id == student_id:
                enrollment = e
                break
        
        if not enrollment:
            raise ValueError("Student not enrolled in course")
        
        if enrollment.status != EnrollmentStatus.COMPLETED:
            raise ValueError("Course not completed")
        
        certificate = Certificate(
            id=uuid4(),
            course_id=course_id,
            student_id=student_id,
            student_name=student_name,
            status=CertificateStatus.PENDING,  # Requires verification
            completion_date=date.today(),
            final_grade=enrollment.final_grade or Decimal("0"),
            certificate_url=None,
            verified_by=None,
            verified_at=None,
            issued_at=None,
            created_at=datetime.utcnow()
        )
        
        self.certificates[certificate.id] = certificate
        return certificate
    
    async def verify_certificate(
        self,
        certificate_id: UUID,
        verifier_id: str
    ) -> Certificate:
        """
        Verify certificate eligibility.
        
        GOVERNANCE: Human verification required.
        """
        certificate = self.certificates.get(certificate_id)
        if not certificate:
            raise ValueError(f"Certificate {certificate_id} not found")
        
        if certificate.status != CertificateStatus.PENDING:
            raise ValueError("Certificate not pending verification")
        
        certificate.status = CertificateStatus.VERIFIED
        certificate.verified_by = verifier_id
        certificate.verified_at = datetime.utcnow()
        
        return certificate
    
    async def issue_certificate(
        self,
        certificate_id: UUID,
        issuer_id: str
    ) -> Certificate:
        """
        Issue certificate after verification.
        
        GOVERNANCE: Only verified certificates can be issued.
        """
        certificate = self.certificates.get(certificate_id)
        if not certificate:
            raise ValueError(f"Certificate {certificate_id} not found")
        
        if certificate.status != CertificateStatus.VERIFIED:
            raise ValueError("Certificate must be verified before issuance")
        
        certificate.status = CertificateStatus.ISSUED
        certificate.issued_at = datetime.utcnow()
        certificate.certificate_url = f"https://che-nu.com/certificates/{certificate.id}"
        
        logger.info(f"Certificate issued: {certificate_id}")
        return certificate
    
    # ========================================================================
    # PROGRESS TRACKING
    # ========================================================================
    
    async def mark_lesson_complete(
        self,
        lesson_id: UUID,
        student_id: str,
        time_spent_minutes: int = 0
    ) -> StudentProgress:
        """Mark lesson as complete."""
        lesson = self.lessons.get(lesson_id)
        if not lesson:
            raise ValueError(f"Lesson {lesson_id} not found")
        
        # Find progress
        progress = None
        for p in self.progress.values():
            if p.student_id == student_id and p.course_id == lesson.course_id:
                progress = p
                break
        
        if not progress:
            raise ValueError("Student progress not found")
        
        progress.lessons_completed.add(lesson_id)
        progress.total_time_minutes += time_spent_minutes
        progress.last_lesson_id = lesson_id
        progress.last_activity = datetime.utcnow()
        
        # Check if module complete
        module_lessons = [l for l in self.lessons.values() 
                        if l.module_id == lesson.module_id and l.is_required]
        if all(l.id in progress.lessons_completed for l in module_lessons):
            progress.modules_completed.add(lesson.module_id)
        
        # Update enrollment progress
        await self._update_enrollment_progress(progress)
        
        return progress
    
    async def _update_enrollment_progress(self, progress: StudentProgress):
        """Update enrollment progress percentage."""
        enrollment = None
        for e in self.enrollments.values():
            if e.id == progress.enrollment_id:
                enrollment = e
                break
        
        if not enrollment:
            return
        
        # Calculate progress
        total_lessons = len([l for l in self.lessons.values() 
                           if l.course_id == progress.course_id and l.is_required])
        total_assignments = len([a for a in self.assignments.values()
                                if a.course_id == progress.course_id])
        
        if total_lessons + total_assignments == 0:
            return
        
        completed = len(progress.lessons_completed) + len(progress.assignments_completed)
        total = total_lessons + total_assignments
        
        enrollment.progress_percent = Decimal(str(round(completed / total * 100, 1)))
        enrollment.last_activity = datetime.utcnow()
        
        # Check if course complete
        if enrollment.progress_percent >= 100:
            enrollment.status = EnrollmentStatus.COMPLETED
            enrollment.completed_at = datetime.utcnow()
    
    async def get_student_progress(
        self,
        course_id: UUID,
        student_id: str
    ) -> Optional[StudentProgress]:
        """Get student progress for course."""
        for progress in self.progress.values():
            if progress.course_id == course_id and progress.student_id == student_id:
                return progress
        return None
    
    # ========================================================================
    # LEARNING PATHS
    # ========================================================================
    
    async def create_learning_path(
        self,
        title: str,
        description: str,
        course_ids: List[UUID],
        user_id: str
    ) -> LearningPath:
        """Create a learning path (sequence of courses)."""
        # Verify all courses exist
        for course_id in course_ids:
            if course_id not in self.courses:
                raise ValueError(f"Course {course_id} not found")
        
        # Calculate estimated hours
        total_hours = 0
        for course_id in course_ids:
            lessons = [l for l in self.lessons.values() if l.course_id == course_id]
            total_hours += sum(l.duration_minutes for l in lessons) // 60
        
        path = LearningPath(
            id=uuid4(),
            title=title,
            description=description,
            course_ids=course_ids,
            estimated_hours=total_hours,
            created_at=datetime.utcnow(),
            created_by=user_id
        )
        
        self.learning_paths[path.id] = path
        return path
    
    async def get_learning_paths(self) -> List[LearningPath]:
        """Get learning paths - alphabetical by title."""
        return sorted(self.learning_paths.values(), key=lambda p: p.title.lower())
    
    # ========================================================================
    # GRADEBOOK
    # ========================================================================
    
    async def get_gradebook(
        self,
        course_id: UUID
    ) -> Dict[str, Any]:
        """
        Get course gradebook.
        
        RULE #5: Students listed ALPHABETICALLY (NOT by grade ranking).
        """
        course = self.courses.get(course_id)
        if not course:
            raise ValueError(f"Course {course_id} not found")
        
        # Get enrolled students - ALPHABETICAL
        enrollments = await self.get_enrolled_students(
            course_id, EnrollmentStatus.ACTIVE
        )
        
        # Get assignments
        assignments = await self.get_assignments(course_id)
        
        gradebook = {
            "course_id": str(course_id),
            "course_title": course.title,
            "assignments": [
                {
                    "id": str(a.id),
                    "title": a.title,
                    "points_possible": float(a.points_possible),
                    "due_date": a.due_date.isoformat() if a.due_date else None
                }
                for a in assignments
            ],
            "students": [],  # Alphabetical order
            "sort_order": "alphabetical_by_name"  # RULE #5
        }
        
        for enrollment in enrollments:  # Already alphabetical
            student_grades = []
            total_earned = Decimal("0")
            total_possible = Decimal("0")
            
            for assignment in assignments:
                submission = None
                for s in self.submissions.values():
                    if (s.assignment_id == assignment.id 
                        and s.student_id == enrollment.student_id
                        and s.grade_status == GradeStatus.APPROVED):
                        submission = s
                        break
                
                if submission:
                    student_grades.append({
                        "assignment_id": str(assignment.id),
                        "score": float(submission.score) if submission.score else None,
                        "status": submission.status.value
                    })
                    if submission.score:
                        total_earned += submission.score
                        total_possible += assignment.points_possible
                else:
                    student_grades.append({
                        "assignment_id": str(assignment.id),
                        "score": None,
                        "status": "not_submitted"
                    })
                    total_possible += assignment.points_possible
            
            gradebook["students"].append({
                "student_id": enrollment.student_id,
                "student_name": enrollment.student_name,
                "grades": student_grades,
                "total_earned": float(total_earned),
                "total_possible": float(total_possible),
                "percentage": float(total_earned / total_possible * 100) if total_possible > 0 else 0
            })
        
        return gradebook
    
    # ========================================================================
    # ANALYTICS DASHBOARD
    # ========================================================================
    
    async def get_course_analytics(
        self,
        course_id: UUID
    ) -> Dict[str, Any]:
        """Get course analytics."""
        course = self.courses.get(course_id)
        if not course:
            raise ValueError(f"Course {course_id} not found")
        
        enrollments = list(self.enrollments.values())
        course_enrollments = [e for e in enrollments if e.course_id == course_id]
        
        active = len([e for e in course_enrollments if e.status == EnrollmentStatus.ACTIVE])
        completed = len([e for e in course_enrollments if e.status == EnrollmentStatus.COMPLETED])
        dropped = len([e for e in course_enrollments if e.status == EnrollmentStatus.DROPPED])
        
        # Calculate average progress
        avg_progress = Decimal("0")
        if course_enrollments:
            avg_progress = sum(e.progress_percent for e in course_enrollments) / len(course_enrollments)
        
        # Assignment completion rates
        assignments = [a for a in self.assignments.values() if a.course_id == course_id]
        assignment_stats = []
        for assignment in assignments:
            submissions = [s for s in self.submissions.values() 
                         if s.assignment_id == assignment.id]
            submitted = len(submissions)
            graded = len([s for s in submissions if s.grade_status == GradeStatus.APPROVED])
            avg_score = Decimal("0")
            if graded > 0:
                avg_score = sum(s.score for s in submissions if s.score) / graded
            
            assignment_stats.append({
                "id": str(assignment.id),
                "title": assignment.title,
                "submitted": submitted,
                "graded": graded,
                "avg_score": float(avg_score)
            })
        
        return {
            "course_id": str(course_id),
            "course_title": course.title,
            "enrollment": {
                "active": active,
                "completed": completed,
                "dropped": dropped,
                "total": len(course_enrollments)
            },
            "completion_rate": float(completed / len(course_enrollments) * 100) if course_enrollments else 0,
            "average_progress": float(avg_progress),
            "assignments": assignment_stats,
            "modules_count": len([m for m in self.modules.values() if m.course_id == course_id]),
            "lessons_count": len([l for l in self.lessons.values() if l.course_id == course_id]),
            "discussions_count": len([d for d in self.discussions.values() if d.course_id == course_id])
        }
    
    # ========================================================================
    # HEALTH CHECK
    # ========================================================================
    
    async def get_health(self) -> Dict[str, Any]:
        """Health check."""
        return {
            "status": "healthy",
            "service": "education_agent",
            "version": "V68",
            "stats": {
                "courses": len(self.courses),
                "enrollments": len(self.enrollments),
                "assignments": len(self.assignments),
                "submissions": len(self.submissions),
                "pending_grade_changes": len([
                    g for g in self.grade_changes.values() 
                    if g.status == GradeStatus.PENDING
                ])
            },
            "timestamp": datetime.utcnow().isoformat()
        }


# Singleton instance
_agent_instance: Optional[EducationAgent] = None


def get_education_agent() -> EducationAgent:
    """Get or create education agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = EducationAgent()
    return _agent_instance
