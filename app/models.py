from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    nickname = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200), nullable=True)  # 头像文件路径
    is_active = db.Column(db.Boolean, default=True)  # 是否被封禁
    is_admin = db.Column(db.Boolean, default=False)  # 是否为管理员
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联的文件
    files = db.relationship('File', backref='owner', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)  # 文件实际存储路径
    filesize = db.Column(db.Integer)  # 文件大小
    filetype = db.Column(db.String(50), nullable=False)  # 文件类型
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_public = db.Column(db.Boolean, default=False)  # 是否为公共文件
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # 所属用户，公共文件为NULL
    
    def __repr__(self):
        return f'<File {self.filename}>'