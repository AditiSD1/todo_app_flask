from asyncio import Task
import os
from flask import Flask, render_template,request,redirect
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime,timezone
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user  
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

db_url = os.environ.get('DATABASE_URL','sqlite:///todo.db')
if db_url and db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)
from flask_migrate import Migrate
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'your_secret_key_here'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def send_email(to_address, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


def send_pending_task_reminders():
    users = User.query.all()
    sent_count = 0
    for user in users:
        pending_tasks = Todo.query.filter_by(user_id=user.id, done=False).all()
        if not pending_tasks:
            continue

        task_list = "\n".join(f"- {t.title}: {t.description}" for t in pending_tasks)
        body = f"Hi {user.username},\n\nYou have {len(pending_tasks)} pending task(s) today:\n\n{task_list}\n\nKeep going!"
        subject = f"You have {len(pending_tasks)} pending task(s) today"

        send_email(user.email, subject, body)
        sent_count += 1
        print(f"Reminder sent to {user.email}")
    return sent_count

@app.route('/toggle/<int:sno>')
@login_required
def toggle_done(sno):
    todo = Todo.query.filter(Todo.sno == sno, Todo.user_id == current_user.id).first_or_404()
    todo.done = not todo.done
    db.session.commit()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return "Username already exists"
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect('/')
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route("/",methods=['GET','POST'])
@login_required
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description, user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
    search_query = request.args.get('query')
    if search_query:
        search_pattern = f"%{search_query}%"
        alltodo = Todo.query.filter(
                Todo.user_id == current_user.id,
                or_(
                    Todo.title.contains(search_pattern),
                    Todo.description.contains(search_pattern)
                )
        ).all()
    else:
        alltodo = Todo.query.filter(Todo.user_id == current_user.id).all()
    return render_template('index.html',alltodo=alltodo)
   # return 'Hello, World!'

@app.route('/show')
def products():
    alltodo = Todo.query.all()
    print(alltodo)
    return 'this is products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
@login_required
def update(sno):
    todo = Todo.query.filter(Todo.sno == sno, Todo.user_id == current_user.id).first_or_404()
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        todo.title = title
        todo.description = description
        db.session.commit()
        return redirect('/')
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
@login_required
def delete(sno):
    todo = Todo.query.filter(Todo.sno == sno, Todo.user_id == current_user.id).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/run-task-reminder')
def run_task_reminder():
    secret = request.args.get('key')
    if secret != os.environ.get('CRON_SECRET'):
        return "Unauthorized", 403
    count = send_pending_task_reminders()
    return f"Reminders sent to {count} users", 200

@app.route('/trigger_email_reminders')
@login_required
def trigger_email_reminders():
    from automation_report import send_pending_task_reminders
    send_pending_task_reminders()
    return "Email reminders triggered!"

# GET all tasks
@app.route('/api/tasks', methods=['GET'])
@login_required
def api_get_tasks():
    tasks = Todo.query.filter(Todo.user_id == current_user.id).all()
    return jsonify(
        {"id": t.sno, "title": t.title, "description": t.description, "done": t.done}
        for t in tasks
    )

# GET single task
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
@login_required
def api_get_task(task_id):
    task = Todo.query.filter(Todo.sno == task_id, Todo.user_id == current_user.id).first_or_404()
    return jsonify({"id": task.sno, "title": task.title, "description": task.description, "done": task.done})

# POST - create a task
@app.route('/api/tasks', methods=['POST'])
@login_required
def api_create_task():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({"error": "Title is required"}), 400
    new_task = Todo(title=data['title'], description=data.get('description', ''), user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.sno, "title": new_task.title}), 201

# PUT - update a task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def api_update_task(task_id):
    task = Todo.query.filter(Todo.sno == task_id, Todo.user_id == current_user.id).first_or_404()
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.done = data.get('done', task.done)
    db.session.commit()
    return jsonify({"message": "Task updated"})

# DELETE
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def api_delete_task(task_id):
    task = Todo.query.filter(Todo.sno == task_id, Todo.user_id == current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200

with app.app_context():
    db.create_all()

if __name__ =="__main__":
    app.run(debug=False) 