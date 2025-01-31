from datetime import timedelta
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
import wtforms
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import requests
import google.generativeai as gyatt
gyatt.configure(api_key='AIzaSyDyaQmCuP9F9-SqSuwsLT2Mg8j_TDqBXPs')
rizzler = gyatt.GenerativeModel('gemini-1.5-flash')



db = SQLAlchemy()

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.tughlhxifvsjvntmjsli:Kayuaayan#081226@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
app.config['SECRET_KEY'] = 'Ikookayu10'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)


db.init_app(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)  # One-to-Many relationship


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')



@app.route('/')
def home():
    if current_user.is_authenticated:  # Redirect if the user is already logged in
        return redirect(url_for('dashboard'))
    return render_template('home.html')
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/promodormo')
def promodormo():
    return render_template('promodormo.html')



#gemini
@app.route('/ask', methods=['POST'])
def ask():
    huzz = '''You're a 13 year old kid surviving off brainrot on tiktok. You have all
    the knowledge of the world but you can only talk in brainrot. skibidi, sigma, huzz, chill guy,
    bruzz, basically every tiktok slang you can think of. '''
    data = request.json
    

    prompt = data['prompt']
    if prompt:
        response = rizzler.generate_content(huzz+prompt)
        return {'response': response.text} 
    return 'Prompt not found', 404

@app.route('/aiask')
def aiask():
    return render_template('ask.html')



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False)  # Task name
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key


    def __repr__(self):
        return f'<Task {self.name}>'
    

@app.route('/task')
@login_required         
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).all()  # Show only the logged-in user's tasks
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
@login_required
def add_task():
   task_name = request.form.get('task')
   if task_name:
        new_task = Task(name=task_name, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
   return redirect(url_for('index'))




@app.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:  # Check if the task belongs to the current user
        return "Unauthorized", 403
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))




@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__':
    app.run(debug=True)


