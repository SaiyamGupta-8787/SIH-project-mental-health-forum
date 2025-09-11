from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from models import User
from extensions import db, migrate, bcrypt, jwt
from app_text import TEXTS, TEXTS_HI  # import both text sets

# Load .env
load_dotenv()


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

    # Routes/endpoitns

    @app.route('/')
    def index():
        lang = request.args.get('lang', 'en')  # default English
        texts = TEXTS_HI if lang == 'hi' else TEXTS
        return render_template('index.html', texts=texts)

    # ----------------- LOGIN ----------------- #
    @app.route('/login', methods=['GET'])
    def login_page():
        lang = request.args.get('lang', 'en')
        texts = TEXTS_HI if lang == 'hi' else TEXTS
        return render_template('login.html', texts=texts)

    @app.route('/login', methods=['POST'])
    def login():
        role = request.form.get('role', 'Student').strip()
        anonymous = request.form.get('anonymous') in ('true', '1', 'on', 'yes')

        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        username = (request.form.get('name') or '').strip() if not anonymous else None

        # Anonymous student login → only email + password
        if role == "Student" and anonymous:
            if not email or not password:
                flash("Email and password are required for anonymous login", "error")
                return redirect(url_for('login_page'))

            user = User.query.filter_by(email=email, anonymous=True).first()

        else:
            # Non-anon login → username + email + password
            if not username or not email or not password:
                flash("Username, email, and password are required", "error")
                return redirect(url_for('login_page'))

            user = User.query.filter_by(name=username, email=email, anonymous=False).first()

        # Verify user
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            flash("Invalid credentials", "error")
            return redirect(url_for('login_page'))

        # Update session
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['role'] = user.role
        session['anonymous'] = user.anonymous

        flash("Successfully logged in!", "success")
        return redirect(url_for('welcome'))

#Welcome
    @app.route('/welcome')
    def welcome():
        if 'user_name' not in session:
            flash("Please log in first", "error")
            return redirect(url_for('login_page'))

        lang = request.args.get('lang', 'en')
        texts = TEXTS_HI if lang == 'hi' else TEXTS
        return render_template('index.html', texts=texts)

    # LOGOUT
    # LOGOUT
    @app.route('/logout')
    def logout():
        session.clear()
        flash("You have been logged out", "success")
        return redirect(url_for('login_page'))



    # REGISTER
    @app.route('/register', methods=['GET'])
    def register_page():
        lang = request.args.get('lang', 'en')
        texts = TEXTS_HI if lang == 'hi' else TEXTS
        return render_template('registration.html', texts=texts)
    
    @app.route('/register', methods=['POST'])
    def register():
        try:
            # Accept JSON or form data
            data = request.get_json() if request.is_json else request.form.to_dict()
            name = (data.get('name') or '').strip()
            email = (data.get('email') or '').strip().lower()
            password = data.get('password') or ''
            role = (data.get('role') or 'Student').strip()
            anon_val = data.get('anonymous', False)
            anonymous = str(anon_val).lower() in ('true', '1', 'on', 'yes')

            import re, random, string

            # Validate role
            if role not in ('Student', 'Counselor', 'Admin'):
                role = 'Student'

            # Anonymous only allowed for Students
            if role != 'Student':
                anonymous = False

            # If student chooses anonymous, generate placeholder name if empty
            if role == 'Student' and anonymous:
                if not name:
                    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                    name = f"Anonymous_{suffix}"
            else:
                # Validate username
                if not name or not re.match(r'^[A-Za-z0-9_.-]{3,30}$', name):
                    return jsonify({
                        "error": "Invalid username. 3-30 chars, letters, numbers, underscore/dot/hyphen."
                    }), 400

            # Validate email
            if not email or not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
                return jsonify({"error": "Invalid email address."}), 400

            # Validate password (min 8 chars, at least one number)
            if not password or not re.match(r'^(?=.*[A-Za-z])(?=.*\d).{8,}$', password):
                return jsonify({
                    "error": "Password must be at least 8 characters and contain at least one number."
                }), 400

            # Check duplicate email
            if User.query.filter_by(email=email).first():
                return jsonify({"error": "A user with that email already exists."}), 400

            # Hash password
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

            # Create user
            user = User(
                name=name,
                email=email,
                password_hash=password_hash,
                role=role,
                anonymous=anonymous
            )

            db.session.add(user)
            db.session.commit()

            return jsonify({"message": f"User {name} registered successfully!"}), 201

        except Exception as e:
            try:
                db.session.rollback()
            except Exception:
                pass
            print("Register error:", e)
            return jsonify({"error": "Internal server error"}), 500
    # making user profile routes
        # ----------------- PROFILES ----------------- #
    def _get_current_user():
        """Helper: returns User object for logged-in user or None."""
        uid = session.get('user_id')
        if not uid:
            return None
        return User.query.get(uid)

    @app.route('/profile')
    def my_profile():
        """Redirect to logged-in user's profile or to login if not logged in."""
        user = _get_current_user()
        if not user:
            flash("Please log in to view your profile", "error")
            return redirect(url_for('login_page'))
        return redirect(url_for('view_profile', user_id=user.id))

    @app.route('/profile/<int:user_id>')
    def view_profile(user_id):
        """
        Public profile view.
        If the profile owner prefers anonymity and the viewer is not the owner or admin,
        show anonymized name.
        """
        viewer = _get_current_user()
        owner = User.query.get_or_404(user_id)

        # load or create UserProfile lazy (if model exists)
        profile = getattr(owner, 'profile', None)
        if profile is None:
            # If no profile row exists yet, create a lightweight object for template use
            profile = None

        # Decide displayed name
        display_name = owner.name
        # if owner prefers anonymous (profile.prefers_anonymous True) and viewer is not owner and viewer not admin:
        prefers_anon = False
        if profile is not None:
            prefers_anon = bool(getattr(profile, 'prefers_anonymous', False))
        if prefers_anon and (viewer is None or viewer.id != owner.id) and viewer and viewer.role != 'Admin':
            # hide identity for non-owner non-admin viewers
            display_name = "Anonymous"

        return render_template('profile.html', owner=owner, profile=profile, display_name=display_name, viewer=viewer)

    @app.route('/profile/edit', methods=['GET', 'POST'])
    def edit_profile():
        """
        Edit current user's profile. Fields:
        - name (only if not preferring anonymous)
        - college
        - year_of_study
        - prefers_anonymous (bool)
        - language_pref
        """
        user = _get_current_user()
        if not user:
            flash("Please log in to edit your profile", "error")
            return redirect(url_for('login_page'))

        # Ensure profile row exists
        profile = getattr(user, 'profile', None)
        if profile is None:
            # create a profile row if not present
            from models import UserProfile
            profile = UserProfile(user_id=user.id)
            db.session.add(profile)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                # if commit fails, continue but keep profile as None for safety
                profile = getattr(user, 'profile', None)

        if request.method == 'GET':
            return render_template('edit_profile.html', user=user, profile=profile)

        # POST: save changes
        data = request.form.to_dict()
        name = (data.get('name') or '').strip()
        college = (data.get('college') or '').strip() or None
        year_of_study = (data.get('year_of_study') or '').strip() or None
        prefers_anonymous = bool(request.form.get('prefers_anonymous'))
        language_pref = (data.get('language_pref') or 'en').strip()

        # Business rule: if user chooses to prefer anonymous, we can leave stored name as-is,
        # but if they disable anonymous and provide a new name, validate it.
        import re
        if not prefers_anonymous:
            if not name or not re.match(r'^[A-Za-z0-9_.-]{3,30}$', name):
                flash("Invalid username. Use 3-30 chars: letters, numbers, underscore/dot/hyphen.", "error")
                return redirect(url_for('edit_profile'))
            # update user.name only if changed
            user.name = name

        # update profile fields
        if profile is None:
            # try to create if still None
            from models import UserProfile
            profile = UserProfile(user_id=user.id, college=college, year_of_study=year_of_study,
                                  prefers_anonymous=prefers_anonymous, language_pref=language_pref)
            db.session.add(profile)
        else:
            profile.college = college
            profile.year_of_study = year_of_study
            profile.prefers_anonymous = prefers_anonymous
            profile.language_pref = language_pref

        try:
            db.session.commit()
            flash("Profile updated successfully.", "success")
            return redirect(url_for('view_profile', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            print("Profile save error:", e)
            flash("Could not save profile. Try again.", "error")
            return redirect(url_for('edit_profile'))
        #RESOURCES
    @app.route('/resources', methods=['GET', 'POST'])
    def resources():
        """List resources; create new resource (Counselor/Admin)."""
        uid = session.get('user_id')
        viewer = User.query.get(uid) if uid else None

        if request.method == 'POST':
            # create new resource
            if not viewer:
                flash("Please log in to add resources.", "error")
                return redirect(url_for('resources'))
            if viewer.role not in ('Counselor', 'Admin'):
                flash("Only Counselors or Admins can add resources.", "error")
                return redirect(url_for('resources'))

            title = (request.form.get('title') or '').strip()
            rtype = (request.form.get('type') or 'article').strip()
            url_val = (request.form.get('url') or '').strip()
            language = (request.form.get('language') or 'en').strip()
            description = (request.form.get('description') or '').strip() or None

            if not title or len(title) < 3:
                flash("Title must be at least 3 characters.", "error")
                return redirect(url_for('resources'))
            if rtype not in ('article','audio','video','other'):
                rtype = 'article'
            if not url_val or (not url_val.startswith('http://') and not url_val.startswith('https://')):
                flash("Please provide a valid URL (starting with http:// or https://).", "error")
                return redirect(url_for('resources'))

            from models import Resource
            res = Resource(title=title, type=rtype, url=url_val, language=language,
                           description=description, creator_id=viewer.id)
            db.session.add(res)
            try:
                db.session.commit()
                flash("Resource added.", "success")
                return redirect(url_for('resources', view=res.id))
            except Exception as e:
                db.session.rollback()
                print("Resource create error:", e)
                flash("Could not save resource.", "error")
                return redirect(url_for('resources'))

        # GET: list
        from models import Resource
        resources_q = Resource.query.order_by(Resource.created_at.desc()).all()
        view_id = request.args.get('view', type=int)
        resource_obj = Resource.query.get(view_id) if view_id else None
        return render_template('resources.html', resources=resources_q, viewer=viewer, resource_obj=resource_obj)

    @app.route('/resources/edit/<int:resource_id>', methods=['GET', 'POST'])
    def resource_edit(resource_id):
        """Edit resource: only creator or Admin allowed."""
        uid = session.get('user_id')
        viewer = User.query.get(uid) if uid else None
        from models import Resource
        res = Resource.query.get_or_404(resource_id)

        # permission check
        allowed = viewer and (viewer.role == 'Admin' or viewer.id == res.creator_id)
        if not allowed:
            flash("You are not authorized to edit this resource.", "error")
            return redirect(url_for('resources', view=res.id))

        if request.method == 'GET':
            return render_template('resource_edit.html', resource=res, viewer=viewer)

        # POST: save changes
        title = (request.form.get('title') or '').strip()
        rtype = (request.form.get('type') or 'article').strip()
        url_val = (request.form.get('url') or '').strip()
        language = (request.form.get('language') or 'en').strip()
        description = (request.form.get('description') or '').strip() or None

        if not title or len(title) < 3:
            flash("Title must be at least 3 characters.", "error")
            return redirect(url_for('resource_edit', resource_id=res.id))
        if rtype not in ('article','audio','video','other'):
            rtype = 'article'
        if not url_val or (not url_val.startswith('http://') and not url_val.startswith('https://')):
            flash("Please provide a valid URL (starting with http:// or https://).", "error")
            return redirect(url_for('resource_edit', resource_id=res.id))

        res.title = title
        res.type = rtype
        res.url = url_val
        res.language = language
        res.description = description

        try:
            db.session.commit()
            flash("Resource updated.", "success")
            return redirect(url_for('resources', view=res.id))
        except Exception as e:
            db.session.rollback()
            print("Resource update error:", e)
            flash("Could not update resource.", "error")
            return redirect(url_for('resource_edit', resource_id=res.id))

    @app.route('/resources/delete/<int:resource_id>', methods=['POST'])
    def resource_delete(resource_id):
        """Delete resource: only creator or Admin allowed."""
        uid = session.get('user_id')
        viewer = User.query.get(uid) if uid else None
        from models import Resource
        res = Resource.query.get_or_404(resource_id)

        allowed = viewer and (viewer.role == 'Admin' or viewer.id == res.creator_id)
        if not allowed:
            flash("You are not authorized to delete this resource.", "error")
            return redirect(url_for('resources', view=res.id))

        try:
            db.session.delete(res)
            db.session.commit()
            flash("Resource deleted.", "success")
            return redirect(url_for('resources'))
        except Exception as e:
            db.session.rollback()
            print("Resource delete error:", e)
            flash("Could not delete resource.", "error")
            return redirect(url_for('resources', view=res.id))


    # ----------------- LIST USERS ----------------- #
    @app.route('/users')
    def list_users():
        users = User.query.all()
        return jsonify([
            {"id": u.id, "name": u.name, "email": u.email, "role": getattr(u, 'role', None)}
            for u in users
        ])
    

        # ----------------- THREADS & POSTS (MVP) ----------------- #
    def _get_current_user():
        uid = session.get('user_id')
        return User.query.get(uid) if uid else None

    #Threads and posts route
    @app.route('/threads', methods=['GET', 'POST'])
    def threads():
        """
        GET: list threads
        POST: create thread (must be logged in)
        """
        viewer = _get_current_user()

        if request.method == 'POST':
            if not viewer:
                flash("Please log in to create a thread.", "error")
                return redirect(url_for('login_page'))

            title = (request.form.get('title') or '').strip()
            if not title or len(title) < 3:
                flash("Thread title must be at least 3 characters.", "error")
                return redirect(url_for('threads'))

            from models import Thread
            t = Thread(title=title, creator_id=viewer.id)
            db.session.add(t)
            try:
                db.session.commit()
                flash("Thread created.", "success")
                return redirect(url_for('thread_view', thread_id=t.id))
            except Exception as e:
                db.session.rollback()
                print("Thread create error:", e)
                flash("Could not create thread.", "error")
                return redirect(url_for('threads'))

        # GET
        from models import Thread
        q = Thread.query.order_by(Thread.is_pinned.desc(), Thread.created_at.desc()).all()
        return render_template('threads.html', threads=q, viewer=viewer)

    @app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
    def thread_view(thread_id):
        """
        GET: show thread + posts
        POST: add a reply (must be logged in)
        """
        viewer = _get_current_user()
        from models import Thread, Post
        thread = Thread.query.get_or_404(thread_id)

        if request.method == 'POST':
            if not viewer:
                flash("Please log in to post a reply.", "error")
                return redirect(url_for('login_page'))

            content = (request.form.get('content') or '').strip()
            if not content or len(content) < 2:
                flash("Post content is too short.", "error")
                return redirect(url_for('thread_view', thread_id=thread_id))

            p = Post(thread_id=thread.id, author_id=viewer.id, content=content)
            db.session.add(p)
            try:
                db.session.commit()
                flash("Reply posted.", "success")
                return redirect(url_for('thread_view', thread_id=thread.id))
            except Exception as e:
                db.session.rollback()
                print("Post create error:", e)
                flash("Could not post reply.", "error")
                return redirect(url_for('thread_view', thread_id=thread.id))

        # GET
        posts = Post.query.filter_by(thread_id=thread.id, is_hidden=False).order_by(Post.created_at.asc()).all()
        return render_template('thread_view.html', thread=thread, posts=posts, viewer=viewer)

    @app.route('/thread/<int:thread_id>/edit', methods=['GET', 'POST'])
    def thread_edit(thread_id):
        viewer = _get_current_user()
        from models import Thread
        thread = Thread.query.get_or_404(thread_id)

        allowed = viewer and (viewer.role == 'Admin' or viewer.id == thread.creator_id)
        if not allowed:
            flash("Not authorized to edit this thread.", "error")
            return redirect(url_for('thread_view', thread_id=thread.id))

        if request.method == 'GET':
            return render_template('thread_edit.html', thread=thread, viewer=viewer)

        # POST: save
        title = (request.form.get('title') or '').strip()
        if not title or len(title) < 3:
            flash("Thread title must be at least 3 characters.", "error")
            return redirect(url_for('thread_edit', thread_id=thread.id))

        thread.title = title
        try:
            db.session.commit()
            flash("Thread updated.", "success")
            return redirect(url_for('thread_view', thread_id=thread.id))
        except Exception as e:
            db.session.rollback()
            print("Thread update error:", e)
            flash("Could not update thread.", "error")
            return redirect(url_for('thread_edit', thread_id=thread.id))

    @app.route('/thread/<int:thread_id>/delete', methods=['POST'])
    def thread_delete(thread_id):
        viewer = _get_current_user()
        from models import Thread
        thread = Thread.query.get_or_404(thread_id)

        allowed = viewer and (viewer.role == 'Admin' or viewer.id == thread.creator_id)
        if not allowed:
            flash("Not authorized to delete this thread.", "error")
            return redirect(url_for('thread_view', thread_id=thread.id))

        try:
            db.session.delete(thread)
            db.session.commit()
            flash("Thread deleted.", "success")
            return redirect(url_for('threads'))
        except Exception as e:
            db.session.rollback()
            print("Thread delete error:", e)
            flash("Could not delete thread.", "error")
            return redirect(url_for('thread_view', thread_id=thread.id))

    @app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
    def post_edit(post_id):
        viewer = _get_current_user()
        from models import Post
        post = Post.query.get_or_404(post_id)

        allowed = viewer and (viewer.role == 'Admin' or viewer.id == post.author_id)
        if not allowed:
            flash("Not authorized to edit this post.", "error")
            return redirect(url_for('thread_view', thread_id=post.thread_id))

        if request.method == 'GET':
            return render_template('post_edit.html', post=post, viewer=viewer)

        content = (request.form.get('content') or '').strip()
        if not content or len(content) < 2:
            flash("Post content is too short.", "error")
            return redirect(url_for('post_edit', post_id=post.id))

        post.content = content
        try:
            db.session.commit()
            flash("Post updated.", "success")
            return redirect(url_for('thread_view', thread_id=post.thread_id))
        except Exception as e:
            db.session.rollback()
            print("Post update error:", e)
            flash("Could not update post.", "error")
            return redirect(url_for('post_edit', post_id=post.id))

    @app.route('/post/<int:post_id>/delete', methods=['POST'])
    def post_delete(post_id):
        viewer = _get_current_user()
        from models import Post
        post = Post.query.get_or_404(post_id)
        allowed = viewer and (viewer.role == 'Admin' or viewer.id == post.author_id)
        if not allowed:
            flash("Not authorized to delete this post.", "error")
            return redirect(url_for('thread_view', thread_id=post.thread_id))
        try:
            db.session.delete(post)
            db.session.commit()
            flash("Post deleted.", "success")
            return redirect(url_for('thread_view', thread_id=post.thread_id))
        except Exception as e:
            db.session.rollback()
            print("Post delete error:", e)
            flash("Could not delete post.", "error")
            return redirect(url_for('thread_view', thread_id=post.thread_id))
    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)