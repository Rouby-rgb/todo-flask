from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)
TASKS_FILE = 'tasks.json'

# Inject current datetime into Jinja templates
@app.context_processor
def inject_now():
    return {'now': datetime.now}

# Load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_text = request.form['task']
    due_date = request.form['due_date']
    priority = request.form['priority']
    category = request.form['category']
    tasks = load_tasks()
    tasks.append({
        'text': task_text,
        'completed': False,
        'priority': priority,
        'category': category,
        'due_date': due_date
    })
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/clear-completed', methods=['POST'])
def clear_completed():
    tasks = load_tasks()
    tasks = [task for task in tasks if not task['completed']]
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    tasks = load_tasks()
    if request.method == 'POST':
        if 0 <= task_id < len(tasks):
            tasks[task_id]['text'] = request.form['task']
            tasks[task_id]['priority'] = request.form['priority']
            tasks[task_id]['category'] = request.form['category']
            tasks[task_id]['due_date'] = request.form['due_date']
            save_tasks(tasks)
        return redirect(url_for('index'))
    else:
        if 0 <= task_id < len(tasks):
            task = tasks[task_id]
            return render_template('edit.html', task=task, task_id=task_id)
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5003)
