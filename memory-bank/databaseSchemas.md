# Database Schemas: Multi-Tenant LMS

## Overview

Our LMS uses a multi-database strategy to optimize for different data types and access patterns:

1. **PostgreSQL**: Core transactional data, relationships, and ACID compliance
2. **MongoDB**: Flexible content storage and document management
3. **Pinecone**: Vector storage for AI/ML features
4. **Elasticsearch**: Search functionality and analytics
5. **Redis**: Caching and real-time features

## PostgreSQL Schemas

### Organizations and Branches

```sql
-- Organizations
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE,
    settings JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Branches
CREATE TABLE branches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    address TEXT,
    settings JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Branch Settings
CREATE TABLE branch_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    branch_id UUID REFERENCES branches(id),
    key VARCHAR(255) NOT NULL,
    value JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(branch_id, key)
);
```

### Users and Authentication

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    settings JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User Profiles
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) UNIQUE,
    profile_type VARCHAR(50) NOT NULL, -- 'student', 'instructor', 'parent', 'admin'
    bio TEXT,
    avatar_url VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    preferences JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Parent-Student Relationships
CREATE TABLE parent_student_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    parent_id UUID REFERENCES users(id),
    student_id UUID REFERENCES users(id),
    relationship_type VARCHAR(50) DEFAULT 'primary', -- 'primary', 'secondary', etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(parent_id, student_id)
);

-- User Organizations
CREATE TABLE user_organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    organization_id UUID REFERENCES organizations(id),
    role VARCHAR(50) NOT NULL, -- 'owner', 'admin', 'instructor', 'student', 'parent'
    permissions JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, organization_id)
);

-- User Branches
CREATE TABLE user_branches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    branch_id UUID REFERENCES branches(id),
    role VARCHAR(50) NOT NULL, -- 'admin', 'instructor', 'student', 'parent'
    permissions JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, branch_id)
);

-- Sessions
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    token VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Courses and Enrollments

```sql
-- Courses
CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id),
    branch_id UUID REFERENCES branches(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    settings JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Course Instructors
CREATE TABLE course_instructors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID REFERENCES courses(id),
    user_id UUID REFERENCES users(id),
    role VARCHAR(50) DEFAULT 'instructor', -- 'instructor', 'assistant', 'co-instructor'
    permissions JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(course_id, user_id)
);

-- Course Enrollments
CREATE TABLE course_enrollments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID REFERENCES courses(id),
    user_id UUID REFERENCES users(id),
    enrollment_type VARCHAR(50) DEFAULT 'student', -- 'student', 'auditor', 'guest'
    status VARCHAR(50) DEFAULT 'active',
    progress JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(course_id, user_id)
);

-- Student Groups
CREATE TABLE student_groups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID REFERENCES courses(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    settings JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Group Memberships
CREATE TABLE group_memberships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID REFERENCES student_groups(id),
    user_id UUID REFERENCES users(id),
    role VARCHAR(50) DEFAULT 'member', -- 'member', 'leader', 'assistant'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(group_id, user_id)
);
```

### Roles and Permissions

```sql
-- Role Definitions
CREATE TABLE role_definitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    scope VARCHAR(50) NOT NULL, -- 'organization', 'branch', 'course', 'group'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Permission Definitions
CREATE TABLE permission_definitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    resource VARCHAR(100) NOT NULL, -- 'user', 'course', 'content', etc.
    action VARCHAR(50) NOT NULL, -- 'create', 'read', 'update', 'delete', 'manage'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Role Permissions
CREATE TABLE role_permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    role_id UUID REFERENCES role_definitions(id),
    permission_id UUID REFERENCES permission_definitions(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(role_id, permission_id)
);

-- Custom Permissions
CREATE TABLE custom_permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    organization_id UUID REFERENCES organizations(id),
    branch_id UUID REFERENCES branches(id),
    permission_id UUID REFERENCES permission_definitions(id),
    granted_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_id, organization_id, branch_id, permission_id)
);
```

## MongoDB Collections

### Content Management

```javascript
// Courses Content
{
  _id: ObjectId,
  courseId: UUID,
  type: String, // 'video', 'document', 'quiz', etc.
  title: String,
  content: Object,
  metadata: {
    duration: Number,
    size: Number,
    format: String,
    tags: [String]
  },
  settings: Object,
  created_at: Date,
  updated_at: Date
}

// Learning Materials
{
  _id: ObjectId,
  courseId: UUID,
  type: String,
  title: String,
  content: Object,
  metadata: {
    author: String,
    version: String,
    language: String
  },
  settings: Object,
  created_at: Date,
  updated_at: Date
}
```

### User Progress

```javascript
// Course Progress
{
  _id: ObjectId,
  userId: UUID,
  courseId: UUID,
  progress: {
    completedModules: [String],
    currentModule: String,
    score: Number,
    timeSpent: Number
  },
  assessments: [{
    type: String,
    score: Number,
    completedAt: Date
  }],
  created_at: Date,
  updated_at: Date
}

// Student Performance
{
  _id: ObjectId,
  userId: UUID,
  courseId: UUID,
  performance: {
    attendance: Number,
    participation: Number,
    assignments: [{
      id: String,
      score: Number,
      feedback: String,
      submittedAt: Date
    }],
    overallGrade: Number
  },
  parentAccess: {
    enabled: Boolean,
    lastViewed: Date
  },
  created_at: Date,
  updated_at: Date
}
```

## Pinecone Indexes

### Vector Storage

```python
# Course Content Vectors
{
    "id": "course_content_{content_id}",
    "values": [float],  # 1536-dimensional vector
    "metadata": {
        "content_id": str,
        "course_id": str,
        "type": str,
        "title": str,
        "tags": List[str]
    }
}

# Learning Material Vectors
{
    "id": "material_{material_id}",
    "values": [float],  # 1536-dimensional vector
    "metadata": {
        "material_id": str,
        "course_id": str,
        "type": str,
        "title": str,
        "language": str
    }
}
```

## Elasticsearch Indices

### Search and Analytics

```json
// Courses Index
{
  "mappings": {
    "properties": {
      "id": { "type": "keyword" },
      "organization_id": { "type": "keyword" },
      "branch_id": { "type": "keyword" },
      "title": { "type": "text" },
      "description": { "type": "text" },
      "status": { "type": "keyword" },
      "tags": { "type": "keyword" },
      "created_at": { "type": "date" },
      "updated_at": { "type": "date" }
    }
  }
}

// User Progress Index
{
  "mappings": {
    "properties": {
      "user_id": { "type": "keyword" },
      "course_id": { "type": "keyword" },
      "organization_id": { "type": "keyword" },
      "branch_id": { "type": "keyword" },
      "progress": { "type": "float" },
      "completed_modules": { "type": "keyword" },
      "last_activity": { "type": "date" }
    }
  }
}

// User Roles Index
{
  "mappings": {
    "properties": {
      "user_id": { "type": "keyword" },
      "organization_id": { "type": "keyword" },
      "branch_id": { "type": "keyword" },
      "roles": { "type": "keyword" },
      "profile_type": { "type": "keyword" },
      "permissions": { "type": "keyword" }
    }
  }
}
```

## Redis Data Structures

### Caching and Real-time Features

```python
# Session Cache
{
    "session:{session_id}": {
        "user_id": str,
        "organization_id": str,
        "roles": List[str],
        "permissions": List[str],
        "expires_at": int
    }
}

# Course Progress Cache
{
    "course_progress:{user_id}:{course_id}": {
        "current_module": str,
        "completed_modules": List[str],
        "last_activity": int
    }
}

# User Roles Cache
{
    "user_roles:{user_id}:{organization_id}": {
        "roles": List[str],
        "permissions": List[str],
        "profile_types": List[str]
    }
}

# Real-time Notifications
{
    "notifications:{user_id}": List[{
        "type": str,
        "message": str,
        "created_at": int
    }]
}
```

## Indexes and Constraints

### PostgreSQL Indexes

```sql
-- Organizations
CREATE INDEX idx_organizations_domain ON organizations(domain);

-- Branches
CREATE INDEX idx_branches_organization ON branches(organization_id);

-- Users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);

-- User Profiles
CREATE INDEX idx_user_profiles_user ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_type ON user_profiles(profile_type);

-- Parent-Student Relationships
CREATE INDEX idx_parent_student_parent ON parent_student_relationships(parent_id);
CREATE INDEX idx_parent_student_student ON parent_student_relationships(student_id);

-- User Organizations
CREATE INDEX idx_user_orgs_user ON user_organizations(user_id);
CREATE INDEX idx_user_orgs_org ON user_organizations(organization_id);
CREATE INDEX idx_user_orgs_role ON user_organizations(role);

-- User Branches
CREATE INDEX idx_user_branches_user ON user_branches(user_id);
CREATE INDEX idx_user_branches_branch ON user_branches(branch_id);
CREATE INDEX idx_user_branches_role ON user_branches(role);

-- Courses
CREATE INDEX idx_courses_organization ON courses(organization_id);
CREATE INDEX idx_courses_branch ON courses(branch_id);
CREATE INDEX idx_courses_status ON courses(status);

-- Course Instructors
CREATE INDEX idx_course_instructors_course ON course_instructors(course_id);
CREATE INDEX idx_course_instructors_user ON course_instructors(user_id);

-- Enrollments
CREATE INDEX idx_enrollments_course ON course_enrollments(course_id);
CREATE INDEX idx_enrollments_user ON course_enrollments(user_id);
CREATE INDEX idx_enrollments_type ON course_enrollments(enrollment_type);

-- Student Groups
CREATE INDEX idx_student_groups_course ON student_groups(course_id);

-- Group Memberships
CREATE INDEX idx_group_memberships_group ON group_memberships(group_id);
CREATE INDEX idx_group_memberships_user ON group_memberships(user_id);

-- Roles and Permissions
CREATE INDEX idx_role_permissions_role ON role_permissions(role_id);
CREATE INDEX idx_role_permissions_permission ON role_permissions(permission_id);
CREATE INDEX idx_custom_permissions_user ON custom_permissions(user_id);
CREATE INDEX idx_custom_permissions_org ON custom_permissions(organization_id);
CREATE INDEX idx_custom_permissions_branch ON custom_permissions(branch_id);
```

### MongoDB Indexes

```javascript
// Content Collections
db.courses_content.createIndex({ "courseId": 1 });
db.courses_content.createIndex({ "type": 1 });
db.courses_content.createIndex({ "metadata.tags": 1 });

// Progress Collections
db.course_progress.createIndex({ "userId": 1, "courseId": 1 });
db.course_progress.createIndex({ "updated_at": -1 });

// Student Performance
db.student_performance.createIndex({ "userId": 1, "courseId": 1 });
db.student_performance.createIndex({ "parentAccess.enabled": 1 });
```

## Data Relationships

1. **Organization -> Branch**: One-to-Many
2. **Organization -> User**: Many-to-Many (through user_organizations)
3. **Branch -> User**: Many-to-Many (through user_branches)
4. **User -> User Profile**: One-to-One
5. **Parent -> Student**: Many-to-Many (through parent_student_relationships)
6. **Course -> Organization**: Many-to-One
7. **Course -> Branch**: Many-to-One
8. **Course -> Instructor**: Many-to-Many (through course_instructors)
9. **Course -> Student**: Many-to-Many (through course_enrollments)
10. **Course -> Student Group**: One-to-Many
11. **Student Group -> Student**: Many-to-Many (through group_memberships)
12. **Content -> Course**: Many-to-One
13. **Progress -> User**: Many-to-One
14. **Progress -> Course**: Many-to-One
15. **Role -> Permission**: Many-to-Many (through role_permissions)
16. **User -> Custom Permission**: Many-to-Many (through custom_permissions)

## Multi-tenancy Implementation

1. **Organization-level Isolation**:
   - All data is associated with an organization_id
   - Row-level security policies enforce organization isolation
   - Cross-organization access is controlled through explicit permissions

2. **Branch-level Isolation**:
   - Branch-specific data is isolated within organizations
   - Branch managers can only access their branch's data
   - Cross-branch access requires explicit permissions

3. **User-level Isolation**:
   - Users can only access data they have permission for
   - Role-based access control (RBAC) enforces permissions
   - Session management ensures proper authentication

## Role Management

1. **User Roles**:
   - A user can have multiple roles across different organizations and branches
   - Roles are stored in user_organizations and user_branches tables
   - Common roles include: owner, admin, instructor, student, parent

2. **Profile Types**:
   - A user can have multiple profile types (student, instructor, parent, admin)
   - Profile types are stored in user_profiles table
   - Profile types determine available features and UI elements

3. **Permission System**:
   - Permissions are stored as JSONB in user_organizations and user_branches
   - Granular permissions can be assigned to each role
   - Permission inheritance can be implemented through role hierarchy

4. **Parent-Student Relationship**:
   - Parents can be linked to multiple students
   - Students can have multiple parents (primary and secondary)
   - Parents can view their children's progress through parentAccess in student_performance

5. **Instructor-Student Relationship**:
   - Instructors are linked to courses through course_instructors
   - Students are linked to courses through course_enrollments
   - Instructors can view and manage their students' progress

## Roles and Permissions Details

### Role Definitions

| Role | Scope | Description | Can Do | Cannot Do |
|------|-------|-------------|--------|-----------|
| **Owner** | Organization | Full control over the organization | - Create/edit/delete organizations<br>- Manage all branches<br>- Assign all roles<br>- Access all data<br>- Configure system settings<br>- Manage billing | - Cannot be restricted by other roles |
| **Admin** | Organization/Branch | Administrative control | - Manage users<br>- Create/edit courses<br>- View analytics<br>- Manage content<br>- Configure branch settings | - Cannot delete organization<br>- Cannot manage billing<br>- Cannot assign owner role |
| **Instructor** | Course | Teaching role | - Create/edit course content<br>- Grade assignments<br>- View student progress<br>- Create assessments<br>- Provide feedback | - Cannot manage users<br>- Cannot access other instructors' courses<br>- Cannot modify system settings |
| **Student** | Course | Learning role | - Access enrolled courses<br>- Submit assignments<br>- Take assessments<br>- View own progress<br>- Participate in discussions | - Cannot create courses<br>- Cannot grade assignments<br>- Cannot access other students' data |
| **Parent** | Student | Monitoring role | - View children's progress<br>- Receive notifications<br>- Access progress reports<br>- Communicate with instructors | - Cannot access course content<br>- Cannot submit assignments<br>- Cannot modify grades |
| **Assistant** | Course | Support role | - Help with course management<br>- Grade assignments<br>- Provide feedback<br>- Moderate discussions | - Cannot create new courses<br>- Cannot modify course structure<br>- Cannot access student personal data |
| **Auditor** | Course | Read-only role | - View course content<br>- Access materials<br>- Participate in discussions | - Cannot submit assignments<br>- Cannot receive grades<br>- Cannot access student data |

### Permission Definitions

| Resource | Action | Description | Example |
|----------|--------|-------------|---------|
| **user** | create | Create new users | Adding students to a course |
| **user** | read | View user information | Viewing student profiles |
| **user** | update | Modify user information | Updating contact details |
| **user** | delete | Remove users | Removing inactive students |
| **user** | manage | Full user management | Managing all user accounts |
| **course** | create | Create new courses | Setting up a new class |
| **course** | read | View course information | Accessing course materials |
| **course** | update | Modify course details | Updating course description |
| **course** | delete | Remove courses | Removing outdated courses |
| **course** | manage | Full course management | Managing all course aspects |
| **content** | create | Create learning content | Adding new lessons |
| **content** | read | View learning content | Accessing course materials |
| **content** | update | Modify learning content | Editing existing lessons |
| **content** | delete | Remove learning content | Removing outdated materials |
| **content** | manage | Full content management | Managing all course content |
| **assessment** | create | Create assessments | Creating quizzes |
| **assessment** | read | View assessments | Taking quizzes |
| **assessment** | update | Modify assessments | Editing quiz questions |
| **assessment** | delete | Remove assessments | Removing outdated quizzes |
| **assessment** | grade | Grade assessments | Grading student submissions |
| **progress** | read | View progress data | Checking student progress |
| **progress** | update | Modify progress data | Updating grades |
| **progress** | manage | Full progress management | Managing all student progress |
| **organization** | manage | Full organization management | Managing organization settings |
| **branch** | manage | Full branch management | Managing branch settings |
| **report** | generate | Create reports | Generating analytics |
| **report** | view | View reports | Accessing analytics |

### Role-Permission Examples

#### Organization Owner
```json
{
  "permissions": [
    "organization:manage",
    "branch:manage",
    "user:manage",
    "course:manage",
    "content:manage",
    "assessment:manage",
    "progress:manage",
    "report:generate",
    "report:view"
  ]
}
```

#### Organization Admin
```json
{
  "permissions": [
    "branch:manage",
    "user:manage",
    "course:manage",
    "content:manage",
    "assessment:manage",
    "progress:manage",
    "report:generate",
    "report:view"
  ]
}
```

#### Branch Admin
```json
{
  "permissions": [
    "user:manage",
    "course:manage",
    "content:manage",
    "assessment:manage",
    "progress:manage",
    "report:generate",
    "report:view"
  ]
}
```

#### Instructor
```json
{
  "permissions": [
    "course:read",
    "course:update",
    "content:create",
    "content:read",
    "content:update",
    "content:delete",
    "assessment:create",
    "assessment:read",
    "assessment:update",
    "assessment:delete",
    "assessment:grade",
    "progress:read",
    "progress:update",
    "report:view"
  ]
}
```

#### Student
```json
{
  "permissions": [
    "course:read",
    "content:read",
    "assessment:read",
    "progress:read"
  ]
}
```

#### Parent
```json
{
  "permissions": [
    "progress:read",
    "report:view"
  ]
}
```

### Permission Inheritance

Permissions follow a hierarchical structure:

1. **Organization Owner** inherits all permissions
2. **Organization Admin** inherits all permissions except organization management
3. **Branch Admin** inherits all permissions except organization management
4. **Instructor** inherits course and content management permissions
5. **Student** inherits read-only permissions for courses and content
6. **Parent** inherits read-only permissions for progress and reports

### Custom Permissions

Custom permissions allow for fine-grained access control:

```sql
-- Example: Grant a student permission to create content in a specific course
INSERT INTO custom_permissions (
    user_id,
    organization_id,
    branch_id,
    permission_id,
    granted_by
) VALUES (
    'student-uuid',
    'org-uuid',
    'branch-uuid',
    'content:create-permission-uuid',
    'admin-uuid'
);
```

### Permission Enforcement

Permissions are enforced at multiple levels:

1. **Application Level**: Through middleware that checks user permissions
2. **Database Level**: Through row-level security policies
3. **API Level**: Through permission checks in API endpoints
4. **UI Level**: Through conditional rendering of UI elements

Example of permission check in API:

```python
@router.get("/courses/{course_id}/students")
async def get_course_students(
    course_id: UUID,
    current_user: User = Depends(get_current_user)
):
    # Check if user has permission to view students
    if not has_permission(current_user, "user:read", course_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Return course students
    return await get_students_for_course(course_id)
```

### Role Assignment Examples

#### Assigning a user as an instructor in an organization
```sql
INSERT INTO user_organizations (
    user_id,
    organization_id,
    role,
    permissions
) VALUES (
    'user-uuid',
    'org-uuid',
    'instructor',
    '{"permissions": ["course:read", "course:update", "content:create", "content:read", "content:update", "content:delete", "assessment:create", "assessment:read", "assessment:update", "assessment:delete", "assessment:grade", "progress:read", "progress:update", "report:view"]}'
);
```

#### Assigning a user as a student in a specific course
```sql
INSERT INTO course_enrollments (
    course_id,
    user_id,
    enrollment_type,
    status
) VALUES (
    'course-uuid',
    'user-uuid',
    'student',
    'active'
);
```

#### Linking a parent to a student
```sql
INSERT INTO parent_student_relationships (
    parent_id,
    student_id,
    relationship_type
) VALUES (
    'parent-uuid',
    'student-uuid',
    'primary'
);
```

### Badges and Certificates

```sql
-- Badge Definitions
CREATE TABLE badge_definitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    image_url VARCHAR(255) NOT NULL,
    criteria JSONB NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Earned Badges
CREATE TABLE earned_badges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    badge_definition_id UUID REFERENCES badge_definitions(id),
    user_id UUID REFERENCES users(id),
    course_id UUID REFERENCES courses(id),
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    UNIQUE(badge_definition_id, user_id, course_id)
);

-- Certificate Templates
CREATE TABLE certificate_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    template_url VARCHAR(255) NOT NULL,
    fields JSONB NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Issued Certificates
CREATE TABLE issued_certificates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    certificate_template_id UUID REFERENCES certificate_templates(id),
    user_id UUID REFERENCES users(id),
    course_id UUID REFERENCES courses(id),
    certificate_url VARCHAR(255) NOT NULL,
    verification_code VARCHAR(100) NOT NULL,
    issued_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    UNIQUE(certificate_template_id, user_id, course_id)
);

-- Certificate Verification Logs
CREATE TABLE certificate_verification_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    certificate_id UUID REFERENCES issued_certificates(id),
    verified_by VARCHAR(255),
    verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    verification_method VARCHAR(50),
    ip_address VARCHAR(50),
    user_agent TEXT
);
```

```javascript
// MongoDB Collections for Badges and Certificates

// Badge Progress
{
  _id: ObjectId,
  userId: UUID,
  badgeDefinitionId: UUID,
  courseId: UUID,
  progress: {
    criteria: [{
      name: String,
      completed: Boolean,
      completedAt: Date
    }],
    percentage: Number
  },
  status: String, // 'in_progress', 'completed'
  created_at: Date,
  updated_at: Date
}

// Certificate Data
{
  _id: ObjectId,
  certificateId: UUID,
  userId: UUID,
  courseId: UUID,
  data: {
    studentName: String,
    courseName: String,
    completionDate: Date,
    grade: String,
    instructorName: String,
    organizationName: String,
    customFields: Object
  },
  metadata: {
    format: String,
    size: Number,
    version: String
  },
  created_at: Date,
  updated_at: Date
}
```

```python
# Redis Data Structures for Badges and Certificates

# Badge Progress Cache
{
    "badge_progress:{user_id}:{badge_id}": {
        "criteria_completed": List[str],
        "percentage": float,
        "last_updated": int
    }
}

# Certificate Cache
{
    "certificate:{certificate_id}": {
        "verification_code": str,
        "status": str,
        "last_verified": int
    }
}
```

### Indexes for Badges and Certificates

```sql
-- Badge Definitions
CREATE INDEX idx_badge_definitions_org ON badge_definitions(organization_id);
CREATE INDEX idx_badge_definitions_name ON badge_definitions(name);

-- Earned Badges
CREATE INDEX idx_earned_badges_user ON earned_badges(user_id);
CREATE INDEX idx_earned_badges_course ON earned_badges(course_id);
CREATE INDEX idx_earned_badges_badge ON earned_badges(badge_definition_id);

-- Certificate Templates
CREATE INDEX idx_certificate_templates_org ON certificate_templates(organization_id);
CREATE INDEX idx_certificate_templates_name ON certificate_templates(name);

-- Issued Certificates
CREATE INDEX idx_issued_certificates_user ON issued_certificates(user_id);
CREATE INDEX idx_issued_certificates_course ON issued_certificates(course_id);
CREATE INDEX idx_issued_certificates_template ON issued_certificates(certificate_template_id);
CREATE INDEX idx_issued_certificates_verification ON issued_certificates(verification_code);

-- Certificate Verification Logs
CREATE INDEX idx_certificate_verification_cert ON certificate_verification_logs(certificate_id);
CREATE INDEX idx_certificate_verification_date ON certificate_verification_logs(verified_at);
```

-- Course Reviews Table
CREATE TABLE course_reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID NOT NULL REFERENCES courses(id),
    student_id UUID NOT NULL REFERENCES users(id),
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    content TEXT,
    is_anonymous BOOLEAN DEFAULT false,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'flagged')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(course_id, student_id)
);

-- Course Review Media Table
CREATE TABLE course_review_media (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    review_id UUID NOT NULL REFERENCES course_reviews(id),
    media_type VARCHAR(50) NOT NULL,
    media_url TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Course Review Responses Table
CREATE TABLE course_review_responses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    review_id UUID NOT NULL REFERENCES course_reviews(id),
    instructor_id UUID NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Instructor Reviews Table
CREATE TABLE instructor_reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    instructor_id UUID NOT NULL REFERENCES users(id),
    student_id UUID NOT NULL REFERENCES users(id),
    course_id UUID NOT NULL REFERENCES courses(id),
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    content TEXT,
    is_anonymous BOOLEAN DEFAULT false,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'flagged')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(instructor_id, student_id, course_id)
);

-- Instructor Review Responses Table
CREATE TABLE instructor_review_responses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    review_id UUID NOT NULL REFERENCES instructor_reviews(id),
    instructor_id UUID NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Review Flags Table
CREATE TABLE review_flags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    review_type VARCHAR(20) NOT NULL CHECK (review_type IN ('course', 'instructor')),
    review_id UUID NOT NULL,
    flagged_by UUID NOT NULL REFERENCES users(id),
    reason VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'resolved', 'dismissed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_course_reviews_course_id ON course_reviews(course_id);
CREATE INDEX idx_course_reviews_student_id ON course_reviews(student_id);
CREATE INDEX idx_course_reviews_status ON course_reviews(status);
CREATE INDEX idx_instructor_reviews_instructor_id ON instructor_reviews(instructor_id);
CREATE INDEX idx_instructor_reviews_student_id ON instructor_reviews(student_id);
CREATE INDEX idx_instructor_reviews_status ON instructor_reviews(status);
CREATE INDEX idx_review_flags_review_id ON review_flags(review_id); 