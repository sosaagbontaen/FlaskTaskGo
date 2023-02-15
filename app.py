from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

print("✅APP RUNNING!✅")

@app.route('/')
def index():
    #show each task by querying database
    task_list = Task.query.all()
    print(task_list)
    return render_template("base.html", task_list_param=task_list)

@app.route("/add", methods=["POST"])
def add():
    # add new task
    title = request.form.get("title")
    new_task = Task(title=title, complete = False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:task_id>")
def update(task_id):
    # update task
    task = Task.query.filter_by(id=task_id).first()
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    # delete task
    task = Task.query.filter_by(id=task_id).first()
    task.complete = not task.complete
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        #new_task = Task(title="Task 1", complete=False)
        #db.session.add(new_task)
        #db.session.commit()

    app.run(debug=True)