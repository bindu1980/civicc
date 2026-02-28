# 🏙 CivicConnect – Civic Issue Reporting Platform

CivicConnect is a web-based civic engagement platform that allows citizens to report infrastructure issues and track their resolution transparently.

This project was built using Python (Flask) and SQLite.

---

# 🚀 Problem Statement

Citizens often lack a structured digital platform to report civic issues like potholes, water leaks, or broken streetlights. Complaints remain untracked, reducing transparency and community engagement.

---

# 💡 Our Solution

CivicConnect provides:

- User registration and login
- Role-based access (Admin & User)
- Issue reporting with:
  - Description
  - Category
  - Google Maps location link
  - Image upload
- Upvote system for prioritization
- Admin status tracking (Open → In Progress → Resolved)
- Public announcements board

---

# 🛠 Backend Technologies Used

## 1️⃣ Python
Used for implementing all backend logic and application flow.

## 2️⃣ Flask
A lightweight Python web framework used for:
- Routing (URLs)
- Handling GET and POST requests
- Managing sessions
- Rendering templates

## 3️⃣ SQLite
A file-based relational database used to store:
- Users
- Issues
- Announcements
- Upvotes
- Status updates

## 4️⃣ Session-Based Authentication
Flask sessions are used to:
- Store logged-in user
- Manage roles (admin / user)
- Restrict admin-only features

## 5️⃣ File Handling
Flask's `request.files` is used to upload images.
Images are stored inside:
