# ProjectSync 

This is the **frontend application** for a bug tracking system, designed to help manage projects and issues efficiently.

---

## 📄 Description

This project provides a user-friendly interface for tracking bugs, managing projects, and collaborating with team members. Streamline your development workflow and manage your team’s projects and issues more efficiently with our powerful tool.

---

## 🚀 Features (Conceptual)

* User authentication and authorization
* Project creation and management
* Issue tracking with status updates (`Open`, `In Progress`, `Completed`)
* Assignment of issues to team members
* Dashboard view for project summaries
* Responsive design for various devices

---

## ⚙️ Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd bug-tracker-frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables:**
   Create a `.env.local` file in the root directory and add any necessary environment variables, such as API endpoints.

---

## ▶️ Usage

### 🔗 Live:

[https://projectsync-alpha.vercel.app/](https://projectsync-alpha.vercel.app/)

### 🖥️ Local Development:

To run the development server locally:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `src/app/page.js`. The page auto-updates as you edit the file.

---

## 🧱 Technologies Used

### 📦 Frontend

* **Next.js**: A React framework for building fast web applications.
* **React**: A JavaScript library for building user interfaces.
* **Tailwind CSS**: A utility-first CSS framework for rapid UI development.
* **Shadcn/ui**: A collection of re-usable components built with Radix UI and Tailwind CSS.
* **Axios**: A promise-based HTTP client for making API requests.
* **react-hook-form**: For flexible and extensible forms with easy-to-use validation.
* **Zod**: A TypeScript-first schema declaration and validation library.

### 🧠 Backend

* **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
* **Python**: The programming language used for the backend.
* **Alembic**: A lightweight database migration tool for usage with the SQLAlchemy Database Toolkit.
* **SQLModel**: A library for interacting with SQL databases, designed to be easy to use and compatible with FastAPI.
* **JWT (JSON Web Tokens)**: For secure authentication.

### 💄 Database

* **NeonDB**: A serverless PostgreSQL.
* **PostgreSQL**: A powerful, open-source object-relational database system.

---

## 🚀 Deployment

* **Frontend**: [Vercel](https://vercel.com)

* **Backend**: [Render](https://render.com)
