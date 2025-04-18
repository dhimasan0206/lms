# LMS Reporting System

## Database Schemas

### PostgreSQL Schemas

```sql
-- Report Definitions
CREATE TABLE report_definitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL, -- 'student', 'parent', 'instructor', 'branch', 'organization'
    template JSONB,
    settings JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Report Schedules
CREATE TABLE report_schedules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_definition_id UUID REFERENCES report_definitions(id),
    organization_id UUID REFERENCES organizations(id),
    branch_id UUID REFERENCES branches(id),
    frequency VARCHAR(50) NOT NULL, -- 'daily', 'weekly', 'monthly', 'quarterly'
    recipients JSONB,
    settings JSONB,
    next_run TIMESTAMP WITH TIME ZONE,
    last_run TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Generated Reports
CREATE TABLE generated_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_definition_id UUID REFERENCES report_definitions(id),
    organization_id UUID REFERENCES organizations(id),
    branch_id UUID REFERENCES branches(id),
    user_id UUID REFERENCES users(id),
    course_id UUID REFERENCES courses(id),
    data JSONB,
    format VARCHAR(50), -- 'pdf', 'excel', 'csv', 'json'
    file_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Report Access Logs
CREATE TABLE report_access_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_id UUID REFERENCES generated_reports(id),
    user_id UUID REFERENCES users(id),
    access_type VARCHAR(50), -- 'view', 'download', 'share'
    ip_address VARCHAR(50),
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Report Types and Templates

### 1. Student Reports

```json
{
  "student_progress_report": {
    "type": "student",
    "frequency": "weekly",
    "data": {
      "personal_info": {
        "student_name": "String",
        "student_id": "UUID",
        "grade_level": "String",
        "enrollment_date": "Date"
      },
      "course_progress": [{
        "course_name": "String",
        "progress_percentage": "Number",
        "current_grade": "Number",
        "completed_modules": "Number",
        "total_modules": "Number",
        "last_activity": "Date"
      }],
      "assessments": [{
        "title": "String",
        "type": "String",
        "score": "Number",
        "completion_date": "Date",
        "feedback": "String"
      }],
      "attendance": {
        "total_sessions": "Number",
        "attended_sessions": "Number",
        "attendance_rate": "Number"
      },
      "learning_objectives": [{
        "objective": "String",
        "status": "String",
        "mastery_level": "String"
      }]
    }
  }
}
```

### 2. Parent Reports

```json
{
  "parent_summary_report": {
    "type": "parent",
    "frequency": "weekly",
    "data": {
      "children": [{
        "student_name": "String",
        "student_id": "UUID",
        "overall_performance": {
          "gpa": "Number",
          "attendance_rate": "Number",
          "courses_enrolled": "Number"
        },
        "course_summaries": [{
          "course_name": "String",
          "current_grade": "Number",
          "progress": "Number",
          "recent_assessments": [{
            "title": "String",
            "score": "Number",
            "date": "Date"
          }]
        }],
        "upcoming_deadlines": [{
          "course": "String",
          "assignment": "String",
          "due_date": "Date"
        }],
        "teacher_comments": [{
          "course": "String",
          "comment": "String",
          "date": "Date"
        }]
      }]
    }
  }
}
```

### 3. Instructor Reports

```json
{
  "class_performance_report": {
    "type": "instructor",
    "frequency": "daily",
    "data": {
      "course_info": {
        "course_name": "String",
        "course_id": "UUID",
        "total_students": "Number"
      },
      "class_statistics": {
        "average_grade": "Number",
        "grade_distribution": {
          "A": "Number",
          "B": "Number",
          "C": "Number",
          "D": "Number",
          "F": "Number"
        },
        "completion_rate": "Number",
        "engagement_rate": "Number"
      },
      "student_performance": [{
        "student_name": "String",
        "current_grade": "Number",
        "attendance_rate": "Number",
        "completed_assignments": "Number",
        "participation_score": "Number"
      }],
      "module_analytics": [{
        "module_name": "String",
        "completion_rate": "Number",
        "average_score": "Number",
        "time_spent": "Number"
      }],
      "at_risk_students": [{
        "student_name": "String",
        "risk_factors": ["String"],
        "last_activity": "Date"
      }]
    }
  }
}
```

### 4. Branch Manager Reports

```json
{
  "branch_performance_report": {
    "type": "branch",
    "frequency": "monthly",
    "data": {
      "branch_info": {
        "name": "String",
        "id": "UUID",
        "total_students": "Number",
        "total_instructors": "Number"
      },
      "enrollment_metrics": {
        "new_enrollments": "Number",
        "active_students": "Number",
        "completion_rate": "Number",
        "retention_rate": "Number"
      },
      "academic_performance": {
        "average_gpa": "Number",
        "course_completion_rate": "Number",
        "student_satisfaction": "Number"
      },
      "course_analytics": [{
        "course_name": "String",
        "enrollment_count": "Number",
        "average_grade": "Number",
        "completion_rate": "Number",
        "instructor_name": "String"
      }],
      "instructor_performance": [{
        "instructor_name": "String",
        "courses_taught": "Number",
        "average_student_rating": "Number",
        "student_success_rate": "Number"
      }],
      "financial_metrics": {
        "revenue": "Number",
        "expenses": "Number",
        "profit_margin": "Number"
      }
    }
  }
}
```

### 5. Organization Manager Reports

```json
{
  "organization_analytics_report": {
    "type": "organization",
    "frequency": "monthly",
    "data": {
      "organization_overview": {
        "total_branches": "Number",
        "total_students": "Number",
        "total_instructors": "Number",
        "total_courses": "Number"
      },
      "growth_metrics": {
        "student_growth": {
          "current": "Number",
          "previous": "Number",
          "growth_rate": "Number"
        },
        "revenue_growth": {
          "current": "Number",
          "previous": "Number",
          "growth_rate": "Number"
        },
        "course_growth": {
          "current": "Number",
          "previous": "Number",
          "growth_rate": "Number"
        }
      },
      "branch_performance": [{
        "branch_name": "String",
        "total_students": "Number",
        "revenue": "Number",
        "student_satisfaction": "Number",
        "completion_rate": "Number"
      }],
      "financial_summary": {
        "total_revenue": "Number",
        "total_expenses": "Number",
        "profit": "Number",
        "revenue_per_student": "Number"
      },
      "educational_metrics": {
        "average_completion_rate": "Number",
        "average_satisfaction_score": "Number",
        "student_retention_rate": "Number"
      },
      "top_performing_courses": [{
        "course_name": "String",
        "enrollment_count": "Number",
        "satisfaction_score": "Number",
        "revenue": "Number"
      }]
    }
  }
}
```

## Report Generation and Access

### Report Generation Process

```python
async def generate_report(report_definition_id: UUID, context: Dict):
    """
    Generate a report based on the report definition and context
    """
    # 1. Load report definition
    report_def = await get_report_definition(report_definition_id)
    
    # 2. Gather data based on report type
    data = await gather_report_data(report_def, context)
    
    # 3. Apply templates and formatting
    formatted_report = await format_report(report_def, data)
    
    # 4. Generate file in specified format
    file_url = await create_report_file(formatted_report, report_def.format)
    
    # 5. Save generated report
    report = await save_generated_report(
        report_definition_id=report_definition_id,
        data=formatted_report,
        file_url=file_url,
        **context
    )
    
    # 6. Log report generation
    await log_report_access(report.id, context['user_id'], 'generate')
    
    return report
```

### Report Access Control

```python
async def check_report_access(user_id: UUID, report_id: UUID):
    """
    Check if user has access to the report
    """
    # Get report details
    report = await get_generated_report(report_id)
    
    # Get user's roles and permissions
    user_roles = await get_user_roles(user_id)
    
    # Check access based on report type and user roles
    if report.type == 'student':
        # Students can only access their own reports
        return report.user_id == user_id
    elif report.type == 'parent':
        # Parents can access their children's reports
        return await is_parent_of_student(user_id, report.user_id)
    elif report.type == 'instructor':
        # Instructors can access reports for their courses
        return await is_course_instructor(user_id, report.course_id)
    elif report.type == 'branch':
        # Branch managers can access their branch reports
        return await is_branch_manager(user_id, report.branch_id)
    elif report.type == 'organization':
        # Organization managers can access org reports
        return await is_organization_manager(user_id, report.organization_id)
    
    return False
```

### Report Distribution

```python
async def distribute_report(report_id: UUID, recipients: List[Dict]):
    """
    Distribute generated report to recipients
    """
    # Get report details
    report = await get_generated_report(report_id)
    
    for recipient in recipients:
        # Check recipient access
        if await check_report_access(recipient['user_id'], report_id):
            # Send notification
            await send_report_notification(
                user_id=recipient['user_id'],
                report_id=report_id,
                notification_type=recipient.get('notification_type', 'email')
            )
            
            # Log access
            await log_report_access(
                report_id=report_id,
                user_id=recipient['user_id'],
                access_type='distribute'
            )
```

## Report Scheduling and Automation

```python
async def schedule_report(
    report_definition_id: UUID,
    frequency: str,
    recipients: List[Dict],
    settings: Dict
):
    """
    Schedule automated report generation and distribution
    """
    # Create schedule
    schedule = await create_report_schedule(
        report_definition_id=report_definition_id,
        frequency=frequency,
        recipients=recipients,
        settings=settings
    )
    
    # Calculate next run time
    next_run = calculate_next_run(frequency)
    
    # Update schedule
    await update_report_schedule(
        schedule_id=schedule.id,
        next_run=next_run
    )
    
    return schedule
```

## Example Usage

### Generate Student Progress Report

```python
# Generate weekly student progress report
student_report = await generate_report(
    report_definition_id=student_progress_report_id,
    context={
        'user_id': student_id,
        'type': 'student',
        'period': 'weekly'
    }
)

# Distribute to student and parents
await distribute_report(
    report_id=student_report.id,
    recipients=[
        {'user_id': student_id, 'notification_type': 'email'},
        {'user_id': parent_id, 'notification_type': 'email'}
    ]
)
```

### Generate Branch Performance Report

```python
# Generate monthly branch performance report
branch_report = await generate_report(
    report_definition_id=branch_performance_report_id,
    context={
        'branch_id': branch_id,
        'type': 'branch',
        'period': 'monthly'
    }
)

# Distribute to branch managers and organization admins
await distribute_report(
    report_id=branch_report.id,
    recipients=[
        {'user_id': branch_manager_id, 'notification_type': 'email'},
        {'user_id': org_admin_id, 'notification_type': 'dashboard'}
    ]
)
``` 