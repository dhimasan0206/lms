#!/usr/bin/env python3
"""
Simple gRPC client to test the course service.

Usage:
    python client.py create_course
    python client.py get_course <course_id>
    python client.py list_courses
"""

import argparse
import sys
import uuid
from pathlib import Path

import grpc
from google.protobuf.json_format import MessageToJson

# Add the parent directory to the Python path for imports
sys.path.append(str(Path(__file__).parent))

# Import the generated protobuf code
from src.infrastructure.proto.course_pb2 import (
    CreateCourseRequest,
    GetCourseRequest,
    ListCoursesRequest,
    CourseStatus,
    CourseSettings,
    GradingSchema,
    GradeRange,
    EnrollmentType,
)
from src.infrastructure.proto.course_pb2_grpc import CourseServiceStub


def create_course(stub):
    """Create a new course."""
    # Create a grading schema
    grading_schema = GradingSchema(
        use_letter_grades=True,
        use_percentage=True,
    )
    
    # Add grade ranges
    grade_range_a = grading_schema.grade_ranges.add()
    grade_range_a.name = "A"
    grade_range_a.min_percentage = 90.0
    grade_range_a.max_percentage = 100.0
    grade_range_a.letter_grade = "A"
    
    grade_range_b = grading_schema.grade_ranges.add()
    grade_range_b.name = "B"
    grade_range_b.min_percentage = 80.0
    grade_range_b.max_percentage = 89.9
    grade_range_b.letter_grade = "B"
    
    grade_range_c = grading_schema.grade_ranges.add()
    grade_range_c.name = "C"
    grade_range_c.min_percentage = 70.0
    grade_range_c.max_percentage = 79.9
    grade_range_c.letter_grade = "C"
    
    # Create course settings
    settings = CourseSettings(
        allow_enrollment=True,
        self_enrollment=True,
        max_students=100,
        hidden=False,
        enrollment_type=EnrollmentType.OPEN,
        grading_schema=grading_schema,
    )
    
    # Add some custom settings
    settings.custom_settings["display_mode"] = "weekly"
    settings.custom_settings["show_progress"] = "true"
    
    # Create the request
    request = CreateCourseRequest(
        organization_id=str(uuid.uuid4()),  # Generate a random UUID
        branch_id=str(uuid.uuid4()),  # Generate a random UUID
        title="Introduction to Python Programming",
        description="Learn the basics of Python programming in this introductory course.",
        code="PY101",
        instructor_id=str(uuid.uuid4()),  # Generate a random UUID
        tags=["python", "programming", "beginner"],
        status=CourseStatus.PUBLISHED,
        settings=settings,
    )
    
    # Call the service
    response = stub.CreateCourse(request)
    
    # Print the response as JSON
    print(MessageToJson(response))
    
    return response


def get_course(stub, course_id):
    """Get a course by ID."""
    request = GetCourseRequest(course_id=course_id)
    
    try:
        response = stub.GetCourse(request)
        print(MessageToJson(response))
        return response
    except grpc.RpcError as e:
        print(f"RPC Error: {e.details()}")
        return None


def list_courses(stub):
    """List all courses."""
    request = ListCoursesRequest(
        page=1,
        page_size=10,
        sort_by="created_at",
        sort_desc=True,
    )
    
    try:
        response = stub.ListCourses(request)
        print(MessageToJson(response))
        return response
    except grpc.RpcError as e:
        print(f"RPC Error: {e.details()}")
        return None


def main():
    # Create command-line arguments parser
    parser = argparse.ArgumentParser(description="Course Service gRPC Client")
    parser.add_argument("command", choices=["create_course", "get_course", "list_courses"], help="Command to execute")
    parser.add_argument("course_id", nargs="?", help="Course ID (required for get_course)")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", default="50051", help="Server port")
    
    args = parser.parse_args()
    
    # Create a gRPC channel
    channel = grpc.insecure_channel(f"{args.host}:{args.port}")
    
    # Create a stub (client)
    stub = CourseServiceStub(channel)
    
    # Execute the requested command
    if args.command == "create_course":
        create_course(stub)
    elif args.command == "get_course":
        if not args.course_id:
            print("Error: course_id is required for get_course command")
            sys.exit(1)
        get_course(stub, args.course_id)
    elif args.command == "list_courses":
        list_courses(stub)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main() 