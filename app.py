from asyncio import Task
import os
from flask import Flask, render_template,request,redirect
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime,timezone
app = Flask(__name__)

db_url = os.environ.get('DATABASE_URL','sqlite:///todo.db')
if db_url and db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
  
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
    search_query = request.args.get('query')
    if search_query:
        search_pattern = f"%{search_query}%"
        alltodo = Todo.query.filter(
            or_(
            Todo.title.contains(search_pattern),
            Todo.description.contains(search_pattern)
                   )                 ).all()
    else:
        alltodo = Todo.query.all()
    return render_template('index.html',alltodo=alltodo)
   # return 'Hello, World!'

@app.route('/show')
def products():
    alltodo = Todo.query.all()
    print(alltodo)
    return 'this is products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.get(sno)
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.get(sno)
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.get(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

# GET all tasks
@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    tasks = Todo.query.all()
    return jsonify([
        {"id": t.id, "title": t.title, "description": t.description, "done": t.done}
        for t in tasks
    ])

# GET single task
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def api_get_task(task_id):
    task = Todo.query.get_or_404(task_id)
    return jsonify({"id": task.id, "title": task.title, "description": task.description, "done": task.done})

# POST - create a task
@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({"error": "Title is required"}), 400
    new_task = Todo(title=data['title'], description=data.get('description', ''))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "title": new_task.title}), 201

# PUT - update a task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    task = Todo.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.done = data.get('done', task.done)
    db.session.commit()
    return jsonify({"message": "Task updated"})

# DELETE
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200

if __name__ =="__main__":
    app.run(debug=False) 