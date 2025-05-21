from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ✅ MySQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql123%40@localhost/flasktodo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 🔗 Connect Flask to the MySQL Database
db = SQLAlchemy(app)

# 📦 Task Model (represents a table in the DB)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    # def __repr__(self):
    #     return f'<Task {self.id}>'

# 🏠 Home route - Show all tasks
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# ➕ Add a task
@app.route('/add', methods=['POST'])
def add():
    task_content = request.form['content']
    new_task = Task(content=task_content)

    try:
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your task.'

# ❌ Delete a task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Problem deleting the task.'

# ✏️ Show Edit Form
@app.route('/edit/<int:id>')
def edit(id):
    task = Task.query.get_or_404(id)
    return render_template('edit.html', task=task)

# ✅ Update Task after Form Submission
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    task = Task.query.get_or_404(id)
    updated_content = request.form['content']

    try:
        task.content = updated_content
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue updating the task.'

# 🚀 Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
