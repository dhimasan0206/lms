from datetime import datetime
import json
from typing import Dict, List, Optional, Tuple, Any
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import select, func

from ..domain.models import (
    Course,
    CourseContent,
    CourseSettings,
    CourseStatus,
    ContentType,
    EnrollmentType,
    GradingSchema,
    GradeRange,
)
from ..domain.repositories import CourseRepository, CourseContentRepository

Base = declarative_base()


class CourseModel(Base):
    __tablename__ = "courses"

    id = sa.Column(PG_UUID, primary_key=True)
    organization_id = sa.Column(PG_UUID, nullable=False, index=True)
    branch_id = sa.Column(PG_UUID, nullable=False, index=True)
    title = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    code = sa.Column(sa.String(100), nullable=False)
    instructor_id = sa.Column(PG_UUID, nullable=False, index=True)
    tags = sa.Column(sa.ARRAY(sa.String), nullable=False, default=[])
    status = sa.Column(sa.String(20), nullable=False, index=True)
    settings = sa.Column(JSONB, nullable=False, default={})
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class CourseContentModel(Base):
    __tablename__ = "course_contents"

    id = sa.Column(PG_UUID, primary_key=True)
    course_id = sa.Column(PG_UUID, sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    title = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    type = sa.Column(sa.String(20), nullable=False)
    content_data = sa.Column(sa.Text, nullable=False)
    order = sa.Column(sa.Integer, nullable=False, default=0)
    section_id = sa.Column(PG_UUID, nullable=True, index=True)
    metadata = sa.Column(JSONB, nullable=False, default={})
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class SQLAlchemyCourseRepository(CourseRepository):
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    @staticmethod
    def _course_domain_to_model(course: Course) -> CourseModel:
        return CourseModel(
            id=course.id,
            organization_id=course.organization_id,
            branch_id=course.branch_id,
            title=course.title,
            description=course.description,
            code=course.code,
            instructor_id=course.instructor_id,
            tags=course.tags,
            status=course.status.name,
            settings=SQLAlchemyCourseRepository._settings_to_dict(course.settings),
            created_at=course.created_at,
            updated_at=course.updated_at,
        )

    @staticmethod
    def _course_model_to_domain(course_model: CourseModel) -> Course:
        return Course(
            id=course_model.id,
            organization_id=course_model.organization_id,
            branch_id=course_model.branch_id,
            title=course_model.title,
            description=course_model.description,
            code=course_model.code,
            instructor_id=course_model.instructor_id,
            tags=course_model.tags,
            status=CourseStatus[course_model.status],
            settings=SQLAlchemyCourseRepository._dict_to_settings(course_model.settings),
            created_at=course_model.created_at,
            updated_at=course_model.updated_at,
        )

    @staticmethod
    def _settings_to_dict(settings: CourseSettings) -> Dict[str, Any]:
        grade_ranges = []
        for gr in settings.grading_schema.grade_ranges:
            grade_ranges.append({
                "name": gr.name,
                "min_percentage": gr.min_percentage,
                "max_percentage": gr.max_percentage,
                "letter_grade": gr.letter_grade,
            })

        return {
            "allow_enrollment": settings.allow_enrollment,
            "self_enrollment": settings.self_enrollment,
            "max_students": settings.max_students,
            "start_date": settings.start_date.isoformat() if settings.start_date else None,
            "end_date": settings.end_date.isoformat() if settings.end_date else None,
            "hidden": settings.hidden,
            "enrollment_type": settings.enrollment_type.name,
            "grading_schema": {
                "grade_ranges": grade_ranges,
                "use_letter_grades": settings.grading_schema.use_letter_grades,
                "use_percentage": settings.grading_schema.use_percentage,
            },
            "custom_settings": settings.custom_settings,
        }

    @staticmethod
    def _dict_to_settings(settings_dict: Dict[str, Any]) -> CourseSettings:
        grade_ranges = []
        if settings_dict.get("grading_schema", {}).get("grade_ranges"):
            for gr_dict in settings_dict["grading_schema"]["grade_ranges"]:
                grade_ranges.append(
                    GradeRange(
                        name=gr_dict["name"],
                        min_percentage=gr_dict["min_percentage"],
                        max_percentage=gr_dict["max_percentage"],
                        letter_grade=gr_dict.get("letter_grade"),
                    )
                )

        start_date = None
        if settings_dict.get("start_date"):
            start_date = datetime.fromisoformat(settings_dict["start_date"])

        end_date = None
        if settings_dict.get("end_date"):
            end_date = datetime.fromisoformat(settings_dict["end_date"])

        return CourseSettings(
            allow_enrollment=settings_dict.get("allow_enrollment", True),
            self_enrollment=settings_dict.get("self_enrollment", False),
            max_students=settings_dict.get("max_students"),
            start_date=start_date,
            end_date=end_date,
            hidden=settings_dict.get("hidden", False),
            enrollment_type=EnrollmentType[settings_dict.get("enrollment_type", "OPEN")],
            grading_schema=GradingSchema(
                grade_ranges=grade_ranges,
                use_letter_grades=settings_dict.get("grading_schema", {}).get("use_letter_grades", False),
                use_percentage=settings_dict.get("grading_schema", {}).get("use_percentage", True),
            ),
            custom_settings=settings_dict.get("custom_settings", {}),
        )

    async def create(self, course: Course) -> Course:
        course_model = self._course_domain_to_model(course)
        
        async with self.session_factory() as session:
            session.add(course_model)
            await session.commit()
            await session.refresh(course_model)
            
        return self._course_model_to_domain(course_model)

    async def get(self, course_id: UUID) -> Optional[Course]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(CourseModel).where(CourseModel.id == course_id)
            )
            course_model = result.scalar_one_or_none()
            
        if not course_model:
            return None
            
        return self._course_model_to_domain(course_model)

    async def update(self, course: Course) -> Course:
        course_model = self._course_domain_to_model(course)
        
        async with self.session_factory() as session:
            result = await session.execute(
                select(CourseModel).where(CourseModel.id == course.id)
            )
            existing_course = result.scalar_one_or_none()
            
            if not existing_course:
                raise ValueError(f"Course with ID {course.id} not found")
                
            for key, value in course_model.__dict__.items():
                if key != "_sa_instance_state" and hasattr(existing_course, key):
                    setattr(existing_course, key, value)
                    
            await session.commit()
            await session.refresh(existing_course)
            
        return self._course_model_to_domain(existing_course)

    async def delete(self, course_id: UUID) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(
                select(CourseModel).where(CourseModel.id == course_id)
            )
            course_model = result.scalar_one_or_none()
            
            if not course_model:
                return False
                
            await session.delete(course_model)
            await session.commit()
            
        return True

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
        query = select(CourseModel)
        count_query = select(func.count()).select_from(CourseModel)
        
        # Apply filters
        if organization_id:
            query = query.where(CourseModel.organization_id == organization_id)
            count_query = count_query.where(CourseModel.organization_id == organization_id)
            
        if branch_id:
            query = query.where(CourseModel.branch_id == branch_id)
            count_query = count_query.where(CourseModel.branch_id == branch_id)
            
        if status:
            query = query.where(CourseModel.status == status.name)
            count_query = count_query.where(CourseModel.status == status.name)
            
        if instructor_id:
            query = query.where(CourseModel.instructor_id == instructor_id)
            count_query = count_query.where(CourseModel.instructor_id == instructor_id)
            
        if search_text:
            search_filter = sa.or_(
                CourseModel.title.ilike(f"%{search_text}%"),
                CourseModel.description.ilike(f"%{search_text}%"),
                CourseModel.code.ilike(f"%{search_text}%"),
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
            
        if tags:
            # Match any tag in the list
            query = query.where(CourseModel.tags.overlap(tags))
            count_query = count_query.where(CourseModel.tags.overlap(tags))
            
        # Apply sorting
        sort_column = getattr(CourseModel, sort_by, CourseModel.created_at)
        query = query.order_by(sort_column.desc() if sort_desc else sort_column)
        
        # Apply pagination
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        async with self.session_factory() as session:
            # Execute count query
            count_result = await session.execute(count_query)
            total_count = count_result.scalar()
            
            # Execute main query
            result = await session.execute(query)
            course_models = result.scalars().all()
            
        # Convert models to domain entities
        courses = [self._course_model_to_domain(model) for model in course_models]
        
        return courses, total_count

    async def exists(self, course_id: UUID) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(
                select(func.count()).select_from(CourseModel).where(CourseModel.id == course_id)
            )
            count = result.scalar()
            
        return count > 0


class SQLAlchemyCourseContentRepository(CourseContentRepository):
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    @staticmethod
    def _content_domain_to_model(content: CourseContent) -> CourseContentModel:
        return CourseContentModel(
            id=content.id,
            course_id=content.course_id,
            title=content.title,
            description=content.description,
            type=content.type.name,
            content_data=content.content_data,
            order=content.order,
            section_id=content.section_id,
            metadata=content.metadata,
            created_at=content.created_at,
            updated_at=content.updated_at,
        )

    @staticmethod
    def _content_model_to_domain(content_model: CourseContentModel) -> CourseContent:
        return CourseContent(
            id=content_model.id,
            course_id=content_model.course_id,
            title=content_model.title,
            description=content_model.description,
            type=ContentType[content_model.type],
            content_data=content_model.content_data,
            order=content_model.order,
            section_id=content_model.section_id,
            metadata=content_model.metadata,
            created_at=content_model.created_at,
            updated_at=content_model.updated_at,
        )

    async def create(self, content: CourseContent) -> CourseContent:
        content_model = self._content_domain_to_model(content)
        
        async with self.session_factory() as session:
            session.add(content_model)
            await session.commit()
            await session.refresh(content_model)
            
        return self._content_model_to_domain(content_model)

    async def get(self, content_id: UUID) -> Optional[CourseContent]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(CourseContentModel).where(CourseContentModel.id == content_id)
            )
            content_model = result.scalar_one_or_none()
            
        if not content_model:
            return None
            
        return self._content_model_to_domain(content_model)

    async def update(self, content: CourseContent) -> CourseContent:
        content_model = self._content_domain_to_model(content)
        
        async with self.session_factory() as session:
            result = await session.execute(
                select(CourseContentModel).where(CourseContentModel.id == content.id)
            )
            existing_content = result.scalar_one_or_none()
            
            if not existing_content:
                raise ValueError(f"Course content with ID {content.id} not found")
                
            for key, value in content_model.__dict__.items():
                if key != "_sa_instance_state" and hasattr(existing_content, key):
                    setattr(existing_content, key, value)
                    
            await session.commit()
            await session.refresh(existing_content)
            
        return self._content_model_to_domain(existing_content)

    async def delete(self, content_id: UUID) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(
                select(CourseContentModel).where(CourseContentModel.id == content_id)
            )
            content_model = result.scalar_one_or_none()
            
            if not content_model:
                return False
                
            await session.delete(content_model)
            await session.commit()
            
        return True

    async def list_by_course(
        self, course_id: UUID, section_id: Optional[UUID] = None
    ) -> List[CourseContent]:
        query = select(CourseContentModel).where(CourseContentModel.course_id == course_id)
        
        if section_id is not None:
            query = query.where(CourseContentModel.section_id == section_id)
            
        # Order by content order
        query = query.order_by(CourseContentModel.order)
        
        async with self.session_factory() as session:
            result = await session.execute(query)
            content_models = result.scalars().all()
            
        # Convert models to domain entities
        contents = [self._content_model_to_domain(model) for model in content_models]
        
        return contents 