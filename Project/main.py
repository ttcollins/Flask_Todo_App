from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from .models import User, Todo
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
   return render_template('profile.html', name=current_user.name)

@main.route('/todolist')
@login_required
def todolist():
    #show all todos
    todo_list = Todo.query.filter_by(user_id = current_user.id)
    return render_template('todo.html', todo_list=todo_list)

@main.route('/add', methods=["POST"])
@login_required
def add():
    #add new item
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False, user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("main.todolist"))

@main.route('/update/<int:todo_id>')
@login_required
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("main.todolist"))

@main.route('/delete/<int:todo_id>')
@login_required
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("main.todolist"))