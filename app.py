from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from sqlalchemy import desc
import os
import uuid

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import Todo


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/todo/<todo_id>")
def todo_view(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        return render_template("todo.html", todo=todo)


@app.get("/todo/<todo_id>/edit")
def edit_todo_view(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        return render_template("edit-todo.html", todo=todo)


@app.post("/api/todo")
def add_todo():
    todo = Todo(id=str(uuid.uuid4()), title=request.form["title"])
    db.session.add(todo)
    db.session.commit()
    return render_template("new-todo.html", todo=todo)


@app.get("/api/todos")
def get_todos():
    todos = db.session.execute(
        db.select(Todo).order_by(desc(Todo.created_at))
    ).scalars()
    return render_template("todos.html", todos=todos)


@app.put("/api/todo/<todo_id>")
def edit_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        todo.completed = request.form.get("completed") == "on"
        if "title" in request.form:
            todo.title = request.form["title"]
        db.session.commit()
        return render_template("todo.html", todo=todo)


@app.delete("/api/todo/<todo_id>")
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return ""
