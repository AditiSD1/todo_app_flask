from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
  
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
if __name__ =="__main__":
    app.run(debug=True) 