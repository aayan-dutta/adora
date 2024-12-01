from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.tughlhxifvsjvntmjsli:Kayuaayan#081226@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

db.init_app(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Task {self.name}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks= Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
   task_name = request.form.get('task')
   if task_name:
        new_task = Task(name=task_name)
        db.session.add(new_task)
        db.session.commit()
   return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__':
    app.run(debug=True)