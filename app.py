from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
TASKS_FILE = 'tasks.json'

# 🔄 Load tasks
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

# 💾 Save tasks
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    deadline = request.form.get('deadline')
    category = request.form.get('category')
    
    new_task = {
        "title": title,
        "done": False,
        "deadline": deadline.strip(),
        "category": category.strip().lower()
    }

    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)
    return redirect('/')

@app.route('/done/<int:index>')
def mark_done(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]['done'] = True
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
