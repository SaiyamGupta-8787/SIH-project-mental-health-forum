# models.py
from datetime import datetime
from extensions import db
import sqlalchemy as sa

# -----------------------
# USERS
# -----------------------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password_hash = db.Column(db.String(250), nullable=False)
    role = db.Column(sa.Enum('Student','Counselor','Admin', name='user_roles'),
                     nullable=False, server_default='Student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    anonymous = db.Column(db.Boolean, default=False)  # <-- ADDED THIS

    threads = db.relationship('Thread', backref='creator', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    moods = db.relationship('Mood', backref='user', lazy=True)
    profile = db.relationship('UserProfile', backref='user', uselist=False, lazy=True)
    reactions = db.relationship('Reaction', backref='user', lazy=True)
    reports = db.relationship('Report', backref='reporter', lazy=True)


# -----------------------
# THREADS
# -----------------------
class Thread(db.Model):
    __tablename__ = 'threads'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    is_pinned = db.Column(db.Boolean, default=False)
    is_closed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='thread', lazy=True)

    __table_args__ = (
        db.Index('idx_threads_created_at', 'created_at'),
    )

# -----------------------
# POSTS
# -----------------------
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id', ondelete='CASCADE'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_hidden = db.Column(db.Boolean, default=False)

    reactions = db.relationship('Reaction', backref='post', lazy=True)
    post_tags = db.relationship('PostTag', backref='post', lazy=True)

    __table_args__ = (
        db.Index('idx_posts_thread_id', 'thread_id'),
        db.Index('idx_posts_created_at', 'created_at'),
    )

# -----------------------
# RESOURCES
# -----------------------
class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    type = db.Column(sa.Enum('article','audio','video','other', name='resource_types'), nullable=False, server_default='article')
    url = db.Column(db.String(1000), nullable=False)
    language = db.Column(db.String(50), default='en')
    description = db.Column(db.Text, nullable=True)          # <-- NEW
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)  # <-- NEW
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_resources_type', 'type'),
    )


# -----------------------
# MOODS
# -----------------------
class Mood(db.Model):
    __tablename__ = 'moods'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    mood = db.Column(db.String(250), nullable=False)
    mood_type = db.Column(sa.Enum(
        'happy','sad','anxious','angry','scared','energetic','tired','meh','lonely','guilty','insecure','great',
        name='mood_types'), default='great')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_mood_type', 'mood_type'),
    )

# -----------------------
# USER PROFILES
# -----------------------
class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    college = db.Column(db.String(255))
    year_of_study = db.Column(db.String(50))
    prefers_anonymous = db.Column(db.Boolean, default=True)
    language_pref = db.Column(db.String(50), default='en')

# -----------------------
# MEDIA
# -----------------------
class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    owner_type = db.Column(sa.Enum('post','resource','user', name='media_owner_types'), nullable=False)
    owner_id = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String(500))
    url = db.Column(db.String(1000))
    mime = db.Column(db.String(100))
    size_bytes = db.Column(db.BigInteger)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_media_owner', 'owner_type', 'owner_id'),
    )

# -----------------------
# TAGS
# -----------------------
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class PostTag(db.Model):
    __tablename__ = 'post_tags'
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)

# -----------------------
# REACTIONS
# -----------------------
class Reaction(db.Model):
    __tablename__ = 'reactions'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    type = db.Column(sa.Enum('like','viewed','dislike', name='reaction_types'), default='viewed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('post_id','user_id','type', name='uq_user_post_reaction'),
    )

# -----------------------
# REPORTS
# -----------------------
class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    target_type = db.Column(sa.Enum('post','comment','user', name='report_targets'), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(500))
    status = db.Column(sa.Enum('open','reviewed','closed', name='report_status'), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
