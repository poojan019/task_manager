# Task Management System

A Django-based REST API for managing tasks with role-based access control. Users can register, log in, and perform actions based on their roles (Admin, Manager, Employee). Admins can manage users and tasks, managers can create and assign tasks, and employees can view and update their assigned tasks.

## Features
+ User ROles:
  * Admin: Full system access (user and task management).
  * Manager: Create and assign tasks to employees.
  * Employee: View and update assigned tasks.

+ Task Management:
  * Create, read, update and delete tasks.
  * Assign tasks to employees.
  * Filter tasks by status, priority, and assigned user.

+ Authentication:
  * Token-based authentication for secure API access.

+ Validation:
  * Email format validation.
  * Password length validation (minumum 8 characters).
  * Role-based access control.
 
## Setup Instructions
### Prerequisites
  + Python 3.8+
  + PostgreSQL
  + pip (Python package manager)

### 1. Clone the Repository
```
git clone https://github.com/your-username/task-management-system.git
cd task-management-system
```

### 2. Set Up a Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configure the Database
>#### 1. Create a PostgreSQL database:
    sudo -u postgres psql
    CREATE DATABASE taskmgmt;
    CREATE USER taskuser WITH PASSWORD 'taskpassword';
    GRANT ALL PRIVILEGES ON DATABASE taskmgmt TO taskuser;

>#### 2. Update the database settings in `task_manager/settings.py`
    DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'taskmgmt',
          'USER': 'taskuser',
          'PASSWORD': 'taskpassword',
          'HOST': 'localhost',
          'PORT': '5432',
      }
    }

### 5. Run Migrations
```
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Admin)
```
python manage.py createsuperuser
```
  Follow the prompts to create an admin user.

### 7. Run the Development Server
```
python manage.py runserver
```
  The API will be availabe at `http://localhost:8000/`.

## API Documentation
### Authentication

#### Register a New user

**Endpoint**: `POST /auth/register/` 

**Request:**
```
curl -X POST http://localhost:8000/auth/register/ \
-H "Content-Type: application/json" \
-d '{
    "username": "test_employee",
    "email": "employee@test.com",
    "password": "EmployeePass123"
}'
```

**Response:**
```
{
    "id": 1,
    "username": "test_employee",
    "email": "employee@test.com",
    "role": "EMPLOYEE"
}
```

#### Login

**Endpoint:** `POST /auth/login/`

**Request:**
```
curl -X POST http://localhost:8000/auth/login/ \
-H "Content-Type: application/json" \
-d '{"username": "test_employee", "password": "EmployeePass123"}'
```

**Response:**
```
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "email": "employee@test.com",
    "role": "EMPLOYEE"
}
```

### User Management

#### List all users (Admin only)

**Endpoint:** `GET /users/`

**Request:**
```
curl -H "Authorization: Token ADMIN_TOKEN" http://localhost:8000/users/
```

**Response:**
```
[
    {
        "id": 1,
        "username": "test_employee",
        "email": "employee@test.com",
        "role": "EMPLOYEE"
    }
]
```

#### Update user role (Admin only)

**Endpoint:** `PUT /users/<id>/role/`

**Request:**
```
curl -X PUT http://localhost:8000/users/1/role/ \
-H "Authorization: Token ADMIN_TOKEN" \
-H "Content-Type: application/json" \
-d '{"role": "MANAGER"}'
```

**Response:**
```
{
    "id": 1,
    "username": "test_employee",
    "email": "employee@test.com",
    "role": "MANAGER"
}
```

### Task Management

#### Create a Task (Admin/Manager Only)

**Endpoint:** `POST /tasks/`

**Request:**
```
curl -X POST http://localhost:8000/tasks/ \
-H "Authorization: Token MANAGER_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "title": "Fix Login Page",
    "description": "Update the login page styling",
    "due_date": "2024-03-01T09:00:00Z",
    "priority": "HIGH",
    "assigned_to": 1
}'
```

**Response:**
```
{
    "id": 1,
    "title": "Fix Login Page",
    "description": "Update the login page styling",
    "due_date": "2024-03-01T09:00:00Z",
    "status": "PENDING",
    "priority": "HIGH",
    "created_date": "2024-01-31T12:00:00Z",
    "assigned_to": 1,
    "assigned_by": 2
}
```

#### Assign a Task (Manager only)

**Endpoint:** `POST /tasks/<id>/assign/`

**Request:**
```
curl -X POST http://localhost:8000/tasks/1/assign/ \
-H "Authorization: Token MANAGER_TOKEN" \
-H "Content-Type: application/json" \
-d '{"employee_id": 1}'
```

**Response:**
```
{
    "status": "task assigned"
}
```

#### Update Task Status (Employee Only)

**Endpoint:** `PATCH /tasks/<id>/`

**Request:**
```
curl -X PATCH http://localhost:8000/tasks/1/ \
-H "Authorization: Token EMPLOYEE_TOKEN" \
-H "Content-Type: application/json" \
-d '{"status": "IN_PROGRESS"}'
```

**Response:**
```
{
    "id": 1,
    "title": "Fix Login Page",
    "description": "Update the login page styling",
    "due_date": "2024-03-01T09:00:00Z",
    "status": "IN_PROGRESS",
    "priority": "HIGH",
    "created_date": "2024-01-31T12:00:00Z",
    "assigned_to": 1,
    "assigned_by": 2
}
```

## Support

For any issues or questions, please open an issue on the repository.

This `README.md` provides a complete guide for setting up and using the Task Management System.
