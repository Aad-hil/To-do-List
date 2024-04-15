from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms import Form, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///To-Do.db'  # SQLite database
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)


class ReusableForm(Form):
    name = StringField('Task Name:', validators=[DataRequired()])
    Priority = SelectField('Priority', choices=['high', 'medium', 'low'], validators=[DataRequired()])
    Submit = SubmitField('Add task')


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.String(), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    high_priority_tasks = Todo.query.filter_by(priority='high').all()
    medium_priority_tasks = Todo.query.filter_by(priority='medium').all()
    low_priority_tasks = Todo.query.filter_by(priority='low').all()
    tasks = high_priority_tasks + medium_priority_tasks + low_priority_tasks
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['GET', 'POST'])
def add_todo():
    form = ReusableForm(request.form)
    if request.method == 'POST':
        name = request.form['taskName']
        priority = request.form['priority']
        time = str(datetime.now().date())
        new_task = Todo(task_name=name, priority=priority, created_at=time)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully')
        return redirect(url_for('index'))
    return render_template('task.html', form=form)


@app.route('/finish/<int:task_id>', methods=['POST'])
def finish_task(task_id):
    task_to_delete = Todo.query.get_or_404(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    flash('Task finished successfully')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
