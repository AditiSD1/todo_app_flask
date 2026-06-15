# My Todo Application

A simple and efficient To-Do list application built with **Flask** and **Bootstrap**. This project helps users manage their daily tasks with a clean, responsive interface.

### 🚀 Live Demo:https://todo-app-fnzd.onrender.com

### 🛠 Tech Stack
* **Framework**: Flask (Python)
* **Database**: PostgreSQL(SQLALchemy ORM)
* **Styling**: CSS,Bootstrap
* **Deployment**: Render

### 📋 Features
* Add new tasks to your list.
* View all current tasks.
* Delete tasks once completed.
* Search functionality:Quickly find specific tasks by searching through your list.
* Responsive design for mobile and desktop.

### ⚙️ How to Run Locally
1. Clone the repository: 
   `git clone https://github.com/AditiSD1/todo_app_flask`
2. Install dependencies:
   `pip install -r requirement.txt`
3. Run the application:
   `python app.py`
4. Access the app at `http://127.0.0.1:5000`

### 💡 Project Highlights
* **CRUD Operations**: Implemented full Create, Read, Update, and Delete functionality to manage task lifecycles effectively.
* **Persistent Storage**: Integrated SQLAlchemy with an PostgreSQL database to ensure user tasks are saved and retrieved reliably.
* **Dynamic Search**: Built a search feature enabling users to filter and locate specific tasks within their list instantly.
* **Modular Architecture**: Structured the application using Flask's template inheritance (base.html), ensuring consistent UI across all pages while reducing code duplication.
* **Production Readiness**: Configured the application with Gunicorn to ensure stable performance and scalability in a production environment.
