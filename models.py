from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rank     = db.Column(db.String(20), default='user')
    ozet     = db.Column(db.Text, default='')
    tw       = db.Column(db.String(255), default='#')
    li       = db.Column(db.String(255), default='#')
    gh       = db.Column(db.String(255), default='#')
    st       = db.Column(db.String(255), default='#')
    pp       = db.Column(db.String(255), default='')

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    __tablename__ = 'posts'

    id      = db.Column(db.Integer, primary_key=True)
    title   = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    resim   = db.Column(db.String(255), default='')
    cat     = db.Column(db.String(50), default='Genel')
    date    = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.title}>'


class About(db.Model):
    __tablename__ = 'about'

    id  = db.Column(db.Integer, primary_key=True)
    hk  = db.Column(db.Text, default='')
    hkm = db.Column(db.Text, default='')
    img = db.Column(db.String(255), default='')
    cat = db.Column(db.String(50), default='')

    def __repr__(self):
        return f'<About {self.id}>'


class Setting(db.Model):
    __tablename__ = 'ayar'

    id       = db.Column(db.Integer, primary_key=True)
    title    = db.Column(db.String(200), default='NF Blog')
    content  = db.Column(db.Text, default='')
    content2 = db.Column(db.Text, default='')

    def __repr__(self):
        return f'<Setting {self.title}>'

class Category(db.Model):
    __tablename__ = 'categories'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'
