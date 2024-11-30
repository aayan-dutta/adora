from flask import Flask, request, render_template, redirect, url_for
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client with credentials from environment variables
SUPABASE_URL = os.getenv('https://tughlhxifvsjvntmjsli.supabase.co')
SUPABASE_KEY = os.getenv('postgresql://postgres.tughlhxifvsjvntmjsli:Kayuaayan#081226@aws-0-ap-south-1.pooler.supabase.com:6543/postgres')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

# Define the task table name (you should have this table in Supabase)
TASK_TABLE = 'tasks'

@app.route('/')
def index():
    # Fetch all tasks from the 'tasks' table in Supabase
    response = supabase.table(TASK_TABLE).select("*").execute()
    tasks = response.data if response.status_code == 200 else []
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form.get('task')
    if task_name:
        # Insert new task into Supabase
        response = supabase.table(TASK_TABLE).insert({"name": task_name}).execute()
        # If the insertion is successful, redirect to the index page
        if response.status_code == 201:
            return redirect(url_for('index'))
        else:
            return "Error adding task", 400
    return "No task provided", 400

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    # Delete task from Supabase by its ID
    response = supabase.table(TASK_TABLE).delete().eq('id', task_id).execute()
    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return "Error deleting task", 400

if __name__ == '__main__':
    app.run(debug=True)
