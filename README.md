# VigiAI – AI-powered surveillance and threat
detection backend application 

## 📌 Project Overview
VigiAI is a backend system designed to ingest security/threat events, automatically generate alerts for critical incidents, and manage alerts using role-based access control (RBAC).

The system is built using **Django** but intentionally avoids Django ORM and models. All database operations are performed using **raw SQL queries on SQLite**. Authentication is implemented using **custom JWT-based authentication**, and all APIs are implemented as **POST-only function-based APIs**.

### Key Features
- Custom JWT authentication 
- User roles: **Admin** and **Analyst**
- Role-Based Access Control (RBAC)
- Automatic alert generation for High / Critical severity events
- SQLite database with raw SQL queries
- No Django ORM or models

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ikrlalit/VigiAI.git
cd VigiAI
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\\Scripts\\activate   # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages include:
- Django
- djangorestframework
- pyjwt

---

### 4️⃣ Database Setup (SQLite)
Run migrations only to initialize Django internals:
```bash
python manage.py migrate
```

Create tables manually using dbshell:
```bash
python manage.py dbshell
```

(Create users, events, and alerts tables as per project design.)

---

### 5️⃣ Run the Server
```bash
python manage.py runserver
```

Server will start at:
```
http://127.0.0.1:8000/
```

---

## 🔐 User Authentication & Signup APIs

### ✅ API 1: Add New User
**Endpoint**
```
POST http://127.0.0.1:8000/api/AddNewUser
```

**Request Payload**
```json
{
  "username": "testuser1",
  "password": "abcd",
  "role": "admin"
}
```

**Response**
```json
{
  "status_code": 200,
  "status": "SUCCESS",
  "data": 2,
  "message": "Data inserted Successfully"
}
```

---

### ✅ API 2: User Login
**Endpoint**
```
POST http://127.0.0.1:8000/api/UserLogin
```

**Request Payload**
```json
{
  "username": "testuser1",
  "password": "abcd"
}
```

**Response**
```json
{
  "access_token": "<JWT_TOKEN>",
  "role": "analyst"
}
```

> The access token must be passed in the `Authorization` header for protected APIs:
```
Authorization: Bearer <JWT_TOKEN>
```

---

## 🚨 Threat / Event APIs

### ✅ API 3: Add Event
**Endpoint**
```
POST http://127.0.0.1:8000/api/AddEvent
```

**Request Payload**
```json
{
  "source_name": "CyeNET-VAPT-Scanner",
  "event_type": "malware",
  "severity": "Critical",
  "description": "Ransomware signature 'WannaCry_Var2' detected on isolated research workstation."
}
```

**Response**
```json
{
  "status_code": 200,
  "status": "SUCCESS",
  "data": 6,
  "message": "Data inserted Successfully"
}
```

> If severity is **High** or **Critical**, an alert is automatically generated.

---

## 🚨 Alert APIs

### ✅ API 4: List Alerts
**Endpoint**
```
POST http://127.0.0.1:8000/api/AlertsList
```

**Optional Filters (Request Body)**
```json
{
  "event_severity": "Critical",
  "event_status": "Open"
}
```

**Response**
```json
{
  "status_code": 200,
  "status": "SUCCESS",
  "data": [
    {
      "id": 2,
      "status": "Open",
      "created_at": "2025-12-25T09:22:30",
      "event_id": 6,
      "source_name": "CyeNET-VAPT-Scanner",
      "event_type": "malware",
      "severity": "Critical",
      "description": "Ransomware signature 'WannaCry_Var2' detected on isolated research workstation."
    }
  ],
  "message": "Data Found Successfully"
}
```

---

### ✅ API 5: Update Alert Status
**Endpoint**
```
POST http://127.0.0.1:8000/api/AlertStatusUpdate
```

**Request Payload**
```json
{
  "alert_id": 1,
  "alert_status": "Acknowledged"
}
```

**Response**
```json
{
  "status_code": 200,
  "status": "SUCCESS",
  "data": 1,
  "message": "Data Updated Successfully"
}
```

> Allowed status values: `Open`, `Acknowledged`, `Resolved`

---

## 🔐 Role-Based Access Control (RBAC)

| Role | Permissions |
|----|----|
| Admin | Full access (create users, events, alerts, update alert status) |
| Analyst | Read-only access to alerts |

RBAC is enforced using:
- Custom JWT middleware
- Role checks via decorators

---

## 📌 Assumptions Made

- All APIs are **POST-only** for consistency
- SQLite is used as the database
- Django ORM and models are intentionally not used
- JWT tokens are custom-generated using `pyjwt`
- Alert generation is synchronous with event creation
- Analysts cannot modify alert status
- Admins manage alert lifecycle

---

## 🏁 Conclusion

This project demonstrates a clean separation of authentication, authorization, and business logic using raw SQL and custom JWT handling. It is suitable for security event ingestion pipelines, alerting systems, and backend engineering assessments.

