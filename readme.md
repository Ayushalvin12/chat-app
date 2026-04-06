# FastAPI Chat Application

A real-time chat application built with **FastAPI**, featuring **JWT authentication**, **role-based access control (RBAC)**, **WebSocket communication**, and **PostgreSQL persistence**.

---

## Features

- JWT Authentication (Signup & Login)
- Role-Based Access Control (Admin/User)
- Real-time chat using WebSockets
- PostgreSQL database integration with SQLAlchemy 2.0
- Chat rooms with message persistence
- Cursor-based pagination for chat history

---

---

## Environment & Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Auth Endpoints

####  Signup
- Registers a new user
- Hashes password before storing

#### Login
- Verifies credentials
- Returns JWT token
- Token contains:
  - `sub` (username)
  - `role`
  - `exp` (expiration)

---

### RBAC Dependency

Reusable dependency to:
- Restrict routes based on roles
- Example:
  - Admin-only routes
  - User-specific access control

---

## WebSocket Chat

### Endpoint

```
/ws/{room_id}?token=JWT_TOKEN
```

---

### Features

- JWT authentication for WebSocket connection
- Load recent messages (cursor-based pagination)
- Broadcast messages to all users in a room
- Store messages in database

---

## Database Design

### Models

####  User
- id
- username
- hashed_password
- role

#### Room
- id
- name
- description

#### Message
- id
- content
- user_id (FK → User)
- room_id (FK → Room)
- created_at

---

### Relationships

- One **User → Many Messages**
- One **Room → Many Messages**

---

## Database Schema


![Database](app/screenshots/db_schema.png)


---

##  API Testing (Postman)

![Signup Screenshot](app/screenshots/signup.png)
![Login Screenshot](app/screenshots/login.png)
![Create Room](app/screenshots/create_room.png)
![WebSocket Screenshot](app/screenshots/websocket1.png)
![WebSocket Screenshot](app/screenshots/websocket2.png)
![Get Messages](app/screenshots/get_messages.png)
![Get Messages with cursor](app/screenshots/get_messages_with_cursor.png)




## Running the Application

```bash
uvicorn app.main:app --reload
```

---