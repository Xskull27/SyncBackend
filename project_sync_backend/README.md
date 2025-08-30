⚡ ProjectSync Backend — API for Project & Issue Management

This is the backend service for ProjectSync, a modern bug tracking and project management tool. It provides a high-performance REST API for managing projects, tracking issues, and handling user authentication.

📖 Overview

The backend is built with FastAPI and PostgreSQL (NeonDB), ensuring fast responses, secure authentication, and reliable data management. It powers the ProjectSync frontend and can be extended for integrations with other tools.

✨ Key Features

🔐 User Authentication & Authorization with JWT
📁 Project Management APIs (create, update, delete projects)
🐞 Issue Tracking APIs with status management (Open, In Progress, Completed)
👥 User & Assignment Management
📊 Project Dashboard APIs for summaries
🗄️ Database Migration Support with Alembic




Install dependencies:

pip install -r requirements.txt



▶️ Running the Server

Development

uvicorn app.main:app --reload


Production (Gunicorn + Uvicorn Workers)

gunicorn -k uvicorn.workers.UvicornWorker app.main:app


API will be available at 👉 http://localhost:8000

Interactive API docs:

Swagger UI → /docs

ReDoc → /redoc

🛠️ Tech Stack

FastAPI — Python web framework

SQLModel — ORM for database interaction

Alembic — migrations

PostgreSQL (NeonDB for hosting)

JWT — authentication

🚀 Deployment

Backend: Render

Database: Neon

🤝 Contributing

Contributions are welcome!

Fork the repo

Create a branch

Submit a PR 🚀

💡 This backend powers the ProjectSync frontend, enabling seamless bug tracking and project management.