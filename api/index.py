from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

tasks=[]

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        task.append(task)
    return redirect(url_for('index'))

@app.route('/delete/<inte:task_id>', methods = ['POST'])
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)