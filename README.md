# NeoShare - 文件共享系统

一个基于Flask开发的简洁高效文件共享平台，支持用户注册登录、文件上传下载、在线预览、头像设置等功能。

## 功能特性

- **用户系统**：支持用户注册、登录、个人资料管理
- **文件管理**：支持文件上传、下载、在线预览
- **权限控制**：管理员可设置公共文件，普通用户上传私有文件
- **头像管理**：支持用户上传自定义头像
- **文件搜索**：支持按文件名搜索
- **响应式设计**：适配各种设备屏幕

## 技术栈

- **后端**：Flask、Flask-Login、Flask-SQLAlchemy
- **数据库**：SQLite
- **前端**：Bootstrap 5、Font Awesome
- **文件处理**：Werkzeug文件处理
- **部署**：支持开发和生产环境部署

## 系统要求

- Python 3.8+
- pip 包管理器
- 操作系统：Windows / macOS / Linux

## 安装部署

### 开发环境

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd neoshare
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   ```

3. **激活虚拟环境**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

5. **启动服务器**
   ```bash
   python run.py
   ```

6. **访问应用**
   打开浏览器访问 http://127.0.0.1:5000

### 生产环境

1. **使用WSGI服务器**（如Gunicorn）
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

2. **配置反向代理**（如Nginx）
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 配置说明

### 环境变量

创建 `.env` 文件配置以下变量：
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///neoshare.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=100 * 1024 * 1024  # 100MB
```

### 上传限制

- 单个文件最大100MB
- 支持的文件类型：文档、图片、视频、音频、压缩包等
- 用户上传目录：`uploads/private/username/`
- 公共文件目录：`uploads/public/`

## 项目结构

```
neoshare/
├── app/                    # Flask应用主目录
│   ├── __init__.py        # 应用工厂函数
│   ├── models.py          # 数据模型定义
│   ├── auth/              # 认证模块
│   ├── files/             # 文件管理模块
│   ├── main/              # 主页面模块
│   ├── admin/             # 管理员模块
│   ├── static/            # 静态资源
│   └── templates/         # HTML模板
├── uploads/               # 文件上传目录
├── instance/              # 数据库文件
├── requirements.txt       # 项目依赖
├── run.py                 # 启动脚本
├── README.md              # 项目说明
└── INSTALL.md             # 安装部署文档
```

## 使用说明

### 用户功能

1. **注册账户**：访问 `/register` 注册新账户
2. **登录系统**：访问 `/login` 登录系统
3. **上传文件**：登录后访问 `/files/upload` 上传文件
4. **管理文件**：访问 `/files/my_files` 管理自己的文件
5. **个人资料**：访问 `/auth/profile` 设置个人资料和头像

### 管理员功能

1. **管理用户**：访问 `/admin` 管理用户账户
2. **设置公共文件**：上传文件时可设置为公共文件
3. **封禁/启用用户**：在管理面板中操作

## API接口

- `GET /` - 首页，显示公共文件列表
- `GET /files/my_files` - 我的文件列表
- `POST /files/upload` - 上传文件
- `GET /files/download/<id>` - 下载文件
- `GET /files/preview/<id>` - 预览文件
- `POST /files/upload_avatar` - 上传头像

## 安全特性

- **密码加密**：使用werkzeug安全哈希
- **会话管理**：Flask-Login提供安全会话
- **文件类型验证**：限制可上传的文件类型
- **XSS防护**：模板自动转义HTML内容
- **CSRF防护**：使用Flask-WTF表单验证

## 开发指南

### 添加新功能

1. 在对应模块下创建路由
2. 定义数据模型（如需要）
3. 创建HTML模板
4. 添加前端样式和脚本

### 测试

```bash
# 运行单元测试
python -m pytest tests/
```

## 故障排除

### 常见问题

1. **启动失败**：检查端口是否被占用
2. **数据库错误**：确认数据库文件权限
3. **文件上传失败**：检查上传目录权限和大小限制
4. **样式不显示**：确认静态资源路径正确

### 日志查看

- 开发环境：控制台输出
- 生产环境：配置日志文件路径

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 许可证

[MIT License](LICENSE)

## 作者

NeoShare开发团队

## 版本历史

- v1.0.0 - 初始版本，实现基本功能
- v1.1.0 - 添加头像管理功能
- v1.2.0 - 优化UI界面和用户体验