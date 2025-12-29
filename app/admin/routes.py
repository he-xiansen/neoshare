from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.admin import bp
from app.models import User
from app import db


@bp.route('/')
@login_required
def admin():
    if not current_user.is_admin:
        flash('您没有管理员权限')
        return redirect(url_for('main.index'))
    
    users = User.query.all()
    return render_template('admin/index.html', users=users)


@bp.route('/ban_user/<int:user_id>')
@login_required
def ban_user(user_id):
    if not current_user.is_admin:
        flash('您没有管理员权限')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('不能封禁管理员账户')
    else:
        user.is_active = False
        db.session.commit()
        flash(f'用户 {user.username} 已被封禁')
    
    return redirect(url_for('admin.admin'))


@bp.route('/unban_user/<int:user_id>')
@login_required
def unban_user(user_id):
    if not current_user.is_admin:
        flash('您没有管理员权限')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    user.is_active = True
    db.session.commit()
    flash(f'用户 {user.username} 已被启用')
    
    return redirect(url_for('admin.admin'))