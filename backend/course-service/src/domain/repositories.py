from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from uuid import UUID

from .models import Course, CourseContent, CourseStatus


class CourseRepository(ABC):
    @abstractmethod
    async def create(self, course: Course) -> Course:
        """Create a new course"""
        pass

    @abstractmethod
    async def get(self, course_id: UUID) -> Optional[Course]:
        """Get a course by ID"""
        pass

    @abstractmethod
    async def update(self, course: Course) -> Course:
        """Update an existing course"""
        pass

    @abstractmethod
    async def delete(self, course_id: UUID) -> bool:
        """Delete a course"""
        pass

    @abstractmethod
    async def list(
        self,
        organization_id: Optional[UUID] = None,
        branch_id: Optional[UUID] = None,
        status: Optional[CourseStatus] = None,
        instructor_id: Optional[UUID] = None,
        search_text: Optional[str] = None,
        tags: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = 50,
        sort_by: str = "created_at",
        sort_desc: bool = True,
    ) -> Tuple[List[Course], int]:
        """List courses with filtering and pagination"""
        pass

    @abstractmethod
    async def exists(self, course_id: UUID) -> bool:
        """Check if a course exists"""
        pass


class CourseContentRepository(ABC):
    @abstractmethod
    async def create(self, content: CourseContent) -> CourseContent:
        """Create new course content"""
        pass

    @abstractmethod
    async def get(self, content_id: UUID) -> Optional[CourseContent]:
        """Get course content by ID"""
        pass

    @abstractmethod
    async def update(self, content: CourseContent) -> CourseContent:
        """Update existing course content"""
        pass

    @abstractmethod
    async def delete(self, content_id: UUID) -> bool:
        """Delete course content"""
        pass

    @abstractmethod
    async def list_by_course(
        self, course_id: UUID, section_id: Optional[UUID] = None
    ) -> List[CourseContent]:
        """List content for a specific course"""
        pass 