# 🗂 Task Management System (Django + DRF + JWT)

A **role-based Task Management System** built using **Django, Django REST Framework, JWT Authentication, and custom HTML Admin Panel**.

This project supports:
- **SuperAdmin**
- **Admin**
- **User**

with **strict access control**, **JWT-secured APIs**, and a **custom-built admin panel (no Django admin UI)**.


## 📌 Features Overview

### 🔐 Authentication
- JWT Authentication (Access + Refresh tokens)
- Separate login for:
  - API users
  - Admin/SuperAdmin web panel

### 🧑‍💼 Roles & Permissions
``` bash
| Role | Capabilities |
|----|----|
| SuperAdmin | Full control over users, admins, tasks, reports |
| Admin | Manages only assigned users & their tasks |
| User | Can view & update own tasks via API |

```
---

## 🛠 Tech Stack
- Python 3.x
- Django
- Django REST Framework
- SimpleJWT
- SQLite (default)
- Bootstrap (Admin Panel UI)


## 📁 Project Structure

``` bash

task_manager/
│
├── task_manager/
│   └── urls.py
│
├── apps/
│   ├── user/
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── serializers.py
│   │
│   ├── admins/
│   │   ├── views.py
│   │   ├── urls.py
│   │   
│   │
│   └── accounts/
│       ├── models.py
│       └── permissions.py
│
├── templates/
│   └── adminpanel/
│
├── manage.py
└── requirements.txt

```

---

## 🚀 Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone <repository-url>
cd task_manager
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv env
source env/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create SuperAdmin

```bash
python manage.py createsuperuser
```

> Make sure to set `role = SUPERADMIN` when prompted.

### 6️⃣ Run Server

```bash
python manage.py runserver
```

---

## 🔑 Authentication (API)

### 🔐 User Login

**POST**

```
/user/login/
```

**Request**

```json
{
  "username": "user1",
  "password": "password"
}
```

**Response**

```json
{
  "access": "<jwt-access-token>",
  "refresh": "<jwt-refresh-token>"
}
```

### 🔄 Refresh Token

**POST**

```
/user/token/refresh/
```

---

## 👤 User APIs

### 📋 View Assigned Tasks

**GET**

```
/user/tasks/
```

### ✏️ Update Task (Submit Completion Report)

**PUT**

```
/user/tasks/<task_id>/
```

**Payload**

```json
{
  "status": "COMPLETED",
  "completion_report": "Task finished successfully",
  "worked_hours": 6.5
}
```

---

## 🛡 Admin Panel (Web)

### 🔐 Login

```
/admins/login/
```

> Only **Admin** and **SuperAdmin** can login.

---

## 🧑‍💼 SuperAdmin Capabilities

| Action               | URL                                |
| -------------------- | ---------------------------------- |
| View All Users       | `/admins/users/`                   |
| Create User/Admin    | `/admins/users/create/`            |
| Delete User          | `/admins/users/<id>/delete/`       |
| Assign User to Admin | `/admins/users/<id>/assign-admin/` |
| View All Tasks       | `/admins/tasks/`                   |
| View Task Reports    | `/admins/tasks/<id>/report/`       |

---

## 👨‍💻 Admin Capabilities

| Action                          | URL                          |
| ------------------------------- | ---------------------------- |
| Dashboard                       | `/admins/dashboard/`         |
| View Own Users                  | Filtered automatically       |
| Create Tasks for Assigned Users | `/admins/tasks/create/`      |
| View Reports                    | `/admins/tasks/<id>/report/` |

> ❌ Admin **cannot manage roles or users outside their scope**

---

## 🔐 Permission Logic

```python
class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'
```

---

## 🧠 User–Admin Relationship

Each **USER** has:

```python
admin = models.ForeignKey('self', related_name='users')
```

This allows:

* Filtering users under an Admin
* Admin assigning tasks only to owned users
* Clean hierarchical RBAC


## 📄 Admin Panel Templates

* Custom HTML (Bootstrap)
* Role-aware navigation
* Secure server-side filtering
* No Django Admin used





