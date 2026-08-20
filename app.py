from cs50 import SQL
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

db = SQL("sqlite:///todo.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            db.execute("INSERT INTO todos (task) VALUES(?)", task)
        return redirect("/")
    else:
        todos = db.execute("SELECT * FROM todos ORDER BY created DESC")
        return render_template("index.html", todos=todos)

@app.route("/complete/<int:id>")
def complete(id):
    db.execute("UPDATE todos SET done = 1 WHERE id = ?", id)
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    db.execute("DELETE FROM todos WHERE id = ?", id)
    return redirect("/")