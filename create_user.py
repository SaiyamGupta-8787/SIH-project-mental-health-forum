# create_users.py
from app import create_app
from extensions import db, bcrypt
from models import User

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
        add_user("Naman", "naman@example.com", "bolabola", role="Student")
        add_user("aadi", "aadi@example.com", "alobalob", role="Counselor")

if __name__ == "__main__":
    main()
