from flask import Flask, request, redirect, render_template 
from flask_sqlalchemy import SQLAlchemy


# app and database setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(60))
	status = db.Column(db.Boolean, default=False)


# CRUD Operations: Create, Retrieve, Update Delete

# Create
@app.route('/add', methods=['POST'])
def add():
	title = request.form.get('title')
	todo = Todo(title=title)
	db.session.add(todo)
	db.session.commit()
	return redirect('/')


# Retrieve
@app.route('/')
def index():
	todo_list = Todo.query.all()
	count = Todo.query.filter_by(status=False).count()
	print(count)
	return render_template('index.html', todo_list=todo_list, count=count)


# Update
@app.route('/update/<int:todo_id>')
def update(todo_id):
	todo = Todo.query.filter_by(id=todo_id).first()
	todo.status = not todo.status
	db.session.add(todo)
	db.session.commit()
	return redirect('/')


# Delete
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
	todo = Todo.query.filter_by(id=todo_id).first()
	db.session.delete(todo)
	db.session.commit()
	return redirect('/')
