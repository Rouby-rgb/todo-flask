from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
TASKS_FILE = 'tasks.json'

# Load tasks from JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

# Save tasks to JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=2)

@app.route('/')
def index():
    tasks = load_tasks()
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', tasks=tasks, current_date=current_date)

@app.route('/add', methods=['POST'])
def add():
    task_text = request.form['task']
    due_date = request.form.get('due_date')
    priority = request.form.get('priority', 'Medium')
    category = request.form.get('category', '')
    description = request.form.get('description', '')

    tasks = load_tasks()
    tasks.append({
        'text': task_text,
        'completed': False,
        'priority': priority,
        'category': category,
        'due_date': due_date,
        'description': description
    })
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
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

@app.route('/clear_completed', methods=['POST'])
def clear_completed():
    tasks = load_tasks()
    tasks = [task for task in tasks if not task.get('completed')]
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    tasks = load_tasks()
    if request.method == 'POST':
        tasks[task_id]['text'] = request.form['task']
        tasks[task_id]['due_date'] = request.form.get('due_date')
        tasks[task_id]['priority'] = request.form.get('priority', 'Medium')
        tasks[task_id]['category'] = request.form.get('category', '')
        tasks[task_id]['description'] = request.form.get('description', '')
        save_tasks(tasks)
        return redirect(url_for('index'))
    else:
        task = tasks[task_id]
        return render_template('edit.html', task=task, task_id=task_id)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
