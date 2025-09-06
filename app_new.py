from flask import Flask, render_template, redirect, url_for, session, flash, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySql configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydatabase'
app.secret_key = 'your_secret_key_here'

mysql = MySQL(app)

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")
    
    def validate_email(self, field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError('Email already taken')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('index'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        else:
            flash("Login failed. Please check your email and password")
            return redirect(url_for('login'))
    
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            return render_template('index.html', user=user)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out successfully.")
    return redirect(url_for("login"))

### ✅ YOUR ADDED ROUTES BELOW ✅

# Route to submit a new mood entry
@app.route('/add_mood', methods=['POST'])
def add_mood():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    user_id = session['user_id']
    data = request.get_json()
    mood = data.get('mood')
    
    if not mood:
        return jsonify({'status': 'error', 'message': 'Mood is required'}), 400
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO moods (user_id, mood) VALUES (%s, %s)", (user_id, mood))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'status': 'success', 'message': 'Mood added successfully'})

# Route to get all moods for the logged-in user
@app.route('/get_moods', methods=['GET'])
def get_moods():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    user_id = session['user_id']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, mood FROM moods WHERE user_id=%s ORDER BY id DESC", (user_id,))
    moods = cursor.fetchall()
    cursor.close()
    
    return jsonify({'status': 'success', 'moods': moods})

# Route to submit a new peer post
@app.route('/add_peer_post', methods=['POST'])
def add_peer_post():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    user_id = session['user_id']
    data = request.get_json()
    content = data.get('content')
    
    if not content:
        return jsonify({'status': 'error', 'message': 'Content is required'}), 400
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO peer_posts (user_id, content) VALUES (%s, %s)", (user_id, content))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'status': 'success', 'message': 'Peer post added successfully'})

# Route to get all peer posts
@app.route('/get_peer_posts', methods=['GET'])
def get_peer_posts():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT peer_posts.id, users.name, peer_posts.content
        FROM peer_posts
        JOIN users ON peer_posts.user_id = users.id
        ORDER BY peer_posts.id DESC
    """)
    posts = cursor.fetchall()
    cursor.close()
    
    return jsonify({'status': 'success', 'posts': posts})

### ✅ END OF YOUR ADDED ROUTES ✅

if __name__ == '__main__':
    app.run(debug=True)
