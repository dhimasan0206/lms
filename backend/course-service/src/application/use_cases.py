from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from uuid import UUID

from ..domain.models import Course, CourseContent, CourseSettings, CourseStatus, ContentType
from ..domain.repositories import CourseRepository, CourseContentRepository


class CourseUseCases:
    def __init__(self, course_repository: CourseRepository):
        self.course_repository = course_repository

    async def create_course(
        self,
        organization_id: UUID,
        branch_id: UUID,
        title: str,
        description: str,
        code: str,
        instructor_id: UUID,
        tags: Optional[List[str]] = None,
        status: CourseStatus = CourseStatus.DRAFT,
        settings: Optional[CourseSettings] = None,
    ) -> Course:
        if tags is None:
            tags = []
        if settings is None:
            settings = CourseSettings()

        course = Course(
            organization_id=organization_id,
            branch_id=branch_id,
            title=title,
            description=description,
            code=code,
            instructor_id=instructor_id,
            tags=tags,
            status=status,
            settings=settings,
        )

        return await self.course_repository.create(course)

    async def get_course(self, course_id: UUID) -> Optional[Course]:
        return await self.course_repository.get(course_id)

    async def update_course(
        self,
        course_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        code: Optional[str] = None,
        instructor_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        status: Optional[CourseStatus] = None,
        settings: Optional[CourseSettings] = None,
    ) -> Optional[Course]:
        course = await self.course_repository.get(course_id)
        if not course:
            return None

        if title is not None:
            course.title = title
        if description is not None:
            course.description = description
        if code is not None:
            course.code = code
        if instructor_id is not None:
            course.instructor_id = instructor_id
        if tags is not None:
            course.tags = tags
        if status is not None:
            course.status = status
        if settings is not None:
            course.settings = settings

        course.updated_at = datetime.utcnow()
        return await self.course_repository.update(course)

    async def delete_course(self, course_id: UUID) -> bool:
        return await self.course_repository.delete(course_id)

    async def list_courses(
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
        return await self.course_repository.list(
            organization_id=organization_id,
            branch_id=branch_id,
            status=status,
            instructor_id=instructor_id,
            search_text=search_text,
            tags=tags,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_desc=sort_desc,
        )


class CourseContentUseCases:
    def __init__(
        self,
        course_repository: CourseRepository,
        content_repository: CourseContentRepository,
    ):
        self.course_repository = course_repository
        self.content_repository = content_repository

    async def add_course_content(
        self,
        course_id: UUID,
        title: str,
        description: str,
        content_type: ContentType,
        content_data: str,
        order: int = 0,
        section_id: Optional[UUID] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Optional[CourseContent]:
        # Verify course exists
        course_exists = await self.course_repository.exists(course_id)
        if not course_exists:
            return None

        if metadata is None:
            metadata = {}

        content = CourseContent(
            course_id=course_id,
            title=title,
            description=description,
            type=content_type,
            content_data=content_data,
            order=order,
            section_id=section_id,
            metadata=metadata,
        )

        return await self.content_repository.create(content)

    async def get_course_content(self, content_id: UUID) -> Optional[CourseContent]:
        return await self.content_repository.get(content_id)

    async def update_course_content(
        self,
        content_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        content_type: Optional[ContentType] = None,
        content_data: Optional[str] = None,
        order: Optional[int] = None,
        section_id: Optional[UUID] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Optional[CourseContent]:
        content = await self.content_repository.get(content_id)
        if not content:
            return None

        if title is not None:
            content.title = title
        if description is not None:
            content.description = description
        if content_type is not None:
            content.type = content_type
        if content_data is not None:
            content.content_data = content_data
        if order is not None:
            content.order = order
        if section_id is not None or section_id == None:  # Explicitly set to None
            content.section_id = section_id
        if metadata is not None:
            content.metadata = metadata

        content.updated_at = datetime.utcnow()
        return await self.content_repository.update(content)

    async def delete_course_content(self, content_id: UUID) -> bool:
        return await self.content_repository.delete(content_id)

    async def list_course_content(
        self, course_id: UUID, section_id: Optional[UUID] = None
    ) -> List[CourseContent]:
        return await self.content_repository.list_by_course(
            course_id=course_id, section_id=section_id
        ) 