# create_users.py
from app import create_app, db, bcrypt
from models import User
from flask import request
from werkzeug.security import generate_password_hash

def add_user(name, email, password, role='Student'):
    existing = User.query.filter_by(email=email).first()
    if existing:
        print(f"User already exists: {email} (id={existing.id})")
        return existing
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    u = User(name=name, email=email, password_hash=pw_hash, role=role)
    db.session.add(u)
    db.session.commit()
    print(f"Created user: {name} <{email}> id={u.id}")
    return u

def main():
    app = create_app()
    with app.app_context():
        add_user("Naman", "Naman@email.com", "bolabola", role="Student")
        add_user("aadi", "aadi@email.com", "alobalob", role="Counselor")

if __name__ == "__main__":
    main()
