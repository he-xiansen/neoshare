from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.main import bp
from app.models import File
import os


@bp.route('/')
def index():
    # 获取公共文件列表
    public_files = File.query.filter_by(is_public=True).all()
    return render_template('index.html', files=public_files)


@bp.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        files = File.query.filter(File.filename.contains(query)).all()
        users = None  # 搜索用户功能可以后续扩展
    else:
        files = []
        users = []
    
    return render_template('search.html', files=files, query=query)