# My Todo Application

A simple and efficient To-Do list application built with **Flask** and **Bootstrap**. This project helps users manage their daily tasks with a clean, responsive interface — now with user authentication, a REST API, automated email reminders, and safe production database migrations.

### 🚀 Live Demo: https://todo-app-fnzd.onrender.com

### 🛠 Tech Stack
* **Framework**: Flask (Python)
* **Database**: PostgreSQL (SQLAlchemy ORM)
* **Migrations**: Flask-Migrate (Alembic)
* **Authentication**: Flask-Login, Werkzeug password hashing
* **Styling**: CSS, Bootstrap
* **Deployment**: Render (Gunicorn)
* **Automation**: Gmail SMTP, cron-job.org

### 📋 Features
* User signup/login with secure password hashing and per-user task scoping
* Add new tasks to your list
* View all current tasks
* Update and delete tasks
* Search functionality: Quickly find specific tasks by searching through your list
* Mark tasks as done via checkbox toggle
* REST API (GET, POST, PUT, DELETE) for programmatic task management
* Automated email reminders for pending tasks, sent via Gmail SMTP on a scheduled cron trigger
* Responsive design for mobile and desktop

### ⚙ How to Run Locally
1. Clone the repository:
   `git clone https://github.com/AditiSD1/todo_app_flask`
2. Install dependencies:
   `pip install -r requirement.txt`
3. Create a `.env` file with:
   ```
   DATABASE_URL=sqlite:///todo.db
   SECRET_KEY=your_secret_key_here
   EMAIL_ADDRESS=your_gmail_address
   EMAIL_PASSWORD=your_gmail_app_password
   CRON_SECRET=your_cron_secret
   ```
4. Apply database migrations:
   `flask db upgrade`
5. Run the application:
   `python app.py`
6. Access the app at `http://127.0.0.1:5000`

### 🔌 REST API Endpoints
| Method | Endpoint          | Description              |
|--------|-------------------|---------------------------|
| GET    | `/api/todos`      | List all tasks for user  |
| POST   | `/api/todos`      | Create a new task        |
| PUT    | `/api/todos/<id>` | Update an existing task  |
| DELETE | `/api/todos/<id>` | Delete a task            |

### 💡 Project Highlights
* **CRUD Operations**: Implemented full Create, Read, Update, and Delete functionality to manage task lifecycles effectively.
* **Persistent Storage**: Integrated SQLAlchemy with a PostgreSQL database to ensure user tasks are saved and retrieved reliably.
* **User Authentication**: Added secure signup/login with Flask-Login and per-user task scoping so each user only sees their own tasks.
* **REST API Layer**: Built full CRUD REST endpoints to support programmatic access and integration with other tools.
* **Automated Reminders**: Built a standalone automation script and a production-safe cron endpoint to send email reminders for pending tasks on a schedule.
* **Safe Schema Migrations**: Set up Flask-Migrate (Alembic) to manage production database schema changes without data loss, and wired migrations into the deploy process so they run automatically.
* **Dynamic Search**: Built a search feature enabling users to filter and locate specific tasks within their list instantly.
* **Modular Architecture**: Structured the application using Flask's template inheritance (base.html), ensuring consistent UI across all pages while reducing code duplication.
* **Production Readiness**: Configured the application with Gunicorn to ensure stable performance and scalability in a production environment.
