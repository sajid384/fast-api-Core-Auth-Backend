# 🔐 Fast API Core Auth Backend

A complete authentication backend system built using **FastAPI**, **JWT Authentication**, **Redis Blacklisting**, **Async SQLAlchemy**, and **Pytest**.

This project provides a secure and scalable authentication system with modern backend practices.

---

# 🚀 Features

## ✅ Authentication Features

- User Registration
- User Login
- JWT Access Tokens
- JWT Refresh Tokens
- Token Refresh Endpoint
- Protected Routes
- Secure Logout System
- Redis Token Blacklisting

---

## ✅ Security Features

- Password Hashing using Bcrypt
- JWT Authentication
- Bearer Token Authorization
- Blacklisted Token Protection
- Secure Password Storage

---

## ✅ Backend Features

- FastAPI Async Backend
- Async SQLAlchemy
- SQLite Database
- Pydantic Validation
- Dependency Injection
- Modular Project Structure
- REST API Architecture

---

## ✅ Testing Features

- Automated API Testing
- Async Testing with Pytest
- Authentication Route Testing
- Protected Route Testing
- Logout & Blacklist Testing

---

# 🛠️ Technologies Used

| Technology | Usage |
|---|---|
| FastAPI | Backend Framework |
| SQLAlchemy | ORM |
| SQLite | Database |
| Redis | Token Blacklisting |
| JWT | Authentication |
| Passlib + Bcrypt | Password Hashing |
| HTTPX | API Testing |
| Pytest | Automated Testing |
| AsyncIO | Async Support |
| Pydantic | Data Validation |

---

# 📁 Project Structure

```bash
core-auth-backend/
│
├── app/
│   │
│   ├── routes/
│   │   └── user_routes.py
│   │
│   ├── utils/
│   │   ├── security.py
│   │   └── redis_blacklist.py
│   │
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── tests/
│   └── test_auth.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ How The Project Works

# 1️⃣ User Registration

The user sends:

- Username
- Email
- Password

The backend:

- Validates the data
- Hashes the password using bcrypt
- Saves user into database

---

# 2️⃣ User Login

User logs in using:

- Email
- Password

Backend verifies credentials and returns:

- Access Token
- Refresh Token

---

# 3️⃣ Protected Routes

Protected routes require:

```http
Authorization: Bearer <access_token>
```

JWT token is validated before access is granted.

---

# 4️⃣ Refresh Token System

Refresh token endpoint generates a new access token without requiring the user to login again.

---

# 5️⃣ Logout System

When user logs out:

- Access token is stored inside Redis blacklist
- Blacklisted token becomes invalid
- Protected routes reject blacklisted tokens

---

# 🔐 JWT Authentication

The project uses:

```python
python-jose
```

JWT payload contains:

- User Email
- Expiration Time
- Token Type

---

# 🔒 Password Hashing

Passwords are hashed using:

```python
bcrypt
```

Plain passwords are never stored in database.

---

# ⚡ Async Support

This project fully uses async programming:

- Async FastAPI Routes
- Async Database Queries
- Async Redis
- Async API Testing

This improves performance and scalability.

---

# 🗄️ Database

The project uses:

```python
SQLite
```

with:

```python
Async SQLAlchemy
```

---

# 📘 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /register | Register User |
| POST | /login | Login User |
| GET | /protected | Protected Route |
| POST | /refresh | Generate New Access Token |
| POST | /logout | Logout User |

---

# 🧪 Automated Testing

Project includes complete authentication tests.

## Included Tests

✅ Register User  
✅ Login User  
✅ Protected Route Access  
✅ Refresh Token  
✅ Logout & Blacklist  

---

# ✅ Test Results

```bash
5 passed
```

All authentication features are successfully tested.

---

# 📦 Installation Guide

# 1️⃣ Clone Repository

```bash
git clone https://github.com/sajid384/fast-api-Core-Auth-Backend.git
```

---

# 2️⃣ Navigate To Project

```bash
cd fast-api-Core-Auth-Backend
```

---

# 3️⃣ Create Virtual Environment

```bash
py -3.14 -m venv venv
```

---

# 4️⃣ Activate Virtual Environment

## Windows

```bash
venv\Scripts\activate
```

---

# 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run The Project

# Start Redis Server

Make sure Redis server is running on:

```bash
localhost:6379
```

---

# Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

# 🌐 API Documentation

FastAPI automatically provides API docs.

## Swagger UI

```bash
http://127.0.0.1:8000/docs
```

---

# ReDoc

```bash
http://127.0.0.1:8000/redoc
```

---

# 🧪 Run Tests

```bash
pytest
```

---

# 📌 Future Improvements

- PostgreSQL Integration
- Docker Support
- Email Verification
- OAuth Authentication
- Role-Based Access Control
- Rate Limiting
- Deployment on Railway/Render
- CI/CD Integration

---

# 👨‍💻 Author

## Syed Sajid Hussain

Backend Developer | FastAPI Enthusiast

GitHub:

```bash
https://github.com/sajid384
```

---

# ⭐ Project Status

✅ Completed  
✅ Fully Functional  
✅ Fully Tested  
✅ GitHub Ready  
✅ Production Ready Structure  

---

# 📄 License

This project is open-source and available for learning and development purposes.
