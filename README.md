# 🧠 Task Manager API (FastAPI + JWT)

## 🚀 Overview

This is a backend task management system built using FastAPI.
It supports user authentication and user-specific task operations.

Each user can securely create, view, update, and delete their own tasks.
The system uses JWT-based authentication to ensure that users can only access their own data.

---

## 🔥 Features

* User Signup & Login
* JWT-based Authentication
* Create, Read, Update, Delete (CRUD) Tasks
* User-specific task isolation
* Pagination support
* Input validation using Pydantic
* Secure password hashing using bcrypt

---

## 🛠 Tech Stack

* Python
* FastAPI
* SQLite
* Pydantic
* Passlib (bcrypt)
* Python-JOSE (JWT)

---

## 📂 Project Structure

```
project/
│
├── api.py              # API routes (entry point)
├── auth.py             # Authentication (signup, login, JWT, hashing)
├── task_manager.py     # Business logic for tasks
├── database.py         # Database queries and connection
├── models.py           # Pydantic models (request/response validation)
```

---

## ⚙️ How It Works

1. User signs up with username and password
2. Password is securely hashed and stored in the database
3. User logs in with credentials
4. Backend verifies password and generates a JWT token
5. Client sends token in the Authorization header
6. Backend decodes token to extract `user_id`
7. All task operations are performed using this `user_id`

---

## 🔐 Authentication Flow

* Login returns a JWT token
* Token must be sent in every request:

```
Authorization: Bearer <token>
```

* Backend:

  * Extracts token
  * Verifies signature
  * Checks expiry
  * Retrieves user identity

---

## 📌 API Endpoints

| Method | Endpoint                  | Description             |
| ------ | ------------------------- | ----------------------- |
| POST   | /signup                   | Register a new user     |
| POST   | /login                    | Login and get JWT token |
| GET    | /tasks                    | Get all tasks for user  |
| POST   | /tasks                    | Create a new task       |
| PATCH  | /tasks/{task_id}/complete | Mark task as completed  |
| DELETE | /tasks/{task_id}          | Delete a task           |

---

## 📥 Example Request

### Login

```
POST /login
{
  "username": "user1",
  "password": "password123"
}
```

### Response

```
{
  "message": "login successfull. ",
  "access_token": "your_jwt_token_here"
}
```

---

### Authorized Request Example

```
DELETE /tasks/1

Headers:
Authorization: Bearer your_jwt_token_here
```

---

## 🧠 Key Concepts Implemented

* Layered Architecture (API → Logic → Database)
* Stateless Authentication using JWT
* Secure Password Hashing
* User-based Data Isolation
* Clean API Design and Structure

---

## 📈 Future Improvements

* Add refresh tokens
* Implement role-based access control
* Switch to PostgreSQL
* Add Docker support
* Deploy to cloud (AWS / Render / Railway)

---

## 🎯 What I Learned

* Designing scalable backend architecture
* Implementing authentication using JWT
* Handling user identity securely
* Structuring APIs for maintainability
* Writing clean and modular code

---

## 🧑‍💻 Author

Built as part of backend development practice to master API design and authentication systems.
