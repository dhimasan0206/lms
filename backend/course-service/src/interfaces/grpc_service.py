import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from uuid import UUID, uuid4

import grpc
from google.protobuf import timestamp_pb2

from ..application.use_cases import CourseUseCases, CourseContentUseCases
from ..domain.models import CourseStatus, ContentType, CourseSettings, EnrollmentType, GradingSchema, GradeRange

# Import generated protobuf code
from ..infrastructure.proto.course_pb2 import (
    CourseResponse,
    CourseContentResponse,
    CourseStatus as PBCourseStatus,
    ContentType as PBContentType,
    EnrollmentType as PBEnrollmentType,
    CourseSettings as PBCourseSettings,
    GradingSchema as PBGradingSchema,
    GradeRange as PBGradeRange,
    DeleteCourseResponse
)
from ..infrastructure.proto.course_pb2_grpc import CourseServiceServicer

logger = logging.getLogger(__name__)


class CourseGrpcService(CourseServiceServicer):
    def __init__(
        self, 
        course_use_cases: CourseUseCases, 
        content_use_cases: CourseContentUseCases
    ):
        self.course_use_cases = course_use_cases
        self.content_use_cases = content_use_cases

    @staticmethod
    def _str_to_uuid(value: str) -> UUID:
        """Convert a string to UUID."""
        try:
            return UUID(value)
        except ValueError as e:
            logger.error(f"Invalid UUID: {value}")
            raise ValueError(f"Invalid UUID: {value}") from e

    @staticmethod
    def _pb_to_course_status(status: int) -> CourseStatus:
        """Convert protobuf CourseStatus to domain CourseStatus."""
        status_map = {
            PBCourseStatus.DRAFT: CourseStatus.DRAFT,
            PBCourseStatus.PUBLISHED: CourseStatus.PUBLISHED,
            PBCourseStatus.ARCHIVED: CourseStatus.ARCHIVED,
        }
        return status_map.get(status, CourseStatus.DRAFT)

    @staticmethod
    def _course_status_to_pb(status: CourseStatus) -> int:
        """Convert domain CourseStatus to protobuf CourseStatus."""
        status_map = {
            CourseStatus.DRAFT: PBCourseStatus.DRAFT,
            CourseStatus.PUBLISHED: PBCourseStatus.PUBLISHED,
            CourseStatus.ARCHIVED: PBCourseStatus.ARCHIVED,
        }
        return status_map.get(status, PBCourseStatus.DRAFT)

    @staticmethod
    def _pb_to_content_type(content_type: int) -> ContentType:
        """Convert protobuf ContentType to domain ContentType."""
        type_map = {
            PBContentType.TEXT: ContentType.TEXT,
            PBContentType.VIDEO: ContentType.VIDEO,
            PBContentType.IMAGE: ContentType.IMAGE,
            PBContentType.DOCUMENT: ContentType.DOCUMENT,
            PBContentType.QUIZ: ContentType.QUIZ,
            PBContentType.ASSIGNMENT: ContentType.ASSIGNMENT,
            PBContentType.LINK: ContentType.LINK,
            PBContentType.CODE: ContentType.CODE,
            PBContentType.INTERACTIVE: ContentType.INTERACTIVE,
        }
        return type_map.get(content_type, ContentType.TEXT)

    @staticmethod
    def _content_type_to_pb(content_type: ContentType) -> int:
        """Convert domain ContentType to protobuf ContentType."""
        type_map = {
            ContentType.TEXT: PBContentType.TEXT,
            ContentType.VIDEO: PBContentType.VIDEO,
            ContentType.IMAGE: PBContentType.IMAGE,
            ContentType.DOCUMENT: PBContentType.DOCUMENT,
            ContentType.QUIZ: PBContentType.QUIZ,
            ContentType.ASSIGNMENT: PBContentType.ASSIGNMENT,
            ContentType.LINK: PBContentType.LINK,
            ContentType.CODE: PBContentType.CODE,
            ContentType.INTERACTIVE: PBContentType.INTERACTIVE,
        }
        return type_map.get(content_type, PBContentType.TEXT)

    @staticmethod
    def _pb_to_enrollment_type(enrollment_type: int) -> EnrollmentType:
        """Convert protobuf EnrollmentType to domain EnrollmentType."""
        type_map = {
            PBEnrollmentType.OPEN: EnrollmentType.OPEN,
            PBEnrollmentType.INVITE_ONLY: EnrollmentType.INVITE_ONLY,
            PBEnrollmentType.APPROVAL_REQUIRED: EnrollmentType.APPROVAL_REQUIRED,
        }
        return type_map.get(enrollment_type, EnrollmentType.OPEN)

    @staticmethod
    def _enrollment_type_to_pb(enrollment_type: EnrollmentType) -> int:
        """Convert domain EnrollmentType to protobuf EnrollmentType."""
        type_map = {
            EnrollmentType.OPEN: PBEnrollmentType.OPEN,
            EnrollmentType.INVITE_ONLY: PBEnrollmentType.INVITE_ONLY,
            EnrollmentType.APPROVAL_REQUIRED: PBEnrollmentType.APPROVAL_REQUIRED,
        }
        return type_map.get(enrollment_type, PBEnrollmentType.OPEN)

    @staticmethod
    def _pb_to_course_settings(pb_settings: PBCourseSettings) -> CourseSettings:
        """Convert protobuf CourseSettings to domain CourseSettings."""
        grade_ranges = []
        for gr in pb_settings.grading_schema.grade_ranges:
            grade_ranges.append(
                GradeRange(
                    name=gr.name,
                    min_percentage=gr.min_percentage,
                    max_percentage=gr.max_percentage,
                    letter_grade=gr.letter_grade if gr.letter_grade else None,
                )
            )

        return CourseSettings(
            allow_enrollment=pb_settings.allow_enrollment,
            self_enrollment=pb_settings.self_enrollment,
            max_students=pb_settings.max_students if pb_settings.max_students > 0 else None,
            start_date=datetime.fromisoformat(pb_settings.start_date) if pb_settings.start_date else None,
            end_date=datetime.fromisoformat(pb_settings.end_date) if pb_settings.end_date else None,
            hidden=pb_settings.hidden,
            enrollment_type=CourseGrpcService._pb_to_enrollment_type(pb_settings.enrollment_type),
            grading_schema=GradingSchema(
                grade_ranges=grade_ranges,
                use_letter_grades=pb_settings.grading_schema.use_letter_grades,
                use_percentage=pb_settings.grading_schema.use_percentage,
            ),
            custom_settings=dict(pb_settings.custom_settings),
        )

    @staticmethod
    def _course_settings_to_pb(settings: CourseSettings) -> PBCourseSettings:
        """Convert domain CourseSettings to protobuf CourseSettings."""
        pb_settings = PBCourseSettings()
        pb_settings.allow_enrollment = settings.allow_enrollment
        pb_settings.self_enrollment = settings.self_enrollment
        pb_settings.max_students = settings.max_students if settings.max_students is not None else 0
        pb_settings.start_date = settings.start_date.isoformat() if settings.start_date else ""
        pb_settings.end_date = settings.end_date.isoformat() if settings.end_date else ""
        pb_settings.hidden = settings.hidden
        pb_settings.enrollment_type = CourseGrpcService._enrollment_type_to_pb(settings.enrollment_type)
        
        pb_grading_schema = PBGradingSchema()
        pb_grading_schema.use_letter_grades = settings.grading_schema.use_letter_grades
        pb_grading_schema.use_percentage = settings.grading_schema.use_percentage
        
        for gr in settings.grading_schema.grade_ranges:
            pb_grade_range = pb_grading_schema.grade_ranges.add()
            pb_grade_range.name = gr.name
            pb_grade_range.min_percentage = gr.min_percentage
            pb_grade_range.max_percentage = gr.max_percentage
            pb_grade_range.letter_grade = gr.letter_grade if gr.letter_grade else ""
            
        pb_settings.grading_schema.CopyFrom(pb_grading_schema)
        
        for key, value in settings.custom_settings.items():
            pb_settings.custom_settings[key] = value
            
        return pb_settings

    @staticmethod
    def _course_to_pb_response(course) -> CourseResponse:
        """Convert domain Course to protobuf CourseResponse."""
        response = CourseResponse()
        response.id = str(course.id)
        response.organization_id = str(course.organization_id)
        response.branch_id = str(course.branch_id)
        response.title = course.title
        response.description = course.description
        response.code = course.code
        response.instructor_id = str(course.instructor_id)
        response.tags.extend(course.tags)
        response.status = CourseGrpcService._course_status_to_pb(course.status)
        response.settings.CopyFrom(CourseGrpcService._course_settings_to_pb(course.settings))
        response.created_at = course.created_at.isoformat()
        response.updated_at = course.updated_at.isoformat()
        return response

    @staticmethod
    def _content_to_pb_response(content) -> CourseContentResponse:
        """Convert domain CourseContent to protobuf CourseContentResponse."""
        response = CourseContentResponse()
        response.id = str(content.id)
        response.course_id = str(content.course_id)
        response.title = content.title
        response.description = content.description
        response.type = CourseGrpcService._content_type_to_pb(content.type)
        response.content_data = content.content_data
        response.order = content.order
        response.section_id = str(content.section_id) if content.section_id else ""
        
        for key, value in content.metadata.items():
            response.metadata[key] = value
            
        response.created_at = content.created_at.isoformat()
        response.updated_at = content.updated_at.isoformat()
        return response

    async def CreateCourse(self, request, context):
        """Implementation of CreateCourse RPC method."""
        try:
            course = await self.course_use_cases.create_course(
                organization_id=self._str_to_uuid(request.organization_id),
                branch_id=self._str_to_uuid(request.branch_id),
                title=request.title,
                description=request.description,
                code=request.code,
                instructor_id=self._str_to_uuid(request.instructor_id),
                tags=list(request.tags) if request.tags else [],
                status=self._pb_to_course_status(request.status),
                settings=self._pb_to_course_settings(request.settings) if request.HasField("settings") else None,
            )
            return self._course_to_pb_response(course)
        except Exception as e:
            logger.error(f"Error creating course: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error creating course: {str(e)}")
            return CourseResponse()  # Return empty response

    async def GetCourse(self, request, context):
        """Implementation of GetCourse RPC method."""
        try:
            course = await self.course_use_cases.get_course(
                course_id=self._str_to_uuid(request.course_id),
            )
            if not course:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Course with ID {request.course_id} not found")
                return CourseResponse()
                
            return self._course_to_pb_response(course)
        except Exception as e:
            logger.error(f"Error getting course: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error getting course: {str(e)}")
            return CourseResponse()

    async def UpdateCourse(self, request, context):
        """Implementation of UpdateCourse RPC method."""
        try:
            updated_course = await self.course_use_cases.update_course(
                course_id=self._str_to_uuid(request.course_id),
                title=request.title if request.HasField("title") else None,
                description=request.description if request.HasField("description") else None,
                code=request.code if request.HasField("code") else None,
                instructor_id=self._str_to_uuid(request.instructor_id) if request.HasField("instructor_id") else None,
                tags=list(request.tags) if request.tags else None,
                status=self._pb_to_course_status(request.status) if request.HasField("status") else None,
                settings=self._pb_to_course_settings(request.settings) if request.HasField("settings") else None,
            )
            
            if not updated_course:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Course with ID {request.course_id} not found")
                return CourseResponse()
                
            return self._course_to_pb_response(updated_course)
        except Exception as e:
            logger.error(f"Error updating course: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error updating course: {str(e)}")
            return CourseResponse()

    async def DeleteCourse(self, request, context):
        """Implementation of DeleteCourse RPC method."""
        try:
            result = await self.course_use_cases.delete_course(
                course_id=self._str_to_uuid(request.course_id),
            )
            
            response = DeleteCourseResponse()
            if result:
                response.success = True
                response.message = f"Course with ID {request.course_id} deleted successfully"
            else:
                response.success = False
                response.message = f"Course with ID {request.course_id} not found"
                
            return response
        except Exception as e:
            logger.error(f"Error deleting course: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error deleting course: {str(e)}")
            return DeleteCourseResponse(success=False, message=f"Error: {str(e)}")

    async def ListCourses(self, request, context):
        """Implementation of ListCourses RPC method."""
        from ..infrastructure.proto.course_pb2 import ListCoursesResponse
        
        try:
            organization_id = None
            if request.HasField("organization_id") and request.organization_id:
                organization_id = self._str_to_uuid(request.organization_id)
                
            branch_id = None
            if request.HasField("branch_id") and request.branch_id:
                branch_id = self._str_to_uuid(request.branch_id)
                
            instructor_id = None
            if request.HasField("instructor_id") and request.instructor_id:
                instructor_id = self._str_to_uuid(request.instructor_id)
                
            status = None
            if request.HasField("status"):
                status = self._pb_to_course_status(request.status)
                
            courses, total_count = await self.course_use_cases.list_courses(
                organization_id=organization_id,
                branch_id=branch_id,
                status=status,
                instructor_id=instructor_id,
                search_text=request.search_text if request.HasField("search_text") else None,
                tags=list(request.tags) if request.tags else None,
                page=request.page,
                page_size=request.page_size,
                sort_by=request.sort_by if request.HasField("sort_by") else "created_at",
                sort_desc=request.sort_desc if request.HasField("sort_desc") else True,
            )
            
            response = ListCoursesResponse()
            for course in courses:
                course_response = response.courses.add()
                course_response.CopyFrom(self._course_to_pb_response(course))
                
            response.total_count = total_count
            response.page = request.page
            response.page_size = request.page_size
            response.total_pages = (total_count + request.page_size - 1) // request.page_size
                
            return response
        except Exception as e:
            logger.error(f"Error listing courses: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error listing courses: {str(e)}")
            return ListCoursesResponse()

    async def WatchCourse(self, request, context):
        """Implementation of WatchCourse RPC method."""
        try:
            course_id = self._str_to_uuid(request.course_id)
            
            # Initial response with current state
            course = await self.course_use_cases.get_course(course_id)
            if not course:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Course with ID {request.course_id} not found")
                return
                
            yield self._course_to_pb_response(course)
            
            # For a real implementation, we would set up a subscription to course changes
            # Here we'll simulate by checking for updates every 5 seconds
            while context.is_active():
                await asyncio.sleep(5)
                updated_course = await self.course_use_cases.get_course(course_id)
                
                if not updated_course:
                    break
                    
                if updated_course.updated_at > course.updated_at:
                    course = updated_course
                    yield self._course_to_pb_response(course)
                    
        except Exception as e:
            logger.error(f"Error watching course: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error watching course: {str(e)}")
            return

    async def AddCourseContent(self, request, context):
        """Implementation of AddCourseContent RPC method."""
        try:
            section_id = None
            if request.HasField("section_id") and request.section_id:
                section_id = self._str_to_uuid(request.section_id)
                
            content = await self.content_use_cases.add_course_content(
                course_id=self._str_to_uuid(request.course_id),
                title=request.title,
                description=request.description,
                content_type=self._pb_to_content_type(request.type),
                content_data=request.content_data,
                order=request.order,
                section_id=section_id,
                metadata=dict(request.metadata) if request.metadata else None,
            )
            
            if not content:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Course with ID {request.course_id} not found")
                return CourseContentResponse()
                
            return self._content_to_pb_response(content)
        except Exception as e:
            logger.error(f"Error adding course content: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error adding course content: {str(e)}")
            return CourseContentResponse()

    async def GetCourseContent(self, request, context):
        """Implementation of GetCourseContent RPC method."""
        try:
            content = await self.content_use_cases.get_course_content(
                content_id=self._str_to_uuid(request.content_id),
            )
            
            if not content:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Course content with ID {request.content_id} not found")
                return CourseContentResponse()
                
            return self._content_to_pb_response(content)
        except Exception as e:
            logger.error(f"Error getting course content: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error getting course content: {str(e)}")
            return CourseContentResponse() 