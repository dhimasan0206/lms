from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional
from uuid import UUID, uuid4


class CourseStatus(Enum):
    DRAFT = auto()
    PUBLISHED = auto()
    ARCHIVED = auto()


class ContentType(Enum):
    TEXT = auto()
    VIDEO = auto()
    IMAGE = auto()
    DOCUMENT = auto()
    QUIZ = auto()
    ASSIGNMENT = auto()
    LINK = auto()
    CODE = auto()
    INTERACTIVE = auto()


class EnrollmentType(Enum):
    OPEN = auto()
    INVITE_ONLY = auto()
    APPROVAL_REQUIRED = auto()


@dataclass
class GradeRange:
    name: str
    min_percentage: float
    max_percentage: float
    letter_grade: Optional[str] = None


@dataclass
class GradingSchema:
    grade_ranges: List[GradeRange] = field(default_factory=list)
    use_letter_grades: bool = False
    use_percentage: bool = True


@dataclass
class CourseSettings:
    allow_enrollment: bool = True
    self_enrollment: bool = False
    max_students: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    hidden: bool = False
    enrollment_type: EnrollmentType = EnrollmentType.OPEN
    grading_schema: GradingSchema = field(default_factory=GradingSchema)
    custom_settings: Dict[str, str] = field(default_factory=dict)


@dataclass
class Course:
    organization_id: UUID
    branch_id: UUID
    title: str
    description: str
    code: str
    instructor_id: UUID
    id: UUID = field(default_factory=uuid4)
    tags: List[str] = field(default_factory=list)
    status: CourseStatus = CourseStatus.DRAFT
    settings: CourseSettings = field(default_factory=CourseSettings)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CourseContent:
    course_id: UUID
    title: str
    description: str
    type: ContentType
    content_data: str
    id: UUID = field(default_factory=uuid4)
    order: int = 0
    section_id: Optional[UUID] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow) 