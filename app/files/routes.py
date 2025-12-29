from flask import render_template, request, redirect, url_for, flash, send_from_directory, current_app, abort
from flask_login import login_required, current_user
from app.files import bp
from app.models import File, User
from app import db
import os
from werkzeug.utils import secure_filename
import uuid


# 允许的文件类型
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'rar', 'doc', 'docx', 
    'xls', 'xlsx', 'ppt', 'pptx', 'py', 'js', 'html', 'css', 'json', 'md'
}
# 可编辑的文件类型
EDITABLE_EXTENSIONS = {'txt', 'py', 'js', 'html', 'css', 'json', 'md'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_type(filename):
    if '.' in filename:
        ext = filename.rsplit('.', 1)[1].lower()
        if ext in ['png', 'jpg', 'jpeg', 'gif']:
            return 'image'
        elif ext in ['pdf']:
            return 'pdf'
        elif ext in ['zip', 'rar']:
            return 'archive'
        elif ext in ['py', 'js', 'html', 'css', 'json']:
            return 'code'
        elif ext in ['txt', 'md']:
            return 'text'
        else:
            return 'file'
    return 'file'


@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有选择文件')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('没有选择文件')
            return redirect(request.url)
        
        is_public = request.form.get('is_public', False, type=bool)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            # 确定上传路径
            if is_public and current_user.is_admin:
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'public', unique_filename)
                is_public_file = True
            else:
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'private', current_user.username, unique_filename)
                is_public_file = False
            
            # 创建用户目录（如果不存在）
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            
            file.save(upload_path)
            
            # 保存文件信息到数据库
            file_record = File(
                filename=filename,
                filepath=upload_path,
                filesize=os.path.getsize(upload_path),
                filetype=get_file_type(filename),
                is_public=is_public_file,
                user_id=current_user.id if not is_public_file else None
            )
            db.session.add(file_record)
            db.session.commit()
            
            flash('文件上传成功')
            return redirect(url_for('files.my_files'))
        else:
            flash('不允许的文件类型')
    
    return render_template('files/upload.html')


@bp.route('/public')
def public_files():
    files = File.query.filter_by(is_public=True).all()
    return render_template('files/public.html', files=files)


@bp.route('/my_files')
@login_required
def my_files():
    files = File.query.filter_by(user_id=current_user.id).all()
    return render_template('files/my_files.html', files=files)


@bp.route('/download/<int:file_id>')
def download(file_id):
    file_record = File.query.get_or_404(file_id)
    
    # 检查权限
    if not file_record.is_public and (not current_user.is_authenticated or file_record.user_id != current_user.id):
        abort(403)
    
    directory = os.path.dirname(file_record.filepath)
    filename = os.path.basename(file_record.filepath)
    
    return send_from_directory(directory, filename, as_attachment=True)


@bp.route('/view/<int:file_id>')
def view_file(file_id):
    file_record = File.query.get_or_404(file_id)
    
    # 检查权限
    if not file_record.is_public and (not current_user.is_authenticated or file_record.user_id != current_user.id):
        abort(403)
    
    # 如果是可编辑文件类型，提供在线查看功能
    if file_record.filetype in ['text', 'code'] or file_record.filename.rsplit('.', 1)[1].lower() in EDITABLE_EXTENSIONS:
        try:
            with open(file_record.filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return render_template('files/view_file.html', file=file_record, content=content)
        except UnicodeDecodeError:
            flash('文件无法以文本格式显示')
            return redirect(url_for('files.download', file_id=file_id))
    else:
        # 对于非文本文件，直接下载
        return redirect(url_for('files.download', file_id=file_id))


@bp.route('/edit/<int:file_id>', methods=['GET', 'POST'])
@login_required
def edit_file(file_id):
    file_record = File.query.get_or_404(file_id)
    
    # 检查权限 - 只有文件所有者可以编辑
    if file_record.user_id != current_user.id:
        abort(403)
    
    # 检查是否为可编辑文件类型
    if file_record.filetype not in ['text', 'code'] and file_record.filename.rsplit('.', 1)[1].lower() not in EDITABLE_EXTENSIONS:
        flash('该文件类型不支持在线编辑')
        return redirect(url_for('files.my_files'))
    
    if request.method == 'POST':
        content = request.form.get('content', '')
        try:
            with open(file_record.filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            flash('文件已保存')
        except Exception as e:
            flash(f'保存文件时出错: {str(e)}')
        
        return redirect(url_for('files.edit_file', file_id=file_id))
    
    try:
        with open(file_record.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        flash('文件无法以文本格式编辑')
        return redirect(url_for('files.my_files'))
    
    return render_template('files/edit_file.html', file=file_record, content=content)


@bp.route('/avatar/<path:filename>')
def avatar_file(filename):
    """提供头像文件访问"""
    avatar_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars')
    return send_from_directory(avatar_path, filename)


@bp.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        flash('没有选择头像文件')
        return redirect(url_for('auth.profile'))
    
    file = request.files['avatar']
    if file.filename == '':
        flash('没有选择头像文件')
        return redirect(url_for('auth.profile'))
    
    # 检查是否为允许的图片类型
    if file and allowed_file(file.filename) and file.filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif']:
        filename = secure_filename(file.filename)
        unique_filename = f"avatar_{current_user.id}_{uuid.uuid4()}_{filename}"
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars', unique_filename)
        
        # 创建头像目录（如果不存在）
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)
        
        # 更新用户头像路径 - 保存相对路径，而不是完整路径
        current_user.avatar = f"avatar/{unique_filename}"
        db.session.commit()
        
        flash('头像上传成功')
    else:
        flash('只允许上传图片文件 (png, jpg, jpeg, gif)')
    
    return redirect(url_for('auth.profile'))