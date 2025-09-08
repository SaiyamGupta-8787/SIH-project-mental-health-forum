from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

# App factory
def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///dev.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import models inside app context
    with app.app_context():
        try:
            import models
        except Exception as e:
            app.logger.exception("Error importing models: %s", e)

    # Routes
    @app.route('/')
    def index():
        return render_template('index.html')
    # Login Page
    @app.route('/login.html')
    def login():
        return render_template('login.html')

    @app.route('/registration.html', methods=['GET'])
    def register_page():
        return render_template('registration.html')

    @app.route('/registration.html', methods=['POST'])
    def register_user():
        from models import User
        try:
            # Accept JSON from JS
            data = request.get_json()
            if not data:
                return jsonify({"error": "No input data provided"}), 400

            name = data.get('name')
            email = data.get('email')
            password = data.get('password')

            if not name or not email or not password:
                return jsonify({"error": "All fields are required"}), 400

            if User.query.filter_by(email=email).first():
                return jsonify({"error": "User already exists"}), 400

            # Hash password and create user
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(name=name, email=email, password_hash=password_hash)
            db.session.add(user)
            db.session.commit()

            return jsonify({"message": f"User {name} registered successfully!"}), 201

        except Exception as e:
            app.logger.exception("Error in /register POST: %s", e)
            return jsonify({"error": "Server error"}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
