from app import create_app, db
from app.models import User, File

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'File': File}


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # 检查是否已存在管理员账户，如果不存在则创建一个
        admin_user = User.query.filter_by(is_admin=True).first()
        if not admin_user:
            admin = User(username='admin', email='admin@example.com', is_admin=True, is_active=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("已创建默认管理员账户: admin / admin123")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
